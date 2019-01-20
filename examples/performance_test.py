import time
import machine
import lib.registers as reg
import lib.ra8875 as ra8875
from lib.ra8875 import color565

BLACK = color565(0, 0, 0)
RED = color565(255, 0, 0)
BLUE = color565(0, 255, 0)
GREEN = color565(0, 0, 255)
YELLOW = color565(255, 255, 0)
CYAN = color565(0, 255, 255)
MAGENTA = color565(255, 0, 255)
WHITE = color565(255, 255, 255)

BAUDRATE = 6000000

def test_fill_screen(display):
    start = time.ticks_us()
    display.fill(BLACK)
    display.fill(RED)
    display.fill(BLUE)
    display.fill(GREEN)
    display.fill(YELLOW)
    display.fill(CYAN)
    display.fill(MAGENTA)
    display.fill(WHITE)
    print("test fill in {} microseconds.".format(time.ticks_us() - start))

spi = machine.SPI(1, baudrate=BAUDRATE, polarity=0, phase=0)

# Create and setup the RA8875 display:
display = ra8875.RA8875(spi, cs=machine.Pin('X5'), rst=machine.Pin('X4'))
display.init()

display.fill(BLACK)

test_fill_screen(display)
