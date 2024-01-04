from config import *
from random import randint

class PipeSet(pygame.sprite.Sprite):
  def __init__(self, image, id, x):
    super().__init__()
    self.image = image
    self.id = id
    self.x = x
    self.y = randint(-450, -100)
    self.render()
  
  def render(self):
    screen.blit(self.image, pygame.Rect(self.x, self.y, 16, 16))
    
  def update_collisions(self):
    self.top_hitbox = pygame.Rect(self.x+10, self.y+650, self.image.get_width()-20, 700)
    self.bottom_hitbox = pygame.Rect(self.x+10, self.y-200, self.image.get_width()-20, 700)
    return self.top_hitbox, self.bottom_hitbox

  def point_box(self):
    self.point_hitbox = pygame.Rect(self.x+60, self.y+500, 10, 150)
    return self.point_hitbox
    
    
    

    