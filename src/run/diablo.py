import cv2
import time
from char.i_char import IChar
from config import Config
from logger import Logger
from pather import Location, Pather
from typing import Union
from item.pickit import PickIt
from template_finder import TemplateFinder
from town.town_manager import TownManager
from ui import UiManager
from utils.misc import wait
from utils.custom_mouse import mouse
from screen import Screen


class Diablo:
    def __init__(
        self,
        screen: Screen,
        template_finder: TemplateFinder,
        pather: Pather,
        town_manager: TownManager,
        ui_manager: UiManager,
        char: IChar,
        pickit: PickIt
    ):
        self._config = Config()
        self._screen = screen
        self._template_finder = template_finder
        self._pather = pather
        self._town_manager = town_manager
        self._ui_manager = ui_manager
        self._char = char
        self._pickit = pickit
        self._picked_up_items = False

    def approach(self, start_loc: Location) -> Union[bool, Location, bool]:
        Logger.info("Run Diablo")
        if not self._char.can_teleport():
            raise ValueError("Diablo requires teleport")
        if not self._town_manager.open_wp(start_loc):
            return False
        wait(0.4)
        self._ui_manager.use_wp(4, 2)
        return Location.A4_DIABLO_WP

    def _river_of_flames(self) -> bool:
        if not self._pather.traverse_nodes([600], self._char): return False
        Logger.debug("Calibrated at WAYPOINT")
        self._pather.traverse_nodes_fixed("diablo_wp_entrance", self._char)
        Logger.info("Moving to CS ENTRANCE")
        found = False
        templates = ["DIABLO_CS_ENTRANCE_0", "DIABLO_CS_ENTRANCE_2", "DIABLO_CS_ENTRANCE_3"]
        # Looping in smaller teleport steps to make sure we find the entrance
        start_time = time.time()
        while not found and time.time() - start_time < 10:
            found = self._template_finder.search_and_wait(templates, threshold=0.8, time_out=0.1, take_ss=False).valid 
            if not found:
                self._pather.traverse_nodes_fixed("diablo_wp_entrance_loop", self._char)
        if not found:
            if self._config.general["info_screenshots"]:
                cv2.imwrite(f"./info_screenshots/failed_cs_entrance_" + time.strftime("%Y%m%d_%H%M%S") + ".png", self._screen.grab())
            return False
        if not self._pather.traverse_nodes([601], self._char, threshold=0.8): return False
        Logger.debug("Calibrated at CS ENTRANCE")
        return True

    def _cs_pentagram(self) -> bool:
        self._pather.traverse_nodes_fixed("diablo_entrance_pentagram", self._char)
        Logger.info("Moving to PENTAGRAM")
        found = False
        templates = ["DIABLO_PENT_0", "DIABLO_PENT_1", "DIABLO_PENT_2", "DIABLO_PENT_3"]
        start_time = time.time()
        while not found and time.time() - start_time < 10:
            found = self._template_finder.search_and_wait(templates, threshold=0.82, time_out=0.1).valid
            if not found:
                self._pather.traverse_nodes_fixed("diablo_entrance_pentagram_loop", self._char)
        if not found:
            if self._config.general["info_screenshots"]:
                cv2.imwrite(f"./info_screenshots/failed_pentagram_" + time.strftime("%Y%m%d_%H%M%S") + ".png", self._screen.grab())
            return False
        self._pather.traverse_nodes([602], self._char, threshold=0.82)
        Logger.info("Calibrated at PENTAGRAM")
        return True

    def _sealdance(self, seal_opentemplates: list[str], seal_closedtemplates: list[str], seal_layout: str) -> bool:
        i = 0
        while i < 4:
            # try to select seal
            Logger.info(seal_layout + ": trying to open " + str(i))
            self._char.select_by_template(seal_closedtemplates, threshold=0.5, time_out=0.5)
            wait(1)
            # check if seal is opened
            found = self._template_finder.search_and_wait(seal_opentemplates, threshold=0.75, time_out=0.5, take_ss=False).valid
            if found:
                Logger.info(seal_layout + ": is open")
                break
            else:
                Logger.info(seal_layout + ": not open")
                pos_m = self._screen.convert_abs_to_monitor((0, 0)) #remove mouse from seal
                mouse.move(*pos_m, randomize=[90, 160])
                wait(0.3)
                if i >= 2:
                    Logger.info(seal_layout + ": getting despreate after " + str(i) + " tries, trying to kill trash now")
                    self._char.kill_cs_trash()
                else:
                    # do a little random hop & try to click the seal
                    direction = 1 if i % 2 == 0 else -1
                    x_m, y_m = self._screen.convert_abs_to_monitor([50 * direction, 50 * direction])
                    self._char.move((x_m, y_m), force_move=True) 
                i += 1
        if self._config.general["info_screenshots"] and not found:
            cv2.imwrite(f"./info_screenshots/failed_seal_{seal_layout}_" + time.strftime("%Y%m%d_%H%M%S") + ".png", self._screen.grab())
        return found

    def _seal_A1(self): # WORKS STABLE
        seal_layout = "A1L"
        Logger.info("Seal Layout: " + seal_layout)
        self._pather.traverse_nodes([611], self._char) # approach & safe-dist
        self._char.kill_cs_trash()
        self._picked_up_items = self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([612, 613], self._char) # center
        self._char.kill_cs_trash()
        self._picked_up_items = self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([614], self._char) # close right fake seal
        #self._char.kill_cs_trash()
        self._sealdance(["DIA_A1L2_14_OPEN"], ["DIA_A1L2_14_CLOSED", "DIA_A1L2_14_MOUSEOVER"], seal_layout + "-Seal2", [614], [613], False)
        self._pather.traverse_nodes([613, 615], self._char) #  close left boss seal 
        self._sealdance(["DIA_A1L2_5_OPEN"], ["DIA_A1L2_5_CLOSED","DIA_A1L2_5_MOUSEOVER"], seal_layout + "-Seal1", [615], [612], False)
        self._pather.traverse_nodes([612, 611, 610], self._char) # safe-dist
        Logger.info("Kill Vizier")
        self._char.kill_vizier([612], [611]) #610
        self._picked_up_items = self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([610], self._char) # calibrate after looting
        Logger.info("Calibrated at " + seal_layout + " SAFE_DIST")
        self._pather.traverse_nodes_fixed("dia_a1l_home", self._char) #lets go home
        self._pather.traverse_nodes([602], self._char) # Pentagram
        Logger.info("Calibrated at PENTAGRAM")

    def _seal_A2(self): # WORKS STABLE
        seal_layout = "A2Y"
        Logger.info("Seal Layout: " + seal_layout)
        if not self._pather.traverse_nodes([622], self._char, threshold=0.82): return False
        self._char.kill_cs_trash()
        if not self._pather.traverse_nodes([624], self._char, threshold=0.82): return False
        self._char.kill_cs_trash()
        if not self._pather.traverse_nodes([625], self._char, threshold=0.82): return False
        #self._char.kill_cs_trash()
        if not self._sealdance(["DIA_A2Y4_29_OPEN"], ["DIA_A2Y4_29_CLOSED","DIA_A2Y4_29_MOUSEOVER"], seal_layout + "-Seal1"): return False
        if not self._pather.traverse_nodes([626], self._char, threshold=0.82): return False
        if not self._sealdance(["DIA_A2Y4_36_OPEN"], ["DIA_A2Y4_36_CLOSED", "DIA_A2Y4_36_MOUSEOVER"], seal_layout + "-Seal2"): return False
        if not self._pather.traverse_nodes([627, 623, 622], self._char, threshold=0.82): return False
        Logger.info("Kill Vizier")
        self._char.kill_vizier(623, 624)
        if not self._pather.traverse_nodes([623], self._char, threshold=0.82): return False
        self._picked_up_items |= self._pickit.pick_up_items(self._char)
        if not self._pather.traverse_nodes([622], self._char, threshold=0.82): return False
        Logger.info("Calibrated at " + seal_layout + " SAFE_DIST")
        self._pather.traverse_nodes_fixed("dia_a2y_home", self._char)
        if not self._pather.traverse_nodes([602], self._char, threshold=0.82): return False
        Logger.info("Calibrated at PENTAGRAM")

    def _seal_A1(self):
        seal_layout = "A1L"
        Logger.info("Seal Layout: " + seal_layout)
        self._pather.traverse_nodes_fixed("diablo_a2_safe_dist", self._char)
        self._char.kill_cs_trash()
        if not self._pather.traverse_nodes([620], self._char, threshold=0.82): return False
        if not self._sealdance(["DIA_A2L_7"], ["DIA_A2L_2", "DIA_A2L_3", "DIA_A2L_2_621", "DIA_A2L_2_620", "DIA_A2L_2_620_MOUSEOVER"], seal_layout + "-Seal1"): return False
        if not self._pather.traverse_nodes([622, 623], self._char, threshold=0.82): return False
        if not self._sealdance(["DIA_A2L_11"], ["DIA_A2L_0", "DIA_A2L_1"], seal_layout + "-Seal2"): return False
        if not self._pather.traverse_nodes([622], self._char, threshold=0.82): return False
        Logger.info("Kill Vizier")
        self._char.kill_vizier()
        self._picked_up_items |= self._pickit.pick_up_items(self._char)
        if not self._pather.traverse_nodes([622], self._char, threshold=0.82): return False
        Logger.info("Calibrated at " + seal_layout + " SAFE_DIST")
        self._pather.traverse_nodes_fixed("diablo_a2_end_pentagram", self._char)
        if not self._pather.traverse_nodes([602], self._char, threshold=0.82): return False
        Logger.info("Calibrated at PENTAGRAM")

    def _seal_B1(self): # old nodes, need to rework
        seal_layout = "B1S"
        Logger.info("Seal Layout: " + seal_layout)
        self._pather.traverse_nodes_fixed("diablo_pentagram_b1_seal", self._char) # to to seal
        self._char.kill_cs_trash() # at seal
        self._picked_up_items |= self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([632], self._char) #clear other side, too
        self._char.kill_cs_trash() # across gap - if they get fana on hell we are doomed
        self._picked_up_items |= self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([630], self._char) #back to seal      
        self._sealdance(["DIA_B1S_1_ACTIVE"], ["DIA_B1S_1", "DIA_B1S_0"], seal_layout) #pop
        self._pather.traverse_nodes([630], self._char) #633 is bugged
        self._pather.traverse_nodes_fixed("diablo_b1_safe_dist", self._char)
        Logger.info("Kill De Seis")
        self._char.kill_deseis()
        self._picked_up_items |= self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([632], self._char) # calibrate after looting
        Logger.info("Calibrated at " + seal_layout + " SAFE_DIST")
        self._pather.traverse_nodes_fixed("diablo_b1_end_pentagram", self._char) #lets go home
        self._pather.traverse_nodes([602], self._char) # Move to Pentagram
        Logger.info("Calibrated at PENTAGRAM")

    def _seal_B2(self): # WORKS STABLE
        seal_layout = "B2U"
        Logger.info("Seal Layout: " + seal_layout)
        self._pather.traverse_nodes([640], self._char) #approach, safe dist
        self._char.kill_cs_trash() # at safe_dist
        self._pather.traverse_nodes([641, 642], self._char) #approach, safe dist
        self._char.kill_cs_trash() # at safe_dist
        self._picked_up_items |= self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([643, 644], self._char) #seal far seal close
        self._sealdance(["DIA_B2U2_16_OPEN"], ["DIA_B2U2_16_CLOSED", "DIA_B2U2_16_MOUSEOVER"], seal_layout)
        self._pather.traverse_nodes([643, 642, 646], self._char) #seal far, safe dist
        Logger.info("Kill De Seis")
        self._char.kill_deseis(641,640)
        self._picked_up_items |= self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([640], self._char) #approach
        self._pather.traverse_nodes_fixed("dia_b2u_home", self._char) 
        self._pather.traverse_nodes([602], self._char) # Move to Pentagram
        Logger.info("Calibrated at PENTAGRAM")

    def _seal_C2(self): # WORKS STABLE
        seal_layout = "C2G"
        Logger.info("Seal Layout: " + seal_layout)
        self._pather.traverse_nodes([660, 661], self._char) # approach
        self._char.kill_cs_trash()
        self._picked_up_items |= self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([661], self._char) # approach
        self._sealdance(["DIA_C2G2_7_OPEN"], ["DIA_C2G2_7_CLOSED", "DIA_C2G2_7_MOUSEOVER"], seal_layout + "1")
        self._pather.traverse_nodes([662, 663], self._char) # fight 651
        Logger.info("Kill Infector")
        self._char.kill_infector()
        self._picked_up_items |= self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([664, 665], self._char) # pop seal 651, 
        self._sealdance(["DIA_C2G2_21_OPEN"], ["DIA_C2G2_21_CLOSED", "DIA_C2G2_21_MOUSEOVER"], seal_layout + "2")
        self._pather.traverse_nodes([665], self._char) # calibrate at SAFE_DIST after looting, before returning to pentagram
        Logger.info("Calibrated at " + seal_layout + " SAFE_DIST")
        self._pather.traverse_nodes_fixed("dia_c2g_home", self._char)
        self._pather.traverse_nodes([602], self._char) # calibrate pentagram
        Logger.info("Calibrated at PENTAGRAM")

    def _seal_C1(self): # old nodes, need to rework
        seal_layout = "C1F"
        Logger.info("Seal Layout: " + seal_layout)
        self._pather.traverse_nodes_fixed("diablo_pentagram_c2_seal", self._char) # moving close to upper seal
        self._pather.traverse_nodes([660], self._char) # position between seals
        self._char.kill_cs_trash()
        self._sealdance(["DIA_C2F_FAKE_ACTIVE"], ["DIA_C2F_FAKE_MOUSEOVER", "DIA_C2F_FAKE_CLOSED"], seal_layout + "-Seal1")
        self._pather.traverse_nodes([660], self._char) # transition to boss seal
        self._pather.traverse_nodes_fixed("diablo_c2f_hopleft", self._char) # moving to lower seal - dirty solution with static path, as the 661 does not work well
        self._char.kill_cs_trash()
        #self._pather.traverse_nodes([661], self._char) # transition to boss seal # we sometimes get stuck here, might need more templates
        self._sealdance(["DIA_C2F_BOSS_ACTIVE"], ["DIA_C2F_BOSS_MOUSEOVER", "DIA_C2F_BOSS_CLOSED"], seal_layout + "-Seal1")
        self._pather.traverse_nodes_fixed("diablo_c2f_hopright", self._char) # move to fight position - dirty solution with static path, as the 661 does not work well
        Logger.info("Kill Infector") 
        self._char.kill_infector()
        self.picked_up_items = self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([660], self._char) # transition to boss seal
        Logger.info("Calibrated at " + seal_layout + " SAFE_DIST")
        self._pather.traverse_nodes_fixed("diablo_c2_end_pentagram", self._char) #lets go home
        self._pather.traverse_nodes([602], self._char) # Move to Pentagram
        Logger.info("Calibrated at PENTAGRAM")

    def _seal_C2(self): # WORKS STABLE
        seal_layout = "C2G"
        Logger.info("Seal Layout: " + seal_layout)
        self._pather.traverse_nodes([660, 661, 662], self._char) # approach
        self._char.kill_cs_trash()
        self._picked_up_items = self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([661], self._char) # approach
        self._sealdance(["DIA_C2G2_7_OPEN"], ["DIA_C2G2_7_CLOSED", "DIA_C2G2_7_MOUSEOVER"], seal_layout + "1", [661], [662], False)
        self._pather.traverse_nodes([662, 663], self._char) # fight 651
        Logger.info("Kill Infector")
        self._char.kill_infector()
        self._picked_up_items = self._pickit.pick_up_items(self._char)
        self._pather.traverse_nodes([664, 665], self._char) # pop seal 651, 
        self._sealdance(["DIA_C2G2_21_OPEN"], ["DIA_C2G2_21_CLOSED", "DIA_C2G2_21_MOUSEOVER"], seal_layout + "2", [665], [664], False)
        self._pather.traverse_nodes([665], self._char) # calibrate at SAFE_DIST after looting, before returning to pentagram
        Logger.info("Calibrated at " + seal_layout + " SAFE_DIST")
        self._pather.traverse_nodes_fixed("dia_c2g_home", self._char)
        self._pather.traverse_nodes([602], self._char) # calibrate pentagram
        Logger.info("Calibrated at PENTAGRAM")

    def battle(self, do_pre_buff: bool) -> Union[bool, tuple[Location, bool]]:
        self._picked_up_items = False
        if do_pre_buff:
            self._char.pre_buff()
        if not self._river_of_flames():
            return False
        # TODO: Option to clear trash?
        if not self._cs_pentagram():
            return False
        # Seal A: Vizier (to the left)
        self._pather.traverse_nodes_fixed("dia_a_layout", self._char) # we check for layout of A (1=Y or 2=L) L lower seal pops boss, upper does not. Y upper seal pops boss, lower does not
        Logger.info("Checking Layout at A")
        if self._template_finder.search_and_wait(["DIABLO_A_LAYOUTCHECK0", "DIABLO_A_LAYOUTCHECK1", "DIABLO_A_LAYOUTCHECK2"], threshold=0.8, time_out=0.1).valid:
            if not self._seal_A2():
                return False
        else:
            if not self._seal_A1():
                return False
        # Seal B: De Seis (to the top)
        self._pather.traverse_nodes_fixed("dia_b_layout", self._char) # we check for layout of B (1=S or 2=U) - just one seal to pop.
        Logger.debug("Checking Layout at B")
        if self._template_finder.search_and_wait(["DIABLO_B_LAYOUTCHECK0", "DIABLO_B_LAYOUTCHECK1"], threshold=0.8, time_out=0.1).valid:
            self._seal_B1()
        else:
            self._seal_B2()
        ### Seal C: Infector (to the right)    
        self._pather.traverse_nodes_fixed("dia_c_layout", self._char)  # we check for layout of C (1=G or 2=F) G lower seal pops boss, upper does not. F first seal pops boss, second does not
        Logger.debug("Checking Layout at C")
        if self._template_finder.search_and_wait(["DIABLO_C_LAYOUTCHECK0", "DIABLO_C_LAYOUTCHECK1", "DIABLO_C_LAYOUTCHECK2"], threshold=0.8, time_out=0.1).valid:
            self._seal_C2() #stable
        else:
            self._seal_C1() # stable, but sometimes ranged mobs at top seal block the template check for open seal, botty then gets stuck 
        ### Diablo
        Logger.debug("Waiting for Diablo to spawn") # we could add a check here, if we take damage: if yes, one of the sealbosses is still alive (otherwise all demons would have died when the last seal was popped)
        wait(5)
        self._char.kill_diablo() 
        wait(0.2, 0.3)
        self._picked_up_items |= self._pickit.pick_up_items(self._char)
        return (Location.A4_DIABLO_END, self._picked_up_items) #there is an error  ValueError: State 'diablo' is not a registered state.

