import time
import machine
import micropython_ra8875.registers as reg
import micropython_ra8875.ra8875 as ra8875
from micropython_ra8875.ra8875 import color565

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
    time.sleep(0.2)
    display.fill(RED)
    time.sleep(0.2)
    display.fill(BLUE)
    time.sleep(0.2)
    display.fill(GREEN)
    time.sleep(0.2)
    display.fill(YELLOW)
    time.sleep(0.2)
    display.fill(CYAN)
    time.sleep(0.2)
    display.fill(MAGENTA)
    time.sleep(0.2)
    display.fill(WHITE)
    time.sleep(0.2)
    print("test fill in {} microseconds.".format(time.ticks_us() - start))


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


spi = machine.SPI(1, baudrate=BAUDRATE, polarity=0, phase=0)

# Create and setup the RA8875 display:
display = ra8875.RA8875(spi, cs=machine.Pin('X5'), rst=machine.Pin('X4'))
display.init()

display.fill(BLACK)

# test_fill_screen(display)

test_lines(display, WHITE)

# print(display.width)
