import bibliopixel.colors as colors
import math

class Scope:

    time = 0
    partials = [
        (math.sin, 0.5, 1, 1),
        (math.sin, 0.75, 1.5, 1),
        (math.sin, 1, 2, 1),
        (math.sin, 0.25, 2.5, 1),
        (math.cos, 0.5, 3, 1),
    ]
    
    def __init__(self, led, wheel, period=3, amplitude=6, timeStep=60, screenX=64, screenY=32):
        self.led = led
        self.wheel = wheel
        self.period = period * 360 / screenX
        self.timeStep = timeStep
        self.amplitude = amplitude
        self.screensize = [screenX, screenY]

    def step(self):
        for x in xrange(0, self.screensize[0]):
            value = 0
            for p in self.partials:
                value += int(round(self.amplitude * p[1] * \
                                   p[0](math.radians(self.period * p[2] * x + \
                                                     (p[3] * self.time)))))
            value = int(round(value /  sum([p[1] for p in self.partials])))
            self.led.set(x, value + self.screensize[1]/2,
                         self.wheel.getColor(x, self.screensize[0]))
        self.time = (self.time + self.timeStep) % 360
        self.wheel.turn(1, self.screensize[0])

    def update_sticks(self, sticks):
        self.period += (1 * sticks[0])
        if self.period <= 1:
            self.period = 1
        self.period = self.period if self.period > 0 else 0.03
        self.amplitude -= sticks[4]
        if self.amplitude > self.screensize[1]/2:
            self.amplitude = self.screensize[1]/2

    def update_pots(self, pots):
        pass
        # for idx, val in enumerate(pots):
        #     if (idx % 2) == 0:
        #         self.partials[idx/2][2] = map(val, 0, 1023, 1, 3)
        #     else:
        #         self.partials[idx/2+1][3] = map(val, 0, 1023, 0.1, 2)

    def update_faders(self, faders):
        pass
        # for idx, val in enumerate(faders):
        #     self.partials[idx/2][1] = map(val, 0, 1023, 0, 1)



