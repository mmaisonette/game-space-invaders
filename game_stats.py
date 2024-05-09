class GameStats:
    """Monitore estatísticas sobre Alien Invasion."""
    def __init__(self, ai_game):
        """Inicia estatísticas."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Inicia Alien Invasion no estado ativo.
        self.game_active = False

        # A pontuação mais alta nunca deve ser zerada.
        self.high_score = 0

    def reset_stats(self):
        """Inicia as configurações que mudam ao longo do jogo."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
