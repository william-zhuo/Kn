import pygame
import sys
import random

pygame.init()
SCR_WIDTH = 1200
SCR_HEIGHT = 600
WHITE = (255, 255, 255)
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

GRAV = 0.9
SCROLLSPEED = 4
begin_game = True

show_hitboxes = False

all_plat = []

back_bound = pygame.Rect(0, 0, 5, SCR_HEIGHT)
floor_bound = pygame.Rect(0, SCR_HEIGHT - 5, SCR_WIDTH, 5)

all_parryable = []
all_enembox = [back_bound, floor_bound]


menu_open = False
menu_font = pygame.font.Font(None, 100)
menu_font2 = pygame.font.Font(None, 50)
toggle_hit_font = pygame.font.Font(None, 50)


def get_image(sheet, frame, w, h, scale, colour):
    image = pygame.Surface((w, h)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame*w), 0, w, h))
    image = pygame.transform.scale(image, (w*scale, h*scale))
    image.set_colorkey(colour)

    return image

sprite_Kn_Body = pygame.image.load("Kn_Body.png").convert_alpha()
sprite_Kn_Sword = pygame.image.load("Kn_Sword.png").convert_alpha()

sprite_Kn_Heart = pygame.image.load("Kn_Heart.png").convert_alpha()
sprite_Kn_Invinc = pygame.image.load("Kn_Invinc.png").convert_alpha()

sprite_Kn_Atk = pygame.image.load("Kn_Atk.png").convert_alpha()


Kn_Body = get_image(sprite_Kn_Body, 0, 15, 54, 1.5, WHITE)
Kn_Sword = get_image(sprite_Kn_Sword, 0, 23, 160, 1, WHITE)

Kn_Heart = get_image(sprite_Kn_Heart, 0, 20, 18, 2, WHITE)
Kn_Invinc = get_image(sprite_Kn_Invinc, 0, 57, 100, 1, WHITE)

Kn_Atk = []
for i in range(4):
    Kn_Atk.append(get_image(sprite_Kn_Atk, i, 9, 25, 4.5, WHITE))



