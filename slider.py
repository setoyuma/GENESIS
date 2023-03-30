import pygame as pg

class Slider:
    def __init__(self, x, y, w, h):
        self.circle_x = x
        self.volume = 0
        self.sliderRect = pg.Rect(x, y, w, h)

    def draw(self, screen):
        pg.draw.rect(screen, (255, 255, 255), self.sliderRect)
        self.circle = pg.draw.circle(screen, (255, 240, 255), (self.circle_x, (self.sliderRect.h / 2 + self.sliderRect.y)), self.sliderRect.h * 1.5)

    def get_volume(self):
        return self.volume

    def set_volume(self, num):
        self.volume = num

    def update_volume(self, x):
        if x < self.sliderRect.x:
            self.volume = 0
        elif x > self.sliderRect.x + self.sliderRect.w:
            self.volume = 100
        else:
            self.volume = int((x - self.sliderRect.x) / float(self.sliderRect.w) * 100)

    def on_slider(self, x, y) -> bool:
        if self.on_slider_hold(x, y) or self.sliderRect.x <= x <= self.sliderRect.x + self.sliderRect.w and self.sliderRect.y <= y <= self.sliderRect.y + self.sliderRect.h:
            # print("mouse on slider")
            return True
        else:
            # print("mouse not on slider")
            return False

    def on_slider_hold(self, x, y):
        if ((x - self.circle_x) * (x - self.circle_x) + (y - (self.sliderRect.y + self.sliderRect.h / 2)) * (y - (self.sliderRect.y + self.sliderRect.h / 2)))\
               <= (self.sliderRect.h * 1.5) * (self.sliderRect.h * 1.5):
            return True
        else:
            return False

    def handle_event(self, screen, x):
        if x < self.sliderRect.x:
            self.circle_x = self.sliderRect.x
        elif x > self.sliderRect.x + self.sliderRect.w:
            self.circle_x = self.sliderRect.x + self.sliderRect.w
        else:
            self.circle_x = x
        self.draw(screen)
        self.update_volume(x)
        print(self.volume)