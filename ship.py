import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Uma classe para modelar a nave"""

    def __init__(self, ai_game):
        """Inicializa a nava e define sua posição inicial."""
        super().__init__()

        """Inicia a nave pegando sua posição inicial."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings        
        self.screen_rect = ai_game.screen.get_rect()

        # Carrega a imagem da nave e passe sendo como um rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Começa o jogo com cada nova nave no meio da tela
        self.rect.midbottom = self.screen_rect.midbottom

        # Armazena um valor decimal para a nave em posição horizontal.
        self.x = float(self.rect.x)

        # Flag de Movimento.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Atualiza a nave baseando-se na flag de movimento."""

        # Atualiza o valor de x da nave e não o rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Atualiza o objeto rect de self.x
        self.rect.x = self.x

    def blitme(self):
        """Desenha a nave na sua posição atual."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centraliza a nave na tela."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
