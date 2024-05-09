import pygame.font

class Buttom:
    def __init__(self, ai_game, msg):
        """Inicia os atributos do botão."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Define as dimensões e propriedades do botão.
        self.width, self.height = 200, 50
        self.buttom_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Construa o botão como um objeto rect e centralize o botão.
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # A mensagem do botão precisa ser preparada apenas uma vez.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Transforme a msg numa imagem renderizada e centralize o texto sobre o botão."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.buttom_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_buttom(self):

        # Desenhe um botão vazio em seguida desenha a mensagem.
        self.screen.fill(self.buttom_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
