from config import *

class Floor(pygame.sprite.Sprite):
  def __init__(self, image, x):
    super().__init__()
    self.image = image
    self.y = 600
    self.x = x
    self.render()
  
  def render(self):
    screen.blit(self.image, pygame.Rect(self.x, self.y, 16, 16))
    #,pygame.Rect(self.x, self.y, 0, 0)
  
  def update_collisions(self):
    return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())