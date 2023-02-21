import time
import random
import kivy.uix.image
from functools import partial


def spawn_boss(self, screen_num):
    curr_screen = self.root.screens[screen_num]
    spawn_pos = (curr_screen.size[0],
                 curr_screen.size[1] * (0.5 - curr_screen.boss_props['height'] / 2))
    finish_pos = (0,
                  curr_screen.size[1] * (0.5 - curr_screen.boss_props['height'] / 2))
    boss = kivy.uix.image.Image(source=f"graphics/entities/boss_{screen_num}.png",
                                size_hint=(curr_screen.boss_props['width'], curr_screen.boss_props['height']),
                                pos=spawn_pos, allow_stretch=True)
    curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(boss, index=-1)
    time_stamp = str(time.time())
    curr_screen.bosses_ids['boss_' + time_stamp] = {'image': boss,
                                                    'hit_points': curr_screen.boss_props['hit_points'],
                                                    'finish_pos': finish_pos,
                                                    'speed_x': curr_screen.boss_props['speed_x']
                                                    }


def update_bosses(self, screen_num, dt):
    curr_screen = self.root.screens[screen_num]
    for boss_key, boss in curr_screen.bosses_ids.items():
        boss['image'].x = boss['image'].x + boss['speed_x'] * dt
        self.check_boss_collision(boss['image'], screen_num)
        if boss['image'].x <= 0. - boss['image'].width / 4:
            self.boss_arrives_animation(screen_num)


def boss_arrives_animation(self, screen_num):
    # Triggered when boss arrives to the finish line
    curr_screen = self.root.screens[screen_num]
    curr_screen.character_dict['damage_received'] = curr_screen.character_dict['hit_points']
    self.adjust_character_life_bar(screen_num)
    self.kill_character(screen_num)


def boss_defeat_animation_start(self, boss, screen_num):
    # Triggered when boss is defeated
    curr_screen = self.root.screens[screen_num]
    new_pos = (curr_screen.size[0],
               curr_screen.size[1] * 0.5)
    boss_defeat_anim = kivy.animation.Animation(pos=new_pos,
                                                size_hint=(0.1, 0.1),
                                                duration=0.6,
                                                transition='in_out_elastic')
    boss_defeat_anim.bind(on_complete=partial(self.boss_defeat_animation_finish, screen_num))
    boss_defeat_anim.start(boss)


def boss_defeat_animation_finish(self, screen_num, *args):
    boss = args[1]
    curr_screen = self.root.screens[screen_num]
    curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(boss)


def check_boss_collision(self, boss_image, screen_num):
    curr_screen = self.root.screens[screen_num]
    character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
    gap_x = curr_screen.width * curr_screen.boss_props['width'] / 4
    gap_y = curr_screen.height * curr_screen.boss_props['height'] / 2
    if boss_image.collide_widget(character_image) and \
            abs(boss_image.center[0] - character_image.center[0]) <= gap_x and \
            abs(boss_image.center[1] - character_image.center[1]) <= gap_y:
        curr_screen.character_dict['damage_received'] += curr_screen.boss_props['damage']
        if curr_screen.character_dict['damage_received'] > curr_screen.character_dict['hit_points']:
            curr_screen.character_dict['damage_received'] = curr_screen.character_dict['hit_points']
            self.adjust_character_life_bar(screen_num)
        if curr_screen.character_dict['damage_received'] == curr_screen.character_dict['hit_points']:
            self.kill_character(screen_num)
