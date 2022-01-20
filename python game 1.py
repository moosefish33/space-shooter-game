import pygame
import math
import random

pygame.init()
clock = pygame.time.Clock()

over_font = pygame.font.Font("FFF_tusj.ttf", 50)
screen = pygame.display.set_mode((800, 600))
cooldown = 0
starImg = []
starCo = []
starCo_change =[]
starNum = 100
current_sprite = 0
speed = 3
neomImg = pygame.image.load("Neom.png")
neomX = random.randint(0, 800-64)
neomY = random.randint(0, 100)
neomYSpeed = 2.5
can_spawn = True
bulletImg = []
bulletCo = []
bulletCo_change = 20
num_bullet = 20
bullet_state = [] #you cant see bullet on screen when ready state
playerImg = pygame.image.load("New Piskel.png")
PlayerX = 370
PlayerY = 480
PlayerX_change = 0
PlayerY_change = 0
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
invisible_frame = 0
frame_count = 0
direction_reset = 0
directionVar = True
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10
for i in range(num_bullet):
    bulletImg.append(pygame.image.load("New Piskel bullet 32x32.png"))
    bulletCo.append([PlayerX + 16, PlayerY +10])
    bullet_state.append("ready")

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy spaceship.png"))
    enemyX.append(random.randint(0, 800 - 64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(random.randint(-3, 3))
    enemyY_change.append(40)

def enemy(x,y, i):
    screen.blit(enemyImg[i], (x, y))

def bullet(i):
    screen.blit(bulletImg[i], (bulletCo[i][0], bulletCo[i][1]))
    bullet_state[i] = "Fire"

def isCollision(enX, enY, obX, obY):
    #math stuff
    distance = math.sqrt((math.pow(enX - obX, 2)) + (math.pow(enY - obY, 2)))
    if distance < 27:
        return True
    else:
        return False    

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    over_text_rect = over_text.get_rect(center = (400, 300))
    screen.blit(over_text, over_text_rect)

def show_score(x,y):
    score = font.render("score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def Neom(x,y):
    screen.blit(neomImg, (x,y))

def player(x,y):
    screen.blit(playerImg, (x, y))

for i in range(starNum):
    starImg.append([pygame.image.load("star1.png"), pygame.image.load("star2.png")])
    starCo.append([random.randint(0, 800),random.randint(0, 600)])
    
def star():
    for i in range(starNum):
        screen.blit(starImg[i][current_sprite], (starCo[i][0], starCo[i][1]))

def star_movement():
    for y in range(starNum):
            
        starCo[y][1] += speed
        if starCo[y][1] > 600 + 32:
            starCo[y][1] = 0 - 32

def game():
    global PlayerX
    global PlayerY
    global  neomX
    global neomY
    global can_spawn
    global PlayerX_change
    global PlayerY_change
    global neomYSpeed
    global spawn_chance
    global speed
    global frame_count
    global score_value
    global directionVar
    global current_sprite
    running = True
    while running:
    
        screen.fill ((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    PlayerX_change = -2
                if event.key == pygame.K_d:
                    PlayerX_change = 2
                if event.key == pygame.K_SPACE:
                    has_fired = False
                    index = 0
                    while has_fired == False:
                        if bullet_state[index] == "ready":
                            bulletCo[index][0] = PlayerX +16
                            bullet_state[index] = "Fire"
                            has_fired = True
                        index += 1
            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_a:
                        PlayerX_change = 0
                if event.key == pygame.K_d:
                        PlayerX_change = 0

        for i in range(num_bullet):
            if bullet_state[i] == "Fire":
                bullet(i)
                bulletCo[i][1] -= bulletCo_change
            if bulletCo[i][1] <= 0:
                bulletCo[i][1] = PlayerY
                bullet_state[i] = "ready"

        star_movement()
            
        if directionVar:
            
            direction_reset = frame_count
            directionVar = False
        for i in range(num_of_enemies):
            if frame_count - direction_reset >= 180:
                enemyX_change[i] = random.randint(-3,3)
                print(enemyX_change[i])
                directionVar = True
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = random.randint(1, 3)
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 800 - 64:
                enemyX_change[i] = random.randint(-3, -1)
                enemyY[i] += enemyY_change[i]
            collision2 = isCollision(enemyX[i], enemyY[i], PlayerX, PlayerY)
            if collision2:
                
                score_value += 1
                enemyX[i] = random.randint(0, 800 - 64)
                enemyY[i] = random.randint(50, 150)
                
                if current_sprite >= 1:
                    current_sprite -= 1
                speed = 3
            for j in range (num_bullet): 
                collision = isCollision(enemyX[i], enemyY[i], bulletCo[j][0], bulletCo[j][1])
                if collision: 
                    bulletCo[j][1] = 480
                    bullet_state[j] = "ready"
                    print("collision")   
                    enemyX[i] = random.randint(0, 800 - 64)
                    enemyY[i] = random.randint(50, 150)
                    score_value += 1
            enemy(enemyX[i], enemyY[i], i)
            show_score(textX, textY)
        collision3 = isCollision(neomX, neomY, PlayerX, PlayerY)
        if collision3:
            
            spawn_chance = random.randint(1,2)
            print("neom")
            choose_enemy = random.randint(0, num_of_enemies - 1)
            if PlayerX > enemyX[choose_enemy]:
                PlayerX_change = 0
                PlayerX = enemyX[choose_enemy] - 16
            if PlayerX < enemyX[choose_enemy]:
                PlayerX_change = 0
                PlayerX = enemyX[choose_enemy] + 16
            if PlayerY > enemyY[choose_enemy]:
                PlayerY_change = 10
            if current_sprite <= 0:
                    current_sprite += 1
                    speed = 6
            if can_spawn:
                can_spawn = False
                neomYSpeed = 0
                invisible_frame = frame_count
                print(frame_count - invisible_frame)
                neomY = 0
        if can_spawn == False and spawn_chance == 1 and frame_count - invisible_frame >= 240:
            can_spawn = True
            neomYSpeed = 2.5
            neomY = random.randint(0, 100)
            neomX = random.randint(0, 800-64)
        elif can_spawn == False and spawn_chance == 2 and frame_count - invisible_frame >= 480:
            can_spawn = True
            neomYSpeed = 2.5
            neomY = random.randint(0, 100)
            neomX = random.randint(0, 800-64)

        PlayerX += PlayerX_change
        if PlayerX <= 0:
            PlayerX = 0
        elif PlayerX >= 800 - 64:
            PlayerX = 800 - 64
        if PlayerY <= 0:
            PlayerY = 480
            PlayerY_change = 0
            if current_sprite >= 1:
                    current_sprite -= 1
            speed = 3
        PlayerY -= PlayerY_change
        neomY += neomYSpeed
        if neomY >= 600:
            neomY = random.randint(0, 100)
            neomX = random.randint(0, 800-64)

        
        for i in range(num_of_enemies):
            #gameover
            if enemyY[i] > 480:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                    neomY = 2000
                game_over_text()
                break

        star()
        player(PlayerX, PlayerY)
        frame_count += 1
        if can_spawn:
            Neom(neomX,neomY)
        clock.tick(60)
        pygame.display.update()

def menu():

    
    spaceText = font.render("Space Shooter Game", True, (255, 255, 255))  
    spaceText_rect = spaceText.get_rect(center =(800/ 2 , 600 / 2 - 150))
    spaceText2 = font.render("Use A and D Keys To Move", True, (255, 255, 255))  
    spaceText2_rect = spaceText2.get_rect(center =(800/ 2 , 600 / 2 - 50))
    spaceText3 = font.render("Press Enter To Play", True, (255, 255, 255))  
    spaceText3_rect = spaceText3.get_rect(center =(800 / 2 , 600 / 2 + 50))
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("works") 
                    return game()
        
        screen.fill ((0, 0, 0))
        screen.blit(spaceText, spaceText_rect)
        screen.blit(spaceText2, spaceText2_rect)
        screen.blit(spaceText3, spaceText3_rect)
        pygame.display.update()
if __name__ == "__main__":
    menu()
