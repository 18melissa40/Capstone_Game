# SPGL Minimal Code by /u/wynand1004 AKA @TokyoEdTech
# Requires SPGL Version 0.8 or Above
# SPGL Documentation on Github: https://wynand1004.github.io/SPGL
# Use this as the starting point for your own games

# Import SPGL
import spgl
import math
import random


# Create Classes

class Player(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.inventory = []
        self.HP = 20
        
    def go_right(self):
        self.setheading(0)
        self.speed = 3
    
    def go_left(self):
        self.setheading(180)
        self.speed = 3
    
    def go_up(self):
        self.setheading(90)
        self.speed = 3

    def go_down(self):
        self.setheading(270)
        self.speed = 3
    	
    def stop(self):
        self.speed = 0

    def basic_attack(self):
        pass
        #should attack, after attack call enemy fight
    
    def sword_attack(self):
        pass

    def defend(self):
        pass

    def tick(self):
        if game.mode == "maze":
            #check wall collision
            for coordinate in wall_coordinates:
                if is_wall_collision(self, coordinate) == True:
                    self.setheading(self.heading() + 180)
                    self.fd(3)
                    self.stop()
            
            for enemy in enemies:
                if game.is_collision(self, enemy):
                    game.mode = "fighting"
                    #write "FIGHT" on the screen, to be erased later
                    #put image of enemy on the side
                    enemy_name_lbl.update("Guard")

            self.fd(self.speed)

        elif game.mode == "fighting":
            player_HP_lbl.update("Health: {}".format(player.HP))
            if player.HP <= 0:
                game_over_lbl.update("GAME OVER")
        

class Enemy(spgl.Sprite):
    def __init__(self, shape, color, mobile, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.is_mobile = mobile
        self.collided = False

    def move(self):
        if self.is_mobile == True:
            for coordinate in wall_coordinates:
                if is_wall_collision(self, coordinate) == True:
                    self.setheading(self.heading() + 180)
            self.fd(2)
        
    def fight(self):
        if self == master_guard:
            player.HP -= random.randint(0, 6)
        else:
            player.HP -= random.randint(0, 4)

    def tick(self):
        if game.mode == "maze":
            self.move()

class Scenery(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
    
    def click(self, x, y):
        distance = math.sqrt((self.xcor()-player.xcor()) ** 2 + (self.ycor()-player.ycor()) ** 2)
        if distance < 30:
            player.inventory.append(self)
           #moves into graphical inventory
            if self == red_key:
                self.setposition(-430, -208)
            elif self == blue_key:
                self.setposition(-360, -208)
        else:
            pass
        
class Borders(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.penup()
        self.hideturtle()
        self.fd_speed = 10
        self.shapesize(0.5, 0.5, 0)

    
    def draw_borders(self):
        #draw horizontal part
        self.setposition(500, -110)
        self.pensize(10)
        self.pendown()
        self.setheading(180)
        self.fd(1000)
    
        #draw vertical part
        self.penup()
        self.setposition(0, -300)
        self.pendown()
        self.setheading(90)
        self.fd(190)
    
    def draw_inventory_spaces(self):
        self.penup()
        self.pensize(2)
        self.setposition(-455, -180)
        self.setheading(0)
        for x in range(0, 4):
            self.pendown()
            for x in range(0, 4):
                self.fd(50)
                self.rt(90)
            self.penup()
            self.fd(70)



# Create Functions


# Initial Game setup
game = spgl.Game(1000, 600, "black", "SPGL Minimum Code Example by /u/wynand1004 AKA @TokyoEdTech")
game.mode = "maze"


#maze functionality
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
]

wall_coordinates = []

def is_wall_collision(sprite, coordinates):
    #uses bounding box from spgl, but takes sprite_2 coordinates from wall_coordinates
    #for some reason it's triggering with -30 as y-cor when it's nowhere near -30. The wall centers should be -70.
    x_collision = (math.fabs(sprite.xcor() - coordinates[0]) * 2) < (sprite.width + 5)
    y_collision = (math.fabs(sprite.ycor() - coordinates[1]) * 2) < (sprite.height + 5)
    return (x_collision and y_collision)


# ---Create Sprites----
#Static objects
menu_borders = Borders("square", "blue", 0, 0)
maze_borders = Borders("square", "red", 0, 0)
maze_borders.set_image("wall_vines5_2.gif", 10, 10)

coffin = Scenery("square", "blue", 200, 200)
coffin.shapesize(5, 10)

red_key = Scenery("turtle", "red", -475, -10)
blue_key = Scenery("turtle", "blue", 470, -15)

#moving objects
player = Player("circle", "red", -475, -90)

master_guard = Enemy("square", "red", False, -315, 90)

guard_1 = Enemy("square", "red", True, 0, -50)
guard_2 = Enemy("square", "red", True, -100, -10)
guard_3 = Enemy("square", "red", True, 50, 70)

menu_borders.draw_borders()
menu_borders.draw_inventory_spaces()

enemies = [master_guard, guard_1, guard_2, guard_3]

#Creates Maze stamps
for y in range(len(maze)):
    for x in range(len(maze[y])):
        screen_x = -490 + (x * 10)
        screen_y = 90 - (y * 10)

        if maze[y][x] == "x":
            maze_borders.goto(screen_x, screen_y)
            maze_borders.stamp()
            #adding coordinates for collision
            wall_coordinates.append((screen_x, screen_y))

# Create Labels
inventory_lbl = spgl.Label("Inventory", "red", -495, -150, font_size=30)
moves_lbl = spgl.Label("Moves", "red", 20, -150, font_size=30)
player_HP_lbl = spgl.Label("Health: {}".format(player.HP), "red", 20, -170, font_size=20)

#Enemy Labels
enemy_name_lbl = spgl.Label("", "red", 300, -150, font_size=30)

game_over_lbl = spgl.Label("", "red", 0, 0, font_size=70)


# Create Buttons
basic_attack = spgl.Button("square", "blue", 40, -200)
basic_attack.shapesize(0.5, 2)

sword_attack = spgl.Button("square", "blue", 40, -220)
sword_attack.shapesize(0.5, 2)

defend = spgl.Button("square", "blue", 40, -240)
defend.shapesize(0.5, 2)

# Set Keyboard Bindings
wn = spgl.turtle.Screen()
#wn.bgpic("background.gif")
wn.onkeypress(player.go_right, "Right")
wn.onkeyrelease(player.stop, "Right")
wn.onkeypress(player.go_left, "Left")
wn.onkeyrelease(player.stop, "Left")
wn.onkeypress(player.go_up, "Up")
wn.onkeyrelease(player.stop, "Up")
wn.onkeypress(player.go_down, "Down")
wn.onkeyrelease(player.stop, "Down")

while True:
    # Call the game tick method
    game.tick()

    
