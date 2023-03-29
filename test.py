import pygame as pg


def main():
    pg.init()
    screen = pg.display.set_mode((1500,800))
    clock = pg.time.Clock()
    FPS = 60

    while True:

        screen.fill("black")

        wedge = pg.draw.polygon(screen, "red", [(572, 30), (572, 80), (0, 80)],)
        # screen.blit(screen, (500,0), pg.draw.polygon(screen, "red", [(572, 80), (572, 30), (0, 80)]))
        
        HUD = pg.image.load("./assets/ui/HUD/In-Battle-HUD2.png")
        scaled_HUD = pg.transform.scale(HUD, (1500,  800/3))
        # screen.blit(scaled_HUD, (0,-55))

        # pg.draw.rect(screen, "blue", wedge)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()


        pg.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()