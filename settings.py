class Settings:
    """Uma classe que armazena todas as configurações de Alien Invasion"""

    def __init__(self):
        """Inicia as configurações do jogo"""

        # Configurações de tela
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Configurações da nave.
        self.ship_limit = 3

        # Configurações da Bala
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 3

        # Configurações do Alien
        self.fleet_drop_speed = 10
        
        # Define a rapidez com que o jogo acelera.
        self.speedup_scale = 1.1

        # Define quão rápido os valores dos pontos alienígenas aumentam.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicia as configurações que mudam ao longo do jogo."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction = 1 representa direita, -1 representa esquerda
        self.fleet_direction = 1

        # Pontuação
        self.alien_points = 50

    def increase_speed(self):
        """Aumentar as configurações de velocidade."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
