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

    def battle(self, do_pre_buff: bool) -> Union[bool, tuple[Location, bool]]:
        # TODO: We might need a second template for each option as merc might run into the template and we dont find it then
        if do_pre_buff:
            self._char.pre_buff()
        wait(0.5)
        stuck_count = 0
        keyboard.send("f4")
        pos_m = self._screen.convert_abs_to_monitor((random.uniform(-50, -200), random.uniform(50, 250)))
        self._char.move(pos_m, force_tp=True)
        templates = ["WPONE1", "WPONE2", "WPONE3", "WPTWO2", "WPTWO2", "WPTWO3", "WPTHREE", "WPFOUR1"] ##checking which way to start exploring
        template_match = self._template_finder.search_and_wait(["WPONE1", "WPONE2", "WPONE3", "WPTWO2", "WPTWO2", "WPTWO3", "WPTHREE", "WPFOUR1"], threshold=0.20, time_out=10)
        if not template_match.valid:
                return False
        layout = template_match.name
        Logger.debug(template_match.name)
        if layout == "WPONE1" or "WPONE2" or "WPONE3":
            #dostuffto durance 3
            found = False
            dinky = 1
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
                    pos_m = self._screen.convert_abs_to_monitor((random.uniform(10, 350), random.uniform(80, 200)))
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
                            pos_m = self._screen.convert_abs_to_monitor((-500, 350))
                            self._char.move(pos_m, force_tp=True)
                            pos_m = self._screen.convert_abs_to_monitor((-500, 350))
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
                else:
                    pass                     
        elif layout == "WPTWO1" or "WPTWO2" or "WPTWO3":
                            #dostuffto durance 3
            found = False
            dinky = 1
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
                    pos_m = self._screen.convert_abs_to_monitor((random.uniform(10, 350), random.uniform(80, 200)))
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
                            pos_m = self._screen.convert_abs_to_monitor((-500, 350))
                            self._char.move(pos_m, force_tp=True)
                            pos_m = self._screen.convert_abs_to_monitor((-500, 350))
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
                else:
                    pass
        elif layout == "WPTHREE" or "WPTHREE2":
            #dostuffto durance 3
            found = False
            dinky = 1
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
                    pos_m = self._screen.convert_abs_to_monitor((random.uniform(10, 350), random.uniform(80, 200)))
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
                            pos_m = self._screen.convert_abs_to_monitor((-500, 350))
                            self._char.move(pos_m, force_tp=True)
                            pos_m = self._screen.convert_abs_to_monitor((-500, 350))
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
                else:
                    pass
        elif layout == "WPFOUR":
            #dostuffto durance 3
            found = False
            dinky = 1
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
                    pos_m = self._screen.convert_abs_to_monitor((random.uniform(10, 350), random.uniform(80, 200)))
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
                            pos_m = self._screen.convert_abs_to_monitor((-500, 350))
                            self._char.move(pos_m, force_tp=True)
                            pos_m = self._screen.convert_abs_to_monitor((-500, 350))
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
                else:
                    pass
        else:
            Logger.debug("nowp")
            # Attack & Pick items
        roomfound = False
        template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
        if template_match.valid:
            keyboard.send("tab")
            pos_m = self._screen.convert_screen_to_monitor(template_match.position)
        while not roomfound:
            roomfound = self._template_finder.search_and_wait(["DURANCEFOUR10", "MEPH_EXIT1", "DURANCEFOUR3", "MEPH_0"], threshold=0.5, time_out=0.1, take_ss=False, use_grayscale=False).valid
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
            keyboard.send("tab")
            wait(.5)
            found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
            keyboard.send("tab")
            wait(2)
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
        while not self._pather.traverse_nodes([69420], self._char, time_out=3) or self._pather.traverse_nodes([69421], self._char, time_out=3):
            self._pather.traverse_nodes([69420], self._char, time_out=3)
            pos_m = self._screen.convert_abs_to_monitor((random.randint(-70, 70), random.randint(-70, 70)))
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

            self._char.move(pos_m, force_move=True)
            self._char.move(pos_m, force_move=True)
            self._char.move(pos_m, force_move=True)
            self._char.move(pos_m, force_move=True)
            self._char.move(pos_m, force_move=True)            
            roomfound = False
            while not roomfound:
                found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
                roomfound = self._template_finder.search_and_wait(["DURANCEFOUR10"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
                self._char.move(pos_m, force_move=True)
                self._char.move(pos_m, force_move=True)
                self._char.move(pos_m, force_move=True)
                self._char.move(pos_m, force_move=True)
                keyboard.send("tab")
                wait(.5)
                img = self._screen.grab()
                wait(.5)
                keyboard.send("tab")    
                template_match = self._template_finder.search(["PURPENT2", "PURPENT3"], img,  best_match=True, threshold=0.8, use_grayscale=False).valid
                if template_match.valid:
                    pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                    self._char.move(pos_m, force_move=True)
                    self._char.move(pos_m, force_move=True)
                    self._char.move(pos_m, force_move=True)
                    self._char.move(pos_m, force_move=True)
                else:
                    img = self._screen.grab()    
                    found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0) or \
                    self._template_finder.search_and_wait(["DURANCELVL3"], threshold=0.8, time_out=0.5).valid
                    roomfound = self._template_finder.search_and_wait(["DURANCEFOUR10"], best_match=True, threshold=0.3, use_grayscale=False)
                    self._char.select_by_template(["DURANCEFOUR3"], found_loading_screen_func, threshold=0.3, time_out=1)
                    template_match = self._template_finder.search(["PURPENT2", "PURPENT3"], img,  best_match=True, threshold=0.8, use_grayscale=False)
                    if template_match.valid:
                        pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                        self._char.move(pos_m, force_move=True)
            Logger.debug("HEADING TO PURPLE!!!!!")
            Logger.debug("HEADING TO PURPLE!!!!!")
            Logger.debug("HEADING TO PURPLE!!!!!")
            Logger.debug("HEADING TO PURPLE!!!!!")
            Logger.debug("HEADING TO PURPLE!!!!!")
        #entrancefound = False
        #keyboard.send("tab")
        #while not entrancefound:    
         #       entrancefound = self._template_finder.search_and_wait(["4PILLAR"], threshold=0.6, time_out=0.1, take_ss=False, use_grayscale=False).valid
          #      self._char.move(pos_m, force_move=True)
           #     self._char.move(pos_m, force_move=True)
            #    self._char.move(pos_m, force_move=True)

        Logger.debug("LEVEL 2 REFINE AND LEVEL 3 ETA 4 YEARS")
        wait(10)
        self._pather.traverse_nodes([69422, 69423, 69424, 69425, 69426, 69427, 69428, 69429], self._char, threshold=0.80, time_out=3)
        Logger.debug("We gonna die to meph lawllll")
        self._char.kill_meph()
        loc = Location.A3_MEPH_END
        picked_up_items = False
        picked_up_items |= self._pickit.pick_up_items(self._char)
        return (loc, picked_up_items)
