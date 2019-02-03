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
            'IrrigationSystem', chars=['Active','ProgramMode','InUse'])

        self.char_sprinkler_status = serv_sprinkler.configure_char(
            'InUse', setter_callback=self.set_sprinkler_status)
        self.char_sprinkler_mode = serv_sprinkler.configure_char(
            'ProgramMode', setter_callback=self.set_sprinkler_program)

        #Add grow lamp
        serv_growlamp = self.add_preload_service(
            'Lightbulb', chars=['On'])
        self.char_growlamp_status = serv_growlamp.configure_char(
            'On', setter_callback=self.set_growlamp_status)

        self.blocking=0

    def set_sprinkler_status(self, value):
        logger.debug("Sprinkler status changed to %s", value)

    def set_sprinkler_program(self, programmode):
        logger.debug("Sprinkler duration set to %s", programmode)

    def set_growlamp_status(self, value):


            if (value == 1 and self.blocking ==0):
                self.send_command("light_on")
            if (value ==0 and self.blocking ==0):
                self.send_command("light_off")

            logger.debug("Grow lamp status changed %s", self.char_growlamp_status)


    def send_command(self,command):
        self.blocking=1
        command_string=command+'\n'
        port.write(str.encode(command_string))
        rcv = port.readline()
        port.flushInput()
        self.blocking=0
        return int(rcv.decode('utf-8'))


    def publish_to_log(self,log_file_path,value):
        with open(log_file_path, "a") as log_file:
            log_file.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(value)))

    def get_average_light(self):
        return ""

    @Accessory.run_at_interval(10)
    def run(self):
        print ("Starting Loop Function")
        if self.blocking ==0:
            print ("serial not blocked")

            current_moisture=self.send_command("moisture")
            sleep(1)
            current_light=self.send_command("light")

            # Log the moisture
            print ("Curret Moisture %s", current_moisture)
            self.publish_to_log(MoistureLogPath,current_moisture)
            # Log the light
            print ("Curret Light %s", current_light)
            self.publish_to_log(LightLogPath,current_light)

           #if moisture is to low, go ahead and water the plants

            if (current_moisture < 500):

                print ("Turning Pump On")
                pump_status=self.send_command("pump_on")
                print ("pump status %s", pump_status)
                self.char_growlamp_status = pump_status
                print ("Pump Should Turn off in 2 Seconds")

            else:
                print ("water seems good")
