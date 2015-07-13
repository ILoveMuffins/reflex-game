'''
 @author ILoveMuffins
'''

import psp2d, pspos
import anydbm
from time import time
from time import sleep
from random import randint
from buttons.Left import Left
from buttons.Right import Right
from buttons.Up import Up
from buttons.Down import Down
from buttons.Circle import Circle
from buttons.Triangle import Triangle
from buttons.Square import Square
from buttons.Cross import Cross

screen = psp2d.Screen()
fnt = psp2d.Font('buttons/res/font.png')

pspos.setclocks(20, 10)

execfile(".\\danzeff\\danzeff.py")

# @unused
class Rectangle(object):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def isIn(self, x, y):
        return x >= self.x1 and y >= self.y1 and x <= self.x2 and y <= self.y2

    def draw(self, img, color=psp2d.Color(255, 0, 0)):
        img.fillRect(self.x1, self.y1, self.x2 - self.x1 + 1,
                self.y2 - self.y1 + 1, color)

class Time:
    def save_current_time(self):
        self.start_time = time()

    def get_difference(self):
        difference = time() - self.start_time
        return difference

class Player:
    def __init__(self):
        self.points = 0
        self.MAX_POINTS = 10

    def update_points(self, is_correct):
        if is_correct:
            self._add_point()
        else:
            self._sub_point()

    def _add_point(self):
        self.points += 1

    def _sub_point(self):
        self.points -= 1
        self.points = max(self.points, 0)

    def has_all_points(self):
        return self.points == self.MAX_POINTS

    def set_nick(nick):
        self.nick = nick

class Logic:
    def __init__(self):
        self.int_to_button = { 0:Left(), 1:Right(), 2:Up(), 3:Down(),
               4:Triangle(), 5:Square(), 6:Cross(), 7:Circle() }
        self.MAX_WAITING_TIME_FOR_BUTTON_APPEAR_SEC = 5
        self.MAX_SHOWING_FREQENCY = 20
        self.MINIMUM_WAITING_TIME = 2
        self.viewing_time = 0.37
        self.counter = 0
        self.time_for_checking_timer_update = Time()
        self.time_for_checking_timer_update.save_current_time()
        self.timer_speed = 0.001

    def generate_button(self):
        rand_int = randint(0, 7)
        rand_button = self.int_to_button[rand_int]
        return rand_button

    def compute_time_to_wait_for_button_appear(self):
        rand = randint(0, self.MAX_SHOWING_FREQENCY)
        time_to_wait_for_button_appear = \
            (self.MAX_WAITING_TIME_FOR_BUTTON_APPEAR_SEC * rand) \
            / self.MAX_SHOWING_FREQENCY
        time_to_wait_for_button_appear += self.MINIMUM_WAITING_TIME
        return time_to_wait_for_button_appear

    def set_viewing_button_time(self, viewing_time):
        self.viewing_time = self._validate_viewing_time(viewing_time)

    def _validate_viewing_time(self, time):
        time = max(time, 0.2)
        time = min(time, 1)
        return time

    def get_viewing_button_time(self):
        return self.viewing_time

    def compute_time_to_update_menu_timer(self):
        if self._was_time_mutation_button_hold():
            self.counter += 1
            if self._is_delay_finished():
                self.counter = 0
                self.timer_speed *= 3
        else:
            self.timer_speed = 0.001
        self.time_for_checking_timer_update.save_current_time()
        return self.timer_speed

    def _was_time_mutation_button_hold(self):
        threshold = 0.22
        if self.time_for_checking_timer_update.get_difference() < threshold:
            return True
        else:
            return False

    def _is_delay_finished(self):
        return True if self.counter == 17 else False

class GUI:
    def __init__(self):
        self.logic = Logic()
        self.marked_option = 0
        self.menu_opt = [ { 'opt_name':'Start', 'yposition':170,
                                    'reaction':self.start_game          },
                              { 'opt_name':'High Score', 'yposition':200,
                                    'reaction':self.high_score          },
                              { 'opt_name':'Exit', 'yposition':230,
                                  'reaction':self.exit                  }   ]
        self.OPTIONS_NUMBER = len(self.menu_opt)
        self.quit = False
        self.font = psp2d.Font('buttons/res/font.png')
        self.BLACK = psp2d.Color(0,0,0,255)
        self.GREEN = psp2d.Color(0,50,0,255)
        self.RED = psp2d.Color(50,0,0,255)
        self._initialize_screen()
        self.database = anydbm.open('scores.db', 'c')

    def _initialize_screen(self):
        self.screen = psp2d.Screen()
        self._clear_screen()

    def _clear_screen(self):
        self.image = psp2d.Image(480, 272)
        self.image.clear(self.BLACK)
        self.screen.blit(self.image)

    def run(self):
        while not self.quit:
            self.quit_to_menu = False
            self._draw_menu()
            self._get_chosen_option_from_menu()
            reaction_funct = self.menu_opt[self.marked_option]['reaction']
            reaction_funct()

    def _draw_menu(self):
        self._clear_screen()
        self._print_menu_options()
        self.screen.swap()

    def _print_menu_options(self):
        if self.marked_option == 0:
            marks = ['->', '', '']
        elif self.marked_option == 1:
            marks = ['', '->', '']
        elif self.marked_option == 2:
            marks = ['', '', '->']
        else:
            raise Exception('_print_menu_options() error')
        for option, mark in zip(self.menu_opt, marks):
            self.font.drawText(self.screen, 180, option['yposition'],
                mark + option['opt_name'])
            viewing_time = self.logic.get_viewing_button_time()
            self.font.drawText(self.screen, 200, 30, str(viewing_time))

    def _get_chosen_option_from_menu(self):
        pad = psp2d.Controller()
        while not pad.start:
            self._react_to_pad_event_in_menu(pad)
            sleep(0.02) # ta wartosc wplywa na threshold w klasie logic
            self._draw_menu()
            pad = psp2d.Controller()

    def _react_to_pad_event_in_menu(self, pad):
        if pad.up:
            self._move_to_prev_option()
        elif pad.down:
            self._move_to_next_option()
        elif pad.right:
            self._increase_viewing_button_time()
        elif pad.left:
            self._decrease_viewing_button_time()

    def _move_to_next_option(self):
        self.marked_option = (self.marked_option + 1) % 3

    def _move_to_prev_option(self):
        self.marked_option -= 1
        if self.marked_option < 0:
            self.marked_option = self.OPTIONS_NUMBER - 1

    def _increase_viewing_button_time(self):
            viewing_time = self.logic.get_viewing_button_time()
            viewing_time += self.logic.compute_time_to_update_menu_timer()
            self.logic.set_viewing_button_time(viewing_time)

    def _decrease_viewing_button_time(self):
            viewing_time = self.logic.get_viewing_button_time()
            viewing_time -= self.logic.compute_time_to_update_menu_timer()
            self.logic.set_viewing_button_time(viewing_time)

    def start_game(self):
        self._clear_screen()
        self.screen.swap()
        self.player = Player()
        while not self.player.has_all_points() and not self.quit_to_menu:
            waiting_time = self.logic.compute_time_to_wait_for_button_appear()
            if self._did_quit_evt_appear_while_waiting_for(time=waiting_time):
                break
            is_correct = self._challenge()
            self._update_game_after_challenge(is_correct)
        if self.player.has_all_points():
            self._update_high_score()

    def _challenge(self):
        self._clear_screen()
        button = self.logic.generate_button()
        viewing_time = self.logic.get_viewing_button_time()
        self._draw_button_on_screen(button)
        pressed_button = self._get_input_by_else_false(viewing_time)
        is_correct = self._check_answer(button, pressed_button)
        return is_correct

    def _update_game_after_challenge(self, is_correct):
        self.player.update_points(is_correct)
        self._view_answer_background(is_correct)

    def _update_high_score(self):
        nick = self._get_nick()
        if nick in self.database:
            if float(self.database[nick]) > self.logic.viewing_time:
                self.database[nick] = str(self.logic.viewing_time)
        else:
            self.database[nick] = str(self.logic.viewing_time)

    def _get_nick(self):
        global screen
        global fnt
        val = ''
        screen = psp2d.Screen()
        danzeff_load()
        danzeff_moveTo(220, 20)
        while (True):
            # Prepare background
            screen.blit(self.image)
            # ptDanzeff PyOSK: Render OSK on screen
            danzeff_render()
            # ptDanzeff PyOSK: Returns OSK input as an integer
            cha = danzeff_readInput(psp2d.Controller())
            # Now Evaluate return value and take proper action
            if (cha != 0 and cha != 1 and cha != 2):
                if (cha == 8):
                    val = val[0:len(val)-1]
                elif (cha == 13):
                    val = ""
                elif (cha == 4):
                    return val
                else:
                    val = val + chr(cha)
            # Print current input string
            fnt.drawText(screen, 5, 230, val)
            # Refresh screen
            screen.swap()
        danzeff_free()
        return val

    def _get_input_by_else_false(self, viewing_time):
        local_time = Time()
        local_time.save_current_time()
        pad = psp2d.Controller()
        pressed_button = self._check_input(pad)
        while not pressed_button:
            if local_time.get_difference() > viewing_time:
                return False
            pad = psp2d.Controller()
            pressed_button = self._check_input(pad)
        return pressed_button

    def _check_input(self, pad):
        if pad.left:
            return Left()
        elif pad.right:
            return Right()
        elif pad.down:
            return Down()
        elif pad.up:
            return Up()
        elif pad.triangle:
            return Triangle()
        elif pad.circle:
            return Circle()
        elif pad.square:
            return Square()
        elif pad.cross:
            return Cross()
        elif pad.select:
            self.quit_to_menu = True
        else:
            return False

    def _view_answer_background(self, is_correct):
        if is_correct:
            self._view_background_colored_to(self.GREEN)
        else:
            self._view_background_colored_to(self.RED)

    def _view_background_colored_to(self, color):
        self.image = psp2d.Image(480, 272)
        self.image.clear(color)
        self.screen.blit(self.image)
        self.screen.swap()

    def _did_quit_evt_appear_while_waiting_for(self, time):
        quantum_time = time / 35
        local_time = Time()
        local_time.save_current_time()
        while local_time.get_difference() < time:
            sleep(quantum_time)
            pad = psp2d.Controller()
            if pad.select:
                return True
        return False

    def _check_answer(self, button, pressed_button):
        if button.__class__ == pressed_button.__class__:
            return True
        else:
            return False

    def _draw_button_on_screen(self, button):
        self.image = psp2d.Image(button.image)
        self.screen.blit(self.image)
        self.screen.swap()

    def high_score(self):
        self._clear_screen()
        x, y = 0, 30
        self.font.drawText(self.screen, x, 0, 'High scores')
        for k, v in self.database.iteritems():
            self.font.drawText(self.screen, x, y, k + "-" * (29-len(k)) + v)
            y += 30
        self.screen.swap()
        pad = psp2d.Controller()
        while not pad.select and not pad.start:
            sleep(0.2)
            pad = psp2d.Controller()

    def exit(self):
        self._clear_screen()
        self.font.drawText(self.screen, 190, 130, "EXIT")
        self.screen.swap()
        self.quit = True

gui = GUI()
gui.run()

