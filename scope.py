import bibliopixel.colors as colors
import math

class Scope:

    screensize = None
    led = None
    period = 0
    amplitude = 0
    time = 0
    
    def __init__(self, led, period=0.08, amplitude=8, screenX=64, screenY=32):
        self.led = led
        self.period = period
        self.amplitude = amplitude
        self.screensize = [screenX, screenY]

    def step(self):
        for x in xrange(0, self.screensize[0]):
            value = int(round(self.amplitude * math.sin(self.period * x + self.time)))
                    # int(round(0.5 * self.amplitude * math.sin(self.period * 3 * x + self.time)))
            self.led.set(x, value + 16, colors.Peru)
        self.time = (self.time + 1) % int(round(math.pi * 2 / self.period))

    def update_sticks(self, js1, js2):
        self.period += (0.01 * js1)
        if self.period <= 0.02:
            self.period = 0.02
        self.period = self.period if self.period > 0 else 0.03
        self.amplitude -= js2
        if self.amplitude > self.screensize[1]/2:
            self.amplitude = self.screensize[1]/2
