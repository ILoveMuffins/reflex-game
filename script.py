'''
 @author ILoveMuffins
'''

import psp2d, pspos
import random
from time import time
from time import sleep
from buttons import Left
from buttons import Right
from buttons import Up
from buttons import Down
from buttons import Circle
from buttons import Triangle
from buttons import Squre
from buttons import Cross

pspos.setclocks(133, 66)

class Time:
    def __init__(self):
        pass

    def save_current_time(self):
        self.start_time = time()

    def get_difference(self):
        difference = abs(time() - self.start_time)
        return difference

class Player:
    def __init__(self, nick, max_points=10):
        self.nick = nick
        self.points = 0
        self.time = 0
        self.MAX_POINTS = max_points

    def add_point(self):
        self.points += 1

    def sub_point(self):
        self.points -= 1

    def has_all_points(self):
        return self.points == MAX_POINTS

    def add_time(self, time):
        self.time += time

    def get_score(self):
        return int(self.time * 1000)

class Logic:
    def __init__(self):
        self.int_to_button = { 0:Left(), 1:Right(), 2:Up(), 3:Down(),
               4:Triangle(), 5:Square(), 6:Cross(), 7:Circle() }
        self.MAX_WAITING_TIME_FOR_BUTTON_APPEAR_SEC = 5
        self.MAX_SHOWING_FREQENCY = 25

    def generate_button(self):
        rand_int = random.randint(0, 7)
        rand_button = self.int_to_button[rand_int]
        return rand_button

    def compute_time_to_wait_for_button_appear(self):
        rand = random.randint(0, self.MAX_SHOWING_FREQENCY)
        time_to_wait_for_button_appear = \
            (self.MAX_WAITING_TIME_FOR_BUTTON_APPEAR_SEC * rand) \
            / self.MAX_SHOWING_FREQENCY
        return time_to_wait_for_button_appear

    def compute_viewing_time(self):
        pass #@TODO

class GUI:
    def __init__(self):
        self.initialize_screen()
        self.font = psp2d.Font('../res/font.png')
        self.player = Player('Zuitek')
        self.logic = Logic()
        self.menu_options = { 0:('Start',220, start_game),
                1:('High Score',235, high_score), 2:('Exit',250, exit) }
        self.OPTIONS_NUMBER = len(self.menu_options)
        self.marked_option = 0

    def initialize_screen(self):
        self.image = psp2d.Image(480, 272)
        self.screen = psp2d.Screen()
        self._clear_screen()

    def _clear_screen(self):
        color = psp2d.Color(0,0,0,255)
        self.image.clear(color)
        self.screen.blit(self.image)
        self.screen.swap()

    def run(self):
        self._draw_menu()
        self._get_chosen_menu_option()
        reaction_function = self.menu_options[self.marked_option][3]
        reaction_function()

    def _draw_menu(self):
        #@TODO
        # wyswietl autora
        # wcisnij <select> aby wybrac gracza
        # if self.player != None: "wcisnij <start> aby zagrac"
        self._draw_mark_rect_in_point(100,
                self.menu_options[self.marked_option][2])
        self._print_menu_options()

    def _draw_mark_rect_in_point(self, x, y):
        color = psp2d.Color(0, 200, 0, 255)
        rectangle = Rect(x, y, width=220, height=15)
        rect(self.screen, color, rectangle)

    def _print_menu_options(self):
        font.drawText(self.screen, 180, 225, self.menu_options[0][0])
        font.drawText(self.screen, 180, 240, self.menu_options[1][0])
        font.drawText(self.screen, 180, 255, self.menu_options[2][0])
        self.screen.swap()

    def _get_chosen_menu_option(self):
        pad = psp2d.Controller()
        while not pad.start:
            self._react_to_pad_event_in_menu(pad)

    def _react_to_pad_event_in_menu(self, pad):
        if pad.up:
            self._move_to_prev_option()
        elif pad.down:
            self._move_to_next_option()

    def _move_to_next_option(self):
        self.marked_option = (self.marked_option + 1) % 3

    def _move_to_prev_option(self):
        self.marked_option -= 1
        if self.marked_option < 0:
            self.marked_option = self.OPTIONS_NUMBER

    #player, logic, time
    def start_game(self):
        pass
        #sleep(1)
        #while not self.player.has_all_points():
        #    sleep(1)
        #    self._clear_screen()
        #    button = self.logic.generate_button()
        #    waiting_time = self.logic.compute_time_to_wait_for_button_appear()
        #    view_time = self.logic.compute_viewing_time()
        #    sleep(waiting_time)
        #    self._draw_button_on_screen(button)
        #    #@TODO
        #    # wystartuj watek czekajacy na wejscie, wystartuj pomiar czasu
        #    # jak tylko wejscie sie pojawi zatrzymaj pomiar, usun obrazek
        #    sleep(view_time)
        #    # zatrzymaj pomiar czasu (jesli watek jeszcze go nie zatrzymal)
        #    # usun obrazek
        #    # oblicz punkty dla gracza
        #    # wywolaj odpowiednie metody z API gracza

    def high_score(self):
        #@TODO
        # wyswietl 5 najlepszych wynikow z pliku/bazy danych
        # wraz z nick'ami graczy
        pass

    def _draw_button_on_screen(self, button):
        pass

    def exit(self):
        # for debug - red screen after 'exit'
        color = psp2d.Color(255,0,0,255)
        self.image.clear(color)
        self.screen.blit(self.image)
        self.screen.swap()
        sleep(2)

gui = GUI()
gui.run()

