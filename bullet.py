import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Uma classe para interpretar as balas atiradas da nave."""

    def __init__(self, ai_game):
        """Cria um objeto para a bala na posição atual da nave."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Cria um rect da bala em (0,0) e define a posição correta.
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Armazena a posição da bala como um valor decimal.
        self.y = float(self.rect.y)

    def update(self):
        """Move a bala para cima da tela."""

        # Atualiza a posição decimal da bala.
        self.y -= self.settings.bullet_speed

        # Atualiza a posição de rect.
        self.rect.y = self.y

    def draw_bullet(self):
        """Desenha a bala para a tela."""
        pygame.draw.rect(self.screen, self.color, self.rect)
