from settings import FPS

class HitStunFrames:
    def __init__(self, clock, stun_frames=5):
        self.clock = clock
        self.frame = 0
        self.stun_frames = stun_frames
        while self.frame <= self.stun_frames:
            self.update()
    
    def update(self):
        self.frame += 1
        self.clock.tick(FPS)
