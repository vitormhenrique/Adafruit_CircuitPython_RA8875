import time
import machine
import busio
import digitalio
import board

import adafruit_ra8875.ra8875 as ra8875
from adafruit_ra8875.ra8875 import color565


BLACK = color565(0, 0, 0)
WHITE = color565(255, 255, 255)


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

display.fill(BLACK)

display.txt_set_cursor(0, 0)
display.txt_trans(WHITE)
display.txt_size(0)

display.txt_write("Once upon a midnight dreary, while I pondered, weak and weary,")
display.txt_write("Over many a quaint and curious volume of forgotten lore,")
display.txt_write("While I nodded, nearly napping, suddenly there came a tapping, ")
display.txt_write("As of some one gently rapping, rapping at my chamber door.")
display.txt_write("'Tis some visitor,' I muttered, 'tapping at my chamber door Only this, and nothing more.' ")
display.txt_write(" ")
display.txt_write("Ah, distinctly I remember it was in the bleak December, ")
display.txt_write("And each separate dying ember wrought its ghost upon the floor. ")
display.txt_write("Eagerly I wished the morrow;- vainly I had sought to borrow ")
display.txt_write("From my books surcease of sorrow- sorrow for the lost Lenore- ")
display.txt_write("For the rare and radiant maiden whom the angels name Lenore- ")
display.txt_write("Nameless here for evermore. ")


display.set_scroll_window(0, display.width- 1, 0, display.height)

time.sleep(1)

for i in range(0, 400):
    display.scroll(0, i)
    time.sleep(0.2)