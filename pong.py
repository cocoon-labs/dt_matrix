import bibliopixel.colors as colors
from time import sleep

class Pong:

    screensize = [64, 32]
    ballSize = 2;
    paddleSize = [2, 6];
    ballVert = 1
    ballHoriz = -1
    led = None
    running = False
    score = None
    playerPositions = None
    ballPos = None
    
    def __init__(self, led):
        print("making pong")
        self.led = led
        self.initialize()

    def initialize(self):
        self.reset()
        self.draw()

    def reset(self):
        self.ballPos = [self.screensize[0] / 2,
                        self.screensize[1] / 2]
        self.score = [0,0]
        self.playerPositions = [self.screensize[1] / 2,
                                self.screensize[1] / 2]
        
    def drawP1(self):
        self.led.fillRect(0, self.playerPositions[0] - self.paddleSize[1]/2,
                          self.paddleSize[0], self.paddleSize[1], colors.Pink)

    def drawP2(self):
        self.led.fillRect(self.screensize[0] - self.paddleSize[0],
                          self.playerPositions[1] - self.paddleSize[1]/2,
                          self.paddleSize[0], self.paddleSize[1], colors.Blue)

    def drawBall(self):
        self.led.fillRect(self.ballPos[0], self.ballPos[1],
                          self.ballSize, self.ballSize, colors.WhiteSmoke)

    def update_sticks(self, js1, js2):
        print("updating sticks", js1, js2)
        self.playerPositions[0] = self.playerPositions[0] + js1
        self.playerPositions[1] = self.playerPositions[1] + js2

    def step(self):
        self.ballPos[0] += self.ballHoriz
        if self.ballPos[0] == self.paddleSize[0] or \
           self.ballPos[0] == self.screensize[0] - self.paddleSize[0] - 1:
            self.ballHoriz *= -1

        self.ballPos[1] += self.ballVert
        if self.ballPos[1] == 0 or \
           self.ballPos[1] == self.screensize[1] - 1:
            self.ballVert *= -1

        self.draw()

    def draw(self):
        self.drawP1()
        self.drawP2()
        self.drawBall()
        
    def run(self):
        self.running = True
        while self.running:
            self.led.all_off()
            self.step()
            self.led.update()
            sleep(0.05)

