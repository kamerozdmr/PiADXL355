import time
import sys
import numpy as np
import matplotlib.pyplot as plt
from obspy.core import Trace, Stream
from obspy import read

sys.path.append("../")
from CEDAS_ACC_library import ADXL355

# --- INPUTS ---
output_range = 2.048            # Select measurement range
sampling_rate = 125             # Select sampling rate
hpass_corner = 0                # Select high-pass filter corner
duration = 10                   # Record lenght as second
network = "CEDAS"
station = "ACC001"
location = ""
channel = ["X","Y","Z"]

# --- VARIABLES ---
interval = 1 / sampling_rate                      # Interval millisecond
npts = int(duration * sampling_rate)              # Number of data points
fn = sampling_rate / 2                            # Nyquist frequency
t = np.linspace(0, duration, npts)                # Create time domain
data = np.zeros((3, npts), dtype = np.float64)    # Create an empty array

# --- SET ADXL355 PARAMETERS ---
adxl355 = ADXL355()
adxl355.setrange(output_range)                    # Set measurement range
adxl355.setfilter(sampling_rate, hpass_corner)    # Set data rate and filter properties 
adxl355.start()                                   # Enable measurement mode
time.sleep(0.1)                                   # Wait briefly until the sensor is ready

# --- READING LOOP ---
print("Recording...")
start = time.time()
for i in range(npts):
    data[0][i], data[1][i], data[2][i] = adxl355.getAxis()
end = time.time()

adxl355.stop()          # Enable standby mode

print(f"Elapsed Time : {round((end-start),2)} second \n")


# --- SAVE TO MINISEED ---
print("Writing miniseed file...\n")
mseed_filename = (str(f"{network}-{station}-{location}-{start}-{end}"))

def getTrace(data, index):
        stats = {"network":network,"station":station,"location":location,
         "channel":channel[index], "npts": npts , "sampling_rate": sampling_rate,
         "delta": 1/sampling_rate, "mseed":{"dataquality":"D"},
         "starttime": start, "endtime": end}
        return Trace(data[index], header=stats) 
    
st = Stream(traces=[getTrace(data, 0), getTrace(data, 1), getTrace(data, 2)])

fmseed = mseed_filename + ".mseed"     
st.write(fmseed, format="MSEED", encoding="FLOAT64", reclen=512)

# --- PLOT ---
#print(st)
#print(st[0].stats)
st.plot()
