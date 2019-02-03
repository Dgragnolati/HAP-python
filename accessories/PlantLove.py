"""Controller for a grow light and water pump, uses sensor info from analog input moisture and light sensor """
import logging

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_OTHER

logger = logging.getLogger(__name__)


class PlantLoveAccessory(Accessory):
    """Stuff"""

    category = CATEGORY_OTHER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add the sprinkler
        serv_sprinkler = self.add_preload_service(
            'IrrigationSystem', chars=['Active','ProgramMode','InUse'])

        self.char_sprinkler_status = serv_sprinkler.configure_char(
            'Active', setter_callback=self.set_sprinkler_status)
        self.char_sprinkler_mode = serv_sprinkler.configure_char(
            'ProgramMode', setter_callback=self.set_sprinkler_program)


        #Add grow lamp
        serv_growlamp = self.add_preload_service(
            'Lightbulb', chars=['On'])
        self.char_growlamp_status = serv_growlamp.configure_char(
            'On', setter_callback=self.set_growlamp_status)

    def set_sprinkler_status(self, value):
        logger.debug("Sprinkler status changed to %s", value)

    def set_sprinkler_program(self, programmode):
        logger.debug("Sprinkler duration set to %s", programmode)

    def set_sprinkler_duration(self, value):
        logger.debug("Grow lamp status changed %s", value)
