import pygame


class Game:
    """
    Game class containing the game loop

    === Attributes ===
    done: whether the game loop is done
    """

    done: bool

    def __init__(self, width: int, height: int) -> None:
        """
        Initializer
        """

        pygame.init()

        self.done = False
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        # can set title later

    def run_game_loop(self) -> None:
        """
        Runs the game loop

        :return:
        """

        while not self.done:
            # fill the screen
            self.screen.fill((255, 255, 255))

            # update display
            pygame.display.flip()
            self.clock.tick(60)
