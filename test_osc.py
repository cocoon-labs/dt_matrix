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
from pong import Pong
from scope import Scope
from color_wheel import ColorWheel
import threading
import os

class Matrix(object):
    server = None
    driver = None
    led = None
    modes = []
    running = False
    color = None
    wheel = None

    pong = None
    scope = None

    mode = 0;

    joysticks = []

    pong_running = False
    scope_running = False

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
        self.wheel = ColorWheel()

        self.running = True

        self.joysticks = [0] * 5
        
        self.pong = Pong(self.led)
        
        self.scope = Scope(self.led, self.wheel)

        self.scheme = []
        
        # funny python's way to add a method to an instance of a class
        # import types
        # self.server.handle_timeout = types.MethodType(lambda: self.handle_timeout(self), self.server)
        self.server.addMsgHandler("/mode", self.mode_callback)
        self.server.addMsgHandler("/coin", self.coin_callback)
        # self.server.addMsgHandler("/color", self.color_callback)
        # self.server.addMsgHandler("/quit", self.quit_callback)
        self.server.addMsgHandler("/js", self.joystick_callback)
        self.server.addMsgHandler("/pot", self.pot_callback)
        self.server.addMsgHandler("/fad", self.fader_callback)
        self.server.addMsgHandler("/scheme", self.scheme_callback)

    # this method of reporting timeouts only works by convention
    # that before calling handle_request() field .timed_out is 
    # set to False
    def handle_timeout(self):
        self.timed_out = True

    # TODO: update this to take all the joysticks and send them off selectively
    def joystick_callback(self, path, tags, args, source):
        print(args)
        if self.pong_running:
            self.pong.update_sticks(args[0], args[4])
        elif self.scope_running:
            self.scope.update_sticks(args)

    def pot_callback(self, path, tags, args, source):
        if self.scope_running:
            self.scope.update_pots(args)

    def fader_callback(self, path, tags, args, source):
        if self.scope_running:
            self.scope.update_faders(args)

    def mode_callback(self, path, tags, args, source):
        self.scope_running = True
        self.led.all_off()
        if (self.mode == 5 and int(args[0]) != 5):
            self.pong_running = False
        self.mode =int(args[0])
        self.modes[self.mode]()
        self.led.update()
        sleep(1)

    def coin_callback(self, path, tags, args, source):
        self.led.all_off()
        self.led.update()
        count = 0
        while count < 5:
            self.led.drawText("Thank You!!", 4, 10, size=1, color=colors.Lavender)
            self.led.update()
            sleep(1)
            self.led.all_off()
            self.led.update()
            sleep(0.5)
            count += 1
        self.modes[self.mode]()
        self.led.update()

    def scheme_callback(self, path, tags, args, source):
        self.scheme = []
        for i in xrange(0, len(args), 3):
            self.scheme.append(args[i:i+3])
        self.wheel.setScheme(self.scheme)
    
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
            if self.pong_running:
                self.led.all_off()
                self.pong.step()
                self.led.update()
                sleep(0.05)
            elif self.scope_running:
                self.led.all_off()
                self.scope.step()
                self.led.update()
                sleep(0.05)

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
        # self.led.drawText("Arcade", 6, 5, size=1, color=self.color)
        # self.led.drawText("Mode!!!", 6, 15, size=1, color=self.color)
        anim = ScrollText(self.led, "Arcade Mode!!!!!", 64, 13, size=1, color=self.color)
        anim.run(fps=30, untilComplete=True, max_cycles=1)
        self.pong.reset()
        self.scope_running = False
        self.pong_running = True
        

    def mindfuck(self):
        self.led.drawText("Y U NO", 6, 5, size=1, color=self.color)
        self.led.drawText("LISTEN?!", 6, 15, size=1, color=self.color)
        self.scope_running = False

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
