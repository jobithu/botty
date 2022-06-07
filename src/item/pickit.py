import time
import keyboard
import cv2
from operator import itemgetter
from ui_manager import ScreenObjects, is_visible
from utils.custom_mouse import mouse
from config import Config
from logger import Logger
from screen import grab, convert_abs_to_monitor, convert_screen_to_monitor
from utils.misc import wait
from item import ItemFinder, Item
from char import IChar
import numpy as np
from inventory import consumables
from template_finder import TemplateFinder
import parse

cv2.setUseOptimized(True)

class PickIt:
    def __init__(self, item_finder: ItemFinder):
        self._item_finder = item_finder
        self._last_closest_item: Item = None

    def check_items(self, old_list, item_list):
        if old_list is not None:
                for old_item in item_list:
                    for item in item_list:
                        if old_item.roi == item.roi:
                            return True
                return False
        return True

    def checkdiff(self, img, current):
        template_match = TemplateFinder().search(current.template.data, img, roi=current.roi, threshold=0.84, use_grayscale=True,)
        #template_match2 = TemplateFinder().search(current.template.data, img, roi=current.roi, threshold=0.1, doubleCheck=False, use_grayscale=True, hyperoptimize = False)
        #template_match = TemplateFinder().search(item.template.data, img, threshold=0.97, doubleCheck=False, use_grayscale=True, hyperoptimize = False)
        #print(f"template ret: {template_match2.score}")
        if template_match.valid:
            return True
        else:
            return False    


    def pick_up_items(self, char: IChar, fastPickit = None) -> bool:
        """
        Pick up all items with specified char
        :param char: The character used to pick up the item
        :return: Bool if any items were picked up or not. (Does not account for picking up scrolls and pots)
        """
        found_nothing = 0
        found_items = False
        pick_timeout = 32
        if fastPickit is not None:
            pick_timeout=5
        keyboard.send(Config().char["show_items"])
        #time.sleep(1.0) # sleep needed here to give d2r time to display items on screen on keypress
        time.sleep(0.1) # sleep needed here to give d2r time to display items on screen on keypress
        #Creating a screenshot of the current loot
        if Config().general["loot_screenshots"]:
            img = grab()
            cv2.imwrite("./loot_screenshots/info_debug_drop_" + time.strftime("%Y%m%d_%H%M%S") + ".png", img)
            Logger.debug("Took a screenshot of current loot")
        start = prev_cast_start = time.time()
        timeout = False
        picked_up_items = []
        skip_items = []
        curr_item_to_pick: Item = None
        second_closest: Item = None
        same_item_timer = None
        did_force_move = False
        done_ocr=False

        old_list = None
        if char is not None:
            if hasattr(char, "idle_aura") and callable(getattr(char, "idle_aura")): char.idle_aura()
        while not timeout:
            start = time.time()
            if (time.time() - start) > pick_timeout:
                timeout = True
                Logger.warning("Got stuck during pickit, skipping it this time...")
                break
            img = grab()
            #img2 = img
            #benchtime = time.time()
            #checkdif = self.checkdiff(img, old_list, curr_item_to_pick)
            #print(f"check diff: {checkdif} time: {time.time() - benchtime}")
            #if not self.checkdiff(img, old_list, curr_item_to_pick):
            if second_closest is None or not self.checkdiff(img, second_closest):
                item_list = self._item_finder.search(img)
            else:
                print("managed to sneak in a pickit skip >:D")
            #for item in item_list:
            #    print(f"{item.name} on ground, picking.")
            #item_list2 = self._item_finder.search2(img2)
            #print(f"DEBUG: Item list lengths, list1={len(item_list)} -- list2: {len(item_list2)}")
            #if not self.check_items(old_list, item_list):
            #    print("something moved, sleeping")
            #    #time.sleep(0.1)
            #    continue
            if item_list: old_list = item_list                
            """
            diffimg = grab()
            diff = cv2.absdiff(img, diffimg)
            diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
            score = (float(np.sum(mask)) / mask.size) * (1/255.0)
            if score > 0.35:
                Logger.debug(f"character still moving.. try again diff: {score}")
                wait(0.04, 0.09)
                continue
            """
            if Config().advanced_options["ocr_during_pickit"] and not done_ocr:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                for cnt, item in enumerate(item_list):
                    for cnt2, x in enumerate(item.ocr_result['word_confidences']):
                        found_low_confidence = False
                        if x <= 88:
                            try:
                                Logger.debug(f"Low confidence word #{cnt2}: {item.ocr_result['original_text'].split()[cnt2]} -> {item.ocr_result['text'].split()[cnt2]}, Conf: {x}, save screenshot")
                                found_low_confidence = True
                            except: pass
                        if found_low_confidence and Config().general["loot_screenshots"]:
                            cv2.imwrite(f"./loot_screenshots/ocr_drop_{timestamp}_{cnt}_o.png", item.ocr_result['original_img'])
                            cv2.imwrite(f"./loot_screenshots/ocr_drop_{timestamp}_{cnt}_n.png", item.ocr_result['processed_img'])
                            with open(f"./loot_screenshots/ocr_drop_{timestamp}_{cnt}_o.gt.txt", 'w') as f:
                                f.write(item.ocr_result['text'])
                done_ocr = True

            # Check if we need to pick up any consumables
            needs = consumables.get_needs()

            if needs["mana"] <= 0:
                item_list = [x for x in item_list if "mana_potion" not in x.name]
            if needs["health"] <= 0:
                item_list = [x for x in item_list if "healing_potion" not in x.name]
            if needs["rejuv"] <= 0:
                item_list = [x for x in item_list if "rejuvenation_potion" not in x.name]
            if needs["tp"] <= 0:
                item_list = [x for x in item_list if "scroll_tp" not in x.name]
            if needs["id"] <= 0:
                item_list = [x for x in item_list if "scroll_id" not in x.name]
            if needs["key"] <= 0:
                item_list = [x for x in item_list if "misc_key" != x.name]

            # filter out gold less than desired quantity
            if (min_gold := Config().char['min_gold_to_pick']):
                for item in item_list[:]:
                    if "misc_gold" == item.name:
                        try:
                            ocr_gold = int(parse.search("{:d} GOLD", item.ocr_result.text).fixed[0])
                        except:
                            ocr_gold = 0
                        if ocr_gold < min_gold:
                            item_list.remove(item)

            if len(item_list) == 0:
                # if twice no item was found, break
                found_nothing += 1
                if found_nothing > 0:
                    break
                else:
                    # Maybe we need to move cursor to another position to avoid highlighting items
                    pos_m = convert_abs_to_monitor((0, 0))
                    mouse.move(*pos_m, randomize=[90, 160])
                    time.sleep(0.03)
            else:
                found_nothing = 0
                item_list.sort(key=itemgetter('dist'))
                closest_item = next((obj for obj in item_list if not any(map(obj["name"].__contains__, ["misc_gold", "misc_scroll", "misc_key"]))), None)
                if not closest_item:
                    closest_item = item_list[0]
                    if len(item_list) > 1: second_closest = item_list[1]
                    else: second_closest = None
                else:
                    second_closest = next((obj for obj in item_list if not closest_item and not any(map(obj["name"].__contains__, ["misc_gold", "misc_scroll", "misc_key"]))), None)
                # check if we trying to pickup the same item for a longer period of time
                force_move = False
                if curr_item_to_pick is not None:
                    is_same_item = (curr_item_to_pick.name == closest_item.name and \
                        abs(curr_item_to_pick.dist - closest_item.dist) < 20)
                    if same_item_timer is None or not is_same_item:
                        same_item_timer = time.time()
                        did_force_move = False
                    elif time.time() - same_item_timer > 3 and not did_force_move:
                        force_move = True
                        did_force_move = True
                    elif time.time() - same_item_timer > 5:
                        # backlist this item type for this pickit round
                        Logger.warning(f"Could not pick up: {closest_item.name}. Continue with other items")
                        skip_items.append(closest_item.name)
                curr_item_to_pick = closest_item

                # To avoid endless teleport or telekinesis loop
                force_pick_up = char.capabilities.can_teleport_natively and \
                                self._last_closest_item is not None and \
                                self._last_closest_item.name == closest_item.name and \
                                abs(self._last_closest_item.dist - closest_item.dist) < 20

                x_m, y_m = convert_screen_to_monitor(closest_item.center)
                if not force_move and (closest_item.dist < Config().ui_pos["item_dist"] or force_pick_up):
                    self._last_closest_item = None
                    # no need to stash potions, scrolls, gold, keys
                    if ("potion" not in closest_item.name) and ("misc_scroll" not in closest_item.name) and ("misc_key" != closest_item.name):
                        if ("misc_gold" != closest_item.name):
                            found_items = True
                            if Config().advanced_options["ocr_during_pickit"]:
                                for item in item_list:
                                    Logger.debug(f"OCR DROP: Name: {item.ocr_result['text']}, Conf: {item.ocr_result['word_confidences']}")
                    else:
                        # note: key pickup appears to be random between 1 and 5, but set here at minimum of 1 for now
                        consumables.increment_need(closest_item.name, -1)

                    prev_cast_start = char.pick_up_item((x_m, y_m), item_name=closest_item.name, prev_cast_start=prev_cast_start)
                    if self.checkdiff(grab(), curr_item_to_pick):
                        prev_cast_start = char.pick_up_item((x_m, y_m), item_name=closest_item.name, prev_cast_start=prev_cast_start)
                    else:
                        #time.sleep(0.05)
                        print("still moving, wait")
                        second_closest = None
                    if not char.capabilities.can_teleport_natively:
                        time.sleep(0.2)
                        #time.sleep(0.1)
                    if is_visible(ScreenObjects.Overburdened):
                        found_items = True
                        Logger.warning("Inventory full, terminating pickit!")
                        # TODO: Could think about sth like: Go back to town, stash, come back picking up stuff
                        break
                    else:
                        # send log to discord
                        if found_items and closest_item.name not in picked_up_items:
                            Logger.info(f"Picking up: {closest_item.name} ({closest_item.score*100:.1f}% confidence)")
                        picked_up_items.append(closest_item.name)
                else:
                    char.pre_move()
                    char.move((x_m, y_m), force_move=True)
                    #if not char.capabilities.can_teleport_natively:
                    #    time.sleep(0.3)
                    #time.sleep(0.1)
                    # save closeset item for next time to check potential endless loops of not reaching it or of telekinsis/teleport
                    self._last_closest_item = closest_item

        keyboard.send(Config().char["show_items"])
        return found_items


if __name__ == "__main__":
    import os
    from config import Config
    from char.sorceress import LightSorc
    from char.hammerdin import Hammerdin
    import template_finder
    from pather import Pather
    import keyboard

    keyboard.add_hotkey('f12', lambda: Logger.info('Force Exit (f12)') or os._exit(1))
    keyboard.wait("f11")
    pather = Pather()
    item_finder = ItemFinder()
    char = Hammerdin(Config().hammerdin, Config().char, pather)
    pickit = PickIt(item_finder)
    print(pickit.pick_up_items(char))
