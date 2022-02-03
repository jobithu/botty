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


class Baal:
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
        Logger.info("Run Baal")
        if not self._char.can_teleport():
            raise ValueError("Baal requires teleport")
        if not self._town_manager.open_wp(start_loc):
            return False
        wait(0.4)
        if self._ui_manager.use_wp(5, 8): # Worldstone
            return Location.A5_BAAL_START
        return False

    def baaltravel(self) -> bool:
            #dostuffto durance 3
            Logger.debug("Heading to WP")
            found = False
            dinky = 1
            keyboard.send("tab")
            score = 1
            stuck_count = 0
            found = False 
            while not found:    
                found = self._template_finder.search_and_wait(["RED_GOOP_PURPLE"], threshold=0.7, time_out=0.1, take_ss=False, use_grayscale=False).valid 
                while dinky < 75 and not found:
                    pos_m = self._screen.convert_abs_to_monitor((random.uniform(150, 350), random.uniform(-50, -400)))
                    t0 = self._screen.grab()
                    self._char.move(pos_m, force_tp=True, force_move=True)
                    t1 = self._screen.grab()
                    # check difference between the two frames to determine if tele was good or not
                    diff = cv2.absdiff(t0, t1)
                    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                    _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                    score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                    dinky += 1
                    found = self._template_finder.search_and_wait(["RED_GOOP_PURPLE"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
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
                    found = self._template_finder.search_and_wait(["RED_GOOP_PURPLE"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
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
                    found = self._template_finder.search_and_wait(["RED_GOOP_PURPLE"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
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
            

    def battle(self, do_pre_buff: bool) -> Union[bool, tuple[Location, bool]]:
        # TODO: We might need a second template for each option as merc might run into the template and we dont find it then
        if do_pre_buff:
            self._char.pre_buff()
        stuck_count = 0
        keyboard.send("f4")
        self.baaltravel()
        ##ending clicker get in
        dinky = 0
        roomfound = False
        template_match = self._template_finder.search_and_wait(["RED_GOOP_PURPLE"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
        if template_match.valid:
            keyboard.send("tab")
            pos_m = self._screen.convert_screen_to_monitor(template_match.position)
        while not roomfound:
            roomfound = self._template_finder.search_and_wait(["BAAL_LVL2_4", "BAAL_LVL2_5", "BAAL_LVL2_EXIT"], threshold=0.65, time_out=0.1, take_ss=False, use_grayscale=False).valid
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
        if not self._char.select_by_template(["BAAL_LVL2_EXIT"], found_loading_screen_func, threshold=0.8, time_out=4):
            # do a random tele jump and try again
            if not self._char.select_by_template(["BAAL_LVL2_EXIT"], found_loading_screen_func, threshold=0.8, time_out=4):
                return False
        # Wait until templates in durance of hate lvl 3 entrance are found
        if not self._template_finder.search_and_wait(["BAAL_LVL3_ENTRANCE"], threshold=0.8, time_out=20).valid:
            return False

                    
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
        


    # Logger.debug("Trying to path to meph")
    # Logger.debug("Finish Arch move and then Up Middle and To Boss")
    # Logger.debug("We gonna die to baal lawllll")
    # self._char.kill_baal()
    # Logger.debug("Go to Last Node and Use Red Portal")
    # self._pather.traverse_nodes([69510], self._char, time_out=3) or self._pather.traverse_nodes([69506], self._char, time_out=3)
    # if not self._char.select_by_template(["MEPH_LVL3_MEPH_PORTAL"], found_loading_screen_func, threshold=0.3, time_out=4):
    #     # do a random tele jump and try again
    #     pos_m = self._screen.convert_abs_to_monitor((-75, -150))
    #     self._char.move(pos_m, force_move=True)
    #     if not self._char.select_by_template(["MEPH_LVL3_MEPH_PORTAL"], found_loading_screen_func, threshold=0.3, time_out=4):
    #         return False
    # # Wait until templates in durance of hate lvl 3 entrance are found
    # loc = Location.A3_MEPH_END
    # picked_up_items = False
    # picked_up_items |= self._pickit.pick_up_items(self._char)
    # return (loc, picked_up_items)
