from config import *
from time import sleep
from random import shuffle
from Sprites.pipe_set import PipeSet
from Sprites.bird import Bird
from Sprites.floor import Floor
from Sprites.skyline import Skyline

def generate_pipe(screen_width, id):
  return PipeSet(pygame.image.load('assets/pipeset.png'), id, (screen_width+100))

def generate_floor(screen_width, x=None):
  if not x:
    x = screen_width+400 
  return Floor(pygame.image.load('assets/ground.png'), x)

def generate_skyline(screen_width, x=None):
  if not x:
    x = screen_width+400 
  return Skyline(pygame.image.load('assets/skyline.png'), x)

# Sprites
floor_tiles = [generate_floor(screen.get_width(), 20), generate_floor(screen.get_width(), 350), generate_floor(screen.get_width(), 685), generate_floor(screen.get_width())]
pipes = [generate_pipe(screen.get_width(), 1)]
bird = Bird(pygame.image.load('assets/bird.png'), (screen.get_height()/2))
sky_tiles = [generate_skyline(screen.get_width(), -1), generate_skyline(screen.get_width(), 330)]


# Font
font = pygame.font.Font('assets/fonts/CONSOLA.TTF', 20)
theme_font = pygame.font.Font('assets/fonts/theme_font.otf', 60)


# Sound effects
pygame.mixer.init()
wing = pygame.mixer.Sound("assets/sfx/wing.mp3")
die = pygame.mixer.Sound("assets/sfx/die.mp3")
point = pygame.mixer.Sound("assets/sfx/point.mp3")
collide = pygame.mixer.Sound("assets/sfx/collide.mp3")
death = pygame.mixer.Sound("assets/sfx/death.mp3")
rage = pygame.mixer.Sound("assets/sfx/rage.mp3")


# Runtime variables
flap_sounds = [wing]
exit = False
deaths = 0
pipes_created = 1
menu = True
ticks_since_death = 0
lvl_reset = False
jump_v = 5
alive = True
show_hitboxes = False
score = 0
point_collected = False


while not exit: # Game ticks!
  dt = clock.tick(fps) # set fps
  screen.fill('#48c0cc')
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_BACKSPACE:
        exit = True
      elif event.type == QUIT:
        exit = True
      if event.key == K_z:
        if show_hitboxes:
          show_hitboxes = False
        else:
          show_hitboxes = True
      if menu and event.key == K_SPACE:
        
        menu = False          #
        lvl_reset = False     #
        alive = True          # Reseting game variables
        score = 0             #
        time_since_death = 0  # 
        
        flap_sounds[0].play()         
        bird.v = jump_v + bird.v * 0.2
        
      if not menu:
        if event.key == K_TAB: # Jump!
          bird.y = 50
          bird.v = 0
        if alive:
          if event.key == K_SPACE: # Jump!
            if bird.y > -10:  
              flap_sounds[0].play()         
              bird.v = 5 + bird.v * 0.2
      else:
        lvl_reset = False
  
  
  # Skyline
  if sky_tiles[len(sky_tiles)-1].x <= screen.get_width()-334:
    sky_tiles.append(generate_skyline(screen.get_width(), screen.get_width()))
  
  for sky_tile in sky_tiles:
    sky_tile.render() 
    if alive:
      sky_tile.x -= dt * 0.001
    # Skyline culling
    if sky_tile.x < -800:
      sky_tiles.pop(0)
  
  
  # Menu      
  if menu:
    image = pygame.image.load('assets/logo.png')
    screen.blit(image, pygame.Rect(145, 280, 160, 160))
  
  
  # Pipes
  if lvl_reset:
    for pipe in pipes:
      if pipe.x > screen.get_width():
        pipes.pop(0)
      else:
        pipe.x += dt*3
        pipe.render()
        
    if len(pipes) == 0:
      lvl_reset = True
      pipes.append(generate_pipe(screen.get_width(), pipes_created))
      
  else:
    if pipes[len(pipes)-1].x <= (screen.get_width()-300):
      pipes.append(generate_pipe(screen.get_width(), pipes_created))
      pipes_created += 1
      point_collected = False
    
    for pipe_set in pipes:
      pipe_set.render()
      if alive:
        if not menu:
          pipe_set.x -= dt * 0.2
      # Pipe culling
      if pipe_set.x < -600:
        pipes.pop(0)
      # Pipe Hitboxes
      pipe_hitboxes = pipe_set.update_collisions()
      point_box = pipe_set.point_box()
      if point_box.colliderect(bird.update_collisions()) and alive and not point_collected:
        score += 1
        point.play()
        point_collected = True
    
      if show_hitboxes:
        pygame.draw.rect(screen, (255,0,0), pipe_hitboxes[0], 4)
        pygame.draw.rect(screen, (255,0,0), pipe_hitboxes[1], 4)
        pygame.draw.rect(screen, (255,255,0), point_box, 4)
   
      
  # Bird
  bird.render()
  if lvl_reset:
    if bird.y >= 300:
      bird.y -= dt*1.5
      bird.v = 0
      menu = True
      ticks_since_death = 0
    else:
      alive = True
      menu = True
  else: 
    var = True
    bird_hitbox = bird.update_collisions()
    for floor_tile in floor_tiles:
      if floor_tile.update_collisions().colliderect(bird_hitbox):
        bird.v = 0
        var = False
    if var:
      if not menu:
        bird.y -= bird.v
        bird.v -= 0.010 * dt
    
    if show_hitboxes:
      pygame.draw.rect(screen, (0,0,255), bird_hitbox, 4)


  # Floor
  if floor_tiles[len(floor_tiles)-1].x <= (screen.get_width()+112):
    floor_tiles.append(generate_floor(screen.get_width()))
  
  for floor_tile in floor_tiles:
    floor_tile.render() 
    if alive:
      floor_tile.x -= dt * 0.2
    else:
      ticks_since_death += 1
    # Floor tile culling
    if floor_tile.x < -800:
      floor_tiles.pop(0)
    # Floor Hitboxes
    floor_hitbox = floor_tile.update_collisions()
    if show_hitboxes:
      pygame.draw.rect(screen, (0,255,0), floor_hitbox, 4)
  
  
  # Collisions
  for pipe_set in pipes:
    pipe_hitbox = pipe_set.update_collisions()
    if bird_hitbox.colliderect(pipe_hitbox[0]) or bird_hitbox.colliderect(pipe_hitbox[1]):
      if alive:
        die.play()
        collide.play()
        deaths += 1
      alive = False
      
      
  for floor_tile in floor_tiles:
    floor_hitbox = floor_tile.update_collisions()
    if bird_hitbox.colliderect(floor_hitbox):
      if alive and not menu:
        die.play()
        death.play()
        alive = False 

  if not alive and ticks_since_death >= clock.get_fps()*10 and lvl_reset == False:
    lvl_reset = True
    ticks_since_death = 0
    
  
  # Score counter
  if not menu:
    score_counter = theme_font.render(f"""{score}""", True, '#ffffff')
    screen.blit(score_counter, (270, 100))
  

  # Frames per second counter + debug
  fps_metre = font.render(f"""FPS {round(clock.get_fps())}    Deaths {deaths}""", True, '#ffffff')
  fpsRect = fps_metre.get_rect()
  screen.blit(fps_metre, fpsRect)
  
  if deaths == 5:
    rage.play()
    deaths = 0

  pygame.display.flip() # display the frame