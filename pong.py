import bibliopixel.colors as colors
from time import sleep
from random import randrange

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
        self.score = [0, 0]
        self.playerPositions = [self.screensize[1] / 2,
                                self.screensize[1] / 2]
        self.resetBall()

    def resetBall(self):
        self.ballPos = [self.screensize[0] / 2 + randrange(-10, 10),
                        self.screensize[1] / 2 + randrange(-10, 10)]
        sleep(1)
        
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
    def drawScore(self):
        if (self.score[0] > 0):
            self.led.drawLine(0, 0, self.score[0] - 1, 0,  colors.Yellow)

        if (self.score[1] > 0):
            self.led.drawLine(self.screensize[0] - self.score[1], 0, self.screensize[0]-1, 0, colors.Yellow)

    def update_sticks(self, js1, js2):
        self.playerPositions[0] = self.playerPositions[0] + js1
        self.playerPositions[1] = self.playerPositions[1] + js2

    def recordFault(self, player):
        other_player = 1 if player == 0 else 0

        if self.ballPos[1] + 1 < self.playerPositions[player] - (self.paddleSize[1] / 2) or \
           self.ballPos[1] >= (self.playerPositions[player] + (self.paddleSize[1] / 2)):
            self.score[other_player] += 1
            self.resetBall()
            
        if self.score[0] == 1:
            self.led.drawText("P1 WINS!!", 6, 12, size=1, color=colors.Pink)
            self.led.update()
            sleep(2)
            self.reset()
        elif self.score[1] == 1:
            self.led.drawText("P2 WINS!!", 6, 12, size=1, color=colors.Blue)
            self.led.update()
            sleep(2)
            self.reset()

    def step(self):
        if self.ballPos[0] == self.paddleSize[0] - 1:
            self.ballHoriz *= -1
            self.recordFault(0)
        elif self.ballPos[0] == (self.screensize[0] - self.paddleSize[0] - 1):
            self.ballHoriz *= -1
            self.recordFault(1)

        self.ballPos[0] += self.ballHoriz
        self.ballPos[1] += self.ballVert

        if self.ballPos[1] == 0 or \
           self.ballPos[1] == self.screensize[1] - 1:
            self.ballVert *= -1

        self.draw()

    def draw(self):
        self.drawP1()
        self.drawP2()
        self.drawBall()
        self.drawScore()
        
    def run(self):
        self.running = True
        while self.running:
            self.led.all_off()
            self.step()
            self.led.update()
            sleep(0.05)

