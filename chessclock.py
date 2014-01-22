#!/usr/bin/env python
import pygame
pygame.init()

import settings as S


screen = (pygame.display.set_mode(S.resolution, pygame.FULLSCREEN) if S.fullscreen else
          pygame.display.set_mode(S.resolution))
width, height = screen.get_size()
font = pygame.font.Font(None, S.fontsize)

def get_color(color):
    return pygame.color.THECOLORS[color] if isinstance(color, str) else color

def pressed(event, key):
    return event.type == pygame.KEYDOWN and event.key == key

class ChessClock:
    def __init__(self):
        self.leftside_time = self.rightside_time = S.time_in_seconds * 1000
        # ^ In millisecs

        self.leftsides_turn = {"left": True, "right": False}[S.startside]
        self.pause = True
        self.clock = pygame.time.Clock()

    def rendertext(self, side, timeleft, active):
        return font.render(S.timeformat(timeleft), True,
                           get_color(S.active_textcolor) if active and not self.pause else
                           get_color(S.textcolor[side]))

    def blit_text(self):
        middle = width/2
    
        for side, time, centerx, active in (
                ("left",  self.leftside_time,  middle/2, self.leftsides_turn),
                ("right", self.rightside_time, middle + middle/2, not self.leftsides_turn)):
            side = self.rendertext(side, time, active)
            screen.blit(side, side.get_rect(centery=height/2, centerx=centerx))

    def timeleft(self):
        return not any(int(t/1000) <= 0 for t in (self.leftside_time, self.rightside_time))

    def mainloop(self):
        while True:
            dt = self.clock.tick(25)
            if not self.pause:
                if not self.timeleft():
                    self.pause = True
                else:
                    self.leftside_time, self.rightside_time = (
                        (self.leftside_time - dt, self.rightside_time)
                        if self.leftsides_turn else
                        (self.leftside_time, self.rightside_time - dt)
                    )


            for event in pygame.event.get():
                if event.type == pygame.QUIT or pressed(event, pygame.K_ESCAPE):
                    return False
                elif pressed(event, pygame.K_r):
                    return True
                elif pressed(event, pygame.K_p):
                    self.pause = not self.pause
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause and self.timeleft():
                        self.pause = False
                    else:
                        self.leftsides_turn = not self.leftsides_turn

            screen.fill(get_color(S.bgcolor["left"]),  rect=pygame.Rect(0,       0, width/2, height))
            screen.fill(get_color(S.bgcolor["right"]), rect=pygame.Rect(width/2, 0, width/2, height))
            self.blit_text()
            pygame.display.flip()

if __name__ == "__main__":
    while ChessClock().mainloop():
        pass
