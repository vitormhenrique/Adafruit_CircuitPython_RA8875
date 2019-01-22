import time
import machine
import micropython_ra8875.registers as reg
import micropython_ra8875.ra8875 as ra8875
from micropython_ra8875.ra8875 import color565

BLACK = color565(0, 0, 0)
WHITE = color565(255, 255, 255)

spi = machine.SPI(1, baudrate=6000000, polarity=0, phase=0)
display = ra8875.RA8875(spi, cs=machine.Pin('X5'), rst=machine.Pin('X4'))

cursor = ra8875.RA8875CursorType.IBEAM

display.show_cursor(cursor, True)
display.set_cursor_blink_rate(10)
display.init()
display.fill(BLACK)
display.txt_set_cursor(0, 0)
display.txt_trans(WHITE)
display.txt_size(0)
display.txt_write(
    "Once upon a midnight dreary, while I pondered, weak and weary,")
