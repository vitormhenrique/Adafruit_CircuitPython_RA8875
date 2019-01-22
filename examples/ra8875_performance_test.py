import time
import busio
import digitalio
import board

import adafruit_ra8875.ra8875 as ra8875
from adafruit_ra8875.ra8875 import color565

BLACK = color565(0, 0, 0)
RED = color565(255, 0, 0)
BLUE = color565(0, 255, 0)
GREEN = color565(0, 0, 255)
YELLOW = color565(255, 255, 0)
CYAN = color565(0, 255, 255)
MAGENTA = color565(255, 0, 255)
WHITE = color565(255, 255, 255)

BAUDRATE = 6000000

def test_lines(display, color):
    display.fill(BLACK)
    w = display.width
    h = display.height

    x1 = y1 = 0
    y2 = h - 1

    for x2 in range(0, w, 6):
        display.line(x1, y1, x2, y2, color)
    x2 = w - 1
    for y2 in range(0, h, 6):
        display.line(x1, y1, x2, y2, color)

    display.fill(BLACK)

    x1 = w - 1
    y1 = 0
    y2 = h - 1

    for x2 in range(0, w, 6):
        display.line(x1, y1, x2, y2, color)
    x2 = 0
    for y2 in range(0, h, 6):
        display.line(x1, y1, x2, y2, color)

    display.fill(BLACK)

    x1 = 0
    y1 = h - 1
    y2 = 0

    for x2 in range(0, w, 6):
        display.line(x1, y1, x2, y2, color)
    x2 = w - 1
    for y2 in range(0, h, 6):
        display.line(x1, y1, x2, y2, color)

    display.fill(BLACK)

    x1 = w - 1
    y1 = h - 1
    y2 = 0

    for x2 in range(0, w, 6):
        display.line(x1, y1, x2, y2, color)
    x2 = 0
    for y2 in range(0, h, 6):
        display.line(x1, y1, x2, y2, color)

    display.fill(BLACK)


# Configuration for CS and RST pins:
cs_pin = digitalio.DigitalInOut(board.D9)
rst_pin = digitalio.DigitalInOut(board.D10)

# Config for display baudrate (default max is 6mhz):
BAUDRATE = 6000000

# Setup SPI bus using hardware SPI:
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Create and setup the RA8875 display:
display = ra8875.RA8875(spi, cs=cs_pin, rst=rst_pin, baudrate=BAUDRATE)
display.init()
display.fill(WHITE)

display.fill(BLACK)

test_lines(display, WHITE)
