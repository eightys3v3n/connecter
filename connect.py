#!/usr/bin/python3

"""
tries a variety of means to connect to a specified host. (direct, through tor)
"""

import os
import json
from os import system
from sys import argv
from getopt import getopt
from subprocess import Popen, PIPE
from time import sleep
from itertools import chain


global RC_FILE_PATHS
global verbose
global wait_time
global tor_address
global tor_port
global hosts

RC_FILE_PATHS = ['connect.json']
verbose = False
wait_time = '4'
tor_address = '127.0.0.1'
tor_port = '9060'
hosts   = {
  # 'example_server':{
  #   'user' :'username',
  #   'dns'  :'DNS name or IP for server',
  #   'onion':'Onion address for same server',
  #   'port' :'22'
  # }
}


def ncat_ping(address, port, wait=None, proxy=None):
  """
  Tests to see if a connection can be established to the given address on the given port.

  address | a dns or ip address
  port    | a port number
  wait    | seconds to wait before failing connection (in a string)
  proxy   | address:port of socks5 proxy to connect through

  Returns:
    True if successfull connection
    False otherwise
  """
  if wait is None:
    wait = wait_time

  c = ['ncat','-w', wait, address, port]
  if proxy is not None:
    c.extend(['--proxy-type', 'socks5', '--proxy', proxy])

  p = Popen( c, stdin=PIPE, stdout=PIPE, stderr=PIPE )
  r = p.communicate()

  if verbose:
    print('ncat returned', r)

  # False means no connection
  # True means successfull connection
  return not p.returncode


def tor_resolve(host):
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
    True if successfully connected
    False otherwise
  """
  return ncat_ping(hosts[host]['dns'], hosts[host]['port'])


def try_onion(host):
  """
  Try to connect to the hosts onion address

  Returns:
    True if successfully connected
    False otherwise
  """
  address = tor_resolve(host)
  return ncat_ping(address, hosts[host]['port'], proxy=tor_address+':'+tor_port)


def ParseOptions( options ):
  return ' '.join( options )


def connect( target, mode, options=[], verbose=False ):
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

  options.append('-p{}'.format(hosts[target]['port']))

  if mode == 'auto' or mode == 'dns':
    if try_dns(target):
      if verbose:
        print("using dns")

      options = ' '.join(options)
      command = 'ssh '+options+' '+hosts[target]['user']+'@'+hosts[target]['dns']
      if verbose:
        open('/tmp/ssh_command', 'w').write(command)
        print("ssh command written to /tmp/ssh_command")
      system(command)
      return

  if mode == 'auto' or mode == 'onion':
    if try_onion(target):
      if verbose:
        print("using onion")

      options.extend( [
        '-oStrictHostKeyChecking=no',
        '-C',
        '-oProxyCommand=\'ncat -w '+wait_time+' --proxy-type socks4 --proxy '+tor_address+':'+tor_port+' %h $p\'',
      ] )

      options = ' '.join( options )
      system( 'ssh '+options+' '+hosts[target]['user']+'@'+hosts[target]['dns'])
      return

  else:
    raise Exception( "invalid mode", mode )


def PrintHelp():
  helps = {
    ('--help',): "Prints this help text",
    ('--verbose',): "Print more information",
    ('--target', 'name'): "Connect to this host configuration",
    ('--dns',): "Connect using the DNS name only",
    ('--onion',): "Connect using the onion DNS name only",
    ('--local', 'local_port:remote_ip:remote_port'): "Port forward local_port through the SSH connection and from the remote PC to remote_ip:remote_port",
    ('--remote', 'remote_port:local_ip:local_port'): "Port forward remote_port on the remote PC through the SSH connection to this PC then to local_ip:local_port",
  }
  optionlen = max([len(h[0]) for h in helps.keys()])
  for help, desc in helps.items():
    if len(help) > 1:
      format = '{:{width}} '
      format += ' '.join(['{}' for h in help[1:]])
      format += ' | {desc}'
      print(format.format(*help, desc=desc, width=optionlen))
    else:
      format = '{:{width}} {desc}'
      print(format.format(*help, desc=desc, width=optionlen))


def load_rc_file(paths, hosts):
	for path in paths:
		if os.path.exists(path):
			try:
				_hosts = json.loads(open(path, 'r').read())
				hosts.update(_hosts)
			except Exception as e:
				print("Failed to load RC file", path, e)
		else:
			print("RC file doesn't exist '{}'".format(path))


def set_rc_file_paths():
	global RC_FILE_PATHS
	self_path = os.path.dirname(os.path.realpath(__file__))
	for i, p in enumerate(RC_FILE_PATHS):
		if not p.startswith('/'):
			RC_FILE_PATHS[i] = os.path.join(self_path, p)


def main():
  global verbose, hosts, RC_FILE_PATHS
  target = None # alias for the computer to connect to
  mode = 'auto'
  extra_options = []


  set_rc_file_paths()

  opts, args = getopt( argv[1:], 'hvt:doL:R:', [ 'help', 'verbose', 'target=', 'dns', 'onion', 'local=', 'remote=' ] )

  # parse options and their arguments
  for opt,arg in opts:
    if opt in ['-h', '--help']:
      PrintHelp()

    elif opt in ['-v', '--verbose']:
      verbose = True
      extra_options.append('-v')

    elif opt in ['-t', '--target']:
      target = arg

    elif opt in ['-d', '--dns']:
      mode = 'dns'

    elif opt in ['-o', '--onion']:
      mode = 'onion'

    elif opt in ['-L', '--local']:
      extra_options.append( '-L'+arg )

    elif opt in ['-R', '--remote']:
      extra_options.append( '-R'+arg )

  # parse arguments
  for arg in args:
    if target is None:
      target = arg

  load_rc_file(RC_FILE_PATHS, hosts)

  # default target
  if target is None:
    target = 'server'

  build_in_rules = []

  # Can append ports to this list to have them forwarded from the local host to the remote host for every connection.
  for p in range(25500, 25600):
  	build_in_rules.append((p, p))
  build_in_rules.append((58847, 58846))

  for port in build_in_rules:
    extra_options.append('-L{l}:{lp}:{r}:{rp}'.format(l='127.0.0.2', r='127.0.0.1', lp=port[0], rp=port[1]))

  connect(target, mode, options=extra_options, verbose=verbose)


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
