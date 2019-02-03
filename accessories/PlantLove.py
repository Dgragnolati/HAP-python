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
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)
LightLogPath = "/home/pi/HAP/light.csv"
MoistureLogPath = "/home/pi/HAP/moisture.csv"

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

    def set_growlamp_status(self, value):
        if (value == 1):
            print ("Turning Lights On")
            port.write(str.encode('light_on\n'))
        if (value ==0):
            print ("Turning Lights Off")
            port.write(str.encode('light_off\n'))

        logger.debug("Grow lamp status changed %s", value)


    def get_light_value(self):
        ort.write(str.encode('light\n'))
        rcv = port.readline()
        return str(rcv.decode('utf-8'))

    def get_moisture_value(self):
        ort.write(str.encode('moisture\n'))
        rcv = port.readline()
        return str(rcv.decode('utf-8'))

    def publish_to_log(self,log_file_path,value):
        with open(log_file_path, "a") as log_file:
            log_file.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(value)))

    def turn_pump_on(self):
        port.write(str.encode('pump_on\n'))

    def get_average_light(self):
        return ""

    @Accessory.run_at_interval(10)
    def run(self):

        publish_to_log(self,LightLogPath,get_light_value())
        publish_to_log(self,MoistureLogPath,get_light_value())
        print ("Curret Moisture %s", get_moisture_value())
        print ("Curret Light %s", get_light_value())

        if (get_moisture_value() < 500):

            print ("Turning Pump On")
            turn_pump_on()
            self.char_sprinkler_status=1
            sleep (3)
            self.char_sprinkler_status=0
            print ("Pump Should be off ????")
        else:
            print ("water seems good")
