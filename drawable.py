import pygame
import menu
import gameVars


class DrawableObject(pygame.sprite.Sprite):
    def __init__(self, img, rect, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(img, rect[2::])
        self.rect = pygame.rect.Rect(rect)
        self.all_sprites = all_sprites

    def has_mouse_contact(self):
        if menu.collides(pygame.mouse.get_pos(), self.rect):
            return True
        return False


class Houses(DrawableObject):
    def __init__(self, img, rect, all_sprites):
        super().__init__(img, rect, all_sprites)
        self.hp = 1000

    def get_hp(self):
        return self.hp

    def update(self, screen, time):
        self.draw_hp_bar(screen)

    def draw_hp_bar(self, surface):
        pygame.draw.rect(surface, pygame.Color("black"),
                         (self.rect.x, self.rect.y - 10, self.rect.w, 10), 1)
        pygame.draw.rect(surface, pygame.Color("red"),
                         (self.rect.x, self.rect.y - 10,
                          self.rect.w - 10 * (1000 - self.hp) / self.rect.w, 10))


class Hud(DrawableObject):
    def __init__(self, img, rect, all_sprites):
        super().__init__(img, rect, all_sprites)
        self.command = None

    def set_command(self, command):
        self.command = command

    def update(self):
        if not self.has_mouse_contact():
            return
        if self.command == "knight":
            gameVars.knights.append(Knight(pygame.image.load("data/knight.png"),
                                           (0, 0, 800, 450), gameVars.kgroup))


class Knight(DrawableObject):
    def __init__(self, img, rect, all_sprites):
        rect = img.get_rect()
        self.sheet = img
        super().__init__(img, rect, all_sprites)
        self.hp = 30
        self.walking_sprite = list()
        self.attack_sprite = list()
        self.nowstate = list()
        self.wscounter = 0
        self.walking_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(57, 223, 45, 43)),
                                   (100, 75))
        )
        self.walking_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(105, 223, 45, 43)),
                                   (100, 75))
        )
        self.walking_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(154, 223, 45, 43)),
                                   (100, 75))
        )
        self.walking_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(205, 223, 45, 43)),
                                   (100, 75))
        )
        self.attack_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(58, 135, 48, 39)),
                                    (100, 75))
        )
        self.attack_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(106, 135, 48, 39)),
                                   (100, 75))
        )
        self.attack_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(151, 135, 48, 39)),
                                   (100, 75))
        )
        self.attack_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(199, 135, 48, 39)),
                                   (100, 75))
        )
        self.rect = pygame.Rect((0, 350, 100, 75))
        self.image = self.walking_sprite[0]
        self.nowstate = self.walking_sprite

    def update(self, time):
        if time >= 100:
            self.wscounter = (self.wscounter + 1) % 4
            self.image = self.nowstate[self.wscounter]
        target = pygame.sprite.spritecollideany(self, gameVars.enemygroup)
        if not target:
            self.nowstate = self.walking_sprite
            self.rect.x += 1
        else:
            self.nowstate = self.attack_sprite
            target.hp -= 1
            if target.hp <= 0:
                gameVars.enemygroup.remove(target)


class EnemyKnight(DrawableObject):
    def __init__(self, img, rect, all_sprites):
        rect = img.get_rect()
        self.sheet = img
        super().__init__(img, rect, all_sprites)
        self.hp = 30
        self.walking_sprite = list()
        self.attack_sprite = list()
        self.nowstate = list()
        self.wscounter = 0
        self.walking_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(57, 223, 45, 43)),
                                   (100, 75))
        )
        self.walking_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(105, 223, 45, 43)),
                                   (100, 75))
        )
        self.walking_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(154, 223, 45, 43)),
                                   (100, 75))
        )
        self.walking_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(205, 223, 45, 43)),
                                   (100, 75))
        )
        self.attack_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(58, 135, 48, 39)),
                                    (100, 75))
        )
        self.attack_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(106, 135, 48, 39)),
                                   (100, 75))
        )
        self.attack_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(151, 135, 48, 39)),
                                   (100, 75))
        )
        self.attack_sprite.append(
            pygame.transform.scale(self.sheet.subsurface(pygame.Rect(199, 135, 48, 39)),
                                   (100, 75))
        )
        for i in range(4):
            self.attack_sprite[i] = pygame.transform.flip(self.attack_sprite[i], True, False)
        for i in range(4):
            self.walking_sprite[i] = pygame.transform.flip(self.walking_sprite[i], True, False)
        self.rect = pygame.Rect(((gameVars.blockscount - 1) * 100, 350, 100, 75))
        self.image = self.walking_sprite[0]
        self.nowstate = self.walking_sprite

    def update(self, screen, time):
        if time >= 100:
            self.wscounter = (self.wscounter + 1) % 4
            self.image = self.nowstate[self.wscounter]
        target = pygame.sprite.spritecollideany(self, gameVars.kgroup)
        enemy_house = pygame.sprite.collide_rect(self, gameVars.spongeHouseSprite)
        if not target:
            if enemy_house:
                self.nowstate = self.attack_sprite
                gameVars.spongeHouseSprite.hp -= 0.5
                if gameVars.spongeHouseSprite.hp <= 0:
                    menu.terminate()
            else:
                self.nowstate = self.walking_sprite
                self.rect.x -= 1
        else:
            self.nowstate = self.attack_sprite
            target.hp -= 0.5
            if target.hp <= 0:
                gameVars.kgroup.remove(target)
                gameVars.knights.remove(target)