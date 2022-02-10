import time
from pimoroni_i2c import PimoroniI2C
from breakout_rgbmatrix5x5 import BreakoutRGBMatrix5x5

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}

i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)
matrix = BreakoutRGBMatrix5x5(i2c)


class Control:
    MaxLevel = 25
    MinLevel = 0
    def __init__(self, position, level, maxcolor, color_shades, matrix):
        #TODO if > 4 or < 0 throw exception
        self.x = position
        self.maxcolor = maxcolor
        self.color_shades = color_shades
        self.matrix = matrix
        self.setLevel(level)
    
    def setLevel(self, level):
        self.level = Control.MaxLevel if level > Control.MaxLevel else (Control.MinLevel if level < Control.MinLevel else level)        
        self.refresh()
        return self.level == level #true if the level was set

    def refresh(self):
        for led in range(0, 5):
            #is the led fully on?
            if self.level >= (led+1)*5:
                self.matrix.set_pixel(self.x, led, self.maxcolor[0], self.maxcolor[1], self.maxcolor[2])
                continue

            #is the led fully off?
            if self.level <= (led*5):
                self.matrix.set_pixel(self.x, led, 0, 0, 0)
                continue

            #partially illuminated
            partial = (self.level - (led*5)) - 1
            self.matrix.set_pixel(self.x, led, self.color_shades[partial][0], self.color_shades[partial][1], self.color_shades[partial][2])
        self.matrix.update()


    def increase(self):
        return self.setLevel(self.level + 1)

    def decrease(self):
        return self.setLevel(self.level - 1)






#there is some internal gamma compensation so we might be able to just linearly distribute levels
#green
overdriveControl = Control(0, 0, (0, 255, 0), [(0, 50, 0), (0, 100, 0), (0, 150, 0), (0, 200, 0)], matrix)
#white
bassControl = Control(1, 0, (127, 127, 127), [(25, 25, 25), (50, 50, 50), (75, 75, 75), (100, 100, 100)], matrix)
#orange
midControl = Control(2, 0, (255, 127, 0), [(50, 25, 0), (100, 50, 0), (150, 75, 0), (200, 100, 0)], matrix)
#blue
trebleControl = Control(3, 0, (0, 0, 255), [(0, 0, 50), (0, 0, 100), (0, 0, 150), (0, 0, 200)], matrix)
#red
levelControl = Control(4, 0, (255, 0, 0), [(50, 0, 0), (100, 0, 0), (150, 0, 0), (200, 0, 0)], matrix)
allControls = [overdriveControl, bassControl, midControl, trebleControl, levelControl]

while True:
    for control in allControls:
        while control.increase():
            time.sleep(0.1)
        
        while control.decrease():
            time.sleep(0.1)

    time.sleep(0.5)
    allControls[0].setLevel(15)
    allControls[1].setLevel(18)
    allControls[2].setLevel(5)
    allControls[3].setLevel(20)
    allControls[4].setLevel(13)
    time.sleep(1)
    control = allControls[2]
    while control.increase():
        time.sleep(0.3)
    
    time.sleep(2)
    for control in allControls:
        control.setLevel(0)
    time.sleep(5)