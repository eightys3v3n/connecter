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
global wait_time
global tor_address
global tor_port
global hosts

verbose     = false
wait_time   = '4'         # how long to wait before timing out (seconds)
tor_address = '127.0.0.1' # tor proxy ip address
tor_port    = '9060'      # tor proxy port
hosts       = {           # a list of hosts that can be connected to
  'server':{
    'user' :'anonymous',
    'dns'  :'dns/ip pointing to server',
    'onion':'onion address pointing to server',
    'port' :'443'
  }
}
# NOTE
# if ssh is hosted on port 22, the onion must also be open on port 22
# then the 'port' should also be 22


def ncat_ping( address, port, wait=None, proxy=None ):
  """
  tests to see if a connection can be established to the given address on the given port.

  address | a dns or ip address
  port    | a port number
  wait    | seconds to wait before failing connection (in a string)
  proxy   | address:port of socks4 proxy to connect through

  Returns:
    true  : a connection can be established
    false : a connection can't be established
  """

  # default wait time if not specified
  if wait is None:
    wait = wait_time

  # command to test connection
  # should return false on successful connection, true on failure
  c = [ 'ncat', '-w', wait, address, port ]

  # add proxy options to command if proxy is requested
  if proxy is not None:
    c.extend( [ '--proxy-type', 'socks4', '--proxy', proxy ] )

  # run the command
  p = Popen( c, stdin=PIPE, stdout=PIPE, stderr=PIPE )

  # get the output from the command and allow it to finish
  r = p.communicate()

  if verbose:
    print( "ncat returned", r )

  return not p.returncode


def tor_resolve( host ):
  """
  uses tor-resolve to resolve an onion address to an ip address for programs that can't change their dns resolution server to tor

  host | an onion address

  Raises an exception on errors
  Returns an ip address to be used through tor
  """
  global hosts

  # make sure the tor proxy is up at the given address
  if not ncat_ping( tor_address, tor_port ):
    raise Exception("couldn't connect to tor to resolve onion address")

  # run tor-resolve
  p = Popen( [ 'tor-resolve', '-4', hosts[host]['onion'], tor_address+':'+tor_port ], stdout=PIPE, stderr=PIPE )

  # get the output of tor-resolve
  r = p.communicate()

  if verbose:
    print( 'tor-resolve returned', r )

  if r[0] == b'':
    raise Exception("tor-resolve didn't return anything")

  # encode output into a string (from bytes) and remove the newline character (last character)
  ip = r[0].decode()
  ip = ip[0:-1]

  # set the redirect ip in the hosts array to be used later for connecting
  # this should be done without a global variable with returning
  hosts[host]['redirect_ip'] = ip

  return ip


def try_dns( host ):
  """
  Try to connect to the hosts dns name or ip address

  Returns:
    true  : successfully connected
    false : otherwise
  """
  return ncat_ping( hosts[host]['dns'], hosts[host]['port'] )


def try_onion( host ):
  """
  Try to connect to the hosts onion address

  Returns:
    true  : successfully connected
    false : otherwise
  """
  address = tor_resolve( host )
  return ncat_ping( address, hosts[host]['port'], proxy=tor_address+':'+tor_port )


def connect( target, mode ):
  """
  Tries to open an ssh connection to the given target

  target | the alias of the computer to try to connect to (in hosts array)
  mode   :
    auto  | try all available means to open an ssh connection
    dns   | only connect directly using the dns or ip
    onion | only connect through a tor tunnel using the onion address

  Returns none
  """
  global hosts

  if mode == 'auto' or mode == 'dns':
    if try_dns( target ):
      if verbose:
        print("using dns")

      # run the ssh command to connect directly
      system( 'ssh -p'+hosts[target]['port']+' '+hosts[target]['dns'] )
      return

  if mode == 'auto' or mode == 'onion':
    if try_onion( target ):
      if verbose:
        print("using onion")

      # run the ssh command to connect through tor
      port        = hosts[target]['port']
      redirect_ip = hosts[target]['redirect_ip']
      user        = hosts[target]['user']

      proxy_command_options = [
        '-w '+wait_time,
        '--proxy-type socks4',
        '--proxy '+tor_address+':'+tor_port,
        '%h %p'
      ]
      proxy_command = 'ncat '+' '.join( proxy_command_options )

      ssh_options = [
        '-oStrictHostKeyChecking=no',
        '-C',
        '-p'+hosts[target]['port'],
        '-oProxyCommand=\''+proxy_command+'\'',
        user+'@'+redirect_ip
      ]
      ssh_command = 'ssh '+' '.join( ssh_options )

      system( ssh_command )
      return

  else:
    raise Exception( "invalid mode", mode )


def main():
  global verbose, hosts
  target = None   # an alias for a computer in hosts array to connect to
  mode = 'auto'   # auto, dns, onion

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