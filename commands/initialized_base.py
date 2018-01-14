"""The initialized base command."""
from ethereum.utils import denoms

from utils.client import Client
from utils.cli import query_yes_no
from utils.eth import current_price

class InitializedBase(object):
    """A initialized base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

        self.client = Client()

        if 'mnemonic' not in self.client.config.attributes:
            self.initialized = False
            print("\nError: Not initialized, run `lly init` to begin")
            return

        self.initialized = True

    def execute(self, message, default_gas_limit, confirm_handler, reject_handler):
        default_gas_price = int(int(self.client.config.attributes['default_gas_price']) / denoms.gwei)

        gas_price = int(self.options['--gasprice']) if self.options['--gasprice'] else default_gas_price
        gas_limit = int(self.options['--gaslimit']) if self.options['--gaslimit'] else default_gas_limit

        max_gas_gwei = gas_price * default_gas_limit
        max_gas_usd = float(current_price()["bid"]) * (max_gas_gwei / denoms.gwei)

        print("\n%s" % message)
        print("\nUsing:")
        print("\tGas price: %dgwei" % gas_price)
        print("\tGas limit: %dgwei" % default_gas_limit)
        print("\tMax price: %dgwei ($%s)" % (max_gas_gwei, '{0:.{1}f}'.format(max_gas_usd, 2)))

        confirm = query_yes_no("\nIs this ok?")

        if confirm:
            return confirm_handler(gas_price, gas_limit)
        else:
            return reject_handler()

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')
