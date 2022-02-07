"""
Python module for interfacing Analog Devices ADXL355 accelererometer through SPI
bus with the Raspberry Pi

Code used from : https://github.com/nuclearfutureslab/adxl355-pi
"""

import spidev
import time
import wiringpi as wp
from ADXL355_definitions import *


class ADXL355():
    def __init__(self):
        # SPI init
        self.spi = spidev.SpiDev()
        self.spi.open(SPI_BUS, SPI_DEVICE)
        self.spi.max_speed_hz = SPI_MAX_CLOCK_HZ
        self.spi.mode = SPI_MODE

        wp.wiringPiSetupPhys()                  # Use physical pin numbers
        self.drdy_pin = DRDY_PIN                # Define Data Ready pin
        self.drdy_delay = DRDY_DELAY            # Define Data Ready delay
        self.drdy_timeout = DRDY_TIMEOUT        # Define Data Ready timeout

        # Default device parameters
        RANGE = 2.048
        ODR   = 125
        HPFC  = 0
        
        # Device init
        self.transfer = self.spi.xfer2
        self.setrange(RANGE)                    # Set default measurement range
        self.setfilter(ODR, HPFC)               # Set default ODR and filter props
        self.wait_drdy()

        self.factor = (RANGE * 2) / 2 ** 20     # Instrument factor raw to g

    def read(self, register, length=1):
        address = (register << 1) | 0b1
        if length == 1:
            result = self.transfer([address, 0x00])
            return result[1]
        else:
            result = self.transfer([address] + [0x00] * (length))
            return result[1:]

    def write(self, register, value):
        # Shift register address 1 bit left, and set LSB to zero
        address = (register << 1) & 0b11111110
        result = self.transfer([address, value])
    
    def wait_drdy(self):
        start = time.time()
        elapsed = time.time() - start
        # Wait DRDY pin to go low or DRDY_TIMEOUT seconds to pass
        if self.drdy_pin is not None:
            drdy_level = wp.digitalRead(self.drdy_pin)
            while (drdy_level == wp.LOW) and (elapsed < self.drdy_timeout):
                elapsed = time.time() - start
                drdy_level = wp.digitalRead(self.drdy_pin)
                # Delay in order to avoid busy wait and reduce CPU load.
                time.sleep(self.drdy_delay)
            if elapsed >= self.drdy_timeout:
                print("\nTimeout while polling DRDY pin")
        else:
            time.sleep(self.drdy_timeout)
            print("\nDRDY Pin did not connected")
    
    def fifofull(self):
        return self.read(REG_STATUS) & 0b10

    def fifooverrange(self):
        return self.read(REG_STATUS) & 0b100
    
    def start(self):
        tmp = self.read(REG_POWER_CTL)
        self.write(REG_POWER_CTL, tmp & 0b0)

    def stop(self):
        tmp = self.read(REG_POWER_CTL)
        self.write(REG_POWER_CTL, tmp | 0b1)
        
    def dumpinfo(self):
        print("ADXL355 SPI Info Dump")
        print("========================================")
        idad = self.read(REG_DEVID_AD)
        print("Analog Devices ID: 0x{:X}".format(idad))
        memsid = self.read(REG_DEVID_MST)
        print("Analog Devices MEMS ID: 0x{:X}".format(memsid))
        devid = self.read(REG_PARTID)
        print("Device ID: 0x{0:X} (octal: {0:o})".format(devid))

        powerctl = self.read(REG_POWER_CTL)
        print("Power Control Status: 0b{:08b}".format(powerctl))
        if(powerctl & 0b1):
            print("--> Standby")
        else:
            print("--> Measurement Mode")

        rng = self.read(REG_RANGE)
        if rng & 0b11 == RANGE_2G:
            print("Operating in 2g range")
        if rng & 0b11 == RANGE_4G:
            print("Operating in 4g range")
        if rng & 0b11 == RANGE_8G:
            print("Operating in 8g range")
        print("========================================")     

    def whoami(self):
        t = self.read(REG_PARTID)
        return t
    
    def twocomp(self, value):
        if (0x80000 & value):
            ret = - (0x0100000 - value)
            # from ADXL355_Acceleration_Data_Conversion function from EVAL-ADICUP360 repository
            # value = value | 0xFFF00000
        else:
            ret = value
        return ret

    def setrange(self, r):
        self.stop()
        temp = self.read(REG_RANGE)
        self.write(REG_RANGE, (temp & 0b11111100) | RANGE_TO_BIT[r])
        self.start()

    def setfilter(self, lpf, hpf):
        self.stop()
        self.write(REG_FILTER, (HPFC_TO_BIT[hpf] << 4) | ODR_TO_BIT[lpf])
        self.start()
    
    def getXRaw(self):
        datal = self.read(REG_XDATA3, 3)
        low = (datal[2] >> 4)
        mid = (datal[1] << 4)
        high = (datal[0] << 12)
        res = low | mid | high
        res = self.twocomp(res)
        return res

    def getYRaw(self):
        datal = self.read(REG_YDATA3, 3)
        low = (datal[2] >> 4)
        mid = (datal[1] << 4)
        high = (datal[0] << 12)
        res = low | mid | high
        res = self.twocomp(res)
        return res

    def getZRaw(self):
        datal = self.read(REG_ZDATA3, 3)
        low = (datal[2] >> 4)
        mid = (datal[1] << 4)
        high = (datal[0] << 12)
        res = low | mid | high
        res = self.twocomp(res)
        return res

    def getX(self):
        return float(self.getXRaw()) * self.factor

    def getY(self):
        return float(self.getYRaw()) * self.factor
    
    def getZ(self):
        return float(self.getZRaw()) * self.factor

    def getTempRaw(self):
        high = self.read(REG_TEMP2)
        low = self.read(REG_TEMP1)
        res = ((high & 0b00001111) << 8) | low
        return res

    def getTemp(self, bias = 1852.0, slope=-9.05):
        temp = self.temperatureRaw()
        res = ((temp - bias) / slope) + 25;
        return res

    def get3Vfifo(self):
        res = []
        x = self.read(REG_FIFO_DATA, 3)
        while(x[2] & 0b10 == 0):
            y = self.read(REG_FIFO_DATA, 3)
            z = self.read(REG_FIFO_DATA, 3)
            res.append([x, y, z])
            x = self.read(REG_FIFO_DATA, 3)
        return res

    def emptyfifo(self):
        x = self.read(REG_FIFO_DATA, 3)
        while(x[2] & 0b10 == 0):
            x = self.read(REG_FIFO_DATA, 3)

    def hasnewdata(self):
        res = self.read(REG_STATUS)
        if res & 0b1:
            return True
        return False

    def fastgetsamples(self, sampleno = 1000):
        """Get specified numbers of samples from FIFO, without any processing.

        This function is needed for fast sampling, without loosing samples. While FIFO should be enough for many situations, there is no check for FIFO overflow implemented (yet).
        """
        res = []
        while(len(res) < sampleno):
            res += self.get3Vfifo()
        return res[0:sampleno]

    def getsamplesRaw(self, sampleno = 1000):
        """Get specified numbers of samples from FIFO, and process them into signed integers"""
        data = self.fastgetsamples(sampleno)
        return self.convertlisttoRaw(data)

    def getsamples(self, sampleno = 1000):
        """Get specified numbers of samples from FIFO, process and convert to g values"""
        data = self.getsamplesRaw(sampleno)
        return self.convertRawtog(data)

    def convertlisttoRaw(self, data):
        """Convert a list of 'list' style samples into signed integers"""
        res = []
        for i in range(len(data)):
            row3v = []
            for j in range(3):
                low = (data[i][j][2] >> 4)
                mid = (data[i][j][1] << 4)
                high = (data[i][j][0] << 12)
                value = 1 * self.twocomp(low | mid | high)
                row3v.append(value)
            res.append(row3v)
        return res

    def convertRawtog(self, data):
        """Convert a list of raw style samples into g values"""
        res = [[d[0] * self.factor, d[1] * self.factor, d[2] * self.factor] for d in data]
        return res

    def getAxisRaw(self):
        self.wait_drdy()
        return self.getXRaw(), self.getYRaw(), self.getZRaw()
    
    def getAxis(self):
        self.wait_drdy()
        return self.getX(), self.getY(), self.getZ()    
