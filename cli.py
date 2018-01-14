"""lly

Usage:
  lly init
  lly account [-k | --private-key]
  lly account send <address> <amount>
  lly repo deploy [--gasprice=<gwei>] [--gaslimit=<gwei>]
  lly repo status <address>
  lly repo create-bounty <address> <bountyid>
  lly contract (call|transact) <address> <function> [--args=<arguments>] [--gasprice=<gwei>] [--gaslimit=<gwei>]
  lly (-h | --help)
  lly --version

Options:
  -h --help             Show this screen.
  --version             Show version.
  -k --private-key      Show account private key
  --args=<arguments>    Arguments for call [default: []].
  --gasprice=<gwei>     Gas price in Gwei [default: 21].
  --gaslimit=<gwei>     Override gas limit in Gwei.

"""
from inspect import getmembers, isclass
from docopt import docopt


if __name__ == '__main__':
    import commands
    options = docopt(__doc__, version='lly 0.1.0')

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.items():
        if v and hasattr(commands, k):
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base' and command[0] != 'InitializedBase'][0]
            command = command(options)
            command.run()
