import time
import sys
sys.path.append("../")
from ADXL355_library import ADXL355

adxl355 = ADXL355()     # Import python class
adxl355.start()         # Enable measurement mode
time.sleep(0.1)         # Wait briefly until the sensor is ready

# Give device info 
print(adxl355.dumpinfo())

# Read raw acceleration value in each axis
#print("Raw acceleration value in X-Y-Z direction")
#print(adxl355.getAxisRaw())

# Read acceleration as g in each axis
print("Acceleration as g in X-Y-Z direction")
print(adxl355.getAxis())

adxl355.stop()          # Enable standby mode
