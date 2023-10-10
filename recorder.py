import time
import matplotlib.pyplot as plt
import scipy.signal as signal
import RPi.GPIO as GPIO

from numpy import asarray,linspace, mean, sqrt, mean, absolute, log10, pi
from obspy.core import Trace, Stream
from obspy import read
from datetime import datetime
from CEDAS_ACC_library import ADXL355

# --- INPUTS ---
output_range = 2.048                # Select measurement range
sampling_rate = 62.5                # Select sampling rate
hpass_corner = 0                    # Select high-pass filter corner
duration = 10                       # Record lenght as second
buzzer_threshold = 0.0004

network = "CEDAS"
station = "ACC"
location = ""
channel = ["X","Y","Z"]

# --- SETUP GPIO ---
LED_PIN = 13
BUZZER_PIN = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# sudo nice -n -20 python3 recorder_v4.py
# --- VARIABLES ---
interval = 1 / sampling_rate                      # Interval millisecond
npts = int(duration * sampling_rate)              # Number of data points
fn = sampling_rate / 2                            # Nyquist frequency

# --- SET ADXL355 PARAMETERS  ---
adxl355 = ADXL355()
adxl355.setrange(output_range)                    # Set measurement range
adxl355.setfilter(sampling_rate, hpass_corner)    # Set data rate and filter properties 
adxl355.start()                                   # Enable measurement mode
time.sleep(0.1)                                   # Wait briefly until the sensor is ready

# --- READING LOOP ---
print("Recording...")

# --- RECORDING LED (PULL HIGH) ---
GPIO.output(LED_PIN, GPIO.HIGH)

counter = 0
data = [[], [], []]


# Get starting time
dt_object = datetime.now()
start = time.time()
while True:
    counter+= 1
    if counter <= npts:
        try:
            x, y, z = adxl355.getAxisRaw()
            data[0].append(x)
            data[1].append(y)
            data[2].append(z)
            
            """
            if absolute(x/256000) > buzzer_threshold or absolute(y/256000) > buzzer_threshold:
                GPIO.output(BUZZER_PIN, GPIO.HIGH)

            elif GPIO.input(BUZZER_PIN) == True:
                GPIO.output(BUZZER_PIN, GPIO.LOW)"""

            
        
        except KeyboardInterrupt:
            # Get ending time
            end = time.time()

            # If interrupted update npts
            npts = len(data[0])
            
            break
    else:
        # Get ending time
        end = time.time()
        
        break


end = time.time()


# Convert list to array
data = asarray(data)

print(f"Elapsed Time : {round((end-start),2)} second \n")
adxl355.stop()          # Enable standby mode

# --- RECORDING LED (PULL LOW) ---
GPIO.output(LED_PIN, GPIO.LOW)
GPIO.output(BUZZER_PIN, GPIO.LOW)
GPIO.cleanup()



# --- SAVE TO MINISEED ---
print("Writing miniseed file...\n")

dt_date = dt_object.strftime('%Y%m%d_%H%M')
mseed_filename = str(f"{network}_{station}_{dt_date}")

def getTrace(data, index):
        stats = {"network":network,"station":station,"location":location,
         "channel":channel[index], "npts": npts , "sampling_rate": sampling_rate,
         "delta": 1/sampling_rate, "mseed":{"dataquality":"D"},
         "starttime": start, "endtime": end}
        return Trace(data[index], header=stats) 
    
st = Stream(traces=[getTrace(data, 0), getTrace(data, 1), getTrace(data, 2)])

fmseed = f"records/{mseed_filename}.mseed"     
st.write(fmseed, format="MSEED", encoding="INT32", reclen=512)


# --- FILTER FUNCTIONS ---
# Apply Filter

def butterworthFilter(btype, highcut, lowcut, fs, order):
    fn = 0.5 * fs
    if btype == "bandpass":
        b, a = signal.butter(order, [highcut/fn, lowcut/fn], btype = btype)
    elif btype == "lowpass":
        b, a = signal.butter(order, lowcut/fn, btype = btype)
    elif btype == "highpass":
        b, a = signal.butter(order, highcut/fn, btype = btype)
    else:
        print(" Filter type error!!! ")
    return b, a

def filterRecord(data, btype, highcut, lowcut, fs, order):
    global w, h
    b, a = butterworthFilter(btype, highcut, lowcut, fs, order = order)
    w, h = getFrequencyResponse(a, b, fs)
    return signal.filtfilt(b, a, data, method = "gust")

def getFrequencyResponse(a, b, fs):
    w, h = signal.freqz(a, b, worN = 4096)
    return w * fs/(2*pi), -20 * log10(abs(h))


btype, lc, hc, order = "lowpass", 0.2, 5, 8

# --- PLOT ---
print("Plotting...")
# Time Series
record = read(fmseed)

#x = filterRecord(record[0].data/256000, btype, lc, hc, sampling_rate, order) 
x = record[0].data/256000

#y = filterRecord(record[1].data/256000, btype, lc, hc, sampling_rate, order) 
y = record[1].data/256000

#z = filterRecord(record[2].data/256000, btype, lc, hc, sampling_rate, order) 
z = record[2].data/256000

time = linspace(0, npts/sampling_rate, npts)

# Fourier Transform
def welchMethod(data, window_length, overlap, sampling_rate):
    data = data-mean(data)
    window_size = int(window_length * sampling_rate)
    window = signal.windows.barthann(window_size)   # hann
    w_fft, welch_m = signal.welch(data, fs = sampling_rate, window = window, nperseg = window_size, noverlap = window_size/overlap) 
    return w_fft, welch_m  #sqrt(welch_m)  


w_size, overlap = 120, 2
if w_size > npts/sampling_rate:
    w_size = npts / sampling_rate
    
frq_x, amp_x = welchMethod(x*1000000, w_size, overlap, sampling_rate)
frq_y, amp_y = welchMethod(y*1000000, w_size, overlap, sampling_rate)
frq_z, amp_z = welchMethod(z*1000000, w_size, overlap, sampling_rate)


# Plot
fig, (ax1, ax2) = plt.subplots(2,1)
fig.subplots_adjust(hspace=0.5)

ax1.plot(time, z, color="green", lw=1, label="Z", alpha=0.6)
ax1.plot(time, x, color="blue", lw=1, label="X", alpha = 0.8)
ax1.plot(time, y, color="red", lw=1, label="Y", alpha = 0.8)
ax1.set_title("Time Series (X,Y,Z)")
ax1.set_xlabel("Time")
ax1.set_ylabel("Acceleration g")
ax1.grid()
ax1.legend(prop={'size': 6})


ax2.plot(frq_z, amp_z, color="green", lw=1, label="Z", alpha=0.6)
ax2.plot(frq_x, amp_x, color="blue", lw=1, label="X", alpha=0.8)
ax2.plot(frq_y, amp_y, color="red", lw=1, label="Y", alpha=0.8)
ax2.set_title("PSD")
ax2.set_xlabel("Frequency Hz")
ax2.set_ylabel("PSD ug^2/Hz")
ax2.set_yscale("log")
ax2.legend(prop={'size': 6})
ax2.grid()

# Save
#plt.savefig('timeseries_fft.png', dpi = 250)
plt.show()





