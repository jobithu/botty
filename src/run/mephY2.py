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
        # Let's check which layout ("NI1_A = bottom exit" , "NI1_B = large room", "NI1_C = small room")
        if do_pre_buff:
            self._char.pre_buff()
        wait(0.5)
        keyboard.send("f4")
        pos_m = self._screen.convert_abs_to_monitor((random.uniform(-50, -200), random.uniform(50, 250)))
        self._char.move(pos_m, force_tp=True)
        template_match = self._template_finder.search_and_wait(["MEPH_WP"], threshold=0.65, time_out=1).valid
        while not template_match:
            pos_m = self._screen.convert_abs_to_monitor((random.uniform(-80, 80), random.uniform(-80, 80)))
            self._char.move(pos_m, force_tp=True, force_move=True)
            
            return False
        keyboard.send("tab")
            
        # Depending on what template is found we do static pathing to the stairs on level1.

        found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0) or \
            self._template_finder.search_and_wait(["MEPH_DURANCE3", "MEPH_LVL3"], threshold=0.8, time_out=100).valid
        found = False
        dinky = 1
        while not found:
            found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.75, time_out=0.1, take_ss=False, use_grayscale=False).valid 
            if not found:    
                while dinky < 100:
                    pos_m = self._screen.convert_abs_to_monitor((random.uniform(-150, -350), random.uniform(10, 80)))
                    self._char.move(pos_m, force_tp=True, force_move=True)
                    dinky += 1
                    if dinky >= 25:
                        pos_m = self._screen.convert_abs_to_monitor((random.uniform(-25, 200), random.uniform(-200, -500)))
                        self._char.move(pos_m, force_tp=True, force_move=True)
                        dinky += 1
                    if dinky >= 60:
                        pos_m = self._screen.convert_abs_to_monitor((random.uniform(-25, 200), random.uniform(-200, -500)))
                        self._char.move(pos_m, force_tp=True, force_move=True)
                        dinky += 1
        if found:
            return False
            # Attack & Pick items
        wait(60)    
        if not self._char.kill_meph():
            return False
        wait(0.2, 0.3)
        picked_up_items = self._pickit.pick_up_items(self._char)
        return (Location.A3_MEPH_END, picked_up_items)
