# Author: VH, ELI Beamlines, October 2021
# This is script running continously on Raspberry Pi as "service" in background.
# It reads serial port for Prusa MM2S and logs it to log files named "mmu_log_XXX.txt",
# where XXX represents EPOCH timestamp in seconds.
# Each log file has number of lines given by "FILE_LINES" value.
# "PRINT_PERIOD" value states period for logging for MM2S's OK status 'TMC2130_REG_GSTAT: 0'

#!/usr/bin/env python
import time
import serial

PRINT_PERIOD = 300 # [s] printing period for "keep alive" print 'TMC2130_REG_GSTAT: 0' i.e. when no error occurred
FILE_LINES = 100 # [-]  number of lines in created log file, after value is reached, file is closed and new file is created

timestamp1 = time.time() # init timestamp1
timestamp2 = timestamp1

line_counter = 0 #  init counter keeping number of already written in current log file

# Open serial port for connection to Prusa MMU2S
ser = serial.Serial(
 port = '/dev/ttyACM0',
 baudrate = 115200,
 parity = serial.PARITY_NONE,
 stopbits = serial.STOPBITS_TWO,
 bytesize = serial.EIGHTBITS,
)
print("Port opened.")

filestamp = int(timestamp2) # converts to int to remove decimal digits
filename = "mmu_log_" + str(filestamp) + ".txt"
filestream = open(filename, "w") # creates new log file
print("Created new log file: " + filename)

while 1:
 line = str(ser.readline()) # read line from serial port 
 if len(line) > 0 :
  if line.find("TMC2130_REG_GSTAT: 0")!= -1 : # 'TMC2130_REG_GSTAT: 0' ... no error
   timestamp2 = time.time()
   if (timestamp2-timestamp1) > PRINT_PERIOD :
    if line_counter >= FILE_LINES :
     filestamp = int(timestamp2) # converts to int to remove decimal digits
     filestream.close()
     line_counter = 0
     filename = "mmu_log_" + str(filestamp) + ".txt"
     filestream = open(filename, "w") # creates new log file
     print("Created new log file: " + filename)
    print(time.ctime(timestamp2) + " " + line, file = filestream)
    line_counter = line_counter + 1
    timestamp1 = time.time()
  else : #  'TMC2130_REG_GSTAT: <x>'...an error -> see info for register GSTAT in the TMC2130 datasheet 
   if line_counter >= FILE_LINES :
    filestamp = int(timestamp2) # converts to int to remove decimal digits
    filestream.close()
    line_counter = 0 # reset line_counter
    filestream = open("mmu_log_" + str(filestamp) + ".txt", "w") # creates new log file
    filename = "mmu_log_" + str(filestamp) + ".txt"
    filestream = open(filename, "w") # creates new log file
    print("Created new log file: " + filename)
   print(time.ctime(timestamp2) + " " + line, file = filestream)
   line_counter = line_counter + 1
