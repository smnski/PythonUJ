import pygame
import sys

# Constants
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0, 128)
RED = (255, 0, 0, 128)

COLS = ROWS = 10
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

class WelcomeScreen:
    WIDTH = 800
    HEIGHT = 600
    BUTTON_WIDTH = 300
    BUTTON_HEIGHT = 50

    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def place_ships_yourself(self):
        WIDTH, HEIGHT = 500, 550
        ROWS, COLS = 10, 10
        SQUARE_SIZE = WIDTH // COLS

        ships = {
            "carrier": 5,
            "battleship": 4,
            "cruiser": 3,
            "submarine": 3,
            "destroyer": 2,
        }
        remaining_ships = list(ships.items())
        
        current_ship_index = 0
        horizontal = True
        preview_pos = None

        def can_place_ship(board, row, col, length, horizontal):
            if horizontal:
                if col + length > COLS:
                    return False
                return all(board[row][col + i] == 0 for i in range(length))
            else:
                if row + length > ROWS:
                    return False
                return all(board[row + i][col] == 0 for i in range(length))

        def place_ship(board, row, col, length, horizontal):
            if horizontal:
                for i in range(length):
                    board[row][col + i] = 1
            else:
                for i in range(length):
                    board[row + i][col] = 1

        grid_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Place Ships")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and remaining_ships:
                    x, y = event.pos
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    ship_name, ship_length = remaining_ships[current_ship_index]

                    if can_place_ship(board, row, col, ship_length, horizontal):
                        place_ship(board, row, col, ship_length, horizontal)
                        current_ship_index += 1

                        if current_ship_index >= len(remaining_ships):
                            remaining_ships.clear()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        horizontal = not horizontal

                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    preview_pos = (row, col)

            grid_screen.fill(WHITE)

            for row in range(ROWS):
                for col in range(COLS):
                    color = BLUE if board[row][col] == 1 else GRAY
                    pygame.draw.rect(
                        grid_screen,
                        color,
                        (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    )
                    pygame.draw.rect(
                        grid_screen,
                        WHITE,
                        (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                        1
                    )

            if remaining_ships and preview_pos:
                ship_name, ship_length = remaining_ships[current_ship_index]
                row, col = preview_pos
                valid = can_place_ship(board, row, col, ship_length, horizontal)
                highlight_color = GREEN if valid else RED

                for i in range(ship_length):
                    if horizontal:
                        rect = ((col + i) * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    else:
                        rect = (col * SQUARE_SIZE, (row + i) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    if (0 <= col + i < COLS and 0 <= row < ROWS) or (0 <= col < COLS and 0 <= row + i < ROWS):
                        pygame.draw.rect(grid_screen, highlight_color, rect)

            if remaining_ships:
                ship_name, ship_length = remaining_ships[current_ship_index]
                placing_text = self.font.render(f"Placing: {ship_name} ({ship_length})", True, BLACK)
                rotate_text = self.font.render("Press R to rotate", True, BLACK)

                grid_screen.blit(placing_text, (WIDTH // 2 - placing_text.get_width() // 2, HEIGHT - 40))
                grid_screen.blit(rotate_text, (WIDTH // 2 - rotate_text.get_width() // 2, HEIGHT - 20))

            pygame.display.flip()

        pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def option2(self):
        print("Option 2: Auto place ships")

    def drawButton(self, text, x, y, color):
        pygame.draw.rect(self.screen, color, (x, y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x + self.BUTTON_WIDTH // 2, y + self.BUTTON_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    if (self.WIDTH // 2 - self.BUTTON_WIDTH // 2 <= x <= self.WIDTH // 2 + self.BUTTON_WIDTH // 2 and
                        self.HEIGHT // 3 - self.BUTTON_HEIGHT // 2 <= y <= self.HEIGHT // 3 + self.BUTTON_HEIGHT // 2):
                        self.place_ships_yourself()

                    if (self.WIDTH // 2 - self.BUTTON_WIDTH // 2 <= x <= self.WIDTH // 2 + self.BUTTON_WIDTH // 2 and
                        2 * self.HEIGHT // 3 - self.BUTTON_HEIGHT // 2 <= y <= 2 * self.HEIGHT // 3 + self.BUTTON_HEIGHT // 2):
                        self.option2()

            self.screen.fill(WHITE)
            self.drawButton("Place ships yourself",
                            self.WIDTH // 2 - self.BUTTON_WIDTH // 2,
                            self.HEIGHT // 3 - self.BUTTON_HEIGHT // 2,
                            GRAY)
            self.drawButton("Auto place ships",
                            self.WIDTH // 2 - self.BUTTON_WIDTH // 2,
                            2 * self.HEIGHT // 3 - self.BUTTON_HEIGHT // 2,
                            GRAY)
            pygame.display.flip()

if __name__ == "__main__":
    welcome_screen = WelcomeScreen()
    welcome_screen.run()
    pygame.quit()
    sys.exit()
