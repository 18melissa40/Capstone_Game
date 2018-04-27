# SPGL Minimal Code by /u/wynand1004 AKA @TokyoEdTech
# Requires SPGL Version 0.8 or Above
# SPGL Documentation on Github: https://wynand1004.github.io/SPGL
# Game Made by Melissa Robertson


#Things left to do:
#licenses + attributions

#What needs Attribution:
#-Tomb Guard and Guard Images
# Elf Warrior - https://thierrycravatte.deviantart.com/art/Archer-4-524413762


#Importing Modules
import spgl
import math
import random

#-----Classes------
class Player(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.inventory = []
        self.HP = 30
        self.wins = 0
        
    #movement functions paired with arrow keys
    def go_right(self):
        # self.set_image("player_right.gif", 20, 20) (Makes the image flicker too much.)
        self.setheading(0)
        self.speed = 4
    
    def go_left(self):
        # self.set_image("player_left.gif", 20, 20)
        self.setheading(180)
        self.speed = 4
    
    def go_up(self):
        self.setheading(90)
        self.speed = 4

    def go_down(self):
        self.setheading(270)
        self.speed = 4
    	
    def stop(self):
        self.speed = 0

    def basic_attack(self):
        attack_damage = random.randint(0, 6)
        player.enemy.HP -= attack_damage
        if attack_damage == 0:
            enemy_damage_lbl.update("Miss")
        else:
            enemy_damage_lbl.update(attack_damage)
        #Calls enemy's "turn". Would like to make this call after a time instead of immediately.
        #But then the player could keep clicking attack and cause a mess
        if player.enemy.HP > 0:
            player.enemy.fight()
        
    def sword_attack(self):
        if sword in player.inventory:
            attack_damage = random.randint(4, 10)
            player.enemy.HP -= attack_damage
            enemy_damage_lbl.update(attack_damage)
            player.enemy.fight()
        else:
            pass

    def defend(self):
        #basically just guarentees you'll get hit with less damage. Yes, I know it's a pointless move.
        player_damage = random.randint(0, 2)
        player.HP -= player_damage
        if player_damage == 0:
            player_damage_lbl.update("Miss")
        else:
            player_damage_lbl.update(player_damage)

    def tick(self):
        if game.mode == "maze":
            #checks wall collision
            for coordinate in wall_coordinates:
                if is_wall_collision(self, coordinate) == True:
                    self.setheading(self.heading() + 180)
                    self.fd(4)
                    self.stop()

            #checks enemy collision
            for enemy in enemies:
                #starts fight when collision occurs
                if game.is_collision(self, enemy):
                    game.mode = "fighting"
                    game.stop_all_sounds()
                    game.play_sound("Game_Jam_03.mp3 -v 0.2", time=108)
                    player.enemy = enemy

                    if player.enemy == master_guard:
                        enemy_name_lbl.update("Tomb Guard")
                        enemy_name_lbl.setposition(300, -152)
                        guard_icon.set_image("master_guard.gif", 30, 30)
                        guard_icon.setposition(400, -220)
                    else:
                        enemy_name_lbl.update("Guard")
                        enemy_name_lbl.setposition(350, -152)
                        guard_icon.set_image("guard.gif", 30, 30)
                        guard_icon.setposition(400, -220)

                #checks coffin collision
                if game.is_collision(self, coffin):
                    self.setheading(self.heading() + 180)
                    self.fd(4)
                    self.stop()

            self.fd(self.speed) #if player is not pressing arrow keys, or is colliding with wall, speed is 0

        elif game.mode == "fighting":
            player_HP_lbl.update("Health: {}".format(player.HP))
            if player.HP <= 0:
                game_over_lbl.update("GAME OVER")
            elif player.enemy.HP <= 0: 
                #starts out with wins at 0, has chance to get sword. Chance increases each time
                #until by the 3rd one, player will always get the sword.
                if sword not in self.inventory:
                    sword_drop = random.randint(self.wins, 2)
                    if sword_drop == 2:
                        player.inventory.append(sword)
                        sword_attack.set_image("sword_attack_button.gif", 100, 28)
                        sword.setposition(-290, -208)
                self.wins += 1
                #gets rid of enemy, picture, and labels
                player.enemy.destroy()
                enemy_name_lbl.update("")
                player_damage_lbl.update("")
                enemy_damage_lbl.update("")
                guard_icon.setposition(900, 0)
                game.mode = "maze"

                #changes music
                game.stop_all_sounds()
                game.play_sound("Night_Crossing.mp3 -v 0.2", time=129)

class Enemy(spgl.Sprite):
    def __init__(self, shape, color, mobile, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.is_mobile = mobile
        if self.is_mobile == True:
            self.HP = 10
        else:
            self.HP = 20
        self.direction = "right"

    def move(self):
        if red_keyhole.state == "locked" or blue_keyhole.state == "locked":
            if self.is_mobile == True:
                for coordinate in wall_coordinates:
                    if is_wall_collision(self, coordinate) == True:
                        self.setheading(self.heading() + 180)
                        self.fd(2)
                        if self.direction == "right":
                            self.set_image("orc_knight_left.gif", 20, 20)
                            self.direction = "left"
                        else:
                            self.set_image("orc_knight_right.gif", 20, 20)
                            self.direction = "right"

                self.fd(2)
            
    def fight(self):
        #changes difficulty of fight based on the type of guard
        if self.is_mobile == True:
            player_damage = random.randint(0, 4)
            player.HP -= player_damage
            if player_damage == 0:
                player_damage_lbl.update("Miss")
            else:
                player_damage_lbl.update(player_damage)

        else:
            player_damage = random.randint(0, 7)
            player.HP -= player_damage
            if player_damage == 0:
                player_damage_lbl.update("Miss")
            else:
                player_damage_lbl.update(player_damage)

        clear_label_after_time(player_damage_lbl)
        clear_label_after_time(enemy_damage_lbl)


    def tick(self):
        if game.mode == "maze":
            self.move()

class Scenery(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.state = "locked"
    
    def click(self, x, y):
        distance = math.sqrt((self.xcor()-player.xcor()) ** 2 + (self.ycor()-player.ycor()) ** 2)
        red_keyhole_distance = math.sqrt((red_keyhole.xcor()-player.xcor()) ** 2 + (red_keyhole.ycor()-player.ycor()) ** 2)
        blue_keyhole_distance = math.sqrt((blue_keyhole.xcor()-player.xcor()) ** 2 + (blue_keyhole.ycor()-player.ycor()) ** 2)
        if self == red_key:
            if distance < 30: #BE SURE TO CHANGE THIS BACK
                #moves into graphical inventory
                self.setposition(-430, -208)
                player.inventory.append(self)

            
            if red_keyhole_distance < 30:
                if red_key in player.inventory:
                    red_key.destroy()
                    red_keyhole.destroy()
                    red_keyhole.state = "unlocked"
                    

        elif self == blue_key:
            if distance < 30: 
                self.setposition(-360, -208)
                player.inventory.append(self)
            if blue_keyhole_distance < 30:
                if blue_key in player.inventory:
                    blue_key.destroy()
                    blue_keyhole.destroy()
                    blue_keyhole.state = "unlocked"
                   
            
        elif self == red_keyhole and red_keyhole_distance < 50:
            if self.state == "locked":
                locked_lbl.update("It's locked...")
                clear_label_after_time(locked_lbl)

        elif self == blue_keyhole and blue_keyhole_distance < 50:
            if self.state == "locked":
                locked_lbl.update("It's locked...")
                clear_label_after_time(locked_lbl)

        

        
class Borders(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.penup()
        self.hideturtle()
        self.fd_speed = 10
        self.shapesize(0.5, 0.5, 0)

    
    def draw_borders(self):
        #draw vertical part
        self.penup()
        self.setposition(0, -300)
        self.pensize(10)
        self.pendown()
        self.setheading(90)
        self.fd(190)
    
    def draw_inventory_spaces(self):
        self.penup()
        self.pensize(2)
        self.setposition(-455, -180)
        self.setheading(0)
        self.color("white")
        for x in range(0, 4):
            self.pendown()
            for x in range(0, 4):
                self.fd(50)
                self.rt(90)
            self.penup()
            self.fd(70)

class Button(spgl.Sprite):
    def __init__(self, shape, color, x, y, name):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.name = name

    def click(self, x, y):
        if game.mode == "fighting":
            if self.name == "basic attack":
                player.basic_attack()
            elif self.name == "sword attack":
                player.sword_attack()
            elif self.name == "defend":
                player.defend()
        if self.name == "exit game":
            game.exit()

#-----Functions-----
def is_wall_collision(sprite, coordinates):
    #uses bounding box from spgl, but takes sprite_2 coordinates from wall_coordinates
    #for some reason it's triggering with -30 as y-cor when it's nowhere near -30. The wall centers should be -70.
    x_collision = (math.fabs(sprite.xcor() - coordinates[0]) * 2) < (sprite.width + 5)
    y_collision = (math.fabs(sprite.ycor() - coordinates[1]) * 2) < (sprite.height + 5)
    return (x_collision and y_collision)

def clear_label_after_time(label):
    spgl.turtle.Screen().ontimer(lambda: label.update(""), t=2000)


#---------------Initialization---------------
# Initial Window 
game = spgl.Game(1000, 600, "black", "THE BLIND GUARDIAN'S  Crypt", 5)
game.mode = "maze"

#Maze design
maze = [
"xxxxxxxxxxxxxxxx    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", 
"x                         x          x                                                            x",
"x                         x          x                                                            x",
"x                         x          x                                                            x",
"x         xxxxxxxxxxxxxxxxx          xxxxxxxxxxxxxxxxxxxxxx    xxxxxxxxxxxxxxxxxxxxxxxxxxxxx      x",
"x         x                                               x    x                                  x",
"x         x                                               x    x                                  x",
"x         x                                               x    x                                  x",
"xxxxx     xxxxxxxxxxxxxxxx      xxxxxxxxxxxxxxxxxxx       x    x      xxxxxxxxxxxxxxxxxxxxxxxxx   x",
"x k x                                             x                                           x   x",
"x   x                                             x                                           x   x",
"x   x                                             x                                           x k x",
"x   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx        xxxxxxxxxx",
"x                                                                                                 x",
"x                                                                                                 x",
"x                                                                                                 x",
"xxxxxxxxxxxxxxxxxx     xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
"x p                                                                                               x",
"x                                                                                                 x",
"x                                                                                                 x",
"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
]

wall_coordinates = []

# Create Maze and Menu Borders
# menu_borders = Borders("square", "black", 0, 0)    #old method of stamping images on the screen to create visual borders
maze_borders = Borders("square", "black", 0, 0)      #replaced with screenshot as background to reduce lag. 
maze_borders.set_image("wall_vines5_2.gif", 10, 10)  #coordinates for collision still added

# menu_borders.draw_borders()
# menu_borders.draw_inventory_spaces()

for y in range(len(maze)):
    for x in range(len(maze[y])):
        screen_x = -490 + (x * 10)
        screen_y = 90 - (y * 10)

        if maze[y][x] == "x":
            maze_borders.goto(screen_x, screen_y)
            #maze_borders.stamp()
            wall_coordinates.append((screen_x, screen_y)) #adding coordinates for collision

# Create Static Objects
coffin = Scenery("square", "green", 200, 200)
coffin.shapesize(5, 10)

red_key = Scenery("turtle", "red", -475, -10)
blue_key = Scenery("turtle", "blue", 470, -15)
blue_keyhole = Scenery("square", "blue", 85, 146)
red_keyhole = Scenery("square", "red", 313, 146)

sword = Scenery("turtle", "orange", -600, -500)

guard_icon = Scenery("square", "green", 900, 0)
player_icon = Scenery("square", "green", 165, -225)

amulet = Scenery("square", "black", 950, 950)

#Create moving objects
player = Player("circle", "red", -475, -92)

master_guard = Enemy("square", "red", False, -315, 90)

guard_1 = Enemy("square", "red", True, -240, -55)
guard_2 = Enemy("square", "red", True, -100, -10)
guard_3 = Enemy("square", "red", True, 115, -15)

enemies = [master_guard, guard_1, guard_2, guard_3]

# Create Labels
#inventory_lbl = spgl.Label("Inventory", "white", -495, -150, font_size=30)
moves_lbl = spgl.Label("Athena", "white", 20, -150, font_size=30)
player_HP_lbl = spgl.Label("Health: {}".format(player.HP), "white", 20, -170, font_size=20)

enemy_name_lbl = spgl.Label("", "white", 350, -155, font_size=30)

game_over_lbl = spgl.Label("", "red", -160, -50, font_size=70)

player_damage_lbl = spgl.Label("", "red", 195, -230, font_size=20)
enemy_damage_lbl = spgl.Label("", "red", 330, -230, font_size=20)
locked_lbl = spgl.Label("", "white", -200, -150, font_size=20)


# Create Buttons
basic_attack = Button("square", "blue", 80, -200, "basic attack")
sword_attack = Button("square", "blue", 80, -235, "sword attack")
defend = Button("square", "blue", 80, -270, "defend")

exit_game = Button("square", "blue", -440, 275, "exit game")


#---Set Images---
player.set_image("player_right.gif", 20, 20)

master_guard.set_image("vault_guard.gif", 20, 20)
guard_1.set_image("orc_knight_right.gif", 20, 20)
guard_2.set_image("orc_knight_right.gif", 20, 20)
guard_3.set_image("orc_knight_right.gif", 20, 20)

coffin.set_image("coffin.gif", 260, 125)
sword.set_image("sword.gif", 32, 32)
amulet.set_image("magic_amulet.gif", 20, 20)

red_key.set_image("red_key.gif", 20, 20)
blue_key.set_image("blue_key.gif", 20, 20)
red_keyhole.set_image("fire_clue.gif", 20, 20)
blue_keyhole.set_image("ice_clue.gif", 20, 20)

player_icon.set_image("player_avatar.gif", 20, 20)

basic_attack.set_image("basic_attack_button.gif", 100, 28)
sword_attack.set_image("grey_sword_attack_button.gif", 100, 28)
defend.set_image("defend_button.gif", 100, 28)
exit_game.set_image("exit_game_button.gif", 100, 28)

#Play Sounds
game.stop_all_sounds()
game.play_sound("Night_Crossing.mp3 -v 0.2", time=129)

# Set Keyboard Bindings
wn = spgl.turtle.Screen()
wn.bgpic("full_background.gif")
wn.onkeypress(player.go_right, "Right")
wn.onkeyrelease(player.stop, "Right")
wn.onkeypress(player.go_left, "Left")
wn.onkeyrelease(player.stop, "Left")
wn.onkeypress(player.go_up, "Up")
wn.onkeyrelease(player.stop, "Up")
wn.onkeypress(player.go_down, "Down")
wn.onkeyrelease(player.stop, "Down")

while True:
    game.tick()
    if red_keyhole.state == "unlocked" and blue_keyhole.state == "unlocked":
        amulet.setposition(-220, -208)
        game_over_lbl.update("YOU WIN!")
         

