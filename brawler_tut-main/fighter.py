import pygame
import math

FPS = 60 

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound,health=100):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True
        self.x = x
        self.y = y
        self.health = health
        self.is_invisible = False  
        self.invisible_timer = 0  

    def toggle_invisibility(self, duration):
        self.is_invisible = True
        self.invisible_timer = duration


    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # Track previous position for drawing the red line
        prev_x = self.rect.x
        prev_y = self.rect.y

        # Get key presses
        key = pygame.key.get_pressed()

        if not self.attacking and self.alive and not round_over:
            if self.player == 1:
                # Movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                # Jump
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                # Attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            if self.player == 2:
                # Movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # Jump
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                # Attack
                if key[pygame.K_b] or key[pygame.K_c]:
                    self.attack(target)
                    if key[pygame.K_b]:
                        self.attack_type = 1
                    if key[pygame.K_c]:
                        self.attack_type = 2

              
        self.vel_y += GRAVITY

        dt = 1 / FPS  

        def f(dx, dy, t):
            return dx  
        def g(dx, dy, t):
            return dy  

        k1_dx = f(dx, dy, 0) * dt
        k1_dy = g(dx, dy, 0) * dt
        k2_dx = f(dx + 0.5 * k1_dx, dy + 0.5 * k1_dy, 0) * dt
        k2_dy = g(dx + 0.5 * k1_dx, dy + 0.5 * k1_dy, 0) * dt
        k3_dx = f(dx + 0.5 * k2_dx, dy + 0.5 * k2_dy, 0) * dt
        k3_dy = g(dx + 0.5 * k2_dx, dy + 0.5 * k2_dy, 0) * dt
        k4_dx = f(dx + k3_dx, dy + k3_dy, 0) * dt
        k4_dy = g(dx + k3_dx, dy + k3_dy, 0) * dt

        dx += (k1_dx + 2 * k2_dx + 2 * k3_dx + k4_dx) / 6
        dy += (k1_dy + 2 * k2_dy + 2 * k3_dy + k4_dy) / 6

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy

        pygame.draw.line(surface, (255, 0, 0), (prev_x, prev_y), (self.rect.x, self.rect.y), 3)

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # 6:death
        elif self.hit:
            self.update_action(5)  # 5:hit
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3)  # 3:attack1
            elif self.attack_type == 2:
                self.update_action(4)  # 4:attack2
        elif self.jump:
            self.update_action(2)  # 2:jump
        elif self.running:
            self.update_action(1)  # 1:run
        else:
            self.update_action(0)  # 0:idle

        if self.is_invisible:
            self.invisible_timer -= 1
            if self.invisible_timer <= 0:
                self.is_invisible = False

        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action in [3, 4]:
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                distance = self.rect.centerx - target.rect.centerx
                # Apply linear interpolation to the damage based on distance
                damage = self.calculate_damage(distance)
                target.health -= damage
                target.hit = True

    def calculate_damage(self, distance):
        # Define the damage interpolation based on distance (for example, range 0-300 pixels)
        max_distance = 300
        min_damage = 10
        max_damage = 30

        # Calculate the interpolation factor based on distance
        if abs(distance) < max_distance:
            # Linear interpolation formula
            damage = max_damage - (abs(distance) / max_distance) * (max_damage - min_damage)
            return int(damage)
        else:
            return min_damage  # If the fighters are too far, apply minimum damage

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
