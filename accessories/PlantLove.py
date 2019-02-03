"""Controller for a grow light and water pump, uses sensor info from analog input moisture and light sensor """
import logging

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_OTHER
import serial
import sys
from time import sleep, strftime, time


# There are serial commands that triger the relays/get data back from analog sensors
# light,moisture,light_on,light_off,pump_on  (Currently pump on only goes for 2 seconds)


logger = logging.getLogger(__name__)
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=6.0)
LightLogPath = "/home/pi/HAP/HAP-python/light.csv"
MoistureLogPath = "/home/pi/HAP/HAP-python/moisture.csv"

class PlantLoveAccessory(Accessory):
    """Stuff"""

    category = CATEGORY_OTHER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add the sprinkler
        serv_sprinkler = self.add_preload_service(
            'Valve', chars=['Active','InUse','ValveType','SetDuration',
     'RemainingDuration',])

    # Configure and set the valve type
        self.char_sprinkler_type = serv_sprinkler.configure_char(
            'ValveType')
        self.char_sprinkler_type.set_value(0)
    #configure and set teh status/active (Inuse/Active)
        self.char_sprinkler_status = serv_sprinkler.configure_char(
            'InUse', setter_callback=self.set_sprinkler_status)
        self.char_sprinkler_active = serv_sprinkler.configure_char(
            'Active', setter_callback=self.set_sprinkler_active)
    # Confgue Duration and Remaining Duration

        self.char_sprinkler_duration = serv_sprinkler.configure_char(
            'SetDuration', setter_callback=self.set_sprinkler_duration)

        self.char_sprinkler_duration = serv_sprinkler.configure_char(
            'RemainingDuration', setter_callback=self.get_sprinkler_duration)

    #Add grow lamp light on there
        serv_growlamp = self.add_preload_service(
            'Lightbulb', chars=['On'])
        self.char_growlamp_status = serv_growlamp.configure_char(
            'On', setter_callback=self.set_growlamp_status)

        self.blocking=0

    # Duration funcations
    def get_sprinkler_duration(self,value):
        logger.debug("Sprinkler duration has %s left", value)
    def set_sprinkler_duration(self,value):
        logger.debug("Sprinkler duration changed to %s", value)
    # Sprinkler Status
    def set_sprinkler_status(self, value):
        logger.debug("Sprinkler status changed to %s", value)

    def set_sprinkler_active(self, programmode):
        logger.debug("Sprinkler activate status to %s", programmode)

    def set_growlamp_status(self, value):
            if (value == 1):
                #self.char_growlamp_status.set_value(self.send_command("light_on"))
                value=self.request_to_send_command("light_on")
                self.char_growlamp_status.set_value(value)
            else if (value ==0):
                #self.char_growlamp_status.set_value(self.send_command("light_off"))
                value=self.request_to_send_command("light_off")
                self.char_growlamp_status.set_value(value)
            logger.debug("Grow lamp status changed %s", self.char_growlamp_status)


    # checks to see if serial port is being blocked, if some other thread is using it wait to send command
    def request_to_send_command(self,command):
        if (self.blocking ==0):
            logger.debug("serial not blocked")
            return(self.send_command(command))
        else:
            while (self.blocking == 1):
                logger.debug("Waiting to unblock %s", self.blocking)
                sleep (2)
                if (self.blocking ==0):
                    return(self.send_command(command))
                    break

    # Used to send commands to the serial port (Puts a blocking flag while in use)
    def send_command(self,command):
        while:blcokign
        self.blocking=1
        port.flushInput()
        command_string=command+'\n'
        port.write(str.encode(command_string))
        rcv = port.readline()
        self.blocking=0
        return int(rcv.decode('utf-8'))


    def publish_to_log(self,log_file_path,value):
        with open(log_file_path, "a") as log_file:
            log_file.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(value)))

    def get_average_light(self):
        return ""

    @Accessory.run_at_interval(500)
    def run(self):
        logger.debug("Starting Loop Function")
        # Request serial info from UART for moisture + light
        current_moisture=self.request_to_send_command("moisture")
        current_light=self.request_to_send_command("light")
        # Log the moisture
        logger.debug("Curret Moisture %s", current_moisture)
        self.publish_to_log(MoistureLogPath,current_moisture)
        # Log the light
        logger.debug("Curret Light %s", current_light)
        self.publish_to_log(LightLogPath,current_light)

        #if moisture is to low, go ahead and water the plants

        if (current_moisture < 500):

            logger.debug("Turning Pump On")
            pump_status=self.request_to_send_command("pump_on")
            logger.debug("pump status %s", pump_status)
            self.char_sprinkler_active.set_value(pump_status)
            logger.debug("Pump Should Turn off in 2 Seconds")
            sleep (2)
            self.char_sprinkler_active.set_value(0)

        else:
            logger.debug("water seems good")
