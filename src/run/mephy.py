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
from template_finder import TemplateMatch
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
        templates = ["WPONE1", "WPONE2", "WPONE3"] ##checking which way to start exploring
        if self._template_finder.search_and_wait(templates, threshold=0.6, time_out=0.5).valid:
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
        Logger.debug("get to stairs")
        wait(20)
            # Attack & Pick items
        Logger.debug("gonna break now")
        config = Config()
        screen = Screen(config.general["monitor"])
        img = screen.grab()
        display_img = img.copy()
        config = Config()
        screen = Screen(config.general["monitor"])
        img = screen.grab()
        template_finder = TemplateFinder(screen)
        display_img = img.copy()
        template_match = template_finder.search(["PURPENT2", "PURPENT3"], img, best_match=True, threshold=0.8, use_grayscale=False)
        if template_match.valid:
            cv2.putText(display_img, str(template_match.name), template_match.position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.circle(display_img, template_match.position, 7, (255, 0, 0), thickness=5)
            x, y = template_match.position
            pos_m = self._screen.convert_abs_to_monitor((x, y))
            self.pre_move()
            self.move(pos_m, force_move=True)
        self._char.kill_meph()
        wait(30)
        loc = Location.A3_MEPH_END
        self._picked_up_items |= self._pickit.pick_up_items(self._char)
        return (loc, self._picked_up_items)
