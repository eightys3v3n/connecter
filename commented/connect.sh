#!/bin/bash

# ssh into various hosts through a variety of means

# variable initialization
timeout=30
verbose=0
display_ip=0
root=""
dns=""
onion=""
arguments=""


# commands this script requries to run
  # requires is another script that just checks if the specified files exist in the PATH
#requires ssh tor-resolve ncat printf


# parse all the command line arguments
for a in "$@"
do
  # print help and quit
	if [[ "$a" == "-h" ]] || [[ "$a" == "--help" ]]
	then
		printf "server [-v]\n-v | --verbose enables verbose mode\nthis script is designed to open a lan,wan, or tunnelled connection to my server using a tor hidden service for initial contact.\n"
		exit 0

  # turn on verbose mode
	elif ((!$verbose)) && [[ "$a" == "-v" ]]
	then
		verbose=1
		printf "verbose mode\n"

  # if it's not an option, it is used as an argument
	else
		if [[ "$a" == "server" ]]
		then
		  dns="dns name pointing to my server"
		  onion="onion address pointing to my server"
		  root="/data"

		  printf "connecting to server\n"
		elif [[ "$a" == "laptop" ]]
    then
    dns="dns for my laptop"
    onion="onion address pointing to my laptop"
    root="/home/anonymous"

    printf "connecting to laptop\n"
		fi
	fi
done

# if no arguments are specified, it defaults to connecting to my server
if [[ -z "$root" ]] && [[ -z "$onion" ]] && [[ -z "$dns" ]]
then
  dns="dns name pointing to my server"
		onion="onion address pointing to my server"
  root="/data"

  printf "connecting to server\n"
fi


# first try to connect directly to the dns name.
# this requires port forwarding.
output=$(echo "" | ncat -w 4 $dns 443 2> /dev/null)
if ((! $?)) && [[ "$output" == *"SSH"* ]]
then
	printf "direct wan connection to $dns\n"
	ssh -p 443 anonymous@$dns
	exit 0
fi


# use tor-resolve to map an ip address to the onion address.
# it's this or redirecting the dns requests made by ssh and ncat, which was more complex
output=$(tor-resolve -4 $onion 127.0.0.1:9060 2>&1)
if [[ "$output" == *"Error while connecting to SOCKS host: Connection refused"* ]]
then
	printf "tor-resolve couldn't connect to tor at 127.0.0.1:9060\n"
	exit 2
fi

if [[ ! $output =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]
then
	printf "tor-resolve returned an invalid ip address '$output'\n"
	exit 3
fi

redirect_ip=$output

if (($verbose)); then printf "requesting host's internal ip via tor\n"; fi


# get the internal ip address by connecting through a tor tunnel, then try to connect to it
internal_ip=$(ssh -oStrictHostKeyChecking=no -C -oProxyCommand='ncat -w '$timeout' --proxy-type socks4 --proxy 127.0.0.1:9060 %h %p' -p 443 anonymous@$redirect_ip '/data/programs/scripts/internal_ip')

if [[ "$internal_ip" != *"command not found"* ]]
then
  response=$(printf "" | ncat -w $timeout $internal_ip 443)
  if [[ "$response" == *"SSH"* ]]
  then
    	if (($verbose)); then printf "connecting to '$internal_ip:443'\n"; fi
    printf "direct lan connection\n"
	  ssh -p 443 anonymous@$internal_ip
	exit 0
fi
if (($verbose)); then printf "host is not accessable over lan\n"; fi

else
  printf "host does not have an internal_ip script\n"
fi


# get the external ip address by connecting through a tor tunnel
if (($verbose)); then printf "requesting server's external ip via tor\n"; fi
external_ip=$(ssh -oStrictHostKeyChecking=no -C -oProxyCommand='ncat -w '$timeout' --proxy-type socks4 --proxy 127.0.0.1:9060 %h %p' -p 443 anonymous@$redirect_ip '/data/programs/scripts/external_ip')

response=$(printf "" | ncat -w $timeout $external_ip 443)
if [[ "$response" == *"SSH"* ]]
then
	if (($verbose)); then printf "connecting to '$external_ip:443'\n"; fi

	printf "direct wan connection\n"
	ssh -p 443 anonymous@$external_ip
@$redirect_ip
	exit 0
fi
if (($verbose)); then printf "host is not accessable over wan\n"; fi


# last resort, open a connection through a tor tunnel.
printf "tor tunnel connection\n"
ssh -oStrictHostKeyChecking=no -C -oProxyCommand='ncat -w '$timeout' --proxy-type socks4 --proxy 127.0.0.1:9060 %h %p' -p 443 anonymous@$redirect_ip 2>/dev/null


# fail and exit
r=$?
if (($r == 255))
then
	printf "tor couldn't connect to the server\n"
	exit 4
elif (($r))
then
	printf "an unknown ssh error occured\n"
	exit 5
fi

exit 0