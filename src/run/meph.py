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
        found = False
        dinky = 0
        keyboard.send("tab")
        score = 1
        stuck_count = 0
        found = False
        corner_picker = 3
        corner_exclude = 3
        super_stuck = 0
        keepernumber = 0
        while not found:   
            found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
            Logger.debug(corner_picker)
            exclude1 = corner_picker - 2
            exclude2 = corner_picker + 2
            if corner_picker == 1:
                Logger.debug("derpin1")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-150, -600), random.uniform(-20, -360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber  
            elif corner_picker == 2:
                Logger.debug("derpin2")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(150, 600), random.uniform(-20, -360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((-600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber   
            elif corner_picker == 3:
                Logger.debug("derpin3")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(480, 600), random.uniform(20, 360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber  
            elif corner_picker == 4:
                Logger.debug("derpin4")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-480, -600), random.uniform(20, 360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber  

                    

    def wptwotravel(self):
        #dostuffto durance 3
        found = False
        dinky = 0
        keyboard.send("tab")
        score = 1
        stuck_count = 0
        found = False
        corner_picker = 4
        corner_exclude = 4
        super_stuck = 0
        keepernumber = 0
        while not found:   
            found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
            Logger.debug(corner_picker)
            exclude1 = corner_picker - 2
            exclude2 = corner_picker + 2
            if corner_picker == 1:
                Logger.debug("derpin1")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-150, -600), random.uniform(-20, -360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber  
            elif corner_picker == 2:
                Logger.debug("derpin2")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(150, 600), random.uniform(-20, -360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((-600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber   
            elif corner_picker == 3:
                Logger.debug("derpin3")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(480, 600), random.uniform(20, 360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber  
            elif corner_picker == 4:
                Logger.debug("derpin4")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-480, -600), random.uniform(20, 360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber 
           

    def wpthreetravel(self):
        #dostuffto durance 3
        found = False
        dinky = 0
        keyboard.send("tab")
        score = 1
        stuck_count = 0
        found = False
        corner_picker = 2
        corner_exclude = 2
        super_stuck = 0
        keepernumber = 0
        while not found:   
            found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
            Logger.debug(corner_picker)
            exclude1 = corner_picker - 2
            exclude2 = corner_picker + 2
            if corner_picker == 1:
                Logger.debug("derpin1")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-150, -600), random.uniform(-20, -360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber  
            elif corner_picker == 2:
                Logger.debug("derpin2")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(150, 600), random.uniform(-20, -360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((-600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber   
            elif corner_picker == 3:
                Logger.debug("derpin3")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(480, 600), random.uniform(20, 360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber  
            elif corner_picker == 4:
                Logger.debug("derpin4")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-480, -600), random.uniform(20, 360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber                
                    
    def wpfourtravel(self):
        #dostuffto durance 3
        found = False
        dinky = 0
        keyboard.send("tab")
        score = 1
        stuck_count = 0
        found = False
        corner_picker = 3
        corner_exclude = 3
        exclude1 = 1
        exclude2 = 1
        super_stuck = 0
        keepernumber = 0
        while not found:   
            found = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], threshold=0.85, time_out=0.1, take_ss=False, use_grayscale=False).valid
            Logger.debug(corner_picker)
            exclude1 = corner_picker - 2
            exclude2 = corner_picker + 2
            if corner_picker == 1:
                Logger.debug("derpin1")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-150, -600), random.uniform(-20, -360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber  
            elif corner_picker == 2:
                Logger.debug("derpin2")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(150, 600), random.uniform(-20, -360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((-600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber   
            elif corner_picker == 3:
                Logger.debug("derpin3")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(480, 600), random.uniform(20, 360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, 350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber  
            elif corner_picker == 4:
                Logger.debug("derpin4")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(-480, -600), random.uniform(20, 360)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                dinky += 1
                if score < .10:
                    stuck_count += 1
                    if stuck_count >=2:
                        Logger.debug("Super stuck this little manuvuer will cost us... umm i dunno")
                        pos_m = self._screen.convert_abs_to_monitor((600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-600, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        super_stuck +=1
                    if super_stuck >= 3:
                        Logger.debug("SWAPPING AREA")
                        keepernumber = random.randint(1, 4)
                        if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                           keepernumber = random.randint(1, 4) 
                        else:
                            corner_exclude = corner_picker
                            corner_picker = keepernumber 


    def battle(self, do_pre_buff: bool) -> Union[bool, tuple[Location, bool]]:
        # TODO: We might need a second template for each option as merc might run into the template and we dont find it then
        if do_pre_buff:
            self._char.pre_buff()
        stuck_count = 0
        keyboard.send("f4")
        templates = ["WPONE1", "WPONE2", "WPONE3", "WPTWO2", "WPTWO2", "WPTWO3", "WPTHREE", "WPFOUR1"] ##checking which way to start exploring
        template_match = self._template_finder.search_and_wait(["MEPH_LVL2_WP2_0", "MEPH_LVL2_WP2_1", "MEPH_LVL2_WP2_2", "WPTHREE", "WPFOUR1", "WPFOUR2", "MEPH_LVL2_WP1_0", "MEPH_LVL2_WP1_1", "MEPH_LVL2_WP1_2", "MEPH_LVL2_WP1_3", "MEPH_LVL2_WP1_4", "MEPH_LVL2_WP1_5", "MEPH_LVL2_WP1_6", "MEPH_LVL2_WP1_7", "MEPH_LVL2_WP1_8", "MEPH_LVL2_WP1_9", "MEPH_LVL2_WP3_0", "MEPH_LVL2_WP3_1", "MEPH_LVL2_WP3_2", "MEPH_LVL2_WP3_3", "MEPH_LVL2_WP3_4", "MEPH_LVL2_WP3_5"], threshold=0.8, time_out=10)
        if not template_match.valid:
                return False
        layout = template_match.name
        Logger.debug(layout)
        if layout == 'MEPH_LVL2_WP1' or layout == "MEPH_LVL2_WP1_0" or layout == "MEPH_LVL2_WP1_1" or layout == "MEPH_LVL2_WP1_2" or layout == "MEPH_LVL2_WP1_3" or layout == "MEPH_LVL2_WP1_4" or layout == "MEPH_LVL2_WP1_5" or layout == "MEPH_LVL2_WP1_6" or layout == "MEPH_LVL2_WP1_7" or layout == "MEPH_LVL2_WP1_8" or layout == "MEPH_LVL2_WP1_9":
            self.wponetravel()
            ##ending clicker get in
            dinky = 0
            roomfound = False
            badroom = False
            template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
            if template_match.valid:
                keyboard.send("tab")
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
            while not roomfound and not badroom:
                roomfound = self._template_finder.search_and_wait(["DURANCEFOUR10", "MEPH_EXIT1", "DURANCEFOUR3", "MEPH_0", "DURANCEFOUR10", "MEPH_LVL2_WP1E_2", "MEPH_LVL2_WP1E_1", "MEPH_LVL2_WP1E_0", "MEPH_LVL2_WP1E_2", "MEPH_LVL2_WP1E_5", "MEPH_LVL2_WP1E_6", "MEPH_LVL2_WP1E_10", "MEPH_LVL2_WP1E_16"], threshold=0.8, time_out=0.1, take_ss=False, use_grayscale=False).valid
                badroom =  self._template_finder.search_and_wait(["MEPH_LVL1_UPSTAIRS_1", "MEPH_LVL1_UPSTAIRS_1", "MEPH_LVL1_STAIRS_0", "MEPH_LVL1_STAIRS_1"], threshold=0.8, time_out=0.1, take_ss=False, use_grayscale=False).valid
                template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
                if template_match.valid:
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
                        pos_m = self._screen.convert_abs_to_monitor((350, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-350, 350))
                        self._char.move(pos_m, force_tp=True)
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
                            if not template_match.valid:
                                Logger.debug("STUCK AND NO PURPLE GONNA REVERSE THIS BAD BOY")
                                pos_m = self._screen.convert_abs_to_monitor((550, 350))
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True)
                                pos_m = self._screen.convert_abs_to_monitor((-480, 350))
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True)
            if badroom == True: 
                Logger.debug("FOUND LEVEL 1 STAIRS! ZOOMING AWAY")
                # img = self._screen.grab()
                # masked_image = mask_by_roi(img, [min_x, min_y, width, height], "invert")
                return False
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
        elif layout == "MEPH_LVL2_WP2_0" or layout == "MEPH_LVL2_WP2_1" or layout == "MEPH_LVL2_WP2_2":
            self.wptwotravel()
            dinky = 0
            roomfound = False
            badroom = False
            template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
            if template_match.valid:
                keyboard.send("tab")
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                self._char.move(pos_m, force_tp=True, force_move=True)
            while not roomfound and not badroom:
                roomfound = self._template_finder.search_and_wait(["MEPH_LVL2_WP2E_1", "MEPH_LVL2_WP2E_12", "MEPH_LVL2_WP2E_5", "MEPH_LVL2_WP2E_6", "MEPH_LVL2_WP2E_7", "MEPH_LVL2_WP2E_8", "MEPH_LVL2_WP2E_9", "MEPH_LVL2_WP2E_11", "MEPH_LVL1_UPSTAIRS_1", "MEPH_LVL1_UPSTAIRS_0"], threshold=0.8, time_out=0.1, take_ss=False, use_grayscale=False).valid
                badroom =  self._template_finder.search_and_wait(["MEPH_LVL1_UPSTAIRS_1", "MEPH_LVL1_UPSTAIRS_1", "MEPH_LVL1_STAIRS_0", "MEPH_LVL1_STAIRS_1"], threshold=0.8, time_out=0.1, take_ss=False, use_grayscale=False).valid
                template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
                if template_match.valid:
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
                        pos_m = self._screen.convert_abs_to_monitor((350, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-350, 350))
                        self._char.move(pos_m, force_tp=True)
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
                            if not template_match.valid:
                                Logger.debug("STUCK AND NO PURPLE GONNA REVERSE THIS BAD BOY")
                                pos_m = self._screen.convert_abs_to_monitor((550, 350))
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True)
                                pos_m = self._screen.convert_abs_to_monitor((-480, 350))
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True)
                        score = .5
                        Logger.debug("STUCK")
                        dinky += 1
            if badroom == True: 
                Logger.debug("FOUND LEVEL 1 STAIRS! ZOOMING AWAY")
                # img = self._screen.grab()
                # masked_image = mask_by_roi(img, [min_x, min_y, width, height], "invert")
                return False                                           
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
        elif layout == 'WPTHREE':
            self.wpthreetravel()
            ##ending clicker get in
            dinky = 0
            badroom = False
            roomfound = False
            template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
            if template_match.valid:
                keyboard.send("tab")
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
            while not roomfound and not badroom:
                roomfound = self._template_finder.search_and_wait(["MEPH_EXIT2", "MEPH_LVL2_WP3E_1", "MEPH_LVL2_WP3E_0", "MEPH_LVL2_WP3E_2", "MEPH_LVL1_UPSTAIRS_1", "MEPH_LVL1_UPSTAIRS_0"], threshold=0.8, time_out=0.1, take_ss=False, use_grayscale=False).valid
                badroom =  self._template_finder.search_and_wait(["MEPH_LVL1_UPSTAIRS_1", "MEPH_LVL1_UPSTAIRS_1", "MEPH_LVL1_STAIRS_0", "MEPH_LVL1_STAIRS_1"], threshold=0.8, time_out=0.1, take_ss=False, use_grayscale=False).valid
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                if score < .15:
                    stuck_count += 1
                    if stuck_count >=3:
                        pos_m = self._screen.convert_abs_to_monitor((350, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-350, 350))
                        self._char.move(pos_m, force_tp=True)
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
                            if not template_match.valid:
                                Logger.debug("STUCK AND NO PURPLE GONNA REVERSE THIS BAD BOY")
                                pos_m = self._screen.convert_abs_to_monitor((550, 350))
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True)
                                pos_m = self._screen.convert_abs_to_monitor((-480, 350))
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True) 
            if badroom == True: 
                Logger.debug("FOUND LEVEL 1 STAIRS! ZOOMING AWAY")
                # img = self._screen.grab()
                # masked_image = mask_by_roi(img, [min_x, min_y, width, height], "invert")
                return False                                        
            picked_up_items = False 
            found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
            if not self._char.select_by_template(["MEPH_LVL2_WP3E_3"], found_loading_screen_func, threshold=0.3, time_out=4):
                # do a random tele jump and try again
                if not self._char.select_by_template(["MEPH_LVL2_WP3E_3", "MEPH_LVL2_WP3E_0","MEPH_LVL2_WP3E_2"], found_loading_screen_func, threshold=0.5, time_out=4):
                    return False
            # Wait until templates in durance of hate lvl 3 entrance are found
            if not self._template_finder.search_and_wait(["MEPH_LVL3_1"], threshold=0.8, time_out=20).valid:
                return False
        elif layout == 'WPFOUR1' or layout == "WPFOUR2":
            self.wpfourtravel()
            ##ending clicker get in
            dinky = 0
            roomfound = False
            badroom = False
            template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
            if template_match.valid:
                keyboard.send("tab")
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
            while not roomfound and not badroom:
                roomfound = self._template_finder.search_and_wait(["MEPH_LVL2_WP4E_1", "MEPH_LVL2_WP4E_00", "MEPH_LVL2_WP4E_0", "MEPH_LVL2_WP4E_2", "MEPH_LVL2_WP4E_3", "MEPH_LVL2_WP4E_4", "MEPH_LVL2_WP22E_1", "MEPH_LVL2_WP22E_12", "MEPH_LVL2_WP22E_5", "MEPH_LVL2_WP22E_6", "MEPH_LVL2_WP22E_7", "MEPH_LVL2_WP22E_8", "MEPH_LVL2_WP22E_9", "MEPH_LVL2_WP22E_11", "MEPH_LVL1_UPSTAIRS_1", "MEPH_LVL1_UPSTAIRS_0"], threshold=0.8, time_out=0.1, take_ss=False, use_grayscale=False).valid
                badroom =  self._template_finder.search_and_wait(["MEPH_LVL1_UPSTAIRS_1", "MEPH_LVL1_UPSTAIRS_1", "MEPH_LVL1_STAIRS_0", "MEPH_LVL1_STAIRS_1"], threshold=0.8, time_out=0.1, take_ss=False, use_grayscale=False).valid
                template_match = self._template_finder.search_and_wait(["PURPENT2", "PURPENT3"], best_match=True, threshold=0.8, time_out=0.1, use_grayscale=False)
                if template_match.valid:
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
                        pos_m = self._screen.convert_abs_to_monitor((350, -350))
                        self._char.move(pos_m, force_tp=True)
                        self._char.move(pos_m, force_tp=True)
                        pos_m = self._screen.convert_abs_to_monitor((-350, 350))
                        self._char.move(pos_m, force_tp=True)
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
                            if not template_match.valid:
                                Logger.debug("STUCK AND NO PURPLE GONNA REVERSE THIS BAD BOY")
                                pos_m = self._screen.convert_abs_to_monitor((550, 350))
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True)
                                pos_m = self._screen.convert_abs_to_monitor((-480, 350))
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True)
                                self._char.move(pos_m, force_tp=True)
            if badroom == True: 
                Logger.debug("FOUND LEVEL 1 STAIRS! ZOOMING AWAY")
                # img = self._screen.grab()
                # masked_image = mask_by_roi(img, [min_x, min_y, width, height], "invert")
                return False
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

        Logger.debug("Trying to path to meph")
        self._pather.traverse_nodes_fixed("meph_to_meph", self._char)
        pos_m = self._screen.convert_abs_to_monitor((0, -120))
        self._char.move(pos_m, force_move=True)
        if not self._pather.traverse_nodes([69104], self._char, time_out=3):
            pos_m = self._screen.convert_abs_to_monitor((50, 50))
            self._char.move(pos_m, force_move=True)
            return False
        wait(0.5)
        Logger.debug("We gonna die to meph lawllll")
        self._char.kill_meph()
        picked_up_items |= self._pickit.pick_up_items(self._char)
        keyboard.send("r")
        Logger.debug("Jumping to Star Node")
        pos_m = self._screen.convert_abs_to_monitor((485, 350))
        self._char.move(pos_m, force_tp=True)
        Logger.debug("Go to Last Node and Use Red Portal")
        if not self._pather.traverse_nodes([69104], self._char, time_out=3):
            # do a random tele jump and try again
            pos_m = self._screen.convert_abs_to_monitor((485, 350))
            self._char.move(pos_m, force_move=True)
        if not self._char.select_by_template(["MEPH_LVL3_MEPH_PORTAL"], found_loading_screen_func, threshold=0.8, time_out=4):
            # do a random tele jump and try again
            pos_m = self._screen.convert_abs_to_monitor((485, 350))
            self._char.move(pos_m, force_move=True)
            if not self._char.select_by_template(["MEPH_LVL3_MEPH_PORTAL"], found_loading_screen_func, threshold=0.6, time_out=4):
                return False
        # Wait until templates in durance of hate lvl 3 entrance are found
        return (Location.A3_MEPH_END, picked_up_items)
