# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
FRICTION = .06
start = False
level = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

nebula_info1 = ImageInfo([400,300], [800, 600])
nebula_image1 = simplegui.load_image("http://www.wallpaperfly.com/thumbnails/detail/20120819/outer%20space%20galaxies%20planets%20nebulae%20rings%201600x1200%20wallpaper_www.wallmay.com_12.jpg")

nebula_info2 = ImageInfo([400,300], [800, 600])
nebula_image2 = simplegui.load_image("http://www.wallpaperhi.com/thumbnails/detail/20120208/outer%20space%20stars%20galaxies%20nebulae%20planet%20earth%201600x1200%20wallpaper_www.wallpaperhi.com_61.jpg")

nebula_info3 = ImageInfo([400,300], [800, 600])
nebula_image3 = simplegui.load_image("http://3.bp.blogspot.com/-570Au19Z-nM/TubjuGxrRuI/AAAAAAAADcE/uZZBjuzg1dE/s1600/cat__s_eye_nebula_by_EQDesigns.png")

background_info = [nebula_info, nebula_info1, nebula_info2, nebula_info3]
background_image = [nebula_image, nebula_image1, nebula_image2, nebula_image3]

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0],
                                             self.image_center[1]], self.image_size,
                                                self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                                     self.pos, self.image_size, self.angle)

    def update(self):
        # Angle Update
        self.angle += self.angle_vel
        # Position Update
        self.pos[0] = (self.pos[0] + self.vel[0])% WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1])% HEIGHT
        # Velocity Update
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0]
            self.vel[1] += forward[1]
       # Friction Update
        self.vel[0] *= (1 - FRICTION)
        self.vel[1] *= (1 - FRICTION)
       # Method for keys
        # Right
    def angle_right(self):
        self.angle_vel += .1
        # Left
    def angle_left(self):
        self.angle_vel -= .1
        # Up Thrust Sound
    def thrust_on(self, condition):
        self.thrust = condition
        if condition:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       # Shoot Method
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        mposition = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        mvelocity = [self.vel[0] + 5 * forward[0], self.vel[1] + 5 * forward[1]]
        a_missile = Sprite(mposition, mvelocity, self.angle, 0, missile_image, missile_info, missile_sound) 
        missile_group.add(a_missile)
    

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.age * self.image_size[0]), self.image_center[1]], self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)
    def update(self):
        # Angle Update
        self.angle += self.angle_vel
        # Position Update
        self.pos[0] = (self.pos[0] + self.vel[0])% WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1])% HEIGHT 
        # Life and Age
        self.age += 1
        keep = False
        if self.age >= self.lifespan:
            keep = True
        return keep
        
    def collide(self, other_object):
        collision = False
        # detect collision
        if dist(self.get_position(), other_object.get_position()) < (self.get_radius() + other_object.get_radius()):
            collision = True
        return collision
            
# Key Handlers
def keydown(key):
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_right()
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.angle_left()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_on(True)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
def keyup(key):
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_left()
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.angle_right()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_on(False)

# Mouse handler
def click(pos):
    global start
    [WIDTH / 2, HEIGHT / 2]
    if WIDTH / 4 < pos[0] < WIDTH *3 / 4 and \
       HEIGHT / 4 < pos[1] < HEIGHT *3 / 4:
        start = True
           
def draw(canvas):
    global time, start, lives, score, rock_group, level
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(background_image[level], background_info[level].get_center(), background_info[level].get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    soundtrack.play()
    # Update Game State
    if group_collide(rock_group, my_ship):
        lives -= 1
    if group_group_collide(rock_group, missile_group):
        score += 10
    
    # Update Level
    if score == 500*(level+1):
            level = (level + 1) % 3
    # Lives and Score
    canvas.draw_text("Lives: "+str(lives), [40, 60], 25, "white")
    canvas.draw_text("Score: "+str(score), [WIDTH - 120, 60], 25, "white")
    #Restart
    if lives == 0:
        start = False
        lives = 3
        score = 0
        rock_group = set()
        level = 0
    
    # Start Info
    if not start:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH / 2, HEIGHT / 2])
        soundtrack.rewind()
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group,canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship and sprites
    my_ship.update()
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    # Rock Position and Velocity
    rposition = [random.randrange(0, WIDTH), random.randrange(0,HEIGHT)]
    rvelocity = [random.randrange(0,5),random.randrange(0,5)]
    rangle = random.random() * .3 - .2
    a_rock = Sprite(rposition, rvelocity, 0, rangle, asteroid_image, asteroid_info)
    if len(rock_group)<12 and start:
        #not to spawn on the ship position
        if(dist(a_rock.get_position(), my_ship.get_position())) > (a_rock.get_radius() + 2*my_ship.get_radius()):
            rock_group.add(a_rock)
            
# Helper Functions
def process_sprite_group(sprite_group, canvas):
    for sprite in set(sprite_group):
        sprite.draw(canvas)
        if sprite.update():
            sprite_group.remove(sprite)

def group_collide(group, other_object):
    collision = False
    copy_group = set(group)
    for copy in copy_group:
        if copy.collide(other_object):
            collision = True
            group.remove(copy) 
            explosion = Sprite(copy.get_position(),[0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
    return collision

def group_group_collide(group1, group2):
    collision = False
    copy_group = set(group2)
    for copy in copy_group:
        if group_collide(group1, copy):
            group2.remove(copy)
            collision = True
    return collision
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
missile_group = set([])
rock_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)


timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
