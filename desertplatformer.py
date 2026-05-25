mport pygame, sys
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SKY_BLUE = (135, 206, 235)
DARK_GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)
PURPLE = (138, 43, 226)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("desert platformer")
clock = pygame.time.Clock()

# player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill((255, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = False
        self.gravity = 0.7
        self.jump_power = -16
        self.speed = 6
    def handle_input(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        else:
            self.vel_x = 0
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and not self.is_jumping:
            self.vel_y = self.jump_power
            self.is_jumping = True
    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        if self.rect.y > SCREEN_HEIGHT + 50:
            return False
        return True
    def update(self, platforms):
        self.rect.x += self.vel_x
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width
        for platform in platforms:
            if self.vel_y > 0 and self.rect.bottom >= platform.rect.top and self.rect.top < platform.rect.top:
                if self.rect.right > platform.rect.left and self.rect.left < platform.rect.right:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.is_jumping = False
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# platforms
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# coins
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 24))
        self.image.fill(YELLOW)
        pygame.draw.circle(self.image, WHITE, (12, 12), 8)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collected = False
    def draw(self, surface):
        if not self.collected:
            surface.blit(self.image, self.rect)

# enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.direction = 1
        self.left_bound = x - 100
        self.right_bound = x + 100
    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x <= self.left_bound or self.rect.x >= self.right_bound:
            self.direction *= -1
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# goal
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 165, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# main game
class Game:
    def __init__(self):
        self.player = Player(80, 400)
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
            Platform(150, 480, 180, 20),
            Platform(450, 420, 140, 20),
            Platform(100, 320, 120, 20),
            Platform(550, 280, 160, 20),
            Platform(300, 200, 100, 20),
        ]
        self.coins = [
            Coin(520, 370),
            Coin(180, 420),
            Coin(620, 230)
        ]
        self.enemy = Enemy(380, 380)
        self.goal = Goal(720, 180)
        self.score = 0
        self.game_over = False
        self.won = False
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        if not self.player.apply_gravity():
            self.game_over = True
        self.player.update(self.platforms)
        self.enemy.update()
        for coin in self.coins:
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                coin.collected = True
                self.score += 20
        if self.player.rect.colliderect(self.enemy.rect):
            self.game_over = True
        if self.player.rect.colliderect(self.goal.rect):
            self.won = True
    def draw(self):
        screen.fill(SKY_BLUE)
        for platform in self.platforms:
            platform.draw(screen)
        for coin in self.coins:
            coin.draw(screen)
        self.enemy.draw(screen)
        self.goal.draw(screen)
        self.player.draw(screen)
        font = pygame.font.Font(None, 40)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        if self.game_over:
            text = font.render("GAME OVER - Press R to Restart", True, RED)
            screen.blit(text, (180, 250))
        if self.won:
            text = font.render("YOU WIN! - Press R to Restart", True, DARK_GREEN)
            screen.blit(text, (200, 250))
        pygame.display.flip()
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            if not self.game_over and not self.won:
                self.update()
            keys = pygame.key.get_pressed()
            if (self.game_over or self.won) and keys[pygame.K_r]:
                self.__init__()
            self.draw()
            clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
