"""Controller for a grow light and water pump, uses sensor info from analog input moisture and light sensor """
import logging

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_FAN

logger = logging.getLogger(__name__)


class PlantLoveAccessory(Accessory):
    """Stuff"""

    category = CATEGORY_SPRINKLER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add the sprinkler
        serv_sprinkler = self.add_preload_service(
            'Sprinkler', chars=['Status','Duration'])

        self.char_sprinkler_status = serv_sprinkler.configure_char(
            'Status', setter_callback=self.set_sprinkler_status)
        self.char_sprinkler_duration = serv_sprinkler.configure_char(
            'Duration', setter_callback=self.set_sprinkler_duration)


        #Add grow lamp
        serv_growlamp = self.add_preload_service(
            'Light', chars=['Status'])
        self.char_growlamp_status = serv_growlamp.configure_char(
            'Status', setter_callback=self.set_growlamp_status)

    def set_sprinkler_status(self, value):
        logger.debug(f"Sprinkler status changed to {value}")

    def set_sprinkler_duration(self, value):
        logger.debug(f"Sprinkler duration set to {value}")

    def set_sprinkler_duration(self, value):
        logger.debug(f"Grow lamp status changed {value}")
