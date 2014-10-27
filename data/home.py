#!/bin/python3

import pygame as pg
from . import cache
from . import constants as ct
from . import tools as t

class Home(t.State):
    def __init__(self):
        super().__init__()
        self.name = 'home'
        self.buttons, self.images = list(), list()
        self.bg = None
        self.__arrow_index = 0
        self.allow_input = False
        self.next = 'main_menu'

    def start(self, screen):
        self.setup_background()
        self.setup_buttons(screen)
        self.setup_images(screen)

    def setup_background(self):
        bg_img = cache._cache.images[self.name]
        self.bg = t.Background(bg_img)
        self.bg.resize(*ct.SCREEN_SIZE)

    def setup_images(self, screen):
        logo = t.Image(cache._cache.images['logo'])
        logo.setup_effect(ct.EFFECT['moveup50'], ct.EFFECT['shake50'])
        logo.center(screen)
        sublogo = t.Image(t.text_to_surface(ct.AUTHOR, 'joystix', 10, ct.WHITE_RGB))
        sublogo.setup_effect(ct.EFFECT['fadein100'], ct.EFFECT['wait50'])
        sublogo.center(screen, 0, 35)
        self.images.append(logo)
        self.images.append(sublogo)

    def setup_buttons(self, screen):
        text1 = 'Press Any Key'
        DO_START = lambda : setattr(self, 'done', True)
        button1 = t.Button(text1, DO_START)
        button1.setup_effect(ct.EFFECT['blink'])
        button1.center(screen, 0, 220)
        self.buttons.append(button1)

    def check_for_input(self, keys):
        if self.allow_input:
            if keys[pg.K_UP]:
                self.arrow_index -= 1
                if self.arrow_index == 0:
                    self.arrow_index = 2
            elif keys[pg.K_DOWN]:
                self.arrow_index += 1
                if self.arrow_index == 3:
                    self.arrow_index = 0
            elif keys[pg.K_RETURN] or keys[pg.K_SPACE]:
                self.do_action(self.arrow_index)
        self.allow_input = False
        if (not keys[pg.K_DOWN]
            and not keys[pg.K_UP]
            and not keys[pg.K_RETURN]
            and not keys[pg.K_SPACE]):
                self.allow_input = True

    def do_action(self, index):
        if index-1 in range(0, t.Button.INDEX+1):
            self.buttons[index-1].callback()

    def update(self, window, keys):
        self.check_for_input(keys)
        window.blit(self.bg.surface, (0,0))
        for item in self.buttons+self.images:
            item.update()
            if item.display:
                window.blit(item.surface, item.rect)

    @property
    def arrow_index(self):
        return self.__arrow_index

    @arrow_index.setter
    def arrow_index(self, value):
        """On cap l'index du curseur au nombre de choix"""
        if value in range(0,4):
            self.__arrow_index = value