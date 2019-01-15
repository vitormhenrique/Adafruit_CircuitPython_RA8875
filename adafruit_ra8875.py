# The MIT License (MIT)
#
# Copyright (c) 2019 Melissa LeBlanc-Williams for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`Adafruit_RA8875`
====================================================

A Driver Library for the RA8875

* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Hardware:**

* `RA8875 Driver Board for 40-pin TFT Touch Displays - 800x480 Max <https://www.adafruit.com/product/1590>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports
import time
import adafruit_bus_device.spi_device as spi_device
try:
    import struct
except ImportError:
    import ustruct as struct

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RA8875.git"

# Command/Data for SPI
_DATWR = b'\x00'    # Data Write
_DATRD = b'\x40'    # Data Read
_CMDWR = b'\x80'    # Command Write
_CMDRD = b'\xC0'    # Status Read

# Registers and Bits
_PWRR = 0x01
_PWRR_DISPON = 0x80
_PWRR_DISPOFF = 0x00
_PWRR_SLEEP = 0x02
_PWRR_NORMAL = 0x00
_PWRR_SOFTRESET = 0x01
_MRWC = 0x02
_GPIOX = 0xC7

_PLLC1 = 0x88
_PLLC1_PLLDIV2 = 0x80
_PLLC1_PLLDIV1 = 0x00

_PLLC2 = 0x89
_PLLC2_DIV1 = 0x00
_PLLC2_DIV2 = 0x01
_PLLC2_DIV4 = 0x02
_PLLC2_DIV8 = 0x03
_PLLC2_DIV16 = 0x04
_PLLC2_DIV32 = 0x05
_PLLC2_DIV64 = 0x06
_PLLC2_DIV128 = 0x07

_SYSR = 0x10
_SYSR_8BPP = 0x00
_SYSR_16BPP = 0x0C
_SYSR_MCU8 = 0x00
_SYSR_MCU16 = 0x03

_PCSR = 0x04
_PCSR_PDATR = 0x00
_PCSR_PDATL = 0x80
_PCSR_CLK = 0x00
_PCSR_2CLK = 0x01
_PCSR_4CLK = 0x02
_PCSR_8CLK = 0x03

_HDWR = 0x14

_HNDFTR = 0x15
_HNDFTR_DE_HIGH = 0x00
_HNDFTR_DE_LOW = 0x80

_HNDR = 0x16
_HSTR = 0x17
_HPWR = 0x18
_HPWR_LOW = 0x00
_HPWR_HIGH = 0x80

_VDHR0 = 0x19
_VDHR1 = 0x1A
_VNDR0 = 0x1B
_VNDR1 = 0x1C
_VSTR0 = 0x1D
_VSTR1 = 0x1E
_VPWR = 0x1F
_VPWR_LOW = 0x00
_VPWR_HIGH = 0x80

_HSAW0 = 0x30
_HSAW1 = 0x31
_VSAW0 = 0x32
_VSAW1 = 0x33

_HEAW0 = 0x34
_HEAW1 = 0x35
_VEAW0 = 0x36
_VEAW1 = 0x37

_MCLR = 0x8E
_MCLR_START = 0x80
_MCLR_STOP = 0x00
_MCLR_READSTATUS = 0x80
_MCLR_FULL = 0x00
_MCLR_ACTIVE = 0x40

_DCR = 0x90
_DCR_LNSQTR_START = 0x80
_DCR_LNSQTR_STOP = 0x00
_DCR_LNSQTR_STAT = 0x80
_DCR_CIRC_START = 0x40
_DCR_CIRC_STAT = 0x40
_DCR_CIRC_STOP = 0x00
_DCR_FILL = 0x20
_DCR_NOFILL = 0x00
_DCR_DRAWLN = 0x00
_DCR_DRAWTRI = 0x01
_DCR_DRAWSQU = 0x10

_ELLIPSE = 0xA0
_ELLIPSE_STAT = 0x80

_MWCR0 = 0x40
_MWCR0_GFXMODE = 0x00
_MWCR0_TXTMODE = 0x80

_CURH0 = 0x46
_CURH1 = 0x47
_CURV0 = 0x48
_CURV1 = 0x49

_P1CR = 0x8A
_P1CR_ENABLE = 0x80
_P1CR_DISABLE = 0x00
_P1CR_CLKOUT = 0x10
_P1CR_PWMOUT = 0x00

_P1DCR = 0x8B

_P2CR = 0x8C
_P2CR_ENABLE = 0x80
_P2CR_DISABLE = 0x00
_P2CR_CLKOUT = 0x10
_P2CR_PWMOUT = 0x00

_P2DCR = 0x8D
_PWM_CLK_DIV1 = 0x00
_PWM_CLK_DIV2 = 0x01
_PWM_CLK_DIV4 = 0x02
_PWM_CLK_DIV8 = 0x03
_PWM_CLK_DIV16 = 0x04
_PWM_CLK_DIV32 = 0x05
_PWM_CLK_DIV64 = 0x06
_PWM_CLK_DIV128 = 0x07
_PWM_CLK_DIV256 = 0x08
_PWM_CLK_DIV512 = 0x09
_PWM_CLK_DIV1024 = 0x0A
_PWM_CLK_DIV2048 = 0x0B
_PWM_CLK_DIV4096 = 0x0C
_PWM_CLK_DIV8192 = 0x0D
_PWM_CLK_DIV16384 = 0x0E
_PWM_CLK_DIV32768 = 0x0F

_TPCR0 = 0x70
_TPCR0_ENABLE = 0x80
_TPCR0_DISABLE = 0x00
_TPCR0_WAIT_512CLK = 0x00
_TPCR0_WAIT_1024CLK = 0x10
_TPCR0_WAIT_2048CLK = 0x20
_TPCR0_WAIT_4096CLK = 0x30
_TPCR0_WAIT_8192CLK = 0x40
_TPCR0_WAIT_16384CLK = 0x50
_TPCR0_WAIT_32768CLK = 0x60
_TPCR0_WAIT_65536CLK = 0x70
_TPCR0_WAKEENABLE = 0x08
_TPCR0_WAKEDISABLE = 0x00
_TPCR0_ADCCLK_DIV1 = 0x00
_TPCR0_ADCCLK_DIV2 = 0x01
_TPCR0_ADCCLK_DIV4 = 0x02
_TPCR0_ADCCLK_DIV8 = 0x03
_TPCR0_ADCCLK_DIV16 = 0x04
_TPCR0_ADCCLK_DIV32 = 0x05
_TPCR0_ADCCLK_DIV64 = 0x06
_TPCR0_ADCCLK_DIV128 = 0x07

_TPCR1 = 0x71
_TPCR1_AUTO = 0x00
_TPCR1_MANUAL = 0x40
_TPCR1_VREFINT = 0x00
_TPCR1_VREFEXT = 0x20
_TPCR1_DEBOUNCE = 0x04
_TPCR1_NODEBOUNCE = 0x00
_TPCR1_IDLE = 0x00
_TPCR1_WAIT = 0x01
_TPCR1_LATCHX = 0x02
_TPCR1_LATCHY = 0x03

_TPXH = 0x72
_TPYH = 0x73
_TPXYL = 0x74

_INTC1 = 0xF0
_INTC1_KEY = 0x10
_INTC1_DMA = 0x08
_INTC1_TP = 0x04
_INTC1_BTE = 0x02

_INTC2 = 0xF1
_INTC2_KEY = 0x10
_INTC2_DMA = 0x08
_INTC2_TP = 0x04
_INTC2_BTE = 0x02

def color565(r, g=0, b=0):
    """Convert red, green and blue values (0-255) into a 16-bit 565 encoding."""
    try:
        r, g, b = r  # see if the first var is a tuple/list
    except TypeError:
        pass
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

class RA8875:
    """Set Variables and Send Init Commands"""
    def __init__(self, spi, cs, rst, width=800, height=480, baudrate=12000000, polarity=0, phase=0):
        self.spi_device = spi_device.SPIDevice(spi, cs, baudrate=baudrate, polarity=polarity, phase=phase)
        if width == 800 and height == 480:
            pixclk = _PCSR_PDATL | _PCSR_2CLK
            hsync_nondisp = 26
            hsync_start = 32
            hsync_pw = 96
            vsync_nondisp = 32
            vsync_start = 23
            vsync_pw = 2
        elif width == 480 and height == 272:
            pixclk = _PCSR_PDATL | _PCSR_4CLK
            hsync_nondisp = 10
            hsync_start = 8
            hsync_pw = 48
            vsync_nondisp = 3
            vsync_start = 8
            vsync_pw = 10
        else:
            raise ValueError('An invalid display size was specified.')
            
        self.width = width
        self.height = height
        self.rst = rst
        if self.rst:
            self.rst.switch_to_output(value=0)
            self.reset()
            
        x = self.read_reg(0)
        if x == 0x75:
            return False
        
        self.pllinit()
        
        self.write_reg(_SYSR, _SYSR_16BPP | _SYSR_MCU8)
        self.write_reg(_PCSR, pixclk)
        time.sleep(0.001)   # 1 millisecond
        
        # Horizontal settings registers
        self.write_reg(_HDWR, int(width / 8) - 1)
        self.write_reg(_HNDFTR, _HNDFTR_DE_HIGH)
        self.write_reg(_HNDR, int((hsync_nondisp - 2) / 8))
        self.write_reg(_HSTR, int(hsync_start/8) - 1)
        self.write_reg(_HPWR, _HPWR_LOW + int(hsync_pw/8 - 1))
        
        # Vertical settings registers
        self.write_reg(_VDHR0, (height - 1) & 0xFF)
        self.write_reg(_VDHR1, (height - 1) >> 8)
        self.write_reg(_VNDR0, vsync_nondisp - 1)
        self.write_reg(_VNDR1, vsync_nondisp >> 8)
        self.write_reg(_VSTR0, vsync_start - 1)        
        self.write_reg(_VSTR1, vsync_start >> 8)
        self.write_reg(_VPWR, _VPWR_LOW + vsync_pw - 1)
        
        # Set active window X
        self.write_reg(_HSAW0, 0)
        self.write_reg(_HSAW1, 0)
        self.write_reg(_HEAW0, (width - 1) & 0xFF)
        self.write_reg(_HEAW1, (width - 1) >> 8)

        # Set active window Y
        self.write_reg(_VSAW0, 0)
        self.write_reg(_VSAW1, 0)
        self.write_reg(_VEAW0, (height - 1) & 0xFF)
        self.write_reg(_VEAW1, (height - 1) >> 8)
        
        # Clear the entire window
        self.write_reg(_MCLR, _MCLR_START | _MCLR_FULL)
        time.sleep(0.500)   # 500 milliseconds

    def pllinit(self):
        """Initialize the PLL"""
        self.write_reg(_PLLC1, _PLLC1_PLLDIV1 + 10)
        time.sleep(0.001)   # 1 millisecond
        self.write_reg(_PLLC2, _PLLC2_DIV4)
        time.sleep(0.001)   # 1 millisecond
        
    def write_reg(self, cmd, data):
        """SPI write to the device: registers"""
        self.write_cmd(cmd)
        self.write_data(data)
        
    def write_cmd(self, cmd):
        """SPI write to the device: commands"""
        with self.spi_device as spi:
            spi.write(_CMDWR, end=1)
            spi.write(bytearray([cmd]))
        
    def write_data(self, data):
        """SPI write to the device: data"""
        with self.spi_device as spi:
            spi.write(_DATWR, end=1)
            spi.write(bytearray([data]))
            
    def read_reg(self, cmd):
        """SPI read from the device: registers"""
        self.write_cmd(cmd)
        return self.read_data()
        
    def read_cmd(self):
        """SPI read from the device: commands"""
        cmd = bytearray(1)
        with self.spi_device as spi:
            spi.write(_CMDRD, end=1)
            spi.readinto(cmd, end=1)
            return struct.unpack(">B", cmd)[0]
        
    def read_data(self):
        """SPI read from the device: data"""
        data = bytearray(1)
        with self.spi_device as spi:
            spi.write(_DATRD)
            spi.readinto(data)
            return struct.unpack(">B", data)[0]
            
    def wait_poll(self, reg, flag):
        """Wait for a register value to not match a flag"""
        while True:
            temp = self.read_reg(reg)
            if not (temp & flag):
                return True
        return False
        
    def reset(self):
        """Reset the device"""
        self.rst.value = 0
        time.sleep(0.100)  # 100 milliseconds
        self.rst.value = 1
        time.sleep(0.100)  # 100 milliseconds
        
    def fill(self, color):
        """Fill The Screen"""
        self.draw_rectangle(0, 0, self.width, self.height, color, True)

    def draw_rectangle(self, x, y, width, height, color, filled):
        """Draw a Rectangle"""
        # Set X
        self.write_cmd(0x91)
        self.write_data(x)
        self.write_cmd(0x92)
        self.write_data(x >> 8)
        
        # Set Y
        self.write_cmd(0x93)
        self.write_data(y)
        self.write_cmd(0x94)
        self.write_data(y >> 8)
        
        # Set X1
        self.write_cmd(0x95)
        self.write_data(width)
        self.write_cmd(0x96)
        self.write_data(width >> 8)
        
        # Set Y1
        self.write_cmd(0x97)
        self.write_data(height)
        self.write_cmd(0x98)
        self.write_data(height >> 8)
        
        # Set Color
        self.write_cmd(0x63)
        self.write_data((color & 0xf800) >> 11)
        self.write_cmd(0x64)
        self.write_data((color & 0x07e0) >> 5)
        self.write_cmd(0x65)
        self.write_data((color & 0x001f))
        
        # Draw it
        self.write_cmd(_DCR)
        if filled:
            self.write_data(0xB0)
        else:
            self.write_data(0x90)
            
        self.wait_poll(_DCR, _DCR_LNSQTR_STAT)
        
    def on(self, on):
        """Turn the Display On or Off"""
        if on: 
            self.write_reg(_PWRR, _PWRR_NORMAL | _PWRR_DISPON)
        else:
            self.write_reg(_PWRR, _PWRR_NORMAL | _PWRR_DISPOFF)

    def gpiox(self, on):
        if on: 
            self.write_reg(_GPIOX, 1)
        else:
            self.write_reg(_GPIOX, 0)
            
    def pwm1_config(self, on, clock):
        if on: 
            self.write_reg(_P1CR, _P1CR_ENABLE | (clock & 0xF))
        else:
            self.write_reg(_P1CR, _P1CR_DISABLE | (clock & 0xF))

    def pwm2_config(self, on, clock):
        if on: 
            self.write_reg(_P2CR, _P2R_ENABLE | (clock & 0xF))
        else:
            self.write_reg(_P2CR, _P2CR_DISABLE | (clock & 0xF))
            
    def pwm1_out(self, p):
        self.write_reg(_P1DCR, p)

    def pwm2_out(self, p):
        self.write_reg(_P2DCR, p)
        
    def gfx_mode(self):
        self.write_cmd(_MWCR0)
        temp = self.read_data()
        temp &= ~_MWCR0_TXTMODE
        self.write_data(temp)