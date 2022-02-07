x, y = (0, 0)
pos_m = self._screen.convert_screen_to_monitor(template_match.position)
x, y = pos_m
pos_m = x * 1.2, y * 1.2
self._char.move(pos_m, force_move=True)





masked_image = cut_roi(img, [-485, 285, 80, 150], "invert")