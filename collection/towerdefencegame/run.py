import random
import pygame as pg
from units import *
from window import Window
from route import BlockManager

def main():

    # Initialize Game Groups
    towers = pg.sprite.Group()
    shots = pg.sprite.Group()
    bombs = pg.sprite.GroupSingle()
    aliens = pg.sprite.Group()
    all_sprites = pg.sprite.RenderUpdates()

    # assign default groups to each sprite class
    Tower.containers = towers, all_sprites
    #Player.containers = all_sprites
    AirForce.containers = aliens, all_sprites
    Shot.containers = shots, all_sprites
    Bomb.containers = bombs, all_sprites
    TimedHint.containers = all_sprites
    # Explosion.containers = all_sprites

 # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    wind = Window()
    bManager = BlockManager(wind)

    AirForce.bornBlock = bManager.startBlock

    wind.screen_display()

 # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Create Some Starting Values
    clock = pg.time.Clock()
    pauseFlag = False

    # initialize player starting sprite
    player = Player()
    StringInfo("type 'h' to see available command keys")

 # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    print(30*'=')

    # Run our main loop whilst the player is alive.
    while player.alive():

        # get input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                player.kill()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    pg.display.toggle_fullscreen()
                    wind.screen_display()
                elif event.key == pg.K_d:
                    breakpoint()
                elif event.key == pg.K_p:
                    pauseFlag = not pauseFlag
                elif event.key == pg.K_h:
                    StringInfo("h - help")
                    StringInfo("p - pause")
                    StringInfo("d - debug(break)")
                    StringInfo("f - fullscreen switch")
                    StringInfo("esc - exit")
                    StringInfo("mouseclick - plant tower")
                    StringInfo("up down left right - tank control")
                    StringInfo("space - fire bomb")
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                bManager.click(event.pos)

        if not pauseFlag:
            # clear/erase the last drawn sprites
            all_sprites.clear(wind.screen, wind.back)
            # update all the sprites
            all_sprites.update()

            # Create new alien
            if random.random() > 0.90+len(aliens)/200:
                LandForce()

            # Detect collisions between aliens and players.
            for alien in pg.sprite.spritecollide(player, aliens, 1):
                Explosion(alien)
                Explosion(player)
                StringInfo('life -1', player.rect.move(0, -10).topleft)

            # See if shots hit the aliens.
            for alien in pg.sprite.groupcollide(aliens, shots, 0, 1).keys():
                alien.been_hit()

            aaa = pg.sprite.collide_circle_ratio(3)
            for t, a in pg.sprite.groupcollide(towers, aliens, 0, 0, aaa).items():
                tmp = pg.math.Vector2(a[0].rect.center) - \
                    pg.math.Vector2(t.rect.center)
                t.set_target(tmp.angle_to(pg.math.Vector2(1, 0)))
                # tmp=t.rect.clipline(t.rect.center, a[0].rect.center)
                # t.set_target( pg.math.Vector2(tmp[1][0]-tmp[0][0],tmp[1][1]-tmp[0][1] ) )

            # See if player's boms hit the aliens.
            if bombs.sprite:
                for alien in pg.sprite.spritecollide(bombs.sprite, aliens, 0):
                    alien.been_hit()

        # draw the scene
        dirty = all_sprites.draw(wind.screen)
        pg.display.update(dirty)

        # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
        clock.tick(30)

    pg.time.wait(2000)


# call the "main" function if running this script
if __name__ == "__main__":

    # print( units_module_constant_dump() )
    # settings.enable=True
    # # settings.update_all_module_constant()
    # units_module_constant_update()
    # print( units_module_constant_dump() )

 # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Initialize pygame
    pg.init()
    pg.mixer.quit()

    main()

    pg.quit()

    print('done')
