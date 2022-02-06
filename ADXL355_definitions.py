# SPI config
SPI_MAX_CLOCK_HZ = 10000000
SPI_MODE = 0b00
SPI_BUS = 0
SPI_DEVICE = 0


# DRDY config 
DRDY_PIN = 11              # Raspberry Pi GPIO pin for DRDY cable 
DRDY_DELAY = 0.000001      # Delay while polling DRDY pin in seconds 
DRDY_TIMEOUT = 3           # Delay to check DRDY pin in seconds


# Register addresses
REG_DEVID_AD     = 0x00
REG_DEVID_MST    = 0x01
REG_PARTID       = 0x02
REG_REVID        = 0x03
REG_STATUS       = 0x04
REG_FIFO_ENTRIES = 0x05
REG_TEMP2        = 0x06
REG_TEMP1        = 0x07
REG_XDATA3       = 0x08
REG_XDATA2       = 0x09
REG_XDATA1       = 0x0A
REG_YDATA3       = 0x0B
REG_YDATA2       = 0x0C
REG_YDATA1       = 0x0D
REG_ZDATA3       = 0x0E
REG_ZDATA2       = 0x0F
REG_ZDATA1       = 0x10
REG_FIFO_DATA    = 0x11
REG_OFFSET_X_H   = 0x1E
REG_OFFSET_X_L   = 0x1F
REG_OFFSET_Y_H   = 0x20
REG_OFFSET_Y_L   = 0x21
REG_OFFSET_Z_H   = 0x22
REG_OFFSET_Z_L   = 0x23
REG_ACT_EN       = 0x24
REG_ACT_THRESH_H = 0x25
REG_ACT_THRESH_L = 0x26
REG_ACT_COUNT    = 0x27
REG_FILTER       = 0x28
REG_FIFO_SAMPLES = 0x29
REG_INT_MAP      = 0x2A
REG_SYNC         = 0x2B
REG_RANGE        = 0x2C
REG_POWER_CTL    = 0x2D
REG_SELF_TEST    = 0x2E
REG_RESET        = 0x2F


# Measaurement range definition
RANGE_2G     = 0b01
RANGE_4G     = 0b10
RANGE_8G     = 0b11


# ODR and low-pass filter corner definition
                            # Data rate-lowpass corner 
ODR_4000     = 0b0000       # 4000-1000 Hz
ODR_2000     = 0b0001       # 2000-500 Hz
ODR_1000     = 0b0010       # 1000-250 Hz
ODR_500      = 0b0011       # 500-125 Hz
ODR_250      = 0b0100       # 250-62.5 Hz
ODR_125      = 0b0101       # 125-31.5 Hz
ODR_62_5     = 0b0110       # 62.5-15.625 Hz
ODR_31_25    = 0b0111       # 31.25-7.813 Hz
ODR_15_625   = 0b1000       # 15.625-3.906 Hz
ODR_7_813    = 0b1001       # 7.813-1.95 3Hz
ODR_3_906    = 0b1010       # 3.906-0.977 Hz


# High-pass filter corner definition
HPFC_0 = 0b000          # No high-pass filter
HPFC_1 = 0b001          # 24.70 x 10-4 x ODR
HPFC_2 = 0b010          # 6.208 x 10-4 x ODR
HPFC_3 = 0b011          # 1.554 x 10-4 x ODR
HPFC_4 = 0b100          # 0.386 x 10-4 x ODR
HPFC_5 = 0b101          # 0.095 x 10-4 x ODR
HPFC_6 = 0b110          # 0.023 x 10-4 x ODR

RANGE_TO_BIT = {2.048 : RANGE_2G,
                4.096 : RANGE_4G,
                8.192 : RANGE_8G}

ODR_TO_BIT = {4000  : ODR_4000,
              2000  : ODR_2000,
              1000  : ODR_1000,
              500   : ODR_500,
              250   : ODR_250,
              125   : ODR_125,
              62.5  : ODR_62_5,
              31.25 : ODR_31_25,
              15.625: ODR_15_625,
              7.813 : ODR_7_813,
              3.906 : ODR_3_906}

HPFC_TO_BIT = {0 : HPFC_0,
               1 : HPFC_1,
               2 : HPFC_2,
               3 : HPFC_3,
               4 : HPFC_4,
               5 : HPFC_5,
               6 : HPFC_6}
