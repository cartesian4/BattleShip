import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UNO - Simplified")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
CARD_COLORS = ["red", "green", "blue", "yellow"]

# Fonts
FONT = pygame.font.SysFont("arial", 20)
BIG_FONT = pygame.font.SysFont("arial", 50)

# Card size
CARD_WIDTH, CARD_HEIGHT = 80, 120

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def matches(self, other):
        return self.color == other.color or self.value == other.value

    def draw(self, x, y):
        pygame.draw.rect(screen, pygame.Color(self.color), (x, y, CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2)
        text = FONT.render(str(self.value), True, BLACK)
        screen.blit(text, (x + 25, y + 45))

def create_deck():
    deck = []
    for color in CARD_COLORS:
        for value in range(0, 10):
            deck.append(Card(color, value))
            if value != 0:
                deck.append(Card(color, value))
    random.shuffle(deck)
    return deck

def draw_card(deck, hand):
    if deck:
        hand.append(deck.pop())

# Function to reset/start the game
def reset_game():
    global deck, player_hand, computer_hand, discard_pile, turn, winner
    deck = create_deck()
    player_hand = [deck.pop() for _ in range(7)]
    computer_hand = [deck.pop() for _ in range(7)]
    discard_pile = [deck.pop()]
    turn = "player"
    winner = None

reset_game()

running = True
while running:
    screen.fill(WHITE)

    # 1. Draw Board
    discard_pile[-1].draw(WIDTH // 2 - CARD_WIDTH // 2, HEIGHT // 2 - CARD_HEIGHT // 2)
    screen.blit(FONT.render("Discard Pile", True, BLACK), (WIDTH // 2 - 45, HEIGHT // 2 + CARD_HEIGHT // 2 + 10))

    for i, card in enumerate(player_hand):
        card.draw(50 + i * (CARD_WIDTH + 10), HEIGHT - CARD_HEIGHT - 20)

    for i in range(len(computer_hand)):
        pygame.draw.rect(screen, BLACK, (50 + i * (CARD_WIDTH + 10), 20, CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(screen, WHITE, (50 + i * (CARD_WIDTH + 10), 20, CARD_WIDTH, CARD_HEIGHT), 2)

    draw_button = pygame.Rect(WIDTH - 150, HEIGHT - 80, 100, 50)
    pygame.draw.rect(screen, GRAY, draw_button)
    pygame.draw.rect(screen, BLACK, draw_button, 2)
    screen.blit(FONT.render("Draw", True, BLACK), (WIDTH - 120, HEIGHT - 65))

    # 2. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not winner: # Only allow moves if no one has won
            if turn == "player" and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                # Check Card Clicks
                for i, card in enumerate(player_hand):
                    card_rect = pygame.Rect(50 + i * (CARD_WIDTH + 10), HEIGHT - CARD_HEIGHT - 20, CARD_WIDTH, CARD_HEIGHT)
                    if card_rect.collidepoint(mouse_x, mouse_y):
                        if card.matches(discard_pile[-1]):
                            discard_pile.append(player_hand.pop(i))
                            turn = "computer"
                        break

                # Check Draw Button Click
                if draw_button.collidepoint(mouse_x, mouse_y):
                    draw_card(deck, player_hand)
                    turn = "computer"
        else:
            # Check for Reset Button click on winner screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                reset_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
                if reset_btn.collidepoint(event.pos):
                    reset_game()

    # 3. Computer Logic
    if turn == "computer" and not winner:
        pygame.display.flip() # Update screen to show player's move first
        pygame.time.delay(800)
        played = False
        for i, card in enumerate(computer_hand):
            if card.matches(discard_pile[-1]):
                discard_pile.append(computer_hand.pop(i))
                played = True
                break
        if not played:
            draw_card(deck, computer_hand)
        turn = "player"

    # 4. Check Win Condition
    if not player_hand:
        winner = "Player"
    elif not computer_hand:
        winner = "Computer"

    # 5. Draw Winner Screen
    if winner:
        # Create a translucent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))
        screen.blit(overlay, (0, 0))

        # Text
        win_text = BIG_FONT.render(f"{winner} Wins!", True, BLACK)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))

        # Reset Button
        reset_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(screen, GRAY, reset_btn)
        pygame.draw.rect(screen, BLACK, reset_btn, 2)
        btn_text = FONT.render("Play Again", True, BLACK)
        screen.blit(btn_text, (WIDTH // 2 - btn_text.get_width() // 2, HEIGHT // 2 + 65))

    pygame.display.flip()

pygame.quit()
sys.exit()