class Kn:
    def __init__(self, scroll_speed):
        self.on_plat = False
        self.scroll_v = scroll_speed
        self.fall_sky = True

        self.x = 500
        self.dx = 0
        self.accel_x = 0
        self.max_dx = 10

        self.y = 0
        self.dy = 3
        self.max_dy = 18

        self.jump_charge = 0
        self.max_jump_charge = 20

        self.w = 35
        self.h = 100

        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.chargebox = pygame.Rect(0, 0, 0, 0)

        self.atkbox = pygame.Rect(0, 0, 0, 0)
        self.atk_ticks = 20

        self.parrybox = pygame.Rect(0, 0, 0, 0)

        self.lives = 5
        self.invinc = 0
        self.invinc_ticks = 60

    def check_on_plat(self):
        global all_plat
        for plat in all_plat:
            if pygame.Rect.colliderect(self.hitbox, plat):
                if self.y + self.h < plat.y + 20:
                    self.on_plat = True
                    self.y = plat.y - self.h + 1
                    break
                else:
                    self.dx = 0
            else:
                self.on_plat = False

    def move(self):
        if -1 * self.max_dx <= self.dx + self.accel_x <= self.max_dx:
            self.dx += self.accel_x
        if self.accel_x == 0:
            self.dx *= 0.9
            if -1.5 < self.dx < 1.5:
                self.dx = 0
        self.x += self.dx - self.scroll_v

        if self.x < 4:
            self.x = 4
        
        if self.jump_charge > self.max_jump_charge:
            self.jump_charge = self.max_jump_charge

        if not self.on_plat:
            self.dy += GRAV
            if self.dy > -2:
                self.dy *= 1.02
            if -0.09 < self.dy < 0.09:
                self.dy = 0
        if self.dy > self.max_dy:
            self.dy = self.max_dy
        if (not self.on_plat) or self.dy < 0:
            self.y += self.dy
        else:
            self.dy = 0

        if self.fall_sky:
            if self.y >= SCR_HEIGHT:
                self.y = 0 - self.h - 50

    def update(self):
        for box in all_enembox:
            if pygame.Rect.colliderect(self.hitbox, box) and self.invinc == 0:
                self.lives -= 1
                self.invinc = self.invinc_ticks
                break
        if self.invinc > 0:
            self.invinc -= 1
        
        if self.atk_ticks < 20:
            if self.atk_ticks == 0:
                self.atk_ticks = 20
            else:
                self.atk_ticks -= 1

    def draw(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.w, self.h)

        if show_hitboxes:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 5)

        self.chargebox = pygame.Rect(self.x - 4, self.y - 25, self.jump_charge * 2, 8)
        pygame.draw.rect(screen, (200, 12 * self.jump_charge, 0), self.chargebox)


        Kn_Body = pygame.transform.rotate(sprite_Kn_Body, -self.dx * 0.5)
        Kn_Body = pygame.transform.scale_by(Kn_Body, 1.8)
        Kn_Body.set_colorkey(WHITE)

        Kn_rect = Kn_Body.get_rect(center=self.hitbox.center)
        screen.blit(Kn_Body, Kn_rect)

        Kn_Sword = pygame.transform.rotate(sprite_Kn_Sword, - (20 - self.atk_ticks) ** 1.8 - self.dx * 0.3)
        Kn_Sword = pygame.transform.scale_by(Kn_Sword, 1)
        Kn_Sword.set_colorkey(WHITE)

        Kn_rect = Kn_Sword.get_rect(center=(self.x + 40, self.y + 55))
        screen.blit(Kn_Sword, Kn_rect)

        if self.invinc > 0:
            screen.blit(Kn_Invinc, (self.x - 10, self.y))

        if show_hitboxes and self.atk_ticks < 20:
            self.atkbox = pygame.Rect(self.x + 80, self.y, self.w, self.h)
            pygame.draw.rect(screen, (255, 0, 0), self.atkbox, 5)

        if self.atk_ticks < 20:
            screen.blit(Kn_Atk[(19-self.atk_ticks)//5], (self.x + 70, self.y - 10))

class PlatformGenerator:
    def __init__(self, scroll_speed):
        self.platforms = []
        
        self.p_width = SCR_WIDTH - 200
        self.p_height = 20
        self.speed = scroll_speed
        self.spacing = 70
        
    def update(self):
        global all_plat

        for platform in self.platforms:
            platform.x -= self.speed
            
        self.platforms = [p for p in self.platforms if p.x + p.width > 0]
        
        if not self.platforms or self.platforms[-1].x + self.platforms[-1].width <= SCR_WIDTH - self.spacing:
            self.spawn_platform()
        
        all_plat = self.platforms
    
    def spawn_platform(self):
        global begin_game
        if begin_game:
            self.platforms.append(pygame.Rect(100, 500, self.p_width, self.p_height))
            begin_game = False

        y = SCR_HEIGHT - random.randint(50, 250)
        self.p_width = random.randint(100, 300)
        self.platforms.append(pygame.Rect(SCR_WIDTH, y, self.p_width, self.p_height))
    
    def draw(self):
        for platform in self.platforms:
            pygame.draw.rect(screen, (120, 120, 120), platform)

class UI:
    def __init__(self):
        self.lives = knight.lives

        self.menu_rect = pygame.Rect(50, 50, SCR_WIDTH - 100, SCR_HEIGHT - 100)

        self.menu_txt = menu_font.render("Game Paused", True, (0, 0, 0))
        self.menu_txt_x = SCR_WIDTH/2 - self.menu_txt.get_width()//2
        self.menu_txt_y = SCR_HEIGHT/2 - self.menu_txt.get_height()//2

        self.menu_txt2 = menu_font2.render("Press 'ESC' to resume", True, (100, 100, 100))
        self.menu_txt2_x = SCR_WIDTH/2 - self.menu_txt2.get_width()//2
        self.menu_txt2_y = SCR_HEIGHT/2 - self.menu_txt2.get_height()//2

        self.toggle_hit = toggle_hit_font.render("Press '1' to toggle hitboxes", True, (100, 70, 70))
        self.toggle_hit_x = SCR_WIDTH/2 - self.toggle_hit.get_width()//2 - 60
        self.toggle_hit_y = SCR_HEIGHT/2 - self.toggle_hit.get_height()//2

    def disp_lives(self):
        self.lives = knight.lives
        for i in range(self.lives):
            screen.blit(Kn_Heart, (50 + i*50, 30))

    def disp_menu(self):
        pygame.draw.rect(screen, (50, 50, 50), (self.menu_rect), 20)

        screen.blit(self.menu_txt, (self.menu_txt_x, self.menu_txt_y - 150))
        screen.blit(self.menu_txt2, (self.menu_txt2_x, self.menu_txt2_y - 80))
        screen.blit(self.toggle_hit, (self.toggle_hit_x, self.toggle_hit_y + 30))

        if show_hitboxes:
            pygame.draw.rect(screen, (0, 255, 0), (850, self.toggle_hit_y + 20, 50, 50))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (850, self.toggle_hit_y + 20, 50, 50))

class Laser:
    def __init__(self):
        self.x = []
        self.y = []
        self.rotation = []

    def smth(self):
        all_enembox.append(all_parryable)

platforms = PlatformGenerator(SCROLLSPEED)
knight = Kn(SCROLLSPEED)
ui = UI()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_open = True
                while menu_open:

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            break
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                menu_open = False
                            elif event.key == pygame.K_1:
                                show_hitboxes = not show_hitboxes
                    if running == False:
                        break
                    
                    ui.disp_menu()

                    pygame.display.flip()
                    clock.tick(60)

            if event.key == pygame.K_c and knight.atk_ticks == 20:
                knight.atk_ticks -= 1

        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            if knight.on_plat:
                knight.dy = -8 - knight.jump_charge*0.5
            knight.jump_charge = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and knight.on_plat:
        knight.jump_charge += 1
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        knight.accel_x = 0
    elif keys[pygame.K_LEFT]:
        knight.accel_x = -0.9
    elif keys[pygame.K_RIGHT]:
        knight.accel_x = 0.9
    else:
        knight.accel_x = 0


    screen.fill((135, 206, 235))

    pygame.draw.rect(screen, (255, 0, 0), back_bound)
    pygame.draw.rect(screen, (255, 0, 0), floor_bound)

    ui.disp_lives()

    knight.check_on_plat()
    knight.move()
    knight.update()
    knight.draw()

    platforms.update()
    platforms.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()