import pygame


def terminate():
    pygame.quit()
    import sys
    sys.exit()


def collides(pos, rect):
    if rect[0] <= pos[0] <= rect[0] + rect[2] and \
            rect[1] <= pos[1] <= rect[1] + rect[3]:
        return True
    return False


def start(sz, screen, path, group):
    running = True
    btexts = ["play", "authors", "quit"]
    if path is not None:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, sz)
    else:
        btexts[0] = "restart"
        image = pygame.Surface(sz).convert()
        image.fill(pygame.Color("white"))
        image.set_alpha(70)
    font = pygame.font.Font(None, 70)
    imgbutton = pygame.image.load("data/menubutton.png")
    imgbutton = pygame.transform.scale(imgbutton, (400, 70))
    nowstr = ""
    authortext = ""
    while running:
        screen.fill(pygame.Color("black"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if nowstr == "quit":
                        terminate()
                    elif nowstr == "play" or nowstr == "restart":
                        return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and path is None:
                    return
        group.draw(screen)
        screen.blit(image, (0, 0))
        ok = False
        for i in range(len(btexts)):
            screen.blit(imgbutton, (10, 20 + i * 100))
            tpl = imgbutton.get_rect()[2::]
            if collides(pygame.mouse.get_pos(), [10, 20 + i * 100] + tpl):
                txt = font.render(btexts[i], 1, pygame.Color("white"))
                nowstr = btexts[i]
                if nowstr == "authors":
                    authortext = "Made by Romaikin Erik"
                ok = True
            else:
                if not ok:
                    authortext = ""
                    nowstr = ""
                txt = font.render(btexts[i], 1, pygame.Color("black"))
            width1 = imgbutton.get_rect()[2]
            width2 = txt.get_rect()[2]
            if btexts[i] == "authors":
                font2 = pygame.font.SysFont("Impact", 30)
                screen.blit(font2.render(authortext, 1, pygame.Color("black")), (450, 70))
            screen.blit(txt, (10 + width1 // 2 - width2 // 2, 30 + i * 100))
        pygame.display.flip()