from config import *

class Skyline(pygame.sprite.Sprite):
  def __init__(self, image, x):
    super().__init__()
    self.image = image
    self.y = 120
    self.x = x
    self.render()
  
  def render(self):
    screen.blit(self.image, pygame.Rect(self.x, self.y, 16, 16))