if __name__ == "__main__":
    from screen import Screen
    import keyboard
    from game_stats import GameStats
    import os
    keyboard.add_hotkey('f12', lambda: os._exit(1))
    keyboard.wait("f11")
    from config import Config
    from ui import UiManager
    from bot import Bot
    config = Config()
    screen = Screen(config.general["monitor"])
    game_stats = GameStats()
    bot = Bot(screen, game_stats, False)
    # bot._diablo.battle(True)
    # bot._diablo._traverse_river_of_flames()
    # bot._diablo._cs_pentagram()
    # bot._pather.traverse_nodes_fixed("dia_a_layout", bot._char) # we check for layout of A (1=Y or 2=L) L lower seal pops boss, upper does not. Y upper seal pops boss, lower does not
    # Logger.info("Checking Layout at A")
    # if bot._template_finder.search_and_wait(["DIABLO_A_LAYOUTCHECK0", "DIABLO_A_LAYOUTCHECK1", "DIABLO_A_LAYOUTCHECK2"], threshold=0.8, time_out=0.1).valid:
    #     bot._diablo._seal_A2()
    # else:
    #     bot._diablo._seal_A1()
    bot._diablo._sealdance(["DIA_A2Y4_29_OPEN"], ["DIA_A2Y4_29_CLOSED","DIA_A2Y4_29_MOUSEOVER"], "TEST-Seal1")
