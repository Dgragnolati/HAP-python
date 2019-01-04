####################################################################
#Import libraries
####################################################################
import time
from datetime import datetime
import pigpio
import DHT22
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import bytespdate2num

#define pigpio and DHT22 sensor
pi=pigpio.pi()
s=DHT22.sensor(pi,22, LED=None, power=4)

#set initial day and the sampling rate
Day=datetime.now().strftime("%d")
Interval = 30.0
target = time.time() + Interval

try:
    while True:
        #set the current day
        NewDay = datetime.now().strftime("%d")

        if int(NewDay)==int(Day):

            #Read data from the DHT22 sensor
            s.trigger()
            time.sleep(0.2) # stops sensor spitting out jargon

            humidity = '{:3.2f}'.format(s.humidity()/1.)
            temperature = '{:3.2f}'.format(s.temperature()/1.)

            #set up file saving
            Date = datetime.now().strftime("%y:%m:%d") #formatted as year:month:day
            Time = datetime.now().strftime("%H:%M:%S")

            data = [Time,humidity,temperature]  #create list with all the parameters that are to be saved

            Dir_name= '/home/pi/HumidityData'  #set file save directory. YOU MUST CREATE A FOLDER IN THE DIRECTORY CALLED 'HumudityData'.
            Filename= '%s_Humidity_Recording' %Date  #set filename to include the date

            # write data to file
            with open(os.path.join(Dir_name,Filename + '.csv'), 'a') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(data)

            # Ensure the sampling rate is correct
            while True:
                if target < time.time():
                    target = target + Interval
                    break
                time.sleep(0.01)

        else:
            #If the date changes a plot will be produced for the previous days recording and the initial 'Day' will be updated to the current day

            #Read in data from file
            ReadFile= os.path.join(Dir_name,Filename + '.csv')
            TimeRead, HumRead, TempRead = np.loadtxt(ReadFile, delimiter=',', unpack=True, converters={0: bytespdate2num('%H:%M:%S')}) # defines the parameters in the .csv file

            #plot data on same graph, different y axis
            #set up the temperature plot
            fig, ax1 = plt.subplots()
            color = 'tab:red'
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Temp (C)', color=color)
            ax1.plot(TimeRead, TempRead, color = color)
            ax1.tick_params(axis='y', labelcolor=color)

            #set up the humidity plot
            ax2 = ax1.twinx()
            color = 'tab:blue'
            ax2.set_ylabel('Humidity (%)', color=color)
            ax2.plot(TimeRead, HumRead, color = color)
            ax2.tick_params(axis='y', labelcolor=color)

            #plot formatting
            fig.tight_layout()
            plt.title(Filename)
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            plt.gcf().autofmt_xdate()

            #save plot to same directory as .csv files. Don't automatically display the plot
            plt.savefig(os.path.join(Dir_name,Filename + '.png'))
            plt.close()

            #reset the previous day to be the current day. This will allow loop to go back to the top of the if statement and start saving in a new file
            Day=NewDay

            time.sleep(0.1)

except KeyboardInterrupt:
        #message to tell user that the python script has closed
        print('Humidity sensor shut down')

finally:
    #clear DHT22 sensor
    s.cancel()
      
