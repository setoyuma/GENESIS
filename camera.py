import pygame

class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.background_width, self.background_height = width*2, height*2

    def update(self, player1, player2, edge_threshold=100, lerp_speed=0.1):
        # averages player positions together
        mid_x = (player1.rect.x + player2.rect.x) // 2
        mid_y = (player1.rect.y + player2.rect.y) // 2

        target_x = self.rect.x
        target_y = self.rect.y

        if abs(mid_x - self.rect.x - self.width // 2) > edge_threshold:
            target_x = mid_x - self.width // 2

        if abs(mid_y - self.rect.y - self.height // 2) > edge_threshold:
            target_y = mid_y - self.height // 2

        # Interpolate the camera's position for smooth movement
        self.rect.x += int((target_x - self.rect.x) * lerp_speed)
        self.rect.y += int((target_y - self.rect.y) * lerp_speed)

        # Keep the camera within the bounds of the background
        self.rect.x = max(0, min(self.rect.x, self.background_width - self.width))
        self.rect.y = max(0, min(self.rect.y, self.background_height - self.height))
