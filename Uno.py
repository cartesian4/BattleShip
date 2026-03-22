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
CARD_COLORS = ["red", "green", "blue", "yellow"]

# Fonts
FONT = pygame.font.SysFont("arial", 20)

# Card size
CARD_WIDTH, CARD_HEIGHT = 80, 120

# Card class
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

# Create deck
def create_deck():
    deck = []
    for color in CARD_COLORS:
        for value in range(0, 10):
            deck.append(Card(color, value))
            if value != 0:
                deck.append(Card(color, value))  # duplicate for standard UNO
    random.shuffle(deck)
    return deck

# Draw card from deck
def draw_card(deck, hand):
    if deck:
        hand.append(deck.pop())

# Game setup
deck = create_deck()
player_hand = [deck.pop() for _ in range(7)]
computer_hand = [deck.pop() for _ in range(7)]
discard_pile = [deck.pop()]
turn = "player"

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw discard pile
    discard_pile[-1].draw(WIDTH // 2 - CARD_WIDTH // 2, HEIGHT // 2 - CARD_HEIGHT // 2)
    discard_text = FONT.render("Discard Pile", True, BLACK)
    screen.blit(discard_text, (WIDTH // 2 - 40, HEIGHT // 2 + CARD_HEIGHT // 2 + 10))

    # Draw player hand
    for i, card in enumerate(player_hand):
        card.draw(50 + i * (CARD_WIDTH + 10), HEIGHT - CARD_HEIGHT - 20)

    # Draw computer hand (hidden)
    for i in range(len(computer_hand)):
        pygame.draw.rect(screen, BLACK, (50 + i * (CARD_WIDTH + 10), 20, CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(screen, WHITE, (50 + i * (CARD_WIDTH + 10), 20, CARD_WIDTH, CARD_HEIGHT), 2)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if turn == "player" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i, card in enumerate(player_hand):
                card_rect = pygame.Rect(50 + i * (CARD_WIDTH + 10), HEIGHT - CARD_HEIGHT - 20, CARD_WIDTH, CARD_HEIGHT)
                if card_rect.collidepoint(mouse_x, mouse_y):
                    if card.matches(discard_pile[-1]):
                        discard_pile.append(player_hand.pop(i))
                        turn = "computer"
                    break

            # Draw card button area
            draw_button = pygame.Rect(WIDTH - 150, HEIGHT - 80, 100, 50)
            if draw_button.collidepoint(mouse_x, mouse_y):
                draw_card(deck, player_hand)
                turn = "computer"

    # Draw "Draw Card" button
    pygame.draw.rect(screen, (200, 200, 200), (WIDTH - 150, HEIGHT - 80, 100, 50))
    pygame.draw.rect(screen, BLACK, (WIDTH - 150, HEIGHT - 80, 100, 50), 2)
    screen.blit(FONT.render("Draw", True, BLACK), (WIDTH - 120, HEIGHT - 65))

    # Computer turn
    if turn == "computer":
        pygame.time.delay(500)
        played = False
        for i, card in enumerate(computer_hand):
            if card.matches(discard_pile[-1]):
                discard_pile.append(computer_hand.pop(i))
                played = True
                break
        if not played:
            draw_card(deck, computer_hand)
        turn = "player"

    # Check win condition
    if not player_hand:
        print("You win!")
        running = False
    elif not computer_hand:
        print("Computer wins!")
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()