# SPGL Minimal Code by /u/wynand1004 AKA @TokyoEdTech
# Requires SPGL Version 0.8 or Above
# SPGL Documentation on Github: https://wynand1004.github.io/SPGL
# Use this as the starting point for your own games

# Import SPGL
import spgl

# Create Classes

class Player(spgl.Sprite):
     def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        inventory = []
        HP = 20

class Enemy(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)

    

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

# Create Sprites
menu_borders = Borders("square", "red", 0, 0)
maze_borders = Borders("square", "red", 0, 0)

player = Player("circle", "red", -485, -90)

master_guard = Enemy("square", "red", -320, 90)

guard_1 = Enemy("square", "red", 0, -50)
guard_2 = Enemy("square", "red", -100, -10)
guard_3 = Enemy("square", "red", 50, 70)

menu_borders.draw_borders()

#Creates Maze sprites

for y in range(len(maze)):
    for x in range(len(maze[y])):
        screen_x = -490 + (x * 10)
        screen_y = 90 - (y * 10)

        if maze[y][x] == "x":
            maze_borders.goto(screen_x, screen_y)
            maze_borders.stamp()


# Create Labels

# Create Buttons

# Set Keyboard Bindings

while True:
    # Call the game tick method
    game.tick()
