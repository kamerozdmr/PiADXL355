"""
Python module for interfacing Analog Devices ADXL355 accelererometer through SPI
bus with the Raspberry Pi
"""

import spidev
import time
import wiringpi as wp
from CEDAS_ACC_definitions import *

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

        self.factor = (RANGE * 2) / 2 ** 20     # Instrument factor raw to g [not accurate]

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
                #self.wait2go_low()
            if elapsed >= self.drdy_timeout:
                print("\nTimeout while polling DRDY pin")
        else:
            time.sleep(self.drdy_timeout)
            print("\nDRDY pin did not connected")

    def wait2go_low(self):
        drdy_level = wp.digitalRead(self.drdy_pin)
        while (drdy_level == wp.HIGH):
            drdy_level = wp.digitalRead(self.drdy_pin)
            time.sleep(self.drdy_delay)
    
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
    
    def conversion(self, value):
        if (0x80000 & value):
            ret = - (0x0100000 - value)
            """Convversion function from EVAL-ADICUP360 repository"""
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
        res = self.conversion(res)
        return res

    def getYRaw(self):
        datal = self.read(REG_YDATA3, 3)
        low = (datal[2] >> 4)
        mid = (datal[1] << 4)
        high = (datal[0] << 12)
        res = low | mid | high
        res = self.conversion(res)
        return res

    def getZRaw(self):
        datal = self.read(REG_ZDATA3, 3)
        low = (datal[2] >> 4)
        mid = (datal[1] << 4)
        high = (datal[0] << 12)
        res = low | mid | high
        res = self.conversion(res)
        return res

    def getX(self):
        return float(self.getXRaw()) * self.factor

    def getY(self):
        return float(self.getYRaw()) * self.factor
    
    def getZ(self):
        return float(self.getZRaw()) * self.factor

    def get3Vfifo(self):
        res = []
        x = self.read(REG_FIFO_DATA, 3)
        while(x[2] & 0b10 == 0):
            y = self.read(REG_FIFO_DATA, 3)
            z = self.read(REG_FIFO_DATA, 3)
            res.append([x, y, z])
            x = self.read(REG_FIFO_DATA, 3)
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
