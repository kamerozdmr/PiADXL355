# PiADXL355
Python module for interfacing Analog Devices ADXL355 accelererometer through SPI bus with the Raspberry Pi.

Module depends on wiringpi python library. 

Module uses data ready pin for timing. ODR values given in datasheet can be used as a sampling rate. Time drift is approximately 12 seconds per hour.

Device can be used for vibration monitoring and structural health monitoring applications.

----------------------------------------------------------------------------------

Example 2 - Read acceleration and plot Spectrum Density of the record.

<img src="pictures/spectral_density.png" width="600" height="480">

----------------------------------------------------------------------------------

Example 3 - Writing acceleration data to Mini-SEED file.

<img src="pictures/time_series.png" width="600" height="480">

----------------------------------------------------------------------------------

Examples are tested with ADXL355Z evaluation board and Raspberry Pi 4 Model B

[ADXL355 Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/adxl354_355.pdf)

[ADXL355Z Eval Board](https://www.analog.com/media/en/technical-documentation/user-guides/eval-adxl354-355-ug-1030.pdf)

<img src="pictures/device1.png" width="600" height="480">
<img src="pictures/device2.png" width="600" height="480">

Wiring of ADXL355 to Raspberry Pi 
| ADXL355 Pin | Description | Raspberry Pin |
|:------------:|:------------:|:------------:|
| 1 (Vddio) | 3.3V Digital Power | 1 |
| 3 (Vdd) | 3.3V Digital Power | 1 |
| 5 (Gnd) | Ground | 9 |
| 6 (Drdy) | Data Ready | 11 |
| 8 (Cs) | Chip Select | 24 |
| 10 (Sclk) | Serial Clock | 23 |
| 11 (Miso) | Master In Slave Out | 21 |
| 12 (Mosi) | Master Out Slave In | 19 |
