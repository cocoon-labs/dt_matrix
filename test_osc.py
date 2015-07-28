#!/usr/bin/env python2.7
from OSC import OSCServer
import sys
from time import sleep
from adamatrix import DriverAdaMatrix
from bibliopixel import *
import bibliopixel.colors as colors
from matrix_animations import *
import Image
import ImageDraw
from rgbmatrix import Adafruit_RGBmatrix

class Matrix(object):
    server = None
    driver = None
    led = None
    modes = []
    running = False
    color = None

    mode = 0;

    def __init__(self):
        
        self.server = OSCServer( ("192.168.2.122", 5005) )
        self.server.timeout = 0

        self.driver = DriverAdaMatrix(rows=32, chain=2)
        self.driver.SetPWMBits(6)

        self.led = LEDMatrix(self.driver, 64, 32, serpentine=False)

        self.modes = [self.mode_presets, self.color_presets,
                      self.color_gradient, self.white_gradient,
                      self.direct_control, self.arcade, self.mindfuck]

        self.color = colors.Salmon

        self.running = True

        # funny python's way to add a method to an instance of a class
        import types
        # self.server.handle_timeout = types.MethodType(lambda: self.handle_timeout(self), self.server)
        self.server.addMsgHandler("/mode", self.mode_callback)
        # self.server.addMsgHandler("/color", self.color_callback)
        self.server.addMsgHandler("/quit", self.quit_callback)

    # this method of reporting timeouts only works by convention
    # that before calling handle_request() field .timed_out is 
    # set to False
    def handle_timeout(self):
        self.timed_out = True

    def mode_callback(self, path, tags, args, source):
        self.led.all_off()
        self.mode =int(args[0]) 
        self.modes[self.mode]()
        self.led.update()

    def color_callback(self, path, tags, args, source):
        self.color = (int(args[0]), 
                      int(args[1]),
                      int(args[2]))
        self.led.all_off()
        self.modes[self.mode]()

    def quit_callback(self, path, tags, args, source):
        print("quit blender")
        # don't do this at home (or it'll quit blender)
        self.running = False

    # user script that's called by the game engine every frame
    def each_frame(self):
        # clear timed_out flag
        self.server.timed_out = False
        # handle all pending requests then return
        while not self.server.timed_out:
            self.server.handle_request()

    def mode_presets(self):
        self.led.drawText("Mode", 6, 5, size=1, color=self.color)
        self.led.drawText("Presets", 6, 15, size=1, color=self.color)

    def color_presets(self):
        self.led.drawText("Color", 6, 5, size=1, color=self.color)
        self.led.drawText("Presets", 6, 15, size=1, color=self.color)

    def color_gradient(self):
        self.led.drawText("Color", 6, 5, size=1, color=self.color)
        self.led.drawText("Gradients", 6, 15, size=1, color=self.color)

    def white_gradient(self):
        self.led.drawText("White", 6, 5, size=1, color=self.color)
        self.led.drawText("Gradients", 6, 15, size=1, color=self.color)

    def direct_control(self):
        self.led.drawText("Direct", 6, 5, size=1, color=self.color)
        self.led.drawText("Control", 6, 15, size=1, color=self.color)

    def arcade(self):
        self.led.drawText("Arcade", 6, 5, size=1, color=self.color)
        self.led.drawText("Mode!!!", 6, 15, size=1, color=self.color)

    def mindfuck(self):
        self.led.drawText("Y U NO", 6, 5, size=1, color=self.color)
        self.led.drawText("LISTEN?!", 6, 15, size=1, color=self.color)

    def run(self):
        while self.running:
            sleep(1)
            self.each_frame()

if __name__ == "__main__":
    mat = None
    try:
        mat = Matrix()
        mat.run()
    except KeyboardInterrupt:
        mat.server.close()
