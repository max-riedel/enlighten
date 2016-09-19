__author__ = 'max'
import os
import time as systime
import signal

from effects import *
from blocks.i_Stripe import *
from blocks.s_colorswipe import *
from blocks.w_Glimmer import *
from blocks.s_UniColor import *
from blocks.s_rainbow import *
import blocks.en_time
from server import server

# <editor-fold desc="configs, signals, ...>

LED_COUNT = 50  # 16      # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = True  # True to invert the signal (when using NPN transistor level shift)

if os.geteuid() != 0:
    print("No superuser? Quit.")
    sys.exit(1)


def signal_handler(signal, frame):
    """
    Makes sure to switch off LEDs when script is killed
    """
    strip.setBrightness(0)
    strip.show()
    try:
        server.httpd.shutdown()
    except:
        print("Could not stop server")
    finally:
        sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGKILL, signal_handler)
# </editor-fold>

print("""              ___                __      __
             /\_ \    \033[33m__\033[39m        /\ \    /\ \__
   __    ___ \//\ \  \033[33m/\_\ \033[39m    __\ \ \___\ \ ,_\    __    ___
 /'__`\/' _ `\ \ \ \ \033[33m\/\033[39m\ \  /'_ `\ \  _ `\ \ \/  /'__`\/' _ `\\
/\  __//\ \/\ \ \_\ \_\ \ \/\ \_\ \ \ \ \ \ \ \_/\  __//\ \/\ \\
\ \____\ \_\ \_\/\____\\\\ \_\ \____ \ \_\ \_\ \__\ \____\ \_\ \_\\
 \/____/\/_/\/_/\/____/ \/_/\/___,\ \/_/\/_/\/__/\/____/\/_/\/_/
                              /\____/
          \033[33mBrowser-controlled\033[39m  \_/__/  \033[33mLED Management\033[39m
""")

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT,
                          LED_BRIGHTNESS)  # Intialize the library (must be called once before other functions).
strip.begin()

# init global time
blocks.en_time.init()

# source = Colorswipe()
source = UniColor()
#source = Rainbow()
sink = Stripe(strip)
work = Glimmer()

#source.outputs[0].add_ancestor(sink.inputs[0])

# Connect source -> work -> sink
source.outputs[0].add_ancestor(work.inputs[0])
work.outputs[0].add_ancestor(sink.inputs[0])

server.init(source)

# infinite loop, stepping global time
while True:
    blocks.en_time.time.tick()
    source.tick()
    systime.sleep(1.0 / 30.0)

