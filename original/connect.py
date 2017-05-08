#!/bin/python3

# tries a variety of means to connect to a specified host. (direct, through tor)


from os import system
from sys import argv
from getopt import getopt
from subprocess import Popen, PIPE
from time import sleep


true  = True
false = False

global verbose
verbose = false
global wait_time
wait_time = '4'
global tor_address
tor_address = '127.0.0.1'
global tor_port
tor_port = '9060'
global hosts
hosts   = {
  'server':{
    'dns'  :'dns name pointing to server',
    'onion':'onion url pointing to my server',
    'port' :'443'
  }
}


def ncat_ping( address, port, wait=None, proxy=None ):
  """
  Tests to see if a connection can be established to the given address on the given port.

  address | a dns or ip address
  port    | a port number
  wait    | seconds to wait before failing connection (in a string)
  proxy   | address:port of socks4 proxy to connect through

  Returns:
    true if successfull connection
    false otherwise
  """
  if wait is None:
    wait = wait_time

  c = ['ncat','-w',wait,address,port]
  if proxy is not None:
    c.extend( ['--proxy-type','socks4','--proxy',proxy] )

  p = Popen( c, stdin=PIPE, stdout=PIPE, stderr=PIPE )
  r = p.communicate()

  if verbose:
    print('ncat returned', r)

  # false means no connection
  # true means successfull connection
  return not p.returncode


def tor_resolve( host ):
  """
  Uses tor-resolve to resolve an onion address to an ip address for programs that can't change their dns resolution server to tor

  host | an onion address

  Returns an ip address to be used through tor
  """
  global hosts

  if not ncat_ping( tor_address, tor_port ):
    raise Exception("couldn't connect to tor to resolve onion address")

  p = Popen( ['tor-resolve','-4',hosts[host]['onion'],tor_address+':'+tor_port], stdout=PIPE, stderr=PIPE )
  r = p.communicate()

  if verbose:
    print('tor-resolve returned', r)

  if r[0] == b'':
    raise Exception("tor-resolve didn't return anything")

  ip = r[0].decode()
  ip = ip[0:-1]

  hosts[host]['redirect_ip'] = ip

  return ip


def try_dns(host):
  """
  Try to connect to the hosts dns name or ip address

  Returns:
    true if successfully connected
    false otherwise
  """
  return ncat_ping( hosts[host]['dns'], hosts[host]['port'] )


def try_onion(host):
  """
  Try to connect to the hosts onion address

  Returns:
    true if successfully connected
    false otherwise
  """
  address = tor_resolve( host )
  return ncat_ping( address, hosts[host]['port'], proxy=tor_address+':'+tor_port )


def connect( target, mode ):
  """
  Tries to open an ssh connection to the given target

  target | the alias of the computer to try to connect to
  mode   :
    auto  | try all available means to open an ssh connection
    dns   | only connect directly using the dns or ip
    onion | only connect through a tor tunnel using the onion address

  Returns none
  """
  global hosts

  if mode == 'auto' or mode == 'dns':
    if try_dns(target):
      if verbose:
        print("using dns")

      system( 'ssh -p'+hosts[target]['port']+' '+hosts[target]['dns'] )
      return

  if mode == 'auto' or mode == 'onion':
    if try_onion(target):
      if verbose:
        print("using onion")

      system( 'ssh -oStrictHostKeyChecking=no -C -oProxyCommand=\'ncat -w '+wait_time+' --proxy-type socks4 --proxy '+tor_address+':'+tor_port+' %h %p\' -p'+hosts[target]['port']+' anonymous@'+hosts[target]['redirect_ip'] )
      return

  else:
    raise Exception( "invalid mode", mode )


def main():
  global verbose, hosts
  target = None # alias for the computer to connect to
  mode = 'auto'

  opts, args = getopt( argv[1:], 'hvt:do', ['help', 'verbose', 'target=', 'dns', 'onion'] )

  # parse options and their arguments
  for opt,arg in opts:
    if opt in ['-h', '--help']:
      print('help text')

    elif opt in ['-v', '--verbose']:
      verbose = true

    elif opt in ['-t', '--target']:
      target = arg

    elif opt in ['-d', '--dns']:
      mode = 'dns'

    elif opt in ['-o', '--onion']:
      mode = 'onion'

  # parse arguments
  for arg in args:
    if target is None:
      target = arg

  # default target
  if target is None:
    target = 'server'

  connect( target, mode )


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass