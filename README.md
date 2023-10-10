# PiADXL355

Python module for interfacing with the Analog Devices ADXL355 accelerometer through the SPI bus on the Raspberry Pi.

All you need is a Raspberry Pi 4, an SD card, a sensor board, and some jumper wires.

The module uses the data-ready pin for accurate sampling rates. ODR values given in the datasheet can be used as the sampling rate.

Acceleration data is written to the miniSEED file format with header information.

This version of the module uses internal synchronization; thus, the sampling rate is not accurate and stable.

----------------------------------------------------------------------------------

Examples are tested with the ADXL355Z evaluation board and the Raspberry Pi 4 Model B 4GB version.


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

----------------------------------------------------------------------------------

Example 1 - Read acceleration and plot Spectral Density of the record.

<img src="pictures/spectral_density.png" width="720" height="540">

----------------------------------------------------------------------------------

Example 2 - Write acceleration data to miniSEED file.

<img src="pictures/time_series.png" width="600" height="600">

