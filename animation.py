class Animator:
    def __init__(self, game, animation, frame_duration, loop=False):
        self.game = game
        self.animation = animation
        self.frame_duration = frame_duration
        self.current_time = 0
        self.frame_index = 0
        self.loop = loop
        self.done = False

    def update(self, dt):
        # add time in ms since last frame
        self.current_time += dt

        # when cumulative time reaches the frame_duration
        if self.current_time > self.frame_duration:

            # add 1 to the frame_index and mod it with the number of frames.
            # this uses the remainder to loop the frame_index repeatedly
            self.frame_index = (self.frame_index + 1) % len(self.animation)

            # reset the cumulative time for the next frame
            self.current_time = 0

            # set the flag for an animation that should not repeat
            if not self.loop:
                self.done = True

        # return the current frame of the animation list
        return self.animation[self.frame_index]