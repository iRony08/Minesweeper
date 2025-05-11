import pygame
import sys
from minesweeper import Minesweeper

# Constants
HEIGHT = 8
WIDTH = 8
MINES = 8

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize pygame
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Minesweeper")

# Fonts
FONT_PATH = r"D:\CS_Sumit\Minesweeper\OpenSans-Regular.ttf"

try:
    smallFont = pygame.font.Font(FONT_PATH, 20)
    mediumFont = pygame.font.Font(FONT_PATH, 28)
    largeFont = pygame.font.Font(FONT_PATH, 40)
except FileNotFoundError:
    print("Custom font not found. Using default.")
    smallFont = pygame.font.SysFont("Arial", 20)
    mediumFont = pygame.font.SysFont("Arial", 28)
    largeFont = pygame.font.SysFont("Arial", 40)

# Board layout
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Load images
flag = pygame.image.load(r"D:\CS_Sumit\Minesweeper\flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load(r"D:\CS_Sumit\Minesweeper\mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Game state
def reset_game():
    return Minesweeper(HEIGHT, WIDTH, MINES), set(), set(), False, False

game, revealed, flags, lost, game_won = reset_game()
instructions = True
reset_button_rect = None

# Utility function to draw buttons
def draw_button(text, x, y, font, color=WHITE, bg=BLACK):
    btn = font.render(text, True, color)
    rect = btn.get_rect(center=(x, y))
    pygame.draw.rect(screen, bg, rect.inflate(20, 10))
    screen.blit(btn, rect)
    return rect

# Main game loop
while True:
    screen.fill(BLACK)
    reset_button_rect = None

    # Draw intro screen
    if instructions:
        title = largeFont.render("Play Minesweeper", True, WHITE)
        screen.blit(title, (width // 2 - title.get_width() // 2, height // 4))
        start_rect = draw_button("Click to Start", width // 2, height // 2, mediumFont)
    else:
        # Draw Reset button and save its rect
        reset_button_rect = draw_button("Reset", width - 70, 40, smallFont, WHITE, BLUE)

        # Draw grid
        for row in range(HEIGHT):
            for col in range(WIDTH):
                rect = pygame.Rect(
                    board_origin[0] + col * cell_size,
                    board_origin[1] + row * cell_size,
                    cell_size, cell_size
                )
                pygame.draw.rect(screen, GRAY if (row, col) not in revealed else WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if (row, col) in flags:
                    screen.blit(flag, rect.topleft)
                elif (row, col) in revealed:
                    if game.is_mine((row, col)):
                        screen.blit(mine, rect.topleft)
                    else:
                        count = game.nearby_mines((row, col))
                        if count > 0:
                            text = smallFont.render(str(count), True, BLACK)
                            screen.blit(text, (rect.x + cell_size // 4, rect.y + cell_size // 4))

        # Victory or Loss messages
        if lost:
            msg = largeFont.render("Game Over!", True, RED)
            screen.blit(msg, (width // 2 - msg.get_width() // 2, height // 2))
        elif game.won() and not game_won:
            game_won = True

        if game_won:
            msg = largeFont.render("You Won!", True, GREEN)
            screen.blit(msg, (width // 2 - msg.get_width() // 2, height // 2))

    pygame.display.flip()

    # Event handling AFTER drawing so buttons are available
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if instructions and start_rect.collidepoint(x, y):
                instructions = False
                game, revealed, flags, lost, game_won = reset_game()

            elif not instructions:
                if reset_button_rect and reset_button_rect.collidepoint(x, y):
                    game, revealed, flags, lost, game_won = reset_game()

                if lost or game_won:
                    continue  # Prevent input after game over

                row = (y - BOARD_PADDING) // cell_size
                col = (x - BOARD_PADDING) // cell_size
                if 0 <= row < HEIGHT and 0 <= col < WIDTH:
                    cell = (row, col)
                    if event.button == 1:
                        if cell not in flags:
                            if not game.reveal(cell):
                                lost = True
                            revealed.add(cell)
                    elif event.button == 3:
                        if cell in flags:
                            flags.remove(cell)
                        else:
                            flags.add(cell)
