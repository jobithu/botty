import math
from pickle import FALSE
from re import search

from char.sorceress import Sorceress
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
import math


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

    def _corner_roller(self, corner_picker, x1_m, x2_m, y1_m, y2_m, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber)-> bool:
            keepernumber = random.randint(1, 4)
            if keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
                keepernumber = random.randint(1, 4) 
                super_stuck = 0
                stuck_count = 0
            else:
                corner_exclude = corner_picker
                corner_picker = keepernumber
                super_stuck = 0
                stuck_count = 0
                if corner_picker == 1:
                    self._scout(1, -250, -600, -200, -345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) #top - left
                elif corner_picker == 2:
                    self._scout(2, 250, 600, -200, -345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) # top - right
                elif corner_picker == 3:
                    self._scout(3, 485, 600, 200, 345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) # bottom - right
                elif corner_picker == 4:
                    self._scout(4, -485, -600, 200, 345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) # bottom - left

    def _scout(self, corner_picker, x1_m, x2_m, y1_m, y2_m, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber)-> bool:
        found = False
        Logger.debug("SCOUTING START")
        if not self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).valid:
            keyboard.send("tab")
            Logger.debug("SCOUT /// MAP ON")
        while not found:
                found = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6"], best_match=True, threshold=0.9, time_out=0.1, use_grayscale=False).valid
                founder = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6"], best_match=True, threshold=0.9, time_out=0.1, use_grayscale=False)
                foundname = founder.name
                if founder.valid:
                    pos_m = self._screen.convert_screen_to_monitor(founder.position)
                # Logger.debug("EXIT CLICKER 1st FIND/// MAP OFF")
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(x1_m, x2_m), random.uniform(y1_m, y2_m)))
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                Logger.debug(str(score) + ": is our current score")
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
                if score < .10:
                    stuck_count += 1               
                    if stuck_count >=2:
                        tele_math = random.randint(1, 3)
                        if math.fmod(tele_math, 3) == 0:
                            Logger.debug(str(corner_picker) + ": Seems we are stuck, let's go reverse 2 x 3 teleports SCOUT 1")
                            pos_m = self._screen.convert_abs_to_monitor((x2_m * -1, y2_m * -1))
                            self._char.move(pos_m, force_tp=True)
                            self._char.move(pos_m, force_tp=True)
                            self._char.move(pos_m, force_tp=True)
                            pos_m = self._screen.convert_abs_to_monitor((x2_m * -1, y2_m))
                            self._char.move(pos_m, force_tp=True)
                            self._char.move(pos_m, force_tp=True)
                            self._char.move(pos_m, force_tp=True)
                            stuck_count = 0
                            super_stuck +=1
                        else:
                            Logger.debug(str(corner_picker) + ": Seems we are stuck, let's go reverse 2 x 3 teleports SCOUT 2")
                            pos_m = self._screen.convert_abs_to_monitor((x2_m * -1, y2_m * -1))
                            self._char.move(pos_m, force_tp=True)
                            self._char.move(pos_m, force_tp=True)
                            self._char.move(pos_m, force_tp=True)
                            pos_m = self._screen.convert_abs_to_monitor((x2_m, y2_m * -1))
                            self._char.move(pos_m, force_tp=True)
                            self._char.move(pos_m, force_tp=True)
                            self._char.move(pos_m, force_tp=True)
                            stuck_count = 0
                            super_stuck +=1    
                        if super_stuck >= 2:
                            self._corner_roller(corner_picker, x1_m, x2_m, y1_m, y2_m, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber)
        if found == True:
            Logger.debug("SCOUT EXITING oustside")
            Logger.debug(foundname)
            Logger.debug(founder.score)
            self._exitclicker(pos_m)

            
    # def _to_throne(self)-> bool:
    #     Logger.debug("TO THRONE")
    #     #do_pre_buff: bool
    #     # if do_pre_buff: self._char.pre_buff()   
    #     keyboard.send("tab")
    #     keyboard.send(self._char._skill_hotkeys["teleport"])
    #     #setting up variables
    #     found = False
    #     corner_picker = 3 #we start searching towards the top, as often the cold plains entrance is at the bottom of the map
    #     corner_exclude = 3
    #     exclude1 = corner_picker - 2
    #     exclude2 = corner_picker + 2 
    #     stuck_count = 0
    #     super_stuck = 0
    #     keepernumber = 0
    #     dinky = 0
    #     #lets start the search
    #     while not found:
    #         Logger.debug(str(corner_picker) + ": is our selected corner.")   
    #         found = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6", "BAAL_LVL2_4", "BAAL_LVL2_5", "BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], best_match=True, threshold=0.7, time_out=0.1, use_grayscale=False).valid
    #         if corner_picker == 1:
    #             self._scout(1, -250, -600, -200, -345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) #top - left
    #             dinky += 1
    #         elif corner_picker == 2:
    #             self._scout(2, 250, 600, -200, -345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) # top - right
    #             dinky += 1
    #         elif corner_picker == 3:
    #             self._scout(3, 250, 600, 200, 345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) # bottom - right
    #             dinky += 1
    #         elif corner_picker == 4:
    #             self._scout(4, -250, -600, 200, 345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) # bottom - left
    #             dinky += 1
   

    def _exitclicker(self, pos_m)-> bool:
            Logger.debug("EXITCLICKER")
            roomfound = False
            stuck_count = 0
            super_stuck = 0
            mapcheck = self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False)
            template_match = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6"], best_match=True, threshold=0.9,  time_out=0.1, use_grayscale=False)
            if template_match.valid and mapcheck.valid:
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                Logger.debug("EXITCLICKER FOUND TEMPLATE TURNING MAP OFF!")
                keyboard.send("tab")
                # Logger.debug("EXIT CLICKER 1st FIND/// MAP OFF")
            while not roomfound:
                roomfound = self._template_finder.search_and_wait(["BAAL_LVL2_4", "BAAL_LVL2_5", "BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], best_match=True, threshold=0.7,  time_out=0.1, use_grayscale=False).valid
                template_match = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6"], best_match=True, threshold=0.9,  time_out=0.1, use_grayscale=False)
                if roomfound == True:
                    Logger.debug("EXIT CLICKER EXIT INSIDE")
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                super_stuck = 0
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)
                self._char.move(pos_m, force_tp=True, force_move=True)              
                if score < .15:
                    stuck_count += 1
                    if stuck_count >= 2 and super_stuck < 2:
                        super_stuck += 1
                        Logger.debug("EXIT CLICKER STUCK")  
                        # t0 = self._screen.grab()                      
                        # pos_m = self._screen.convert_abs_to_monitor((-315, -100))
                        # self._char.move(pos_m, force_move=True)
                        # pos_m = self._screen.convert_abs_to_monitor((-315, 150))
                        # self._char.move(pos_m, force_move=True)
                        # t1 = self._screen.grab()
                        # # check difference between the two frames to determine if tele was good or not
                        # diff = cv2.absdiff(t0, t1)
                        # diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                        # _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                        # score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                        # if score < .15:
                        #     pos_m = self._screen.convert_abs_to_monitor((-300, 200))
                        #     self._char.move(pos_m, force_move=True)
                        #     pos_m = self._screen.convert_abs_to_monitor((300, -250))
                        #     self._char.move(pos_m, force_move=True)
                        # stuck_count = 0
                        ##################MAYBE GOOD TELE LENGTHENER
                        x, y = pos_m
                        pos_m2 = x, y
                        coordlog = x, y
                        Logger.debug(coordlog)
                        x, y = self._screen.convert_monitor_to_screen(pos_m2)
                        x, y = x * -1, y *-1
                        pos_m2 = x, y
                        x, y = self._screen.convert_screen_to_abs(pos_m2)                        
                        pos_m2 = x, y
                        coordlog = x, y
                        Logger.debug(coordlog)
                        # x, y = self._screen.convert_abs_to_monitor((pos_m2))
                        #########################
                        if x < 0 and y < 0: # -, - Corner 1 Top Left
                            Logger.debug("corner one stuck")
                            pos_m2 = self._screen.convert_abs_to_monitor((-600, -350))
                            self._char.move(pos_m2, force_tp=True)
                            super_stuck += 1
                            stuck_count = 0
                        if x > 0 and y < 0: #corner 2
                            Logger.debug("corner two stuck")
                            pos_m2 = self._screen.convert_abs_to_monitor((600, -350))
                            self._char.move(pos_m2, force_tp=True)
                            super_stuck += 1
                            stuck_count = 0
                        if x > 0 and y > 0: #corner 3
                            Logger.debug("corner three stuck")
                            pos_m2 = self._screen.convert_abs_to_monitor((600, 350))
                            self._char.move(pos_m2, force_tp=True)
                            super_stuck += 1
                            stuck_count = 0
                        if x < 0 and y > 0: #corner 4
                            Logger.debug("corner four stuck")
                            pos_m2 = self._screen.convert_abs_to_monitor((-600, 350))
                            self._char.move(pos_m2, force_tp=True)
                            super_stuck += 1
                            stuck_count = 0
                    if super_stuck == 2:
                        Logger.debug("SUPER DUPER STUCK")
                        if not self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).valid:
                            Logger.debug("MAP CHECKER /// MAP ON")
                            keyboard.send("tab")
                        template_match = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6"], best_match=True, threshold=0.9,  time_out=0.5, use_grayscale=False)
                        if template_match.valid and mapcheck.valid:
                            template_match = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6"], best_match=True, threshold=0.9,  time_out=0.5, use_grayscale=False)
                            pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                            keyboard.send("tab")
                            Logger.debug("EXIT CLICKER MATCH AND MAP MATCH /// MAP OFF")
                            stuck_count = 0
                            super_stuck = 0
                        elif template_match == False:
                            Logger.debug("NO MATCH NO POSITION2222222")                                      
                            stuck_count = 0
                            super_stuck = 0
            Logger.debug("FOUND EXIT")
            found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
            if not self._char.select_by_template(["BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], found_loading_screen_func, threshold=0.7, time_out=4):
                # do a random tele jump and try again
                Logger.debug("FOUND EXIT BUT BROKE")
                pos_m = self._screen.convert_abs_to_monitor((315, -150))
                self._char.move(pos_m, force_move=True)
                if not self._char.select_by_template(["BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], found_loading_screen_func, threshold=0.7, time_out=4):
                    self._char.move(pos_m, force_move=True)
                    if not self._char.select_by_template(["BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], found_loading_screen_func, threshold=0.7, time_out=4):
                        pos_m = self._screen.convert_abs_to_monitor((-315, -100))
                        self._char.move(pos_m, force_move=True)
                        Logger.debug("CANT GET TO EXIT")
                        if not self._char.select_by_template(["BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], found_loading_screen_func, threshold=0.7, time_out=4):
                            Logger.debug("ABANDON HOPE!!!")
                            return False
            if not self._template_finder.search_and_wait(["BAAL_THRONE_START_0", "BAAL_THRONE_START_1", "BAAL_THRONE_START_2", "BAAL_THRONE_START_3"], threshold=0.7, time_out=1).valid:
                self._scout(4, -250, -600, 200, 345, stuck_count, super_stuck, 4, 2, 2, 4) # bottom - left
            else:
                #throne killd
                keyboard.send("tab")
                self._throne_room()

    def _throne_room(self)-> bool:
        Logger.debug("TO MONSTERIN THRONE")
        if not self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).valid:
            Logger.debug("MAP IS OFF! DO THRONE!")
        else:
            Logger.debug("MAP IS ON TURNING OFF! DO THRONE!")
            keyboard.send("tab")
        roomfound = False
        while not roomfound:
            roomfound = self._template_finder.search_and_wait(["BAAL_THRONE_ROOM_0", "BAAL_THRONE_ROOM_7", "BAAL_THRONE_ROOM_2", "BAAL_THRONE_ROOM_3", "BAAL_THRONE_ROOM_4", "BAAL_THRONE_ROOM_5", "BAAL_THRONE_ROOM_6"], best_match=True, threshold=0.8,  time_out=0.1, use_grayscale=False).valid
            pos_m = self._screen.convert_abs_to_monitor((550, -340))
            self._char.move(pos_m, force_tp=True)
            self._char.move(pos_m, force_tp=True)
            self._char.move(pos_m, force_tp=True)
        if not self._pather.traverse_nodes([9000], self._char, time_out=3):
            # do a random tele jump and try again
            pos_m = self._screen.convert_abs_to_monitor((250, 220))
            self._char.move(pos_m, force_move=True)
        Logger.debug("KILLING TRASH TWO TIMES!!!")     
        self._char._kill_throne_trash()
        pos_m = self._screen.convert_abs_to_monitor((-250, 150))
        self._char.move(pos_m, force_move=True)
        self._char._kill_throne_trash()
        if not self._pather.traverse_nodes([9000], self._char, time_out=3):
            # do a random tele jump and try again
            pos_m = self._screen.convert_abs_to_monitor((250, 220))
            self._char.move(pos_m, force_move=True)
        Logger.debug("WAITING FOR LAUGH?")
        baaldude = True
        found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
        laughcount = 0
        while laughcount < 7:
            if self._template_finder.search_and_wait(["LAUGHING"], best_match=True, threshold=0.75, time_out=0.1, use_grayscale=False).valid:
                laughcount += 1
                if not self._pather.traverse_nodes([9000], self._char, time_out=3):
                    # do a random tele jump and try again
                    pos_m = self._screen.convert_abs_to_monitor((250, 220))
                    self._char.move(pos_m, force_move=True)
                self._char._kill_throne_trash()
            if laughcount >= 5:
                if not self._pather.traverse_nodes([9000], self._char, time_out=3):
                    # do a random tele jump and try again
                    pos_m = self._screen.convert_abs_to_monitor((250, 220))
                    self._char.move(pos_m, force_move=True)
                    found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
                    if not self._char.select_by_template(["BAAL_THRONE_ROOM_7"], found_loading_screen_func, threshold=0.7, time_out=4):
                        pos_m = self._screen.convert_abs_to_monitor((250, -200))
                        self._char.move(pos_m, force_move=True)
                        Logger.debug("MAYBE MORE SPAWNS!!")
                        if not self._char.select_by_template(["BAAL_THRONE_ROOM_7"], found_loading_screen_func, threshold=0.7, time_out=4):
                            Logger.debug("KILL SOME MORE TRASH!")
                            pass                            

        #         self._char._kill_throne_trash()
        # while baaldude:
        #     baaldude = self._template_finder.search_and_wait(["BAAL_HIMSELF"], best_match=True, threshold=0.6, time_out=0.1, use_grayscale=False).valid or self._template_finder.search_and_wait(["BAAL_HIMSELF"], best_match=True, threshold=0.9, time_out=0.1, use_grayscale=False).valid
        #     if self._template_finder.search_and_wait(["LAUGHING"], best_match=True, threshold=0.75, time_out=0.1, use_grayscale=False).valid:
        #         self._char._kill_throne_trash() 
        #     else:
        #          Logger.debug("Uh.. WAITING FOR LAUGH")                   
        keyboard.send("f4")
        found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
        if not self._char.select_by_template(["BAAL_THRONE_ROOM_7"], found_loading_screen_func, threshold=0.7, time_out=4):
            pos_m = self._screen.convert_abs_to_monitor((250, -200))
            self._char.move(pos_m, force_move=True)
            Logger.debug("CANT GET TO EXIT")
            if not self._char.select_by_template(["BAAL_THRONE_ROOM_7"], found_loading_screen_func, threshold=0.7, time_out=4):
                Logger.debug("ABANDON HOPE!!!")
                return False

                    
    
    def battle(self, do_pre_buff: bool) -> Union[bool, tuple[Location, bool]]:
        # TODO: We might need a second template for each option as merc might run into the template and we dont find it then
        if do_pre_buff:
            self._char.pre_buff()
        stuck_count = 0
        keyboard.send("f4")
        self._scout(4, -485, -600, 200, 345, stuck_count, 0, 4, 2, 2, 0) #tries to get to exit
        Logger.debug("KILLING BAAL????")
        pos_m = self._screen.convert_abs_to_monitor((-550, -330))
        self._char.move(pos_m, force_move=True)
        pos_m = self._screen.convert_abs_to_monitor((-250, 150))
        self._char.move(pos_m, force_move=True)
        self._char.kill_baal()            

     

