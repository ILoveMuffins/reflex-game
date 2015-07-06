'''
 @author Kamil Drozdzal
'''

import psp2d, pspos
import random
from time import time
from time import sleep

pspos.setclocks(333,166) # @TODO ustaw minimalne wartosc

class Time:
    def __init__(self):
        pass

    def save_current_time(self):
        self.start_time = time()

    def get_difference(self):
        self.stop_time = time()
        difference = abs(self.stop_time - self.start_time)

class Player:
    def __init__(self, nick):
        self.nick = nick
        self.points = 0
        self.time = 0

    def add_point(self):
        self.points += 1

    def sub_point(self):
        self.points -= 1

    def add_time(self, time):
        self.time += time

    def get_score(self):
        return int(self.time * 1000)

# @TODO odkomentowac po stworzeniu odpowiednich klas
class Logic:
    def __init__(self):
        pass
        #self.int_to_button = {0:Left(), 1:Right(), 2:Up(), 3:Down(),
        #       4:Triangle(), 5:Square(), 6:Cross(), 7:Circle() }

    def generate_button(self):
        rand_int = random.randint(0, 7)
        self.rand_button = self.int_to_button[rand_int]

    def check_button(self, button):
        return self.button == button

# @TODO wszystko
class GUI:
    def __init__(self):
        self.screen = psp2d.Screen()
        color = psp2d.Color(0,0,0,255)
        self.screen.clear(color)

        self.player = None
        self.logic = Logic()

    def menu(self):
        # wyswietl 5 najlepszych wynikow z pliku
        # wraz z nick'ami graczy
        # wyswietl autora
        # wcisnij <select> aby wybrac gracza
        # if self.player != None: "wcisnij <start> aby zagrac"

        # @TODO opakowac w klase, uzyc w programie
        pad = psp2d.Controller()
        if pad.start:
            gui.start_game()

        pass

    def start_game(self):
        sleep(2)
        pass

gui = GUI()
gui.menu()

