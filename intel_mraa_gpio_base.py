import mraa
from nio.common.block.base import Block
from nio.metadata.properties import VersionProperty, IntProperty


class IntelMraaGpioBase(Block):

    """ Use Intel's libmraa to interface with the IO on various platforms """

    version = VersionProperty('0.1.0')
    mraa_gpio_pin = IntProperty(title='Mraa Pin #', default='31')

    def __init__(self):
        super().__init__()
        self._gpio_pin = None

    def configure(self, context):
        super().configure(context)
        self._gpio_pin = mraa.Gpio(self.mraa_gpio_pin)
        self._gpio_pin.dir(self._pin_mode())

    def process_signals(self, signals, input_id='default'):
        out_sigs = []
        for signal in signals:
            try:
                out_sig = self._process_signal(signal)
            except:
                self._logger.exception('Failed to process signal')
                continue
            out_sigs.append(out_sig)
        if out_sigs:
            self.notify_signals(out_sigs, output_id='default')

    def _pin_mode(self):
        raise NotImplementedError

    def _process_signal(self, signal):
        """ Return a Signal """
        raise NotImplementedError
