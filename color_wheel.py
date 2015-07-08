class ColorWheel:
    
    scheme = [[255, 0, 0],
              [0, 255, 0],
              [0, 0, 255]]
    wheelPos = 0

    def setScheme(self, scheme):
        self.scheme = scheme

    def getColor(self, offset, nColors):
        schemeN = len(self.scheme)
        dist = nColors / schemeN
        position = (self.wheelPos + offset) % nColors
        c = None
        for i in xrange(schemeN):
            if position < (i+1) * dist:
                c = self.genColor(position, i, dist)
                # print(c)
                return c

        c = self.genColor(position, schemeN - 1, dist)
        # print(c)
        return c
        
    def genColor(self, position, idx, dist):
        position = position - (idx * dist);
        schemeN = len(self.scheme)
        result = [0, 0, 0]
        for i in xrange(0, 3):
            result[i] = \
                self.scheme[idx][i] + \
                (position * \
                     (self.scheme[(idx+1) % schemeN][i] - self.scheme[idx][i]) / \
                     dist)
        return result

    def turn(self, step, nColors):
        self.wheelPos = (self.wheelPos + step) % nColors
