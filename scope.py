import bibliopixel.colors as colors
import math

class Scope:

    time = 0
    partials = [
        [math.sin, 0.5, 1, 1],
        [math.sin, 0.75, 1.5, 1],
        [math.sin, 1, 2, 1],
        [math.sin, 0.25, 2.5, 1],
        [math.cos, 0.5, 3, 1],
        [math.sin, 0, 2, 1]
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
        amp_inc = 0
        per_inc = 0
        for s in sticks:
            if s == 1:    #UP
                amp_inc += -1
            elif s == 2:  #DOWN
                amp_inc += 1
            elif s == 3:  #LEFT
                per_inc += 1
            elif s == 4:  #RIGHT
                per_inc += -1
            elif s == 5:  #UP LEFT
                amp_inc += -1
                per_inc += 1
            elif s == 6:  #UP RIGHT
                amp_inc += -1
                per_inc += -1
            elif s == 7:  #DOWN LEFT
                amp_inc += 1
                per_inc += 1
            elif s == 8:  #DOWN RIGHT
                amp_inc += 1
                per_inc += -1
        self.period += (1 * per_inc)
        if self.period <= 1:
            self.period = 1
        self.period = self.period if self.period > 0 else 0.03
        self.amplitude -= amp_inc
        if self.amplitude > self.screensize[1]/2:
            self.amplitude = self.screensize[1]/2

    def update_pots(self, pots):
        for idx, val in enumerate(pots):
            if (idx % 2) == 0:
                self.partials[idx/2][2] = self.translate(val, 0, 1023, 1, 3)
            else:
                self.partials[idx/2+1][3] = self.translate(val, 0, 1023, 0.1, 2)

    def update_faders(self, faders):
        for idx, val in enumerate(faders):
            self.partials[idx/2][1] = self.translate(val, 0, 1023, 0, 1)

    def update_beam(self, beam):
        self.partials[5][1] = self.translate(beam, 0, 255, 2, 0)
        self.partials[5][3] = self.translate(beam, 0, 255, 3, 1)
        # self.timeStep = self.translate(beam, 0, 255, 120, 60)

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return rightMin + (valueScaled * rightSpan)



