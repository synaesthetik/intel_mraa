import mraa
from nio.common.signal.base import Signal
from nio.common.discovery import Discoverable, DiscoverableType
from .intel_mraa_gpio_base import IntelMraaGpioBase


def interrupt_callback(self):
    self._logger.debug("Executing interrupt callback")
    pin_number = self.mraa_gpio_pin
    pin_value = self._gpio_pin.read()
    self._logger.debug("Mraa pin # {} is now {}".format(pin_number, pin_value))
    self.notify_signals([Signal({"pin_value": pin_value,
                                 "pin_number": pin_number})])


@Discoverable(DiscoverableType.block)
class IntelMraaInterruptGpio(IntelMraaGpioBase):

    """ Use Intel's libmraa to interface with the IO on various platforms """

    def configure(self, context):
        super().configure(context)
        # TODO: make EDGE_BOTH configurable
        self._gpio_pin.isr(mraa.EDGE_BOTH, interrupt_callback, self)
        self._logger.debug(
            "Configured mraa pin # {} interrupt".format(self.mraa_gpio_pin))

    def _pin_mode(self):
        return mraa.DIR_IN

    def process_signals(self, signals, input_id='default'):
        # This block should not respond to input signals
        pass
