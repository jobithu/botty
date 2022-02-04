from pickle import FALSE
from re import search


from char.i_char import IChar
from typing import Dict, Tuple, Union, List, Callable
from config import Config
from logger import Logger
import keyboard
from pather import Location, Pather
from typing import Union
from item.pickit import PickIt
from template_finder import TemplateFinder
from town.town_manager import TownManager
from ui import UiManager
from utils.misc import wait
from utils.custom_mouse import mouse
from dataclasses import dataclass
import math
import cv2
import time
from screen import Screen
from char import IChar
import numpy as np
from utils.misc import load_template, list_files_in_folder, alpha_to_mask
import random


class Meph:
    def __init__(
        self,
        screen: Screen,
        template_finder: TemplateFinder,
        pather: Pather,
        town_manager: TownManager,
        ui_manager: UiManager,
        char: IChar,
        pickit: PickIt,

    ):
        self._config = Config()
        self._screen = screen
        self._template_finder = template_finder
        self._pather = pather
        self._town_manager = town_manager
        self._ui_manager = ui_manager
        self._char = char
        self._pickit = pickit
        self._pather = pather
 
    def approach(self, start_loc: Location) -> Union[bool, Location, bool]:
        Logger.info("Run Meph")
        if not self._char.can_teleport():
            raise ValueError("Meph requires teleport")
        if not self._town_manager.open_wp(start_loc):
            return False
        wait(0.4)
        if self._ui_manager.use_wp(3, 8): # Durance 2
            return Location.A3_MEPH_START
        return False

    def wponetravel(self):
        #dostuffto durance 3
        Logger.debug("DOING WP ONE STUFF")
        found = False
        dinky = 1
        keyboard.send("tab")
        score = 1
        stuck_count = 0
        found = False 
        while not found:    
            found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
            while dinky < 75 and not found:
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(10, 250), random.uniform(-100, -250)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((-500, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-500, 275))
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            if dinky >= 25:
                t0 = self._screen.grab()
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(25, 200), random.uniform(50, 300)))
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((-150, -200))
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-350, -150))
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            if dinky >= 60:
                t0 = self._screen.grab()
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(25, 200), random.uniform(50, 300)))
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                self._char.move(pos_m, force_tp=True, force_move=True)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((-150, -200))
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-350, -150))
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            

    def wptwotravel(self):
        #dostuffto durance 3
        found = False
        dinky = 0
        stuck_count = 0
        keyboard.send("tab")
        pos_m = self._screen.convert_abs_to_monitor((-60, 200))
        self._char.move(pos_m, force_move=True)
        wait(0.5)
        pos_m = self._screen.convert_abs_to_monitor((-80, 150))
        self._char.move(pos_m, force_move=True)
        score = 1
        found = False 
        while not found:    
            found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
            while dinky < 75 and not found:
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-1, -400), random.uniform(250, -10)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((-500, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-250, 200))
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            if dinky >= 25:
                t0 = self._screen.grab()
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-10, -350), random.uniform(-80, -200)))
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((500, -350))
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((500, 350))
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((500, -350))
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            if dinky >= 60:
                t0 = self._screen.grab()
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-10, 150), random.uniform(-80, -200)))
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                self._char.move(pos_m, force_tp=True, force_move=True)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((500, -350))
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((500, 350))
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((500, -350))
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1

    def wpthreetravel(self):
        #dostuffto durance 3
        Logger.debug("DOING WP THREE STUFF")
        dinky = 1
        keyboard.send("tab")
        stuck_count = 0
        score = 1
        found = False 
        while not found:    
            found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
            while dinky < 100 and not found:
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-500, 150), random.uniform(75, -250)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((550, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((550, -100))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            if dinky >= 50:
                t0 = self._screen.grab()
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-550, 60), random.uniform(-500, -600)))
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((550, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((550, -100))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            if dinky >= 80:
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-400, 10), random.uniform(-50, -250)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((550, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((550, -100))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            if dinky == 100:
                return False

    def wpfourtravel(self):
        #dostuffto durance 3
        dinky = 1
        keyboard.send("tab")
        stuck_count = 0
        score = 1
        found = False 
        while not found:    
            found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
            while dinky < 75 and not found:
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(150, 450), random.uniform(-50, -400)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((-500, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((500, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            if dinky >= 25:
                t0 = self._screen.grab()
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-20, 300), random.uniform(-150, -450)))
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((-450, -200))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((450, 250))
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            if dinky >= 60:
                t0 = self._screen.grab()
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-150, 550), random.uniform(-150, -450)))
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                self._char.move(pos_m, force_tp=True, force_move=True)
                dinky += 1
                found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((-450, -200))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-450, 150))
                        self._char.move(pos_m, force_tp=True)
                        Logger.debug("STUCK")
                        dinky += 1


    def battle(self, do_pre_buff: bool) -> Union[bool, tuple[Location, bool]]:
        # TODO: We might need a second template for each option as merc might run into the template and we dont find it then
        if do_pre_buff:
            self._char.pre_buff()
        stuck_count = 0
        keyboard.send("f4")
        templates = ["WPONE1", "WPONE2", "WPONE3", "WPTWO2", "WPTWO2", "WPTWO3", "WPTHREE", "WPFOUR1"] ##checking which way to start exploring
        template_match = self._template_finder.search_and_wait(["WPTWO1", "WPTHREE", "WPFOUR1", "WPFOUR2", "MEPH_LVL2_WP1_0", "MEPH_LVL2_WP1_1", "MEPH_LVL2_WP1_2", "MEPH_LVL2_WP1_3", "MEPH_LVL2_WP1_4", "MEPH_LVL2_WP1_5", "MEPH_LVL2_WP1_6", "MEPH_LVL2_WP1_7", "MEPH_LVL2_WP1_8", "MEPH_LVL2_WP1_9", "MEPH_LVL2_WP3_0", "MEPH_LVL2_WP3_1", "MEPH_LVL2_WP3_2", "MEPH_LVL2_WP3_3", "MEPH_LVL2_WP3_4", "MEPH_LVL2_WP3_5"], threshold=0.65, time_out=10)
        if not template_match.valid:
                return False
        layout = template_match.name
        Logger.debug(layout)
        if layout == 'WPTHREE':
            self.wpthreetravel()
            ##ending clicker get in
            dinky = 0
            roomfound = False
            template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
            if template_match.valid:
                keyboard.send("tab")
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
            while not roomfound:
                roomfound = self._template_finder.search_and_wait(["MEPH_EXIT2", "MEPH_LVL2_WP3E_1", "MEPH_LVL2_WP3E_0", "MEPH_LVL2_WP3E_2"], threshold=0.65, time_out=0.1, take_ss=False, use_grayscale=False).valid
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m2 = self._screen.convert_abs_to_monitor((-150, -200))
                        self._char.move(pos_m2, force_tp=True)
                        pos_m2 = self._screen.convert_abs_to_monitor((-350, -150))
                        self._char.move(pos_m2, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1                    
            picked_up_items = False 
            found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
            if not self._char.select_by_template(["MEPH_LVL2_WP3E_3"], found_loading_screen_func, threshold=0.3, time_out=4):
                # do a random tele jump and try again
                if not self._char.select_by_template(["MEPH_LVL2_WP3E_3", "MEPH_LVL2_WP3E_0","MEPH_LVL2_WP3E_2"], found_loading_screen_func, threshold=0.5, time_out=4):
                    return False
            # Wait until templates in durance of hate lvl 3 entrance are found
            if not self._template_finder.search_and_wait(["MEPH_LVL3_1"], threshold=0.8, time_out=20).valid:
                return False
        elif layout == 'MEPH_LVL2_WP1' or layout == "MEPH_LVL2_WP1_0" or layout == "MEPH_LVL2_WP1_1" or layout == "MEPH_LVL2_WP1_2" or layout == "MEPH_LVL2_WP1_3" or layout == "MEPH_LVL2_WP1_4" or layout == "MEPH_LVL2_WP1_5" or layout == "MEPH_LVL2_WP1_6" or layout == "MEPH_LVL2_WP1_7" or layout == "MEPH_LVL2_WP1_8" or layout == "MEPH_LVL2_WP1_9":
            self.wponetravel()
            ##ending clicker get in
            dinky = 0
            roomfound = False
            template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
            if template_match.valid:
                keyboard.send("tab")
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
            while not roomfound:
                roomfound = self._template_finder.search_and_wait(["DURANCEFOUR10", "MEPH_EXIT1", "DURANCEFOUR3", "MEPH_0", "DURANCEFOUR10", "MEPH_LVL2_WP1E_2", "MEPH_LVL2_WP1E_1", "MEPH_LVL2_WP1E_0", "MEPH_LVL2_WP1E_2", "MEPH_LVL2_WP1E_5", "MEPH_LVL2_WP1E_6", "MEPH_LVL2_WP1E_10", "MEPH_LVL2_WP1E_16"], threshold=0.65, time_out=0.1, take_ss=False, use_grayscale=False).valid
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m2 = self._screen.convert_abs_to_monitor((-150, -200))
                        self._char.move(pos_m2, force_tp=True)
                        pos_m2 = self._screen.convert_abs_to_monitor((-350, -150))
                        self._char.move(pos_m2, force_tp=True)
                        stuck_count = 0
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            if not self._pather.traverse_nodes([69420], self._char, time_out=3):
                self._pather.traverse_nodes([69405], self._char, time_out=3)
                pos_m = self._screen.convert_abs_to_monitor((random.randint(-70, -70), random.randint(-70, -70)))
                self._char.move(pos_m, force_move=True)                    
            picked_up_items = False 
            found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
            if not self._char.select_by_template(["MEPH_EXIT1"], found_loading_screen_func, threshold=0.63, time_out=4):
                # do a random tele jump and try again
                pos_m = self._screen.convert_abs_to_monitor((150, -200))
                self._char.move(pos_m, force_move=True)
                if not self._char.select_by_template(["MEPH_EXIT1"], found_loading_screen_func, threshold=0.63, time_out=4):
                    return False
            # Wait until templates in durance of hate lvl 3 entrance are found
            if not self._template_finder.search_and_wait(["MEPH_LVL3_1"], threshold=0.8, time_out=20).valid:
                return False
        elif layout == 'WPTWO1':
            self.wptwotravel()
            dinky = 0
            roomfound = False
            template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
            if template_match.valid:
                keyboard.send("tab")
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
            while not roomfound:
                roomfound = self._template_finder.search_and_wait(["MEPH_LVL2_WP2E_1", "MEPH_LVL2_WP2E_12", "MEPH_LVL2_WP2E_5", "MEPH_LVL2_WP2E_6", "MEPH_LVL2_WP2E_7", "MEPH_LVL2_WP2E_8", "MEPH_LVL2_WP2E_9", "MEPH_LVL2_WP2E_11"], threshold=0.65, time_out=0.1, take_ss=False, use_grayscale=False).valid
                t0 = self._screen.grab()
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((500, 350))
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((370, 200))
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        keyboard.send("tab")
                        wait(.5)
                        template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
                        if template_match.valid:
                            keyboard.send("tab")
                            pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                            self._char.move(pos_m, force_tp=True, force_move=True)
                            self._char.move(pos_m, force_tp=True, force_move=True)
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1                    
            picked_up_items = False 
            found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
            self._pather.traverse_nodes([69900], self._char, time_out=3)
            if not self._char.select_by_template(["MEPH_LVL2_WP2E_23", "MEPH_LVL2_WP2E_24", "MEPH_LVL2_WP2E_22"], found_loading_screen_func, threshold=0.5, time_out=4):
                # do a random tele jump and try again
                pos_m = self._screen.convert_abs_to_monitor((150, -200))
                self._char.move(pos_m, force_move=True)
                if not self._char.select_by_template(["MEPH_LVL2_WP2E_22", "MEPH_LVL2_WP2E_24"], found_loading_screen_func, threshold=0.7, time_out=4):
                    return False
            # Wait until templates in durance of hate lvl 3 entrance are found
            if not self._template_finder.search_and_wait(["MEPH_LVL3_1"], threshold=0.65, time_out=20).valid:
                return False
        elif layout == 'WPFOUR1' or layout == "WPFOUR2":
            self.wpfourtravel()
            ##ending clicker get in
            dinky = 0
            roomfound = False
            template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
            if template_match.valid:
                keyboard.send("tab")
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
            while not roomfound:
                roomfound = self._template_finder.search_and_wait(["MEPH_LVL2_WP4E_1", "MEPH_LVL2_WP4E_00", "MEPH_LVL2_WP4E_0", "MEPH_LVL2_WP4E_2", "MEPH_LVL2_WP4E_3", "MEPH_LVL2_WP4E_4", "MEPH_LVL2_WP22E_1", "MEPH_LVL2_WP22E_12", "MEPH_LVL2_WP22E_5", "MEPH_LVL2_WP22E_6", "MEPH_LVL2_WP22E_7", "MEPH_LVL2_WP22E_8", "MEPH_LVL2_WP22E_9", "MEPH_LVL2_WP22E_11"], threshold=0.65, time_out=0.1, take_ss=False, use_grayscale=False).valid
                t0 = self._screen.grab()
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((500, 350))
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((370, 200))
                        self._char.move(pos_m, force_tp=True)
                        stuck_count = 0
                        keyboard.send("tab")
                        wait(.5)
                        template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
                        if template_match.valid:
                            keyboard.send("tab")
                            pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                            self._char.move(pos_m, force_tp=True, force_move=True)
                            self._char.move(pos_m, force_tp=True, force_move=True)
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1                    
            picked_up_items = False 
            found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
            self._pather.traverse_nodes([69406, 69407], self._char, time_out=3)
            if not self._char.select_by_template(["MEPH_LVL2_WP4E_7"], found_loading_screen_func, threshold=0.5, time_out=4):
                # do a random tele jump and try again
                pos_m = self._screen.convert_abs_to_monitor((150, -200))
                self._char.move(pos_m, force_move=True)
                if not self._char.select_by_template(["MEPH_LVL2_WP4E_7", "DURANCEFOUR3", "DURANCEFOURSTAIRS1", "MEPH_EXIT1", "MEPH_EXIT2"], found_loading_screen_func, threshold=0.3, time_out=4):
                    return False
            # Wait until templates in durance of hate lvl 3 entrance are found
            if not self._template_finder.search_and_wait(["MEPH_LVL3_1"], threshold=0.65, time_out=20).valid:
                return False
        else:
            return False        
        ##ending clicker get in
       #  dinky = 0
       #roomfound = False
        #template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
        #if template_match.valid:
         #   keyboard.send("tab")
         #   pos_m = self._screen.convert_screen_to_monitor(template_match.position)
        #while not roomfound:
         #   roomfound = self._template_finder.search_and_wait(["DURANCEFOUR10", "MEPH_EXIT1", "DURANCEFOUR3", "MEPH_0", "DURANCEFOUR10", "MEPH_LVL2_WP1E_2", "MEPH_LVL2_WP1E_1", "MEPH_LVL2_WP1E_0", "MEPH_LVL2_WP1E_2", "MEPH_LVL2_WP1E_5", "MEPH_LVL2_WP1E_6", "MEPH_LVL2_WP1E_10", "MEPH_LVL2_WP1E_16"], threshold=0.65, time_out=0.1, take_ss=False, use_grayscale=False).valid
          #  t0 = self._screen.grab()
           # self._char.move(pos_m, force_tp=True, force_move=True)
            #t1 = self._screen.grab()
            ## check difference between the two frames to determine if tele was good or not
            #diff = cv2.absdiff(t0, t1)
            #diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            #_, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
            ##score = (float(np.sum(mask)) / mask.size) * (1/255.0)
            #self._char.move(pos_m, force_tp=True, force_move=True)
            #self._char.move(pos_m, force_tp=True, force_move=True)
            #self._char.move(pos_m, force_tp=True, force_move=True)
            #if score < .15:
            #    stuck_count += 1
            #    if stuck_count >=3:
            #        pos_m2 = self._screen.convert_abs_to_monitor((-150, -200))
            ##       pos_m2 = self._screen.convert_abs_to_monitor((-350, -150))
              #      self._char.move(pos_m2, force_tp=True)
               #     stuck_count = 0
                #    score = .5
                 #   Logger.debug("STUCK")
                  #  dinky += 1
        #if not self._pather.traverse_nodes([69420], self._char, time_out=3):
         #   self._pather.traverse_nodes([69405], self._char, time_out=3)
          #  pos_m = self._screen.convert_abs_to_monitor((random.randint(-70, -70), random.randint(-70, -70)))
           # self._char.move(pos_m, force_move=True)
                
      #  picked_up_items = False 
       # found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
        #if not self._char.select_by_template(["MEPH_EXIT1"], found_loading_screen_func, threshold=0.63, time_out=4):
            # do a random tele jump and try again
         #   pos_m = self._screen.convert_abs_to_monitor((150, -200))
          #  self._char.move(pos_m, force_move=True)
           # if not self._char.select_by_template(["MEPH_EXIT1"], found_loading_screen_func, threshold=0.63, time_out=4):
            #    return False
        # Wait until templates in durance of hate lvl 3 entrance are found
        #if not self._template_finder.search_and_wait(["MEPH_LVL3_1"], threshold=0.8, time_out=20).valid:
         #   return False

            # self._char.move(pos_m, force_move=True)
            # self._char.move(pos_m, force_move=True)
            # self._char.move(pos_m, force_move=True)
            # self._char.move(pos_m, force_move=True)
            # self._char.move(pos_m, force_move=True)            
            # roomfound = False
            # while not roomfound:
            #     found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
            #     roomfound = self._template_finder.search_and_wait(["DURANCEFOUR10"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
            #     self._char.move(pos_m, force_move=True)
            #     self._char.move(pos_m, force_move=True)
            #     self._char.move(pos_m, force_move=True)
            #     self._char.move(pos_m, force_move=True)
            #     keyboard.send("tab")
            #     wait(.5)
            #     img = self._screen.grab()
            #     wait(.5)
            #     keyboard.send("tab")    
            #     template_match = self._template_finder.search(["PURPENT2", "PURPENT3"], img,  best_match=True, threshold=0.8, use_grayscale=False).valid
            #     if template_match.valid:
            #         pos_m = self._screen.convert_screen_to_monitor(template_match.position)
            #         self._char.move(pos_m, force_move=True)
            #         self._char.move(pos_m, force_move=True)
            #         self._char.move(pos_m, force_move=True)
            #         self._char.move(pos_m, force_move=True)
            #     else:
            #         img = self._screen.grab()    
            #         found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0) or \
            #         self._template_finder.search_and_wait(["DURANCELVL3"], threshold=0.8, time_out=0.5).valid
            #         roomfound = self._template_finder.search_and_wait(["DURANCEFOUR10"], best_match=True, threshold=0.3, use_grayscale=False)
            #         self._char.select_by_template(["DURANCEFOUR3"], found_loading_screen_func, threshold=0.3, time_out=1)
            #         template_match = self._template_finder.search(["PURPENT2", "PURPENT3"], img,  best_match=True, threshold=0.8, use_grayscale=False)
            #         if template_match.valid:
            #             pos_m = self._screen.convert_screen_to_monitor(template_match.position)
            #             self._char.move(pos_m, force_move=True)
            # Logger.debug("HEADING TO PURPLE!!!!!")
            # Logger.debug("HEADING TO PURPLE!!!!!")
            # Logger.debug("HEADING TO PURPLE!!!!!")
            # Logger.debug("HEADING TO PURPLE!!!!!")
            # Logger.debug("HEADING TO PURPLE!!!!!")
        #entrancefound = False
        #keyboard.send("tab")
        #while not entrancefound:    
         #       entrancefound = self._template_finder.search_and_wait(["4PILLAR"], threshold=0.6, time_out=0.1, take_ss=False, use_grayscale=False).valid
          #      self._char.move(pos_m, force_move=True)
           #     self._char.move(pos_m, force_move=True)
            #    self._char.move(pos_m, force_move=True)

        Logger.debug("Trying to path to meph")
        self._pather.traverse_nodes_fixed("meph_to_meph", self._char)
        wait(0.5)
        self._pather.traverse_nodes([69104], self._char, time_out=3)
        pos_m = self._screen.convert_abs_to_monitor((-20, -200))
        self._char.move(pos_m, force_tp=True)
        pos_m = self._screen.convert_abs_to_monitor((20, 200))
        self._char.move(pos_m, force_tp=True)
        # Logger.debug("501")
        # self._pather.traverse_nodes([69501], self._char, threshold=0.01, time_out=3, force_move=True)
        # Logger.debug("502")
        # self._pather.traverse_nodes([69502], self._char, threshold=0.5, time_out=3, force_move=True)
        # #self._pather.traverse_nodes([69506], self._char, threshold=0.75, time_out=3, force_move=True)
        # #pos_m = self._screen.convert_abs_to_monitor((-400, -200))
        # self._char.move(pos_m, force_move=True) 
        # Logger.debug("503")
        # self._pather.traverse_nodes([69503], self._char, threshold=0.75, time_out=3, force_move=True)
        # Logger.debug("504")
        # self._pather.traverse_nodes([69504], self._char, threshold=0.75, time_out=3, force_move=True)
        # Logger.debug("505")
        # self._pather.traverse_nodes([69505], self._char, threshold=0.75, time_out=3, force_move=True)
        # self._pather.traverse_nodes([69106], self._char, time_out=3)
        # wait(1)
        # self._pather.traverse_nodes([69107], self._char, time_out=3)
        # self._pather.traverse_nodes([69106], self._char, time_out=3)
        self._char.kill_meph()
        Logger.debug("Jumping Down Toward Portal Node")
        pos_m = self._screen.convert_abs_to_monitor((500, -350))
        self._char.move(pos_m, force_tp=True)
        self._pather.traverse_nodes([69104], self._char, time_out=3)
        if not self._char.select_by_template(["MEPH_LVL3_MEPH_PORTAL"], found_loading_screen_func, threshold=0.8, time_out=4):
            # do a random tele jump and try again
            pos_m = self._screen.convert_abs_to_monitor((5, 25))
            self._char.move(pos_m, force_move=True)
            if not self._char.select_by_template(["MEPH_LVL3_MEPH_PORTAL"], found_loading_screen_func, threshold=0.6, time_out=4):
                return False
        # Wait until templates in durance of hate lvl 3 entrance are found
        loc = Location.A3_MEPH_END
        picked_up_items = False
        picked_up_items |= self._pickit.pick_up_items(self._char)
        return (loc, picked_up_items)
