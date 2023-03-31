class Animator:
    def __init__(self, game, animation, speed, loop=False):
        self.game = game
        self.frame_index = 0
        self.animation = animation
        self.animation_len = len(animation)
        self.speed = speed
        self.loop = loop

    def update(self):
        self.frame_index += self.speed

        if self.frame_index >= self.animation_len:
            if self.loop:
                self.frame_index = 0
            else:
                self.done = True

        return self.animation[int(self.frame_index)]