# SPGL Minimal Code by /u/wynand1004 AKA @TokyoEdTech
# Requires SPGL Version 0.8 or Above
# SPGL Documentation on Github: https://wynand1004.github.io/SPGL
# Use this as the starting point for your own games

# Import SPGL
import spgl
import math


# Create Classes

class Player(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        inventory = []
        HP = 20
        
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

    def tick(self):
        for coordinate in wall_coordinates:
            if is_wall_collision(self, coordinate) == True:
                self.setheading(self.heading() + 180)
                self.fd(3)
                self.stop()

        self.fd(self.speed)
        

class Enemy(spgl.Sprite):
    def __init__(self, shape, color, mobile, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.is_mobile = mobile
        self.collided = False

    def move(self):
        if self.is_mobile == True:
            if self.collided == False:
                pass
            

            

        
    def tick(self):
        self.move()

class Scenery(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        

class Borders(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.penup()
        self.hideturtle()
        self.fd_speed = 10
        self.shapesize(0.5, 0.5, 0)

    
    def draw_borders(self):
        #draw horizontal part
        self.setposition(500, -100)
        self.pendown()
        self.setheading(180)
        self.fd(1000)
    
        #draw vertical part
        self.penup()
        self.setposition(0, -300)
        self.pendown()
        self.setheading(90)
        self.fd(200)



# Create Functions

# Initial Game setup
game = spgl.Game(1000, 600, "black", "SPGL Minimum Code Example by /u/wynand1004 AKA @TokyoEdTech")

#maze functionality
maze = [
"xxxxxxxxxxxxxxxx    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", 
"                          x          x                                                             x",
"                          x          x                                                             x",
"                          x          x                                                             x",
"          xxxxxxxxxxxxxxxxx          xxxxxxxxxxxxxxxxxxxxxx    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx      x",
"          x                                               x    x                                   x",
"          x                                               x    x                                   x",
"          x                                               x    x                                   x",
"xxxx      xxxxxxxxxxxxxxxx      xxxxxxxxxxxxxxxxxxx       x    x      xxxxxxxxxxxxxxxxxxxxxxxxxx   x",
" k x                                              x                                            x   x",
"   x                                              x                                            x   x",
"   x                                              x                                            x k x",
"   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx         xxxxxxxxxx",
"                                                                                                   x",
"                                                                                                   x",
"                                                                                                   x",
"xxxxxxxxxxxxxxxxxx     xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx         xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
"p                                                                                                  x",
"                                                                                                   x",
"                                                                                                   x",
]

wall_coordinates = []

def is_wall_collision(sprite, coordinates):
    #uses bounding box from spgl, but takes sprite_2 coordinates from wall_coordinates
    #for some reason it's triggering with -30 as y-cor when it's nowhere near -30. The wall centers should be -70.
    x_collision = (math.fabs(sprite.xcor() - (coordinates[0] * 2)) < (sprite.width + 5))
    y_collision = (math.fabs(sprite.ycor() - (coordinates[1] * 2)) < (sprite.height + 5))
    if (x_collision and y_collision) == True:
        print(sprite.xcor(), sprite.ycor())
        print(coordinates)
        print(math.fabs(sprite.xcor() - (coordinates[0] * 2)))
        print(math.fabs(sprite.ycor() - (coordinates[1] * 2)))
    return (x_collision and y_collision)


# ---Create Sprites----
#Static objects
menu_borders = Borders("square", "red", 0, 0)
maze_borders = Borders("square", "red", 0, 0)

coffin = Scenery("square", "blue", 200, 200)

#moving objects
player = Player("circle", "red", -485, -90)

master_guard = Enemy("square", "red", False, -320, 90)

guard_1 = Enemy("square", "red", True, 0, -50)
guard_2 = Enemy("square", "red", True, -100, -10)
guard_3 = Enemy("square", "red", True, 50, 70)

menu_borders.draw_borders()

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

print(wall_coordinates)
# Create Labels

# Create Buttons

# Set Keyboard Bindings
wn = spgl.turtle.Screen()
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

    
