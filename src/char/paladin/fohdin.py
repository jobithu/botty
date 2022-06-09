from asyncio.windows_events import NULL
from pickle import TRUE
import random
import keyboard
from screen import convert_abs_to_monitor, convert_screen_to_abs, grab, convert_abs_to_screen
from utils.custom_mouse import mouse
from char.paladin import Paladin
from logger import Logger
from config import Config
from utils.misc import wait
import time
from pather import Location
import numpy as np

from target_detect import get_visible_targets, TargetInfo, log_targets

class FoHdin(Paladin):
    def __init__(self, *args, **kwargs):
        Logger.info("Setting up FoHdin")
        super().__init__(*args, **kwargs)
        self._pather.adapt_path((Location.A3_TRAV_START, Location.A3_TRAV_CENTER_STAIRS), [220, 221, 222, 903, 904, 905, 906])

    def _log_cast(self, skill_name: str, cast_pos_abs: tuple[float, float], spray: int, time_in_s: float, aura: str):
        msg = f"Casting skill {skill_name}"
        if cast_pos_abs:
            msg += f" at screen coordinate {convert_abs_to_screen(cast_pos_abs)}"
        if spray:
            msg += f" with spray of {spray}"
        if time_in_s:
            msg += f" for {round(time_in_s, 1)}s"
        if aura:
            msg += f" with aura {aura} active"
        Logger.debug(msg)


    def _click_cast(self, cast_pos_abs: tuple[float, float], spray: int):
        if cast_pos_abs:
            x = cast_pos_abs[0]
            y = cast_pos_abs[1]
            if spray:
                x += (random.random() * 2 * spray - spray)
                y += (random.random() * 2 * spray - spray)
            pos_m = convert_abs_to_monitor((x, y))
            mouse.move(*pos_m, delay_factor=[0.1, 0.2])
            wait(0.06, 0.08)
        mouse.press(button="left")
        wait(0.06, 0.08)
        mouse.release(button="left")

    def _cast_skill(self, skill_name: str, cast_pos_abs: tuple[float, float] = None, spray: int = 0, time_in_s: float = 0, aura: str = ""):
        self._log_cast(skill_name, cast_pos_abs, spray, time_in_s, aura)
        if aura and aura in self._skill_hotkeys and self._skill_hotkeys[aura]:
            keyboard.send(self._skill_hotkeys[aura])
            wait(0.05, 0.1)
        else:
            Logger.warning(f"No hotkey for aura: {aura}")
        keyboard.send(Config().char["stand_still"], do_release=False)
        wait(0.05, 0.1)
        if self._skill_hotkeys[skill_name]:
            keyboard.send(self._skill_hotkeys[skill_name])
        wait(0.05, 0.1)
        start = time.time()
        if time_in_s:
            while (time.time() - start) <= time_in_s:
                self._click_cast(cast_pos_abs, spray)
        else:
            self._click_cast(cast_pos_abs, spray)
        wait(0.01, 0.05)
        keyboard.send(Config().char["stand_still"], do_press=False)

    def _cast_foh(self, cast_pos_abs: tuple[float, float], spray: int = 10, time_in_s: float = 0, aura: str = "conviction"):
        return self._cast_skill(skill_name = "foh", cast_pos_abs = cast_pos_abs, spray = spray, time_in_s = time_in_s, aura = aura)

    def _cast_holy_bolt(self, cast_pos_abs: tuple[float, float], spray: int = 10, time_in_s: float = 0, aura: str = "conviction"):
        return self._cast_skill(skill_name = "holy_bolt", cast_pos_abs = cast_pos_abs, spray = spray, time_in_s = time_in_s, aura = aura)

    def _cast_hammers(self, time_in_s: float = 0, aura: str = "concentration"): #for nihlathak
        return self._cast_skill(skill_name = "blessed_hammer", spray = 0, time_in_s = time_in_s, aura = aura)

    def _move_and_attack(self, abs_move: tuple[int, int], atk_len: float): #for nihalthak
        pos_m = convert_abs_to_monitor(abs_move)
        self.pre_move()
        self.move(pos_m, force_move=True)
        self._cast_hammers(atk_len)


    def _pindle_foh_attack_sequence(self, atk_len_dur: float):
        # check for targets and attack if they still exist
        start = time.time()
        target_check_count = 0
        while (targets := get_visible_targets()) and (time.time() - start) <= atk_len_dur * 2:
            log_targets(targets)
            nearest_mob_pos_abs = targets[0].center_abs
            # if target check is divisible by X, cast holy bolt
            if not target_check_count % 3:
                self._cast_holy_bolt(nearest_mob_pos_abs, spray=5)
            else:
            # otherwise, cast FOH
                self._cast_foh(nearest_mob_pos_abs, spray=5)
            target_check_count += 1

    def kill_pindle(self) -> bool:
        atk_len_dur = float(Config().char["atk_len_pindle"])
        pindle_pos_abs = convert_screen_to_abs(Config().path["pindle_end"][0])

        if self.capabilities.can_teleport_natively or self.capabilities.can_teleport_with_charges:
            # Slightly retreating, so the Merc gets charged
            if not self._pather.traverse_nodes([102], self, timeout=1.0, do_pre_move=self._do_pre_move, force_move=True,force_tp=False, use_tp_charge=False): return False
            # Doing one Teleport to safe_dist to grab our Merc
            if not self._pather.traverse_nodes([103], self, timeout=1.0, do_pre_move=self._do_pre_move, force_tp=True, use_tp_charge=True): return False
            # Slightly retreating, so the Merc gets charged
            if not self._pather.traverse_nodes([103], self, timeout=1.0, do_pre_move=self._do_pre_move, force_move=True, force_tp=False, use_tp_charge=False): return False
        else:
            if not self._do_pre_move:
                keyboard.send(self._skill_hotkeys["conviction"])
                wait(0.05, 0.15)
            self._pather.traverse_nodes([103], self, timeout=1.0, do_pre_move=self._do_pre_move)

        # Use the standard attack pattern w/o mob detection first
        cast_pos_abs = [pindle_pos_abs[0] * 0.9, pindle_pos_abs[1] * 0.9]
        self._cast_foh(cast_pos_abs, spray=11, time_in_s=atk_len_dur)
        wait(self._cast_duration, self._cast_duration + 0.2)

        # Then use target-based attack sequence
        self._pindle_foh_attack_sequence(atk_len_dur)

        if self.capabilities.can_teleport_natively:
            self._pather.traverse_nodes_fixed("pindle_end", self)
        else:
            if not self._do_pre_move:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.05, 0.15)
            self._pather.traverse_nodes((Location.A5_PINDLE_SAFE_DIST, Location.A5_PINDLE_END), self, timeout=1.0, do_pre_move=self._do_pre_move)

        # Use target-based attack sequence one more time before pickit
        self._pindle_foh_attack_sequence(atk_len_dur)

        return True


    def _council_foh_attack_sequence(self, traverse_node: int = None, atk_len_dur: float = Config().char["atk_len_trav"], attack_node: bool = False):
        if traverse_node is not None:
            self._pather.traverse_nodes([traverse_node], self, timeout=2.5, force_tp=True)

        if self._skill_hotkeys["conviction"]:
            keyboard.send(self._skill_hotkeys["conviction"]) #conviction needs to be on for mob_detection

        start = time.time()
        # perform initial mobcheck and cast foh
        elapsed = 0
        while (targets := get_visible_targets()) and (elapsed := (time.time() - start) <= atk_len_dur):
            nearest_mob_pos_abs = targets[0].center_abs
            Logger.debug("Mob found at " + str(nearest_mob_pos_abs) + '\033[96m'+" fisting him now "+ str(atk_len_dur) + " seconds!" +'\033[0m')
            self._cast_foh(nearest_mob_pos_abs, spray=11)
        # less than x seconds means no mobs were found
        if elapsed < 0.3:
            # if attack_node is true, then spray there
            if attack_node:
                img = grab()
                msg = "No Mob found"
                trav_attack_pos = self._pather.find_abs_node_pos(traverse_node, img) or self._pather.find_abs_node_pos(906, img)
                if trav_attack_pos:
                    Logger.debug(f"{msg}, attacking node #{traverse_node} instead")
                    self._cast_foh(trav_attack_pos, spray=80)
                else:
                    Logger.debug(msg)
        # mobs were found and initial attack sequence complete
        else:
            # if mobs still exist try holy bolt
            while (targets := get_visible_targets()) and (elapsed := (time.time() - start) <= atk_len_dur):
                nearest_mob_pos_abs = targets[0].center_abs
                Logger.debug("Mob found at " + str(nearest_mob_pos_abs) + '\033[93m'+" bolting him now "+ str(atk_len_dur) + " seconds!" +'\033[0m')
                self._cast_holy_bolt(nearest_mob_pos_abs, spray=80)

            if self._skill_hotkeys["cleansing"]:
                keyboard.send(self._skill_hotkeys["cleansing"])
                wait(0.1, 0.2) #clear yourself from curses

            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.5, 0.7) #clear area from corpses & heal


    def kill_council(self) -> bool:
        atk_len_factor = 3
        atk_len = "atk_len_trav"
        atk_len_dur = Config().char[atk_len] * atk_len_factor

        self._council_foh_attack_sequence(atk_len_dur = atk_len_dur)
        self._council_foh_attack_sequence(traverse_node = 225, atk_len_dur = atk_len_dur, attack_node = True)
        self._council_foh_attack_sequence(traverse_node = 226, atk_len_dur = atk_len_dur, attack_node = True)
        self._council_foh_attack_sequence(traverse_node = 300, atk_len_dur = atk_len_dur, attack_node = True)

        # Move outside since the trav.py expects to start searching for items there if char can teleport
        self._pather.traverse_nodes([226], self, timeout=2.5, force_tp=True)
        return True


    def kill_eldritch(self) -> bool:
        eld_pos_abs = convert_screen_to_abs(Config().path["eldritch_end"][0])
        cast_pos_abs = [eld_pos_abs[0] * 0.9, eld_pos_abs[1] * 0.9]
        atk_len_factor = 0.5 #we have a longer initial cast duration, but for the mob check iterations, we just use half of that
        atk_len = "atk_len_trav"
        atk_len_dur = int(Config().char[atk_len])*atk_len_factor

        if self._skill_hotkeys["conviction"]: keyboard.send(self._skill_hotkeys["conviction"]) #conviction needs to be on for mob_detection
        self._cast_foh(cast_pos_abs, spray=80, time_in_s=int(Config().char["atk_len_eldritch"]))

        for _ in range(int(Config().char["atk_len_eldritch"])):
            #lets check if there are still mobs & kill them

            if (targets := get_visible_targets()):
                nearest_mob_pos_abs = convert_screen_to_abs(targets[0].center)
                Logger.debug("Mob found at " + str(nearest_mob_pos_abs) + '\033[96m'+" fisting him now "+ str(atk_len_dur) + " times (atk_len)!" +'\033[0m')
                atk_len_dur = int(atk_len_dur)
                print(atk_len_dur)
                for _ in range(atk_len_dur):
                    self._cast_foh(nearest_mob_pos_abs, spray=11, time_in_s=atk_len_dur)

                if (targets := get_visible_targets()):
                    nearest_mob_pos_abs = convert_screen_to_abs(targets[0].center)
                    Logger.debug("Mob found at " + str(nearest_mob_pos_abs) + '\033[93m'+" bolting him now "+ str(atk_len_dur) + " seconds (atk_len)!" +'\033[0m')
                    for _ in range(atk_len_dur):
                        self._cast_holy_bolt(nearest_mob_pos_abs, spray=80, time_in_s=atk_len_dur)

                else:
                    Logger.debug("No Mob found, moving on")

                if self._skill_hotkeys["cleansing"]:
                    keyboard.send(self._skill_hotkeys["cleansing"])
                    wait(0.1, 0.2) #clear yourself from curses

        # Move to items
        if self._skill_hotkeys["redemption"]:
            keyboard.send(self._skill_hotkeys["redemption"])

        pos_m = convert_abs_to_monitor((70, -200))
        self.pre_move()
        self.move(pos_m, force_move=True)
        self._pather.traverse_nodes(Location.A5_ELDRITCH_SAFE_DIST, Location.A5_ELDRITCH_END)
        return True


    def kill_shenk(self):
        if not self._do_pre_move:
            keyboard.send(self._skill_hotkeys["conviction"])
            wait(0.05, 0.15)
        self._pather.traverse_nodes((Location.A5_SHENK_SAFE_DIST, Location.A5_SHENK_END), self, timeout=1.0, do_pre_move=self._do_pre_move, force_tp=True, use_tp_charge=True)
        wait(0.05, 0.1)
        self._cast_foh((0, 0), spray=11)
        atk_len_factor = 1
        atk_len = "atk_len_shenk"
        atk_len_dur = int(Config().char[atk_len])*atk_len_factor
        if self._skill_hotkeys["conviction"]: keyboard.send(self._skill_hotkeys["conviction"]) #conviction needs to be on for mob_detection
        if (targets := get_visible_targets()):
            nearest_mob_pos_abs = convert_screen_to_abs(targets[0].center)
            Logger.debug("Mob found at " + str(nearest_mob_pos_abs) + '\033[96m'+" fisting him now "+ str(atk_len_dur) + " times!" +'\033[0m')
            for _ in range(atk_len_dur):
                self._cast_foh(nearest_mob_pos_abs, spray=11)
            #    self._cast_holy_bolt(nearest_mob_pos_abs, spray=80, time_in_s=atk_len_dur)
            #wait(self._cast_duration, self._cast_duration + 0.2)
            if (targets := get_visible_targets()):
                nearest_mob_pos_abs = convert_screen_to_abs(targets[0].center)
                Logger.debug("Mob found at " + str(nearest_mob_pos_abs) + '\033[93m'+" bolting him now "+ str(atk_len_dur) + " seconds!" +'\033[0m')
                #print (nearest_mob_pos_abs)
                for _ in range(atk_len_dur):
                #    self._cast_foh(nearest_mob_pos_abs, spray=11)
                    self._cast_holy_bolt(nearest_mob_pos_abs, spray=80, time_in_s=atk_len_dur)
                #wait(self._cast_duration, self._cast_duration + 0.2)
            else:
                Logger.debug("No Mob found, moving on")
            if self._skill_hotkeys["cleansing"]:
                keyboard.send(self._skill_hotkeys["cleansing"])
            wait(0.1, 0.2) #clear yourself from curses
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.5, 1.0) #clear area from corpses & heal
        else:
            Logger.debug("No Mob found, moving on")
        return True


    #we just use hammers :)
    def kill_nihlathak(self, end_nodes: list[int]) -> bool:
        # Move close to nihlathak
        self._pather.traverse_nodes(end_nodes, self, timeout=0.8, do_pre_move=False)
        # move mouse to center, otherwise hammers sometimes dont fly, not sure why
        pos_m = convert_abs_to_monitor((0, 0))
        mouse.move(*pos_m, randomize=80, delay_factor=[0.5, 0.7])
        self._cast_hammers(Config().char["atk_len_nihlathak"] * 0.4)
        self._cast_hammers(0.8, "redemption")
        self._move_and_attack((30, 15), Config().char["atk_len_nihlathak"] * 0.3)
        self._cast_hammers(0.8, "redemption")
        self._move_and_attack((-30, -15), Config().char["atk_len_nihlathak"] * 0.4)
        wait(0.1, 0.15)
        self._cast_hammers(1.2, "redemption")
        return True

    def kill_summoner(self) -> bool:
        # Attack
        cast_pos_abs = np.array([0, 0])
        pos_m = convert_abs_to_monitor((-20, 20))
        mouse.move(*pos_m, randomize=80, delay_factor=[0.5, 0.7])
        for _ in range(int(Config().char["atk_len_arc"])):
            self._cast_foh(cast_pos_abs, spray=80, time_in_s=int(Config().char["atk_len_arc"]))
            self._cast_holy_bolt(cast_pos_abs, spray=90, time_in_s=int(Config().char["atk_len_arc"]))
        wait(self._cast_duration, self._cast_duration + 0.2)
        return True


     ########################################################################################
     # Chaos Sanctuary, Trash, Seal Bosses (a = Vizier, b = De Seis, c = Infector) & Diablo #
     ########################################################################################

    #FOHdin Attack Sequence Optimized for trash
    def cs_trash_atk_seq(self, atk_len, atk_len_factor):
        """
        :FOHdin Attack Sequence Optimized for killing trash in Chaos Sanctuary:
        :param atk_len: Attack Length as defined in Config
        :param atk_len_factor: Multiplier (int) for the Param atk_len to adapt length for locations with large number of mobs
        Returns True
        """
        #self._cast_foh((0,0), spray=11) #never wrong to cast a FOH on yourself :)
        atk_len = int(Config().char[atk_len])*atk_len_factor
        if self._skill_hotkeys["conviction"]: keyboard.send(self._skill_hotkeys["conviction"]) #conviction needs to be on for mob_detection
        if (targets := get_visible_targets()):
            nearest_mob_pos_abs = convert_screen_to_abs(targets[0].center)
            Logger.debug("Mob found at " + str(nearest_mob_pos_abs) + '\033[96m'+" fisting him now "+ str(atk_len) + " times!" +'\033[0m')
            #for _ in range(atk_len):
            self._cast_foh(nearest_mob_pos_abs, spray=11, time_in_s=atk_len)
            #    self._cast_holy_bolt(nearest_mob_pos_abs, spray=80, time_in_s=atk_len)
            #wait(self._cast_duration, self._cast_duration + 0.2)
            if (targets := get_visible_targets()):
                nearest_mob_pos_abs = convert_screen_to_abs(targets[0].center)
                Logger.debug("Mob found at " + str(nearest_mob_pos_abs) + '\033[93m'+" bolting him now "+ str(atk_len) + " seconds!" +'\033[0m')
                #print (nearest_mob_pos_abs)
                # for _ in range(atk_len):
                #    self._cast_foh(nearest_mob_pos_abs, spray=11)
                self._cast_holy_bolt(nearest_mob_pos_abs, spray=80, time_in_s=atk_len)
                #wait(self._cast_duration, self._cast_duration + 0.2)
            else:
                Logger.debug("No Mob found, moving on")
            if self._skill_hotkeys["cleansing"]:
                keyboard.send(self._skill_hotkeys["cleansing"])
            wait(0.1, 0.2) #clear yourself & merc from curses to avoid interfering with mob detection
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.5, 1.0) #clear area from corpses & heal
        else:
            Logger.debug("No Mob found, moving on")
        return True

    def kill_cs_trash(self, location:str) -> bool:
        if not Config().char['cs_mob_detect']:
            Logger.error("This run requires 'cs_mob_detect' to be set to 1")
            return False

        ###########
        # SEALDANCE
        ###########

        #these locations have no traverses and are basically identical.
        #if location in ("sealdance", "rof_01", "rof_02", "entrance_hall_01", "entrance_hall_02", "entrance1_01", "entrance1_02", "entrance1_03", "entrance1_04", "entrance2_01", "entrance2_03"):

        if location == "sealdance": #if seal opening fails & trash needs to be cleared -> used at ANY seal
            ### APPROACH
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 3)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)

        ################
        # CLEAR CS TRASH
        ################

        elif location == "rof_01": #node 603 - outside CS in ROF
            ### APPROACH ###
            if not self._pather.traverse_nodes([603], self, timeout=3): return False #calibrate after static path
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([603], self): return False #calibrate after looting


        elif location == "rof_02": #node 604 - inside ROF
            ### APPROACH ###
            if not self._pather.traverse_nodes([604], self, timeout=3): return False  #threshold=0.8 (ex 601)
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)

        elif location == "entrance_hall_01": ##static_path "diablo_entrance_hall_1", node 677, CS Entrance Hall1
            ### APPROACH ###
            self._pather.traverse_nodes_fixed("diablo_entrance_hall_1", self) # 604 -> 671 Hall1
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)

        elif location == "entrance_hall_02":  #node 670,671, CS Entrance Hall1, CS Entrance Hall1
            ### APPROACH ###
            if not self._pather.traverse_nodes([670], self): return False # pull top mobs 672 to bottom 670
            self._pather.traverse_nodes_fixed("diablo_entrance_1_670_672", self) # 604 -> 671 Hall1
            if not self._pather.traverse_nodes([670], self): return False # pull top mobs 672 to bottom 670
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)            #Move to Layout Check
            if not self._pather.traverse_nodes([671], self): return False # calibrate before static path
            self._pather.traverse_nodes_fixed("diablo_entrance_hall_2", self) # 671 -> LC Hall2



        # TRASH LAYOUT A

        elif location == "entrance1_01": #static_path "diablo_entrance_hall_2", Hall1 (before layout check)
            ### APPROACH ###
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([673], self): return False # , timeout=3): # Re-adjust itself and continues to attack

        elif location == "entrance1_02": #node 673
            ### APPROACH ###
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            self._pather.traverse_nodes_fixed("diablo_entrance_1_1", self) # Moves char to postion close to node 674 continues to attack
            if not self._pather.traverse_nodes([674], self): return False#, timeout=3)

        elif location == "entrance1_03": #node 674
            ### APPROACH ###
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([675], self): return False#, timeout=3) # Re-adjust itself
            self._pather.traverse_nodes_fixed("diablo_entrance_1_1", self) #static path to get to be able to spot 676
            if not self._pather.traverse_nodes([676], self): return False#, timeout=3)

        elif location == "entrance1_04": #node 676- Hall3
            ### APPROACH ###
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)

        # TRASH LAYOUT B

        elif location == "entrance2_01": #static_path "diablo_entrance_hall_2"
            ### APPROACH ###
                       ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)

        elif location == "entrance2_02": #node 682
            ### APPROACH ###
            #if not self._pather.traverse_nodes([682], self): return False # , timeout=3):
            if self._skill_hotkeys["conviction"]: keyboard.send(self._skill_hotkeys["conviction"]) #conviction needs to be on for mob_detection
            if (targets := get_visible_targets()):
                nearest_mob_pos_abs = convert_screen_to_abs(targets[0].center)
                print (nearest_mob_pos_abs)
                for _ in range(int(Config().char["atk_len_cs_trashmobs"])*2):
                    self._cast_foh(nearest_mob_pos_abs, spray=11)
                    self._cast_holy_bolt(nearest_mob_pos_abs, spray=80, time_in_s=int(Config().char["atk_len_cs_trashmobs"])*2)
                wait(self._cast_duration, self._cast_duration + 0.2)
                if self._skill_hotkeys["cleansing"]:
                    keyboard.send(self._skill_hotkeys["cleansing"])
                    wait(0.1, 0.2)
                if self._skill_hotkeys["redemption"]:
                    keyboard.send(self._skill_hotkeys["redemption"])
                    wait(0.3, 0.6)
                ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)

        elif location == "entrance2_03": #node 683
            ### APPROACH ###
            #if not self._pather.traverse_nodes([682], self): return False # , timeout=3):
            #self._pather.traverse_nodes_fixed("diablo_entrance2_1", self)
            #if not self._pather.traverse_nodes([683], self): return False # , timeout=3):
            self._pather.traverse_nodes_fixed("diablo_trash_b_hall2_605_top1", self) #pull mobs from top
            wait (0.2, 0.5)
            self._pather.traverse_nodes_fixed("diablo_trash_b_hall2_605_top2", self) #pull mobs from top
            if not self._pather.traverse_nodes([605], self): return False#, timeout=3)
                       ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)

        elif location == "entrance2_04": #node 686 - Hall3
            ### APPROACH ###
            if not self._pather.traverse_nodes([605], self): return False#, timeout=3)
            #if not self._pather.traverse_nodes([683,684], self): return False#, timeout=3)
            #self._pather.traverse_nodes_fixed("diablo_entrance2_2", self)
            #if not self._pather.traverse_nodes([685,686], self): return False#, timeout=3)
            self._pather.traverse_nodes_fixed("diablo_trash_b_hall2_605_hall3", self)
            if not self._pather.traverse_nodes([609], self): return False#, timeout=3)
            self._pather.traverse_nodes_fixed("diablo_trash_b_hall3_pull_609", self)
            if not self._pather.traverse_nodes([609], self): return False#, timeout=3)
                       ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([609], self): return False#, timeout=3)
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([609], self): return False#, timeout=3)

        ####################
        # PENT TRASH TO SEAL
        ####################

        elif location == "dia_trash_a": #trash before between Pentagramm and Seal A Layoutcheck
            ### APPROACH ###
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
        elif location == "dia_trash_b": #trash before between Pentagramm and Seal B Layoutcheck
            ### APPROACH ###
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
        elif location == "dia_trash_c": ##trash before between Pentagramm and Seal C Layoutcheck
            ### APPROACH ###
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
        ###############
        # LAYOUT CHECKS
        ###############

        elif location == "layoutcheck_a": #layout check seal A, node 619 A1-L, node 620 A2-Y
            ### APPROACH ###
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)            #Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "layoutcheck_b": #layout check seal B, node 634 B1-S, node 649 B2-U
            ### APPROACH ###
                ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
        elif location == "layoutcheck_c": #layout check seal C, node 656 C1-F, node 664 C2-G
            ### APPROACH ###
            ## ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
        ##################
        # PENT BEFORE SEAL
        ##################

        elif location == "pent_before_a": #node 602, pentagram, before CTA buff & depature to layout check - not needed when trash is skipped & seals run in right order
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "pent_before_b": #node 602, pentagram, before CTA buff & depature to layout check
            ### APPROACH ###
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
        elif location == "pent_before_c": #node 602, pentagram, before CTA buff & depature to layout check
            ### APPROACH ###
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
        ###########
        # SEAL A1-L
        ###########

        elif location == "A1-L_01":  #node 611 seal layout A1-L: safe_dist
            ### APPROACH ###
            if not self._pather.traverse_nodes([611], self): return False # , timeout=3):
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            # we loot at boss

        elif location == "A1-L_02":  #node 612 seal layout A1-L: center
            ### APPROACH ###
            if not self._pather.traverse_nodes([612], self): return False # , timeout=3):
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            # we loot at boss

        elif location == "A1-L_03":  #node 613 seal layout A1-L: fake_seal
            ### APPROACH ###
            if not self._pather.traverse_nodes([613], self): return False # , timeout=3):
                       ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)

        elif location == "A1-L_seal1":  #node 613 seal layout A1-L: fake_seal
            ### APPROACH ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([614], self): return False
            ### ATTACK ###
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.3, 0.6)
            ### LOOT ###
            # we loot at boss

        elif location == "A1-L_seal2":  #node 614 seal layout A1-L: boss_seal
            ### APPROACH ###
            if not self._pather.traverse_nodes([613, 615], self): return False # , timeout=3):
            ### ATTACK ###
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.3, 0.6)
            ### LOOT ###
            # we loot at boss

        ###########
        # SEAL A2-Y
        ###########

        elif location == "A2-Y_01":  #node 622 seal layout A2-Y: safe_dist
            ### APPROACH ###
            if not self._pather.traverse_nodes_fixed("dia_a2y_hop_622", self): return False
            Logger.debug("A2-Y: Hop!")
            #if not self._pather.traverse_nodes([622], self): return False # , timeout=3):
            if not self._pather.traverse_nodes([622], self): return False
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            # we loot at boss

        elif location == "A2-Y_02":  #node 623 seal layout A2-Y: center
            ### APPROACH ###
            # if not self._pather.traverse_nodes([623,624], self): return False #
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            # we loot at boss

        elif location == "A2-Y_03": #skipped
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "A2-Y_seal1":  #node 625 seal layout A2-Y: fake seal
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            if not self._pather.traverse_nodes([625], self): return False # , timeout=3):
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.3, 0.6)

        elif location == "A2-Y_seal2":
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            self._pather.traverse_nodes_fixed("dia_a2y_sealfake_sealboss", self) #instead of traversing node 626 which causes issues
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.3, 0.6)

        ###########
        # SEAL B1-S
        ###########

        elif location == "B1-S_01":
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "B1-S_02":
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "B1-S_03":
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "B1-S_seal2": #B only has 1 seal, which is the boss seal = seal2
            ### APPROACH ###
            if not self._pather.traverse_nodes([634], self): return False # , timeout=3):
            ### ATTACK ###
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.3, 0.6)
            ### LOOT ###


        ###########
        # SEAL B2-U
        ###########

        elif location == "B2-U_01":
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "B2-U_02":
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "B2-U_03":
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "B2-U_seal2": #B only has 1 seal, which is the boss seal = seal2
            ### APPROACH ###
            self._pather.traverse_nodes_fixed("dia_b2u_bold_seal", self)
            if not self._pather.traverse_nodes([644], self): return False # , timeout=3):
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.3, 0.6)


        ###########
        # SEAL C1-F
        ###########

        elif location == "C1-F_01":
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "C1-F_02":
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "C1-F_03":
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "C1-F_seal1":
            ### APPROACH ###
            wait(0.1,0.3)
            self._pather.traverse_nodes_fixed("dia_c1f_hop_fakeseal", self)
            wait(0.1,0.3)
            if not self._pather.traverse_nodes([655], self): return False # , timeout=3):
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([655], self): return False # , timeout=3):
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.3, 0.6)

        elif location == "C1-F_seal2":
            ### APPROACH ###
            self._pather.traverse_nodes_fixed("dia_c1f_654_651", self)
            if not self._pather.traverse_nodes([652], self): return False # , timeout=3):
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([652], self): return False # , timeout=3):
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.3, 0.6)

        ###########
        # SEAL C2-G
        ###########

        elif location == "C2-G_01": #skipped
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "C2-G_02": #skipped
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "C2-G_03": #skipped
            ### APPROACH ###
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")

        elif location == "C2-G_seal1":
            ### APPROACH ###
            #if not self._pather.traverse_nodes([663, 662], self): return False # , timeout=3): #caused 7% failed runs, replaced by static path.
            self._pather.traverse_nodes_fixed("dia_c2g_lc_661", self)
            ### ATTACK ###
            ### LOOT ###
            # we loot at boss
            Logger.debug("No attack choreography available in hammerdin.py for this node " + location + " - skipping to shorten run.")


        elif location == "C2-G_seal2":
            ### APPROACH ###
            # Killing infector here, because for C2G its the only seal where a bossfight occures BETWEEN opening seals
            seal_layout="C2-G"
            self._pather.traverse_nodes_fixed("dia_c2g_663", self)
            ### ATTACK ###
            Logger.debug(seal_layout + ": Attacking Infector at position 1/1")
            self.cs_trash_atk_seq("atk_len_diablo_infector", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([664, 665], self): return False # , timeout=3):

        else:
            ### APPROACH ###
            Logger.warning("I have no location argument given for kill_cs_trash(" + location + "), should not happen. Throwing some random hammers")
            ### ATTACK ###
            self.cs_trash_atk_seq("atk_len_cs_trashmobs", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            return True


    def kill_vizier(self, seal_layout:str) -> bool:
        if seal_layout == "A1-L":
            ### APPROACH ###
            if not self._pather.traverse_nodes([612], self): return False # , timeout=3):
            ### ATTACK ###
            Logger.debug(seal_layout + ": Attacking Vizier at position 1/2")
            self.cs_trash_atk_seq("atk_len_diablo_vizier", 1)
            Logger.debug(seal_layout + ": Attacking Vizier at position 2/2")
            self._pather.traverse_nodes([611], self, timeout=3)
            self.cs_trash_atk_seq("atk_len_diablo_vizier", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([612], self): return False # , timeout=3):
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.3, 0.6)
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([612], self): return False # , timeout=3): # recalibrate after loot

        elif seal_layout == "A2-Y":
            ### APPROACH ###
            if not self._pather.traverse_nodes([627, 622], self): return False # , timeout=3):
            ### ATTACK ###
            Logger.debug(seal_layout + ": Attacking Vizier at position 1/2")
            self.cs_trash_atk_seq("atk_len_diablo_vizier", 1)
            Logger.debug(seal_layout + ": Attacking Vizier at position 2/2")
            self._pather.traverse_nodes([623], self, timeout=3)
            self.cs_trash_atk_seq("atk_len_diablo_vizier", 1)
            Logger.debug(seal_layout + ": Attacking Vizier at position 3/3")
            if not self._pather.traverse_nodes([624], self): return False
            self.cs_trash_atk_seq("atk_len_diablo_vizier", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([624], self): return False
            if not self._pather.traverse_nodes_fixed("dia_a2y_hop_622", self): return False
            Logger.debug(seal_layout + ": Hop!")
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.3, 0.6)
            if not self._pather.traverse_nodes([622], self): return False #, timeout=3):
            if self._skill_hotkeys["redemption"]:
                keyboard.send(self._skill_hotkeys["redemption"])
                wait(0.3, 0.6)
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([622], self): return False # , timeout=3): #recalibrate after loot

        else:
            Logger.warning(seal_layout + ": Invalid location for kill_deseis("+ seal_layout +"), should not happen.")
            return False
        return True

### STOP HERE ###

    def kill_deseis(self, seal_layout:str) -> bool:
        if seal_layout == "B1-S":
            ### APPROACH ###
            self._pather.traverse_nodes_fixed("dia_b1s_seal_deseis", self) # quite aggressive path, but has high possibility of directly killing De Seis with first hammers, for 50% of his spawn locations
            nodes1 = [632]
            nodes2 = [631]
            nodes3 = [632]
            ### ATTACK ###
            Logger.debug(seal_layout + ": Attacking De Seis at position 1/4")
            self.cs_trash_atk_seq("atk_len_diablo_deseis", 1)
            Logger.debug(seal_layout + ": Attacking De Seis at position 2/4")
            self._pather.traverse_nodes(nodes1, self, timeout=3)
            self.cs_trash_atk_seq("atk_len_diablo_deseis", 1)
            Logger.debug(seal_layout + ": Attacking De Seis at position 3/4")
            self._pather.traverse_nodes(nodes2, self, timeout=3)
            self.cs_trash_atk_seq("atk_len_diablo_deseis", 1)
            Logger.debug(seal_layout + ": Attacking De Seis at position 4/4")
            self._pather.traverse_nodes(nodes3, self, timeout=3)
            self.cs_trash_atk_seq("atk_len_diablo_deseis", 1)
            wait(2.5, 3.5) # to keep redemption on for a couple of seconds before the next teleport to have more corpses cleared & increase chance to find next template
            Logger.debug(seal_layout + ": Waiting with Redemption active to clear more corpses.")
            #if Config().general["info_screenshots"]: cv2.imwrite(f"./info_screenshots/info_check_deseis_dead" + seal_layout + "_" + time.strftime("%Y%m%d_%H%M%S") + ".png", grab())
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)

        elif seal_layout == "B2-U":
            ### APPROACH ###
            self._pather.traverse_nodes_fixed("dia_b2u_644_646", self) # We try to breaking line of sight, sometimes makes De Seis walk into the hammercloud. A better attack sequence here could make sense.
            #self._pather.traverse_nodes_fixed("dia_b2u_seal_deseis", self) # We try to breaking line of sight, sometimes makes De Seis walk into the hammercloud. A better attack sequence here could make sense.
            nodes1 = [640]
            nodes2 = [646]
            nodes3 = [641]
            ### ATTACK ###
            Logger.debug(seal_layout + ": Attacking De Seis at position 1/4")
            self.cs_trash_atk_seq("atk_len_diablo_deseis", 1)
            Logger.debug(seal_layout + ": Attacking De Seis at position 2/4")
            self._pather.traverse_nodes(nodes1, self, timeout=3)
            self.cs_trash_atk_seq("atk_len_diablo_deseis", 1)
            Logger.debug(seal_layout + ": Attacking De Seis at position 3/4")
            self._pather.traverse_nodes(nodes2, self, timeout=3)
            self.cs_trash_atk_seq("atk_len_diablo_deseis", 1)
            Logger.debug(seal_layout + ": Attacking De Seis at position 4/4")
            self._pather.traverse_nodes(nodes3, self, timeout=3)
            self.cs_trash_atk_seq("atk_len_diablo_deseis", 1)
            #if Config().general["info_screenshots"]: cv2.imwrite(f"./info_screenshots/info_check_deseis_dead" + seal_layout + "_" + time.strftime("%Y%m%d_%H%M%S") + ".png", grab())
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([641], self): return False # , timeout=3):
            if not self._pather.traverse_nodes([646], self): return False # , timeout=3):
            self._picked_up_items |= self._pickit.pick_up_items(self)
            if not self._pather.traverse_nodes([646], self): return False # , timeout=3):
            if not self._pather.traverse_nodes([640], self): return False # , timeout=3):
            self._picked_up_items |= self._pickit.pick_up_items(self)

        else:
            Logger.warning(seal_layout + ": Invalid location for kill_deseis("+ seal_layout +"), should not happen.")
            return False
        return True



    def kill_infector(self, seal_layout:str) -> bool:
        if seal_layout == "C1-F":
            ### APPROACH ###
            self._pather.traverse_nodes_fixed("dia_c1f_652", self)
            ### ATTACK ###
            Logger.debug(seal_layout + ": Attacking Infector at position 1/1")
            self.cs_trash_atk_seq("atk_len_diablo_infector", 1)
            ### LOOT ###
            self._picked_up_items |= self._pickit.pick_up_items(self)

        elif seal_layout == "C2-G":
            # NOT killing infector here, because for C2G its the only seal where a bossfight occures BETWEEN opening seals his attack sequence can be found in C2-G_seal2
            Logger.debug(seal_layout + ": No need for attacking Infector at position 1/1 - he was killed during clearing the seal")

        else:
            Logger.warning(seal_layout + ": Invalid location for kill_infector("+ seal_layout +"), should not happen.")
            return False
        return True


    #no aura effect on dia. not good for mob detection
    def kill_diablo(self) -> bool:
        ### APPROACH ###
        ### ATTACK ###
        pos_m = convert_abs_to_monitor((0, 0))
        mouse.move(*pos_m, randomize=80, delay_factor=[0.5, 0.7])
        Logger.debug("Attacking Diablo at position 1/1")
        atk_len_factor = 1
        atk_len = "atk_len_diablo"
        atk_len_dur = int(Config().char[atk_len])*atk_len_factor
        if self._skill_hotkeys["conviction"]: keyboard.send(self._skill_hotkeys["conviction"]) #conviction needs to be on for mob_detection
        nearest_mob_pos_abs = [100,-100] #hardcoded dia pos.
        Logger.debug("Mob found at " + str(nearest_mob_pos_abs) + '\033[96m'+" fisting him now "+ str(atk_len_dur) + "times!" +'\033[0m')
        for _ in range(atk_len_dur):
            self._cast_foh(nearest_mob_pos_abs, spray=11)
            Logger.debug("Mob found at " + str(nearest_mob_pos_abs) + '\033[93m'+" bolting him now "+ str(atk_len_dur) + "seconds!" +'\033[0m')
            self._cast_holy_bolt(nearest_mob_pos_abs, spray=80, time_in_s=atk_len_dur)
        if self._skill_hotkeys["cleansing"]:
            keyboard.send(self._skill_hotkeys["cleansing"])
        wait(0.1, 0.2) #clear yourself from curses
        if self._skill_hotkeys["redemption"]:
            keyboard.send(self._skill_hotkeys["redemption"])
            wait(0.5, 1.0) #clear area from corpses & heal
        #
        Logger.debug("Lets mobcheck for safety reasons & hope in that second we have posion nova active")
        self.cs_trash_atk_seq("atk_len_diablo", 1)
        ### LOOT ###
        self._picked_up_items |= self._pickit.pick_up_items(self)
        return True

    """
    def kill_diablo(self) -> bool:
        ### APPROACH ###
        ### ATTACK ###
        pos_m = convert_abs_to_monitor((0, 0))
        mouse.move(*pos_m, randomize=80, delay_factor=[0.5, 0.7])
        Logger.debug("Attacking Diablo at position 1/1")
        self._cast_hammers(Config().char["atk_len_diablo"])
        self._cast_hammers(0.8, "redemption")
        self._move_and_attack((60, 30), Config().char["atk_len_diablo"])
        self._cast_hammers(0.8, "redemption")
        self._move_and_attack((-60, -30), Config().char["atk_len_diablo"])
        wait(0.1, 0.15)
        self._cast_hammers(1.2, "redemption")
        ### LOOT ###
        self._picked_up_items |= self._pickit.pick_up_items(self)
        return True
    """