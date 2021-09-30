from rpi_ws281x import *
import argparse
import RPi.GPIO as GPIO


class LedStrip:
    def __init__(self):
        # LED strip configuration:
        self.LED_COUNT = 16      # Number of LED pixels.
        # GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_PIN = 12
        # LED signal frequency in hertz (usually 800khz)
        self.LED_FREQ_HZ = 800000
        # DMA channel to use for generating signal (try 10)
        self.LED_DMA = 10
        self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        # True to invert the signal (when using NPN transistor level shift)
        self.LED_INVERT = False
        self.LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)

        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ,
                                       self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)

        # Intialize the library (must be called once before other functions).
        self.strip.begin()

        # Get colors from LED node --> RGB message
        parser = argparse.ArgumentParser()
        parser.add_argument("RED", type=float, help="value of red color")
        parser.add_argument("GREEN", type=float, help="value of green color")
        parser.add_argument("BLUE", type=float, help="value of blue color")

        self.args = parser.parse_args()

    def set_color(self, red, green, blue):
        RED = int(float(red)*255)
        GREEN = int(float(green)*255)
        BLUE = int(float(blue)*255)

        color = Color(RED, GREEN, BLUE)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
