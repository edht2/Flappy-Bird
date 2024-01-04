from config import *

class Bird(pygame.sprite.Sprite):
  def __init__(self, image, y):
    super().__init__()
    self.image = image
    self.x = screen.get_width()/2-50
    self.y = y
    self.v = 0
    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = y
    self.render()
  
  def render(self):
    self.rect.x = self.x
    self.rect.y = self.y
    image = pygame.transform.rotate(self.image, self.v*5+15)
    screen.blit(image, image.get_rect(center=self.rect.center))
    #,pygame.Rect(self.x, self.y, 0, 0)
  
  def update_collisions(self):
    return pygame.Rect(self.x+4, self.y+84, self.image.get_width()-10, self.image.get_height()-168)
    #return self.image.get_rect()