# SSH Connector
A script that tries to connect to a configured host using the fastest method possible of IP/DNS through port forwarding or through a Tor hidden service. Also configurable ports to forward from local to server (see Auto-port forwarding)

## Requires:
### Client on Arch Linux
* A tor client setup and running, listening on port 9060 for incoming socks proxy connections.
* `tor-resolve` command that is included in the "tor" package.
* `ncat` command that is included in the "nmap" package.
* ssh
* python3 to run the script.
### Server on Arch Linux
* A tor hidden service setup and running on the same port as the SSH server.
* An SSH server.

## How to use
Setup an Arch Linux server running an SSH server with the port forwarded.
Rename example_connect.json to connect.json (see RC_FILE_PATHS).
Replace the values in connect.json with those for your server.
Run the script with connect.json in one of the searched paths (see RC_FILE_PATHS).

## Information
### Connections are attempted as follows:
* Directly to IP/DNS:port.
* (TODO) Directly to IP as reported by server via a Tor connection.
* Through Tor.

### RC_FILE_PATHS
The variable at the top of connect.py contains all the paths that will be read in. It will read all the files that exist. Any path that doesn't start with `/` will have the path of the script prepended to it upon run.
E.G. If the script is located in `/usr/bin/connect.py` and `RC_FILE_PATHS = ['connect.json']` then `/usr/bin/connect.json` will be read in.

### Auto-port forwarding
Ports can be added to the build_in_rules list in the main function around line 263. They will be forwarded using the SSH option -L.