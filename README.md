# PiADXL355
Python module for interfacing Analog Devices ADXL355 accelererometer through SPI
bus with the Raspberry Pi





Examples are tested with ADXL355Z evaluation board and Raspberry Pi 4 Model B

[ADXL355 Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/adxl354_355.pdf)

[ADXL355Z Eval Board](https://www.analog.com/media/en/technical-documentation/user-guides/eval-adxl354-355-ug-1030.pdf)

<img src="pictures/device1.png" width="480" height="400">
<img src="pictures/device2.png" width="480" height="400">

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
