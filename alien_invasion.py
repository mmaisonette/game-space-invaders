from ast import alias
import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from buttom import Buttom
from scoreboard import Scoreboard

class AlienInvasion:
    """Classe criada para controlar o comportamento do jogo"""

    def __init__(self):
        """Função responsável por iniciar o jogo e criar recursos no game"""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Cria uma instância para armazenar estatísticas do jogo.
        # e cria um placar.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Cria uma instância para armazenar estatísticas do jogo.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Cria o botão Play.
        self.play_buttom = Buttom(self, "Play")

    def run_game(self):
        """Inicia o loop principal do nosso jogo"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._udpate_screen()

    def _check_events(self):
        """Responde a teclas do teclado e eventos do mouse."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_buttom(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_buttom(self, mouse_pos):
        """Começa um novo jogo quando o jogador clicar em Play."""
        buttom_clicked = self.play_buttom.rect.collidepoint(mouse_pos)
        if buttom_clicked and not self.stats.game_active:

            # Redefina as configurações do jogo.
            self.settings.initialize_dynamic_settings()

            # Reinicia as estatísticas do jogo.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()

            # Se desfaz dos aliens e balas restantes.
            self.aliens.empty()
            self.bullets.empty()

            # Cria um novo esquadrão e centraliza a nave.
            self._create_fleet()
            self.ship.center_ship()

            # Oculta o cursor do mouse.
            pygame.mouse.set_visible(False)

            self.sb.prep_ships()

    def _check_keydown_events(self, event):
        """Responde a teclas do teclado."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Responde a teclas do teclado liberadas."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Cria uma nova bala e adiciona ao grupo de balas."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Atualiza a posição das balas e se desfaz das antigas."""

        # Atualiza a posição das balas.
        self.bullets.update()

        # Se desfaz das balas que desapareceram.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Responde a colisões entre bala-alien."""

        # Remove qualquer bala e alien que se colidiram.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += self.settings.alien_points * len(self.aliens)
            self.sb.prep_score
            self.sb.check_high_score()

        if not self.aliens:

            # Destroi balas existentes e cria um novo esquadrão.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Aumenta o level.
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Responde quando a nave é atingida por um alien."""
        if self.stats.ships_left > 0:

            # Decrementa ships_left e atualiza pontuação.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Se desfaz de qualquer alien e bala restante.
            self.aliens.empty()
            self.bullets.empty()

            # Cria um novo esquadrão e centraliza a nave.
            self._create_fleet()
            self.ship.center_ship()

            # Pausa.
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Cria um novo esquadrão de aliens."""

        # Cria um alien e procura o número de aliens na fila.
        # Espaçamento entre cada alien é igual a uma largura do alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determina o número de fileiras de aliens que cabem na tela.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Cria a primeira fileira de aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Cria um alien e coloca na fileira."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Responde aproximadamente se algum alien atingiu uma borda."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Larga todo esquadrão e muda a direção do esquadrão."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Atualiza a posição de todos os aliens no esquadrão."""
        """Checa se o esquadrão está numa borda, então atualiza as posições 
        de todos os aliens no esquadrão."""
        self._check_fleet_edges()
        self.aliens.update()

        # Procura por colisões entre alien-nave.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Procura por aliens atingindo a parte inferior da tela.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Verifica se algum alien atingiu a parte inferior da tela."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:

                # Trate da mesma forma como se a nave fosse atingida.
                self._ship_hit()
                break

    def _udpate_screen(self):
        """Atualiza imagens na tela, e gira para a nova tela."""
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Desenha as informações da pontuação. Quadro de pontuação.
        self.sb.show_score()

        # Desenha o botão play se o jogo está inativo.
        if not self.stats.game_active:
            self.play_buttom.draw_buttom()

        # Tornar visível a tela desenhada mais recentemente.
        pygame.display.flip()

if __name__ == '__main__':

    # Crie uma instância e inicie o jogo
    ai = AlienInvasion()
    ai.run_game()
