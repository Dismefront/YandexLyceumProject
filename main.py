import pygame
import menu
import drawable
import camera
import gameVars


def generate_level():
    global cmr, background
    q = gameVars.blockscount
    background = drawable.DrawableObject(pygame.image.load("data/gamebground.png"),
                                         [0, 0] + sz, all_sprites)
    for i in range(q):
        drawable.DrawableObject(pygame.image.load("data/grass.png"),
                                (i * 100, 350, 100, 100), all_sprites)
    gameVars.spongeHouseSprite = drawable.Houses(
        pygame.image.load("data/spongehouse.png"),
        (0, 200, 100, 200), all_sprites)
    gameVars.patHouseSprite = drawable.Houses(
        pygame.image.load("data/patrikhouse.png"),
        ((q - 1) * 100, 300, 100, 100), gameVars.enemygroup)

    temp = pygame.Surface((50, 50))
    temp.fill(pygame.Color("red"))
    gameVars.hud_1 = drawable.Hud(
        temp,
        (100, 0, 50, 50), hud)
    gameVars.hud_1.set_command("knight")
    gameVars.hud_2 = drawable.Hud(
        temp,
        (170, 0, 50, 50), hud)
    gameVars.hud_3 = drawable.Hud(
        temp,
        (240, 0, 50, 50), hud)
    gameVars.hud_4 = drawable.Hud(
        temp,
        (310, 0, 50, 50), hud)

    cmr = camera.Camera(sz, (0, q * 100))


pygame.init()
sz = [800, 450]
cmr = None
background = None
screen = pygame.display.set_mode(sz)
running = True
all_sprites = pygame.sprite.Group()
hud = pygame.sprite.Group()
clock = pygame.time.Clock()
frame_updater = 0
enemy_spawn_updater = 0
now_money = 0
font = pygame.font.Font(None, 50)
if menu.start(sz, screen, "data/bgimage.jpg", all_sprites) is True:
    generate_level()
while running:
    screen.fill(pygame.Color("black"))
    cmr.update(pygame.mouse.get_pos())
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu.start(sz, screen, None, all_sprites)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if now_money >= 100:
                    now_money -= 100
                    hud.update()

    for sprite in all_sprites:
        if sprite != background and sprite.__class__ != drawable.Hud:
            cmr.apply(sprite)
    for sprite in gameVars.kgroup:
        cmr.apply(sprite)
    for sprite in gameVars.enemygroup:
        cmr.apply(sprite)

    money_text = font.render('$' + str(now_money), 1, pygame.Color("yellow"))

    all_sprites.draw(screen)
    gameVars.enemygroup.draw(screen)
    gameVars.kgroup.draw(screen)
    hud.draw(screen)
    all_sprites.update(screen, frame_updater)
    gameVars.enemygroup.update(screen, frame_updater)
    screen.blit(money_text, (0, 0))

    pygame.display.flip()
    for knight in gameVars.knights:
        knight.update(frame_updater)
    if enemy_spawn_updater >= 10000:
        drawable.EnemyKnight(
            pygame.image.load("data/knight.png"), (0, 0, 800, 450), gameVars.enemygroup
        )
        enemy_spawn_updater = 0
    if frame_updater >= 100:
        frame_updater = 0
        if now_money < 1000:
            now_money += 10
    if gameVars.patHouseSprite.hp <= 0 or gameVars.spongeHouseSprite.hp <= 0:
        menu.terminate()
    frame_updater += clock.tick(60)
    enemy_spawn_updater += frame_updater