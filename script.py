'''
 @author ILoveMuffins
'''

import psp2d, pspos
import random
from time import time
from time import sleep
from buttons.Left import Left
from buttons.Right import Right
from buttons.Up import Up
from buttons.Down import Down
from buttons.Circle import Circle
from buttons.Triangle import Triangle
from buttons.Square import Square
from buttons.Cross import Cross

pspos.setclocks(75, 37)

class Rectangle(object):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def isIn(self, x, y):
        return x >= self.x1 and y >= self.y1 and x <= self.x2 and y <= self.y2

    def draw(self, img, color=psp2d.Color(255, 0, 0)):
        img.fillRect(self.x1, self.y1, self.x2 - self.x1 + 1, self.y2 - self.y1 + 1, color)

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

    def update_points(self, is_correct):
        if is_correct:
            self._add_point()
        else:
            self._sub_point()

    def _add_point(self):
        self.points += 1

    def _sub_point(self):
        self.points -= 1

    def has_all_points(self):
        return self.points == self.MAX_POINTS

    def add_time(self, time):
        self.time += time

    def get_score(self):
        return int(self.time * 1000)

class Logic:
    def __init__(self):
        self.int_to_button = { 0:Left(), 1:Right(), 2:Up(), 3:Down(),
               4:Triangle(), 5:Square(), 6:Cross(), 7:Circle() }
        self.MAX_WAITING_TIME_FOR_BUTTON_APPEAR_SEC = 3 # 5 is too much
        self.MAX_SHOWING_FREQENCY = 25
        self.MINIMUM_WAITING_TIME = 1
        #self.FIRST_VIEWING_TIME_SEC = 0.4

    def generate_button(self):
        rand_int = random.randint(0, 7)
        rand_button = self.int_to_button[rand_int]
        return rand_button

    def compute_time_to_wait_for_button_appear(self):
        rand = random.randint(0, self.MAX_SHOWING_FREQENCY)
        time_to_wait_for_button_appear = \
            (self.MAX_WAITING_TIME_FOR_BUTTON_APPEAR_SEC * rand) \
            / self.MAX_SHOWING_FREQENCY
        time_to_wait_for_button_appear += self.MINIMUM_WAITING_TIME
        return time_to_wait_for_button_appear

    def compute_viewing_time(self):
        #@TODO ulepsz algorytm
        return 0.7

class GUI:
    def __init__(self):
        self.initialize_screen()
        self.font = psp2d.Font('buttons/res/font.png')
        self.player = Player('Zuitek')
        self.logic = Logic()
        #to powinna byc lista slownikow, kazdy slownik zawierac
        #powinien cale info o jednej opcji menu
        self.menu_options = { 0:('Start',170, self.start_game),
                1:('High Score',200, self.high_score),
                2:('Exit',230, self.exit) }
        self.OPTIONS_NUMBER = len(self.menu_options)
        self.marked_option = 0

    def initialize_screen(self):
        self.image = psp2d.Image(480, 272)
        self.screen = psp2d.Screen()
        self._clear_screen_to_black()

    def _clear_screen_to_black(self):
        color = psp2d.Color(0,0,0,255)
        self.image.clear(color)
        self.screen.blit(self.image)

    def run(self):
        self._get_chosen_option_from_menu()
        reaction_function = self.menu_options[self.marked_option][2]
        reaction_function()

    def _get_chosen_option_from_menu(self):
        self._draw_menu()
        pad = psp2d.Controller()
        while not pad.start:
            self._react_to_pad_event_in_menu(pad)
            sleep(0.067) #idealnie dobrana stala
            self._draw_menu()
            pad = psp2d.Controller()

    def _draw_menu(self):
        self._clear_screen_to_black()
        self._print_menu_options()
        #self._draw_mark_rect_in_point(150,
        #        self.menu_options[self.marked_option][1])
        self.screen.swap() #bez tego ekran nic nie wyswietla

    def _draw_mark_rect_in_point(self, x, y):
        color = psp2d.Color(0, 200, 0, 255)
        rectangle = Rectangle(x, y, x+220, y+15)
        rectangle.draw(self.image, color)

    def _print_menu_options(self):
        if self.marked_option == 0:
            m0, m1, m2 = '->', '', ''
        elif self.marked_option == 1:
            m0, m1, m2 = '', '->', ''
        elif self.marked_option == 2:
            m0, m1, m2 = '', '', '->'
        else:
            return #raise
        self.font.drawText(self.screen, 180, 170, m0 + self.menu_options[0][0])
        self.font.drawText(self.screen, 180, 200, m1 + self.menu_options[1][0])
        self.font.drawText(self.screen, 180, 230, m2 + self.menu_options[2][0])

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
            self.marked_option = self.OPTIONS_NUMBER - 1

    #player, logic, time
    def start_game(self):
        sleep(1)
        while not self.player.has_all_points():
            self._clear_screen_to_black()
            button = self.logic.generate_button()
            waiting_time = self.logic.compute_time_to_wait_for_button_appear()
            self._wait_time_between_displaying_buttons(time=waiting_time)
            view_time = self.logic.compute_viewing_time()
            sleep(waiting_time)
            self._draw_button_on_screen(button)
            self._wait_viewing_time(time=view_time)
            pad = psp2d.Controller()
            is_correct = self._check_answer(button, pad)
            self.player.update_points(is_correct)
            self._view_answer_background(is_correct)

    def _view_answer_background(self, is_correct):
        #@TODO view_background_colored_to(GREEN)
        if is_correct:
            self._view_green_background()
        else:
            self._view_red_background()
        sleep(0.1)

    def _view_green_background(self):
        color = psp2d.Color(0,255,0,255)
        self.image = psp2d.Image(480, 272)
        self.image.clear(color)
        self.screen.blit(self.image)
        self.screen.swap()

    def _view_red_background(self):
        color = psp2d.Color(255,0,0,255)
        self.image = psp2d.Image(480, 272)
        self.image.clear(color)
        self.screen.blit(self.image)
        self.screen.swap()

    def _wait_viewing_time(self, time):
        sleep(time)

    def _wait_time_between_displaying_buttons(self, time):
        sleep(time)

    def _check_answer(self, button, pad):
        if pad.left and type(button) is Left:
            return True
        elif pad.right and type(button) is Right:
            return True
        elif pad.down and type(button) is Down:
            return True
        elif pad.up and type(button) is Up:
            return True
        elif pad.triangle and type(button) is Triangle:
            return True
        elif pad.circle and type(button) is Circle:
            return True
        elif pad.square and type(button) is Square:
            return True
        elif pad.cross and type(button) is Cross:
            return True
        else:
            return False


    def _wait_minimal_time_between_displaying_buttons(time):
        sleep(time)

    def _draw_button_on_screen(self, button):
        self.image = psp2d.Image(button.image)
        #@TODO x, y = _get_coordinates_to_center_image(button.image, (480, 272))
        self.screen.blit(self.image)
        self.screen.swap()

    def high_score(self):
        #@TODO
        # wyswietl 5 najlepszych wynikow z pliku/bazy danych
        # wraz z nick'ami graczy
        pass

    def exit(self):
        self._clear_screen_to_black()
        self.font.drawText(self.screen, 190, 130, "EXIT")
        self.screen.swap()

gui = GUI()
gui.run()

# wyswietl autora
# wcisnij <select> aby wybrac gracza
# if self.player != None: "wcisnij <start> aby zagrac"

