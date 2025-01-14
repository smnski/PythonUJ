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
p_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
e_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

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
            "carrier": {"symbol": "c", "size": 5},
            "battleship": {"symbol": "b", "size": 4},
            "cruiser": {"symbol": "r", "size": 3},
            "submarine": {"symbol": "s", "size": 3},
            "destroyer": {"symbol": "d", "size": 2},
        }

    def startGame(self, auto_place=False):
        self.autoPlaceShips(e_board)

        if auto_place:
            self.autoPlaceShips(p_board)
        else:
            self.placeShipsYourself()

        self.clearUnableToPlaceMarkers(p_board, ROWS, COLS)
        self.clearUnableToPlaceMarkers(e_board, ROWS, COLS)
        gameplay = Gameplay()
        gameplay.run()

    @staticmethod
    def canPlace(board, row, col, length, horizontal):
        if horizontal:
            if col + length > COLS:
                return False
            return all(board[row][col + i] == 0 for i in range(length))
        else:
            if row + length > ROWS:
                return False
            return all(board[row + i][col] == 0 for i in range(length))

    @staticmethod
    def place(board, row, col, length, horizontal, symbol):
        if horizontal:
            for i in range(length):
                board[row][col + i] = symbol
        else:
            for i in range(length):
                board[row + i][col] = symbol

        def markAdjacent(row, col):
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < len(board) and 0 <= c < len(board[0]) and \
                        board[r][c] != symbol:
                        board[r][c] = "x"

        if horizontal:
            for i in range(length):
                markAdjacent(row, col + i)
        else:
            for i in range(length):
                markAdjacent(row + i, col)

    @staticmethod
    def clearUnableToPlaceMarkers(board, row, col):
        for r in range (row):
            for c in range (col):
                if board[r][c] == "x":
                    board[r][c] = 0

    def placeShipsYourself(self):
        GRID_WIDTH, GRID_HEIGHT = 500, 500
        TEXT_HEIGHT = 50
        DISPLAY_HEIGHT = GRID_HEIGHT + TEXT_HEIGHT
        ROWS, COLS = 10, 10
        SQUARE_SIZE = GRID_WIDTH // COLS

        ships_left = list(self.ships.items())
        ship_id = 0
        horiz = True
        preview_pos = None

        grid_screen = pygame.display.set_mode((GRID_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("Place Ships")

        while ships_left:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Placing ships with clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    if y >= GRID_HEIGHT:  # Ignore clicks in the text area
                        return
                    
                    ship_name, ship_data = ships_left[ship_id]
                    char = ship_data["symbol"]
                    ship_len = ship_data["size"]
                    if self.canPlace(p_board, row, col, ship_len,horiz):
                        self.place(p_board, row, col, ship_len, horiz, char)
                        ship_id += 1

                        # Remove placed ship from the list
                        if ship_id >= len(ships_left):
                            ships_left.clear()

                # Rotate ships with "r" key
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    horiz = not horiz

                # Track mouse movement for preview
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

                    # Ensure the calculated row and col are within bounds
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        preview_pos = (row, col)
                    else:
                        preview_pos = None  # Clear preview if out of bounds

            grid_screen.fill(WHITE)

            # Draw grid for placing ships
            for row in range(ROWS):
                for col in range(COLS):
                    ship_here = (p_board[row][col] != 0 and \
                                 p_board[row][col] != "x")
                    color = BLUE if ship_here else GRAY
                    pygame.draw.rect(
                        grid_screen,
                        color,
                        (col * SQUARE_SIZE,
                         row * SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE)
                    )
                    pygame.draw.rect(
                        grid_screen,
                        WHITE,
                        (col * SQUARE_SIZE,
                         row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                         1
                    )

            # Draw the ship preview
            if ships_left and preview_pos:
                ship_name, ship_data = ships_left[ship_id]
                ship_len = ship_data["size"]
                row, col = preview_pos
                valid = self.canPlace(p_board, row, col, ship_len, horiz)
                highlight_color = GREEN if valid else RED

                for i in range(ship_len):
                    if horiz:
                        rect = ((col + i) * SQUARE_SIZE,
                                row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    else:
                        rect = (col * SQUARE_SIZE,
                                (row + i) * SQUARE_SIZE,
                                SQUARE_SIZE, SQUARE_SIZE)
                    if (0 <= col + i < COLS and 0 <= row < ROWS) or \
                        (0 <= col < COLS and 0 <= row + i < ROWS):
                        pygame.draw.rect(grid_screen, highlight_color, rect)

            # Draw info text
            if ships_left:
                ship_name, ship_data = ships_left[ship_id]
                ship_len = ship_data["size"]
                placing_text = self.font.render(
                    f"Placing:{ship_name} ({ship_len})", True, BLACK)
                rotate_text = self.font.render(
                    "Press R to rotate", True, BLACK)

                grid_screen.blit(
                    placing_text,(GRID_WIDTH // 2
                                  - placing_text.get_width() // 2,
                                  GRID_HEIGHT + 5))
                grid_screen.blit(rotate_text, (GRID_WIDTH // 2
                                               - rotate_text.get_width() // 2,
                                               GRID_HEIGHT + 25))

            pygame.display.flip()

        pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def autoPlaceShips(self, board):
        for ship_name, ship_data in self.ships.items():
            placed = False
            while not placed:
                horizontal = random.choice([True, False])
                if horizontal:
                    row, col = random.randint(0, ROWS - 1), random.randint(0, COLS - ship_data["size"])
                else:
                    row, col = random.randint(0, ROWS - ship_data["size"]), random.randint(0, COLS - 1)
                if self.canPlace(board, row, col, ship_data["size"], horizontal):
                    self.place(board, row, col, ship_data["size"], horizontal, ship_data["symbol"])
                    placed = True

    def drawButton(self, text, x, y, color):
        pygame.draw.rect(self.screen, color,
                         (x, y, self.BUTTON_WIDTH,self.BUTTON_HEIGHT))
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x + self.BUTTON_WIDTH // 2,
                                                  y + self.BUTTON_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                width = self.WIDTH // 2
                bt_width = self.BUTTON_WIDTH // 2
                height = self.HEIGHT // 3
                bt_height = self.BUTTON_HEIGHT // 2

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (width - bt_width <= x <= width + bt_width and
                        height - bt_height <= y <= height + bt_height):
                        running = False
                        self.startGame(auto_place=False)

                    if (width - bt_width <= x <= width + bt_width and
                        2 * height - bt_height <= y <= 2 * height + bt_height):
                        running = False
                        self.startGame(auto_place=True)

            self.screen.fill(WHITE)
            self.drawButton("Place ships yourself",
                            width - bt_width, height - bt_height, GRAY)
            self.drawButton("Auto place ships",
                            width - bt_width, 2 * height - bt_height, GRAY)
            pygame.display.flip()

class Gameplay:
    WIDTH = 1200
    HEIGHT = 700

    GRID_WIDTH, GRID_HEIGHT = 500, 500
    ROWS, COLS = 10, 10
    SQUARE_SIZE = GRID_WIDTH // COLS

    UNDISC = 0
    DISC_M = 1
    DISC_H = 2
    SUNK = 3

    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Gameplay")
        self.font = pygame.font.Font(None, 36)
        self.p_hits = [[0 for _ in range(self.COLS)]
                                 for _ in range(self.ROWS)]
        self.e_hits = [[0 for _ in range(self.COLS)]
                                for _ in range(self.ROWS)]
        self.p_hp = {
            "carrier": 5,
            "battleship": 4,
            "cruiser": 3,
            "submarine": 3,
            "destroyer": 2,
        }
        self.e_hp = {
            "carrier": 5,
            "battleship": 4,
            "cruiser": 3,
            "submarine": 3,
            "destroyer": 2,
        }

    def drawPlayerGrid(self, x_offset, y_offset, title, hit_board):
        title_surface = self.font.render(title, True, BLACK)
        title_rect = title_surface.get_rect(
            center=(x_offset+ self.GRID_WIDTH // 2, y_offset - 20))
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
                ship_here = (p_board[row][col] != 0 and \
                             p_board[row][col] != "x")
                if ship_here:
                    color = DARK_GREEN
                else:
                    color = GRAY
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

                # Hits overlay
                if hit_board[row][col] == self.DISC_M:
                    color = DARK_GRAY
                elif hit_board[row][col] == self.DISC_H:
                    color = BLUE
                elif hit_board[row][col] == self.SUNK:
                    color = RED
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

    def drawEnemyGrid(self, x_offset, y_offset, title, hit_board, hl_pos=None):
        title_surface = self.font.render(title, True, BLACK)
        title_rect = title_surface.get_rect(
            center=(x_offset + self.GRID_WIDTH // 2, y_offset - 20))
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
                if hit_board[row][col] == self.UNDISC:
                    color = GRAY
                elif hit_board[row][col] == self.DISC_M:
                    color = DARK_GRAY
                elif hit_board[row][col] == self.DISC_H:
                    color = BLUE
                elif hit_board[row][col] == self.SUNK:
                    color = RED
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

                if hl_pos == (row, col):
                    pygame.draw.rect(self.screen, GREEN, rect, 3)

    def hitRemaining(self, hit_board, board, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),          (0, 1),
                    (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.ROWS and 0 <= c < self.COLS:
                if hit_board[r][c] == self.UNDISC and\
                    board[r][c] == 0:
                    hit_board[r][c] = self.DISC_M

    def sinkRemaining(self, board, hit_board, symbol):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if board[row][col] == symbol:
                    hit_board[row][col] = self.SUNK
                    self.hitRemaining(hit_board, board, row, col)

    def handleClickOnEnemyGrid(self, x, y, x_offset, y_offset):
        col = (x - x_offset) // self.SQUARE_SIZE
        row = (y - y_offset) // self.SQUARE_SIZE

        out_of_bounds = not (0 <= row < self.ROWS and 0 <= col < self.COLS)
        already_discovered = self.e_hits[row][col] == self.DISC_H or\
            self.e_hits[row][col] == self.DISC_M\
                or self.e_hits[row][col] == self.SUNK
        if out_of_bounds or already_discovered:
            return False

        return self.handleHit(row, col, e_board, self.e_hits, self.e_hp)

    def handleHit(self, row, col, board, hit_board, remaining_hp):
        def handleShipHit(name, symbol):
            remaining_hp[name] -= 1
            if remaining_hp[name] <= 0:
                self.sinkRemaining(board, hit_board, symbol)
            else:
                hit_board[row][col] = self.DISC_H

        if hit_board[row][col] == self.UNDISC:
            if board[row][col] == 0:
                hit_board[row][col] = self.DISC_M
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
    
    def selectionAI(self, hit_board):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def is_valid(row, col):
            return 0 <= row < self.ROWS and 0 <= col < self.COLS and\
                hit_board[row][col] == self.UNDISC

        def follow_direction(row, col, direction):
            dr, dc = direction
            while is_valid(row + dr, col + dc):
                row += dr
                col += dc
                if hit_board[row][col] == self.UNDISC:
                    return row, col
            return None

        # Search for a direction to follow if there's a hit
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if hit_board[row][col] == self.DISC_H:
                    for dr, dc in directions:
                        new_shot = follow_direction(row, col, (dr, dc))
                        if new_shot:
                            return new_shot

        # If no directions to follow, find an adjacent undiscovered square
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if hit_board[row][col] == self.DISC_H:
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        if is_valid(new_row, new_col):
                            return new_row, new_col

        # Fallback to random selection
        undiscovered = [(r, c) for r in range(self.ROWS)
                        for c in range(self.COLS)
                        if hit_board[r][c] == self.UNDISC]
        if undiscovered:
            return random.choice(undiscovered)
        
        raise ValueError("No valid moves left")

    def isGameOver(self):
        total_hp_enemy = sum(self.e_hp.values())
        total_hp_player = sum(self.p_hp.values())

        return total_hp_enemy <= 0 or total_hp_player <= 0

    def handleGameOver(self):
        winner = "Player" if sum(self.e_hp.values()) == 0 else "Enemy"

        # Display the winner modal
        modal_running = True
        modal_width, modal_height = 400, 200
        modal_x = (self.WIDTH - modal_width) // 2
        modal_y = (self.HEIGHT - modal_height) // 2

        while modal_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or\
                    (event.type == pygame.MOUSEBUTTONDOWN and\
                     modal_x <= event.pos[0] <= modal_x + modal_width and\
                        modal_y <= event.pos[1] <= modal_y + modal_height):
                    modal_running = False
                    pygame.quit()
                    sys.exit()

            # Redraw the game board
            self.screen.fill(WHITE)
            self.drawPlayerGrid(50, 100, "Your Board", self.p_hits)
            self.drawEnemyGrid(self.WIDTH - self.GRID_WIDTH - 50, 100,
                               "Enemy Board", self.e_hits)

            # Draw the modal
            pygame.draw.rect(self.screen, WHITE,
                             (modal_x, modal_y,modal_width, modal_height))
            pygame.draw.rect(self.screen, BLACK,
                             (modal_x, modal_y, modal_width, modal_height), 2)
            font = pygame.font.Font(None, 36)
            text_surface = font.render(f"{winner} Wins!", True, BLACK)
            text_rect = text_surface.get_rect(
                center=(modal_x + modal_width // 2,
                        modal_y + modal_height // 2))
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

    def handleGameTurn(self, x, y, enemy_grid_x_offset, enemy_grid_y_offset):
        # Player tries to take a turn
        valid_move = self.handleClickOnEnemyGrid(
            x, y, enemy_grid_x_offset, enemy_grid_y_offset)
        if not valid_move:
            return

        # If player turn valid, enemy moves
        row, col = self.selectionAI(self.p_hits)
        self.handleHit(row, col, p_board, self.p_hits, self.p_hp)

    def run(self):
        running = True

        e_x_offset = self.WIDTH - self.GRID_WIDTH - 50
        e_y_offset = 100
        hl_pos = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Clicking on enemy grid
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if e_x_offset <= x < e_x_offset + self.GRID_WIDTH and \
                            e_y_offset <= y < e_y_offset + self.GRID_HEIGHT:
                        
                        self.handleGameTurn(x, y, e_x_offset, e_y_offset)

                # Tracking mouse position and highlighting target
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if e_x_offset <= x < e_x_offset + self.GRID_WIDTH and \
                            e_y_offset <= y < e_y_offset + self.GRID_HEIGHT:
                        col = (x - e_x_offset) // self.SQUARE_SIZE
                        row = (y - e_y_offset) // self.SQUARE_SIZE
                        hl_pos = (row, col)
                    else:
                        hl_pos = None

            self.screen.fill(WHITE)
            self.drawPlayerGrid(50, 100, "Your Board", self.p_hits)
            self.drawEnemyGrid(e_x_offset, e_y_offset, "Enemy Board",
                               self.e_hits, hl_pos)
            pygame.display.flip()

if __name__ == "__main__":
    welcome_screen = WelcomeScreen()
    welcome_screen.run()
    pygame.quit()
    sys.exit()