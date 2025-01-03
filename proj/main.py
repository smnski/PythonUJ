import pygame
import sys
import os
import random

# Constants
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0, 128)
RED = (255, 0, 0, 128)
DARK_GREEN = (1, 50, 32)

COLS = ROWS = 10
player_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
enemy_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

class WelcomeScreen:
    WIDTH = 800
    HEIGHT = 600
    BUTTON_WIDTH = 300
    BUTTON_HEIGHT = 50

    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.ships = {
            "carrier": { "symbol": "c", "size": 5 },
            "battleship": { "symbol": "b", "size": 4 },
            "cruiser": { "symbol": "r", "size": 3 },
            "submarine": { "symbol": "s", "size": 3 },
            "destroyer": { "symbol": "d", "size": 2 },
        }

    @staticmethod
    def canPlaceShip(board, row, col, length, horizontal):
        if horizontal:
            if col + length > COLS:
                return False
            return all(board[row][col + i] == 0 for i in range(length))
        else:
            if row + length > ROWS:
                return False
            return all(board[row + i][col] == 0 for i in range(length))

    @staticmethod
    def placeShip(board, row, col, length, horizontal, symbol):
        if horizontal:
            for i in range(length):
                board[row][col + i] = symbol
        else:
            for i in range(length):
                board[row + i][col] = symbol

    def startGameplay(self):
        gameplay = Gameplay()
        gameplay.run()

    def placeShipsYourself(self):
        GRID_WIDTH, GRID_HEIGHT = 500, 500
        TEXT_HEIGHT = 50
        DISPLAY_HEIGHT = GRID_HEIGHT + TEXT_HEIGHT
        ROWS, COLS = 10, 10
        SQUARE_SIZE = GRID_WIDTH // COLS

        remaining_ships = list(self.ships.items())
        
        current_ship_index = 0
        horizontal = True
        preview_pos = None

        grid_screen = pygame.display.set_mode((GRID_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("Place Ships")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Placing ships down with clicks
                if event.type == pygame.MOUSEBUTTONDOWN and remaining_ships:
                    x, y = event.pos
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    if y < GRID_HEIGHT:  # Ignore clicks in the text area
                        ship_name, ship_data = remaining_ships[current_ship_index]
                        ship_symbol = ship_data["symbol"]
                        ship_length = ship_data["size"]
                        if self.canPlaceShip(player_board, row, col, ship_length, horizontal):
                            self.placeShip(player_board, row, col, ship_length, horizontal, ship_symbol)
                            current_ship_index += 1

                            # If no more ships to place, start gameplay
                            if current_ship_index >= len(remaining_ships):
                                remaining_ships.clear()
                                self.startGameplay()
                                return

                # Rotate ships with "r" key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        horizontal = not horizontal

                # Track mouse position and square clicked
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    preview_pos = (row, col)

            grid_screen.fill(WHITE)

            # Draw grid for placing ships
            for row in range(ROWS):
                for col in range(COLS):
                    color = BLUE if player_board[row][col] != 0 else GRAY
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

            # Draw preview of placed ships
            if remaining_ships and preview_pos:
                ship_name, ship_data = remaining_ships[current_ship_index]
                ship_length = ship_data["size"]
                row, col = preview_pos
                valid = self.canPlaceShip(player_board, row, col, ship_length, horizontal)
                highlight_color = GREEN if valid else RED

                for i in range(ship_length):
                    if horizontal:
                        rect = ((col + i) * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    else:
                        rect = (col * SQUARE_SIZE, (row + i) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    if (0 <= col + i < COLS and 0 <= row < ROWS) or (0 <= col < COLS and 0 <= row + i < ROWS):
                        pygame.draw.rect(grid_screen, highlight_color, rect)

            # Draw info text
            if remaining_ships:
                ship_name, ship_data = remaining_ships[current_ship_index]
                ship_length = ship_data["size"]
                placing_text = self.font.render(f"Placing: {ship_name} ({ship_length})", True, BLACK)
                rotate_text = self.font.render("Press R to rotate", True, BLACK)

                grid_screen.blit(placing_text, (GRID_WIDTH // 2 - placing_text.get_width() // 2, GRID_HEIGHT + 5))
                grid_screen.blit(rotate_text, (GRID_WIDTH // 2 - rotate_text.get_width() // 2, GRID_HEIGHT + 25))

            pygame.display.flip()

        pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def autoPlaceShips(self, board):
        remaining_ships = list(self.ships.items())

        while remaining_ships:
            ship_name, ship_data = remaining_ships.pop()
            ship_symbol = ship_data["symbol"]
            ship_length = ship_data["size"]
            placed = False

            while not placed:
                horizontal = random.choice([True, False])
                if horizontal:
                    row = random.randint(0, ROWS - 1)
                    col = random.randint(0, COLS - ship_length)
                else:
                    row = random.randint(0, ROWS - ship_length)
                    col = random.randint(0, COLS - 1)

                if self.canPlaceShip(board, row, col, ship_length, horizontal):
                    self.placeShip(board, row, col, ship_length, horizontal, ship_symbol)
                    placed = True

        # If finished placing ships for player, start the game
        if board is player_board:
            self.startGameplay()

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
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    # "Place ships yourself" button is pressed
                    if (self.WIDTH // 2 - self.BUTTON_WIDTH // 2 <= x <= self.WIDTH // 2 + self.BUTTON_WIDTH // 2 and
                        self.HEIGHT // 3 - self.BUTTON_HEIGHT // 2 <= y <= self.HEIGHT // 3 + self.BUTTON_HEIGHT // 2):
                        self.autoPlaceShips(enemy_board)
                        self.placeShipsYourself()

                    # "Auto place ships" button is pressed
                    if (self.WIDTH // 2 - self.BUTTON_WIDTH // 2 <= x <= self.WIDTH // 2 + self.BUTTON_WIDTH // 2 and
                        2 * self.HEIGHT // 3 - self.BUTTON_HEIGHT // 2 <= y <= 2 * self.HEIGHT // 3 + self.BUTTON_HEIGHT // 2):
                        self.autoPlaceShips(enemy_board)
                        self.autoPlaceShips(player_board)

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

class Gameplay:
    # Constants
    WIDTH = 1200
    HEIGHT = 700

    GRID_WIDTH, GRID_HEIGHT = 500, 500
    ROWS, COLS = 10, 10
    SQUARE_SIZE = GRID_WIDTH // COLS

    UNDISCOVERED = 0
    DISCOVERED_MISS = 1
    DISCOVERED_HIT = 2
    SUNK = 3

    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Gameplay")
        self.font = pygame.font.Font(None, 36)
        self.player_hit_board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.enemy_hit_board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.remaining_hp_player = {
            "carrier": 5,
            "battleship": 4,
            "cruiser": 3,
            "submarine": 3,
            "destroyer": 2,
        }
        self.remaining_hp_enemy = {
            "carrier": 5,
            "battleship": 4,
            "cruiser": 3,
            "submarine": 3,
            "destroyer": 2,
        }

    def drawPlayerGrid(self, x_offset, y_offset, title, hit_board):
        title_surface = self.font.render(title, True, BLACK)
        title_rect = title_surface.get_rect(center=(x_offset + self.GRID_WIDTH // 2, y_offset - 20))
        self.screen.blit(title_surface, title_rect)

        for row in range(self.ROWS):
            for col in range(self.COLS):
                rect = pygame.Rect(
                    x_offset + col * self.SQUARE_SIZE,
                    y_offset + row * self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                )

                # Game basic grid
                if player_board[row][col] != 0:
                    color = DARK_GREEN
                else:
                    color = GRAY
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

                # Hits overlay
                if hit_board[row][col] == self.DISCOVERED_MISS:
                    color = DARK_GRAY
                elif hit_board[row][col] == self.DISCOVERED_HIT:
                    color = BLUE
                elif hit_board[row][col] == self.SUNK:
                    color = RED
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

    def drawEnemyGrid(self, x_offset, y_offset, title, hit_board, highlight_pos=None):
        title_surface = self.font.render(title, True, BLACK)
        title_rect = title_surface.get_rect(center=(x_offset + self.GRID_WIDTH // 2, y_offset - 20))
        self.screen.blit(title_surface, title_rect)

        for row in range(self.ROWS):
            for col in range(self.COLS):
                rect = pygame.Rect(
                    x_offset + col * self.SQUARE_SIZE,
                    y_offset + row * self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                )

                color = GRAY # default
                if hit_board[row][col] == self.UNDISCOVERED:
                    color = GRAY
                elif hit_board[row][col] == self.DISCOVERED_MISS:
                    color = DARK_GRAY
                elif hit_board[row][col] == self.DISCOVERED_HIT:
                    color = BLUE
                elif hit_board[row][col] == self.SUNK:
                    color = RED
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

                if highlight_pos == (row, col):
                    pygame.draw.rect(self.screen, GREEN, rect, 3)

    def markRemainingSunkSquares(self, board, hit_board, symbol):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if board[row][col] == symbol:
                    hit_board[row][col] = self.SUNK

    def handleHit(self, row, col, board, hit_board, remaining_hp):

        def handleShipHit(name, symbol):
            remaining_hp[name] -= 1
            if remaining_hp[name] <= 0:
                self.markRemainingSunkSquares(board, hit_board, symbol)
            else:
                hit_board[row][col] = self.DISCOVERED_HIT

        if hit_board[row][col] == self.UNDISCOVERED:
            if board[row][col] == 0:
                hit_board[row][col] = self.DISCOVERED_MISS
            else:
                ship_type = board[row][col]
                if ship_type == "c":
                    handleShipHit("carrier", "c")
                elif ship_type == "b":
                    handleShipHit("battleship", "b")
                elif ship_type == "r":
                    handleShipHit("cruiser", "r")
                elif ship_type == "s":
                   handleShipHit("submarine", "s")
                elif ship_type == "d":
                   handleShipHit("destroyer", "d")

        if(self.isGameOver()): self.handleGameOver()
        return True

    def handleClickOnEnemyGrid(self, x, y, x_offset, y_offset):
        col = (x - x_offset) // self.SQUARE_SIZE
        row = (y - y_offset) // self.SQUARE_SIZE

        out_of_bounds = not (0 <= row < self.ROWS and 0 <= col < self.COLS)
        already_discovered = self.enemy_hit_board[row][col] == self.DISCOVERED_HIT or self.enemy_hit_board[row][col] == self.DISCOVERED_MISS or self.enemy_hit_board[row][col] == self.SUNK
        if out_of_bounds or already_discovered:
            return False

        return self.handleHit(row, col, enemy_board, self.enemy_hit_board, self.remaining_hp_enemy)
    
    def selectionAI(self, hit_board):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def is_valid(row, col):
            return 0 <= row < self.ROWS and 0 <= col < self.COLS and hit_board[row][col] == self.UNDISCOVERED

        def follow_direction(row, col, direction):
            dr, dc = direction
            while is_valid(row + dr, col + dc):
                row += dr
                col += dc
                if hit_board[row][col] == self.UNDISCOVERED:
                    return row, col
            return None

        # Search for a direction to follow if there's a hit
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if hit_board[row][col] == self.DISCOVERED_HIT:
                    for dr, dc in directions:
                        new_shot = follow_direction(row, col, (dr, dc))
                        if new_shot:
                            return new_shot

        # If no directions to follow, find an adjacent undiscovered square
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if hit_board[row][col] == self.DISCOVERED_HIT:
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        if is_valid(new_row, new_col):
                            return new_row, new_col

        # Fallback to random selection
        undiscovered = [(r, c) for r in range(self.ROWS) for c in range(self.COLS) if hit_board[r][c] == self.UNDISCOVERED]
        if undiscovered:
            return random.choice(undiscovered)
        
        raise ValueError("No valid moves left. Board state might be corrupted.")

    def isGameOver(self):
        total_hp_enemy = sum(self.remaining_hp_enemy.values())
        total_hp_player = sum(self.remaining_hp_player.values())

        return total_hp_enemy <= 0 or total_hp_player <= 0

    def handleGameOver(self):
        pygame.quit()
        winner = "Player" if sum(self.remaining_hp_enemy.values()) == 0 else "Enemy"

        pygame.init()
        winner_screen = pygame.display.set_mode((400, 200))
        pygame.display.set_caption("Game Over")
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"{winner} Wins!", True, BLACK)
        text_rect = text_surface.get_rect(center=(200, 100))
        
        running = True
        while running:
            winner_screen.fill(WHITE)
            winner_screen.blit(text_surface, text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
        sys.exit()

    def run(self):
        running = True
        player_turn = True

        enemy_grid_x_offset = self.WIDTH - self.GRID_WIDTH - 50
        enemy_grid_y_offset = 100
        highlight_pos = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Clicking on enemy grid
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if enemy_grid_x_offset <= x < enemy_grid_x_offset + self.GRID_WIDTH and \
                            enemy_grid_y_offset <= y < enemy_grid_y_offset + self.GRID_HEIGHT:
                        player_turn = not self.handleClickOnEnemyGrid(x, y, enemy_grid_x_offset, enemy_grid_y_offset)

                if not player_turn:
                    row, col = self.selectionAI(self.player_hit_board)
                    self.handleHit(row, col, player_board, self.player_hit_board, self.remaining_hp_player)
                    player_turn = True

                # Tracking mouse position and highlighting target
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if enemy_grid_x_offset <= x < enemy_grid_x_offset + self.GRID_WIDTH and \
                            enemy_grid_y_offset <= y < enemy_grid_y_offset + self.GRID_HEIGHT:
                        col = (x - enemy_grid_x_offset) // self.SQUARE_SIZE
                        row = (y - enemy_grid_y_offset) // self.SQUARE_SIZE
                        highlight_pos = (row, col)
                    else:
                        highlight_pos = None

            self.screen.fill(WHITE)
            self.drawPlayerGrid(50, 100, "Your Board", self.player_hit_board)
            self.drawEnemyGrid(enemy_grid_x_offset, enemy_grid_y_offset, "Enemy Board", self.enemy_hit_board, highlight_pos)
            pygame.display.flip()

if __name__ == "__main__":
    welcome_screen = WelcomeScreen()
    welcome_screen.run()
    pygame.quit()
    sys.exit()