from time import sleep
from misc.Misc import random_range
from core import Globals
from input.Keyboard import type_key
from input.Mouse import *
from input.Mouse import move
from misc.Timer import *


def is_at_lobby():
    count = Misc.count_color((1, 255, 70), (6, 255, 90), [270, 290, 500, 375])
    return count > 4000


def get_login_screen():
    if not is_logged_in():
        if is_at_lobby():
            return Globals.LOGIN_SCREEN_LOBBY
        count = Misc.count_color((30, 255, 255), (30, 255, 255), [205, 170, 560, 370])
        if count == 479:
            return Globals.LOGIN_SCREEN_MAIN
        elif (count == 1037) or (count == 1061):
            return Globals.LOGIN_SCREEN_ENTRY
        elif count == 407:
            return Globals.LOGIN_SCREEN_LOADING
        else:
            return Globals.LOGIN_SCREEN_INVALID_PASS


def is_logged_in():
    return Misc.count_color((0, 0, 0), (0, 0, 0), [437, 480, 474, 493]) == 30


def gain_focus():
    move(box=Globals.LOGIN_LOGIN_BOX, click_left=True)


def get_cursor():
    t = Timer()
    t.start()
    while t.elapsed_time() < 0.5:
        user = Misc.count_color((30, 255, 255), (30, 255, 255), Globals.LOGIN_LOGIN_BOX)
        if user > 15:
            break
    if user > 15:
        return Globals.LOGIN_LOGIN_BOX_BYTE
    else:
        return Globals.LOGIN_PASSWORD_BOX_BYTE


def set_cursor(new):
    if get_cursor() != new:
        type_key('{tab}')
        sleep(Misc.random_range(350, 650) / 1000)


def enter_details(username, password):
    gain_focus()
    clear = [False, False]
    time_out = Timer()
    clear[Globals.LOGIN_LOGIN_BOX_BYTE] = Misc.count_color((0, 0, 255), (0, 0, 255), Globals.LOGIN_LOGIN_BOX)

    clear[Globals.LOGIN_PASSWORD_BOX_BYTE] = Misc.count_color((0, 0, 255), (0, 0, 255), Globals.LOGIN_PASSWORD_BOX)

    if get_cursor() != Globals.LOGIN_LOGIN_BOX_BYTE:
        set_cursor(Globals.LOGIN_LOGIN_BOX_BYTE)
    if clear[Globals.LOGIN_LOGIN_BOX_BYTE]:
        while (Misc.count_color((0, 0, 255), (0, 0, 255), Globals.LOGIN_LOGIN_BOX) > 5) \
                and (time_out.elapsed_time() < 8000):

            type_key('{backspace}')
            sleep(Misc.random_range(30, 120) / 1000)
    type_key(username)
    if get_cursor() != Globals.LOGIN_PASSWORD_BOX_BYTE:
        set_cursor(Globals.LOGIN_PASSWORD_BOX_BYTE)
    if clear[Globals.LOGIN_PASSWORD_BOX_BYTE]:
        while (Misc.count_color((0, 0, 255), (0, 0, 255), Globals.LOGIN_PASSWORD_BOX) > 5) \
                and (time_out.elapsed_time() < 8000):

            type_key('{backspace}')
            sleep(Misc.random_range(30, 120) / 1000)
    type_key(password + '{enter}')
    sleep(Misc.random_range(1000, 1500) / 1000)


def login_player(username, password):
    cur_state, tries = 0, 0
    t, t_logged = Timer(), Timer()

    if not is_logged_in():
        while (tries < 30) and (not is_logged_in()):
            tries += 1
            t.start()
            cur_state = get_login_screen()

            if cur_state == Globals.LOGIN_SCREEN_MAIN:
                move(box=[395, 275, 525, 300], click_left=True)
            if cur_state == Globals.LOGIN_SCREEN_ENTRY:
                enter_details(username, password)
            if cur_state == Globals.LOGIN_SCREEN_LOADING:
                sleep(random_range(500, 750) / 1000)
            if cur_state == Globals.LOGIN_SCREEN_LOBBY:
                sleep(random_range(300, 600) / 1000)
                move(box=[330, 315, 483, 360], click_left=True)
                t_logged.start()
                while (t_logged.elapsed_time() < 3000) and (not is_logged_in()):
                    sleep(0.1)
            else:
                sleep(0.1)
    sleep(0.5)
    return is_logged_in()
