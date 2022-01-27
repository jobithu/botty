    def explore(self) -> bool:
                if not self._template_finder.search_and_wait(["purple2", "purple"], threshold=0.65).valid:
            dinky = 0
            if dinky < 15:
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(a, b), random.uniform(a, b)))
                self.pre_move()
                self.move(pos_m, force_move=True)
            elif dinky >= 15 and <= 30:
                pos_m = self._screen.convert_abs_to_monitor((random.uniform(a, b), random.uniform(a, b)))
                self.pre_move()
                self.move(pos_m, force_move=True)
            else:
                dinky = 0
        return True




            while not found:
                found = self._template_finder.search_and_wait(templates, threshold=0.82, time_out=0.1).valid
                if not found: 
                    while dinky < 75:
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
                    if score < .15:
                        stuck_count += 1
                        if stuck_count >=5:
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
            if not found:
                #if self._config.general["info_screenshots"]: cv2.imwrite(f"./info_screenshots/failed_pentagram_" + time.strftime("%Y%m%d_%H%M%S") + ".png", self._screen.grab())
                return False


                template_match = template_finder.search(key, img, best_match=True, threshold=0.2, use_grayscale=False)
            if template_match.valid:
                cv2.putText(display_img, str(template_match.name), template_match.position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.circle(display_img, template_match.position, 7, (255, 0, 0), thickness=5)
                x, y = template_match.position
                pos_m = self._screen.convert_abs_to_monitor((x, y))
                self.pre_move()
                self.move(pos_m, force_move=True)
                



        config = Config()
        screen = Screen(config.general["monitor"])
        img = screen.grab()
        display_img = img.copy()
        img = screen.grab()
        template_finder = TemplateFinder(screen)
        template_match = template_finder.search(["PURPENT2", "PURPENT3"], img, best_match=True, threshold=0.8, use_grayscale=False, normalize_monitor=True)
        if template_match.valid:
            cv2.putText(display_img, str(template_match.name), template_match.position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.circle(display_img, template_match.position, 7, (255, 0, 0), thickness=5)
            x, y = template_match.position
            x, y = self._screen.convert_monitor_to_screen((x, y))
            x, y = self._screen.convert_screen_to_abs((x, y))
            pos_m = ((x, y))
            self._char.move(pos_m, force_move=True)
            Logger.debug("not toward the tamplate")