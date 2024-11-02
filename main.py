import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

import time

class Game:
    def __init__(self, logfile):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        self.logfile = logfile
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self, None)
        self.object_handler = ObjectHandler(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self, self.object_handler)
        self.player.raycast = self.raycasting
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.logfile.write(str(self.raycasting.ray_casting_for_perception_res) + "\n")
        self.logfile.write(str(self.player.health) + "\n")
        self.logfile.write(str(self.player.rel) + "\n")
        keys = pg.key.get_pressed()
        self.logfile.write(str(8*keys[pg.K_w] + 4*keys[pg.K_a] + 2*keys[pg.K_s] + keys[pg.K_d]) + "\n")
        self.logfile.write(str(int(self.player.shot)) + "\n")
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = min(16, self.clock.tick(FPS))
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def update_auto(self, move_keys, mouse_rel, shot):
        self.player.movement_auto(move_keys)
        self.player.mouse_control_auto(mouse_rel)
        self.player.single_fire_event_auto(shot)
        self.player.recover_health()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        return (self.raycasting.ray_casting_for_perception_res, self.player.health)

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    with open(str(time.time()), 'w', encoding='utf8') as f:
        game = Game(f)
        game.run()
