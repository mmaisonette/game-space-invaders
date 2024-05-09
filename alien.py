import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Uma classe para representar um único alien no esquadrão."""

    def __init__(self, ai_game):
        """Inicia o alien e define sua posição inicial."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Carrega a imagem do alien e define o atributo rect.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Inicia cada alien novo próximo do topo esquerdo da tela.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def check_edges(self):
        """Retorna True se o alien estiver na borda da tela."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Mova o alien para a direita ou esquerda."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
