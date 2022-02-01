import sys
import random
import pygame

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
pygame.display.set_caption("Crab Game")

gameFont = pygame.font.Font("C://Users//oliwia//Desktop//projekty//Krab//pngs//PressStart2P-Regular.ttf", 24)


class Crab(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        super().__init__()
        self.runningSp = []
        self.duckingSp = []
        
        self.runningSp.append(pygame.image.load("pngs/KrabRun1.png"))
        self.runningSp.append(pygame.image.load("pngs/KrabRun2.png"))
        
        self.duckingSp.append(pygame.image.load("pngs/KrabDuck1.png"))
        self.duckingSp.append(pygame.image.load("pngs/KrabDuck2.png"))
        
        self.posX = posX
        self.posY = posY
        self.presentimage = 0
        self.image = self.runningSp[self.presentimage]
        self.rect = self.image.get_rect(center=(self.posX, self.posY))
        self.velocity = 8.5
        self.gravity = 4.5
        self.ducking = False
        
    def jump (self):
        if self.rect.centery >= 340:
            while self.rect.centery - self.velocity > 40:
                self.rect.centery -= 1
                
    def duck(self):
        self.ducking = True
        self.rect.centery = 380
        
    def unduck(self):
        self.ducking = False
        self.rect.centery = 340
        
    def apply_grav(self):
        if self.rect.centery <= 340:
            self.rect.centery += self.gravity
            
    def update(self):
        self.animate()
        self.apply_grav()
        
    def animate(self):
        self.presentimage += 0.05
        if self.presentimage >=2:
            self.presentimage = 0
            
        if self.ducking:
            self.image = self.duckingSp[int(self.presentimage)]
        else:
            self.image = self.runningSp[int(self.presentimage)]
        

class Trash(pygame.sprite.Sprite):
    
    def __init__(self, posX, posY):
        super().__init__()
        self.posX = posX
        self.posY = posY
        self.sprites = []
        
        for i in range(1, 7):
            presentSp = pygame.image.load("pngs/Trash1.png")
        self.sprites.append(presentSp)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.posX, self.posY))
        
    def update(self):
        self.posX -= gameSpeed
        self.rect = self.image.get_rect(center=(self.posX, self.posY))
        
class Trash2(pygame.sprite.Sprite):
    
    def __init__(self, posX, posY):
        super().__init__()
        self.posX = posX
        self.posY = posY
        self.sprites = []
        
        for i in range(1, 7):
            presentSp = pygame.image.load("pngs/Trash2.png")
        self.sprites.append(presentSp)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.posX, self.posY))
        
    def update(self):
        self.posX -= gameSpeed
        self.rect = self.image.get_rect(center=(self.posX, self.posY))
        
class Trash3(pygame.sprite.Sprite):
    
    def __init__(self, posX, posY):
        super().__init__()
        self.posX = posX
        self.posY = posY
        self.sprites = []
        
        for i in range(1, 7):
            presentSp = pygame.image.load("pngs/TrashSmall2.png")
        self.sprites.append(presentSp)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.posX, self.posY))
        
    def update(self):
        self.posX -= gameSpeed
        self.rect = self.image.get_rect(center=(self.posX, self.posY))
        


class Shark(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.posX = 1300
        self.posY = random.choice([280, 295, 350])
        self.sprites = []
        self.sprites.append(pygame.image.load("pngs/Shark1.png"))
        self.sprites.append(pygame.image.load("pngs/Shark2.png"))
        self.presentimage = 0
        self.image = self.sprites[self.presentimage]
        self.rect = self.image.get_rect(center=(self.posX, self.posY))
        
    def update(self):
        self.animate()
        self.posX -= gameSpeed
        self.rect = self.image.get_rect(center=(self.posX, self.posY))
        
    def animate(self):
        self.presentimage += 0.025
        if self.presentimage >= 2:
            self.presentimage = 0
        self.image = self.sprites[int(self.presentimage)]


gameSpeed = 5
jumpCount = 10
playerScore = 0
gameOver = False
obsTimer = 0 
obsSpawn = False
obsCooldown = 1000

background = pygame.image.load("pngs/Track.png")
background = pygame.transform.scale(background, (1280,20))
backgroundX = 0
backgroundRect = background.get_rect(center=(640,400))

obsGroup = pygame.sprite.Group()
crabGroup = pygame.sprite.GroupSingle()
sharkGroup = pygame.sprite.Group()

crab = Crab(80, 350)
crabGroup.add(crab)

def endGame():
    global playerScore, gameSpeed
    gameOverText = gameFont.render("Game Over...", True, "black")
    gameOverRect = gameOverText.get_rect(center=(640,300))
    scoreText = gameFont.render(f"Score: {int(playerScore)}", True, "black")
    scoreRect = scoreText.get_rect(center=(640,400))
    screen.blit(gameOverText, gameOverRect)
    screen.blit(scoreText, scoreRect)
    gameSpeed = 5
    obsGroup.empty()

while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        crab.duck()
    else:
        if crab.ducking:
            crab.unduck()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                crab.jump()
                if gameOver:
                    gameOver = False
                    gameSpeed = 5
                    playerScore = 0
                
    screen.fill("sky blue")
    
    if pygame.sprite.spritecollide(crabGroup.sprite, obsGroup, False):
        gameOver = True
    if gameOver:
        endGame()
        
    if not gameOver:
        gameSpeed += 0.0025
        if pygame.time.get_ticks() - obsTimer >= obsCooldown:
            obsSpawn = True
            
        if obsSpawn:
            obsRandom = random.randint(0, 50)
            if obsRandom in range(0,5):
                newObs = Trash(1280, 340)
                obsGroup.add(newObs)
                obsTimer = pygame.time.get_ticks()
                obsSpawn = False
            elif obsRandom in range(6,8):
                newObs = Trash2(1280, 340)
                obsGroup.add(newObs)
                obsTimer = pygame.time.get_ticks()
                obsSpawn = False
            if obsRandom in range(9,11):
                newObs = Trash3(1280, 340)
                obsGroup.add(newObs)
                obsTimer = pygame.time.get_ticks()
                obsSpawn = False
            elif obsRandom in range(12,20):
                newObs = Shark()
                obsGroup.add(newObs)
                obsTimer = pygame.time.get_ticks()
                obsSpawn = False
                
        playerScore += 0.1
    
        playerScoreSurface = gameFont.render(str(int(playerScore)), True, ("black"))
        screen.blit(playerScoreSurface, (1150, 10))
            
    
        sharkGroup.update()
        sharkGroup.draw(screen)
    
        crabGroup.update()
        crabGroup.draw(screen)
    
        obsGroup.update()
        obsGroup.draw(screen)
    
        backgroundX -= gameSpeed
    
        screen.blit(background, (backgroundX, 360))
        screen.blit(background, (backgroundX + 1280, 360))
    
        if backgroundX <= -1280:
            backgroundX = 0
        
    clock.tick(120)
    pygame.display.update()