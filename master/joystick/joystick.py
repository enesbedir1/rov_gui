"""
axis list yapıldı
hats button_liste eklendi
05.02.2019
Abdullah Enes
"""

import pygame
import time
from threading import Thread


def scale(joy_val, max):
    return int(round((joy_val+1)/2.0*max))

class Joy():
    def __init__(self):
        try:
            self.pressed_buttons = []
            self.pygame = pygame
            self.pygame.init()
            self.clock = pygame.time.Clock()
            self.pygame.joystick.init()
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.axes = self.joystick.get_numaxes()  # num of axes
            self.buttons = self.joystick.get_numbuttons()  # num of buttons
            self.hats = self.joystick.get_numhats()  # num of hats
            self.clock.tick(10)  # tick per second
            self.connected = True
            self.axis_list = []
            self.pressed_buttons = []

        except:
            self.connected = False

    def joy_get(self):
        while True:
            try:
                self.clock.tick(15)  # tick per second
                self.pygame.event.get()  # get joystick event
                self.which_button()
            except pygame.error:
                return False

    def which_button(self):
        self.pressed_buttons = []
        for i in range(self.buttons):
            if self.joystick.get_button(i) == 1:
                if (i == 2) or (i==3) or (i==4) or (i==5):
                    self.pressed_buttons.append(i)

    def get_hats(self):
        return self.joystick.get_hat(0)

if __name__ == "__main__":
    joy = Joy()
    joy_timer = Thread(target=joy.joy_get)
    joy_timer.start()
    while True:
        if joy.pressed_buttons:
            print(joy.pressed_buttons.pop(0))