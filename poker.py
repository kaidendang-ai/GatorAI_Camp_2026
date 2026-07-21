import random
from collections import Counter
from itertools import combinations
import pygame

WIDTH, HEIGHT = 1100, 700
FPS = 60

SUITS = ["♠", "♥", "♦", "♣"]
RANK_NAMES = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K", 14: "A"}


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.face_up = True

    def __repr__(self):
        return f"{RANK_NAMES[self.rank]}{self.suit}"

    def __str__(self):
        return self.__repr__()


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in range(2, 15)]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.folded = False
        self.all_in = False


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False

    def draw(self, surface, font):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=10)
        label = font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def handle_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)


class PokerGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gator Poker vs AI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.title_font = pygame.font.SysFont("arial", 36, bold=True)
        self.running = True
        self.human = Player("You", 1000)
        self.ai = Player("AI", 1000)
        self.community = []
        self.deck = Deck()
        self.pot = 0
        self.current_bet = 0
        self.stage = "preflop"
        self.awaiting_player_action = False
        self.game_over = False
        self.log_lines = []
        self.winner = None
        self.buttons = []
        self.new_hand()

    def new_hand(self):
        if self.human.chips <= 0 or self.ai.chips <= 0:
            self.human = Player("You", 1000)
            self.ai = Player("AI", 1000)

        self.community = []
        self.deck = Deck()
        self.human.hand = []
        self.ai.hand = []
        self.human.folded = False
        self.ai.folded = False
        self.human.all_in = False
        self.ai.all_in = False
        self.pot = 0
        self.current_bet = 20
        self.stage = "preflop"
        self.awaiting_player_action = True
        self.game_over = False
        self.winner = None
        self.log_lines = [
            "New hand started.",
            "You posted the small blind.",
            "AI posted the big blind.",
        ]

        self.human.chips -= 10
        self.ai.chips -= 20
        self.pot += 30

        self.human.hand = [self.deck.deal(), self.deck.deal()]
        self.ai.hand = [self.deck.deal(), self.deck.deal()]
        self.log_lines.append(f"Your hand: {self.display_cards(self.human.hand)}")

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    button.handle_hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            self.handle_button_action(button.action)
                            break

    def update(self):
        self.buttons = []
        button_y = HEIGHT - 120
        button_width = 140
        button_height = 60
        button_spacing = 160
        x_start = 80

        if self.game_over:
            self.buttons.append(Button(x_start, button_y, button_width, button_height, "New Hand", (40, 120, 190), (70, 150, 220), "new_hand"))
            return

        if self.awaiting_player_action:
            label = "Call" if self.current_bet > 0 else "Check"
            self.buttons.append(Button(x_start, button_y, button_width, button_height, "Fold", (180, 60, 60), (220, 100, 100), "fold"))
            self.buttons.append(Button(x_start + button_spacing, button_y, button_width, button_height, label, (35, 120, 180), (65, 150, 220), "call"))
            self.buttons.append(Button(x_start + button_spacing * 2, button_y, button_width, button_height, "Raise 20", (180, 120, 40), (220, 160, 80), "raise"))
        else:
            self.buttons.append(Button(x_start, button_y, button_width, button_height, "Next", (40, 120, 190), (70, 150, 220), "next"))

    def handle_button_action(self, action):
        if action == "new_hand":
            self.new_hand()
            return

        if not self.awaiting_player_action:
            if action == "next":
                self.advance_game()
            return

        if action == "fold":
            self.human.folded = True
            self.log_lines.append("You folded.")
            self.resolve_round_end("AI")
        elif action == "call":
            self.take_action_from_player("call")
            self.ai_turn()
        elif action == "raise":
            self.take_action_from_player("raise")
            self.ai_turn()

    def take_action_from_player(self, action):
        if action == "call":
            if self.current_bet > 0:
                self.pay_player(self.human, self.current_bet)
                self.log_lines.append(f"You called {self.current_bet}.")
            else:
                self.log_lines.append("You checked.")
        else:
            raise_amount = 20
            if self.human.chips >= raise_amount:
                self.human.chips -= raise_amount
                self.pot += raise_amount
                self.current_bet += raise_amount
                self.log_lines.append(f"You raised by {raise_amount}.")
            else:
                self.human.all_in = True
                self.pot += self.human.chips
                self.human.chips = 0
                self.log_lines.append("You went all in.")

    def ai_turn(self):
        if self.human.folded or self.ai.folded:
            self.resolve_round_end("AI" if self.human.folded else "You")
            return

        action = self.choose_ai_action()
        if action == "fold":
            self.ai.folded = True
            self.log_lines.append("AI folded.")
            self.resolve_round_end("You")
        elif action == "call":
            self.pay_player(self.ai, self.current_bet)
            self.log_lines.append(f"AI called {self.current_bet}.")
            self.awaiting_player_action = False
            self.advance_game()
        else:
            raise_amount = max(20, self.current_bet // 2)
            if self.ai.chips >= raise_amount:
                self.ai.chips -= raise_amount
                self.pot += raise_amount
                self.current_bet += raise_amount
                self.log_lines.append(f"AI raised by {raise_amount}.")
            else:
                self.ai.all_in = True
                self.pot += self.ai.chips
                self.ai.chips = 0
                self.log_lines.append("AI went all in.")
            self.awaiting_player_action = False
            self.advance_game()

    def evaluate_ai_strength(self, score):
        category = score[0]
        category_weights = {
            8: 0.98,
            7: 0.93,
            6: 0.88,
            5: 0.80,
            4: 0.72,
            3: 0.64,
            2: 0.58,
            1: 0.46,
            0: 0.28,
        }
        strength = category_weights.get(category, 0.2)
        if len(score) > 1:
            top_value = score[1]
            strength += min(0.08, top_value / 140.0)
        return min(0.99, strength)

    def choose_ai_action(self):
        if self.ai.folded or self.ai.chips <= 0:
            return "fold"

        combined = self.ai.hand + self.community
        score = hand_rank(combined)
        strength = self.evaluate_ai_strength(score)

        if self.stage == "preflop":
            if len(self.ai.hand) == 2:
                first, second = self.ai.hand[0].rank, self.ai.hand[1].rank
                if first == second:
                    if first >= 10:
                        return "raise"
                    if first >= 7:
                        return "call"
                    return "fold" if self.current_bet >= 40 else "call"
                if {first, second} >= {14, 13} or {first, second} >= {14, 12} or {first, second} >= {13, 12}:
                    return "raise"
                if first >= 10 or second >= 10:
                    return "call"
                return "fold" if self.current_bet >= 40 else "call"

        if self.current_bet >= 80 and strength < 0.55:
            return "fold"
        if strength >= 0.85:
            return "raise"
        if strength >= 0.65:
            if self.current_bet <= 30 or random.random() < 0.2:
                return "call"
            return "raise"
        if strength >= 0.45:
            if self.current_bet <= 20:
                return "call"
            if random.random() < 0.25:
                return "raise"
            return "call"

        if self.stage in {"flop", "turn", "river"} and random.random() < 0.15 and self.current_bet <= 30:
            return "raise"
        return "fold" if self.current_bet > 30 else "call"

    def advance_game(self):
        if self.human.folded or self.ai.folded:
            self.resolve_round_end("AI" if self.human.folded else "You")
            return

        if self.stage == "preflop":
            self.community.extend([self.deck.deal() for _ in range(3)])
            self.stage = "flop"
            self.current_bet = 0
            self.awaiting_player_action = True
            self.log_lines.append("Flop dealt.")
        elif self.stage == "flop":
            self.community.append(self.deck.deal())
            self.stage = "turn"
            self.current_bet = 0
            self.awaiting_player_action = True
            self.log_lines.append("Turn dealt.")
        elif self.stage == "turn":
            self.community.append(self.deck.deal())
            self.stage = "river"
            self.current_bet = 0
            self.awaiting_player_action = True
            self.log_lines.append("River dealt.")
        else:
            self.showdown()

    def resolve_round_end(self, winner_name):
        self.game_over = True
        self.awaiting_player_action = False
        self.winner = winner_name
        self.log_lines.append(f"{winner_name} wins the pot of {self.pot}.")

    def showdown(self):
        human_score = hand_rank(self.human.hand + self.community)
        ai_score = hand_rank(self.ai.hand + self.community)
        if compare_hands(human_score, ai_score):
            self.winner = "You"
            self.human.chips += self.pot
        else:
            self.winner = "AI"
            self.ai.chips += self.pot
        self.game_over = True
        self.awaiting_player_action = False
        self.log_lines.append("Showdown!")
        self.log_lines.append(f"Your hand rank: {human_score}")
        self.log_lines.append(f"AI hand rank: {ai_score}")

    def pay_player(self, player, amount):
        if player.chips >= amount:
            player.chips -= amount
            self.pot += amount
        else:
            self.pot += player.chips
            player.chips = 0
            player.all_in = True

    def display_cards(self, cards):
        return " | ".join(str(card) for card in cards)

    def draw(self):
        self.screen.fill((20, 80, 40))
        pygame.draw.rect(self.screen, (35, 120, 70), pygame.Rect(50, 40, WIDTH - 100, HEIGHT - 160), border_radius=25)
        pygame.draw.rect(self.screen, (30, 80, 55), pygame.Rect(70, 60, WIDTH - 140, HEIGHT - 200), border_radius=25)

        title = self.title_font.render("Gator Poker", True, (255, 255, 255))
        self.screen.blit(title, (80, 70))

        self.draw_table()
        self.draw_player_area(self.ai, 120, 140, False)
        self.draw_player_area(self.human, 120, 430, True)
        self.draw_community_cards()
        self.draw_sidebar()
        self.draw_buttons()
        pygame.display.flip()

    def draw_table(self):
        table_rect = pygame.Rect(180, 160, WIDTH - 360, HEIGHT - 360)
        pygame.draw.ellipse(self.screen, (80, 160, 90), table_rect)
        pygame.draw.ellipse(self.screen, (110, 200, 110), table_rect.inflate(-12, -12))
        pot_text = self.font.render(f"Pot: {self.pot}", True, (255, 255, 255))
        self.screen.blit(pot_text, (table_rect.centerx - 40, table_rect.centery - 10))
        stage_text = self.font.render(self.stage.upper(), True, (255, 255, 255))
        self.screen.blit(stage_text, (table_rect.centerx - 40, table_rect.centery + 25))

    def draw_player_area(self, player, x, y, face_up):
        panel = pygame.Rect(x, y, 260, 140)
        pygame.draw.rect(self.screen, (60, 40, 20), panel, border_radius=12)
        pygame.draw.rect(self.screen, (255, 255, 255), panel, 2, border_radius=12)
        name_text = self.font.render(player.name, True, (255, 255, 255))
        self.screen.blit(name_text, (x + 20, y + 15))
        chips_text = self.small_font.render(f"Chips: {player.chips}", True, (255, 255, 255))
        self.screen.blit(chips_text, (x + 20, y + 45))

        cards = player.hand
        start_x = x + 20
        for index, card in enumerate(cards):
            self.draw_card(start_x + index * 70, y + 70, card, face_up)

    def draw_community_cards(self):
        x = 360
        y = 260
        for index, card in enumerate(self.community):
            self.draw_card(x + index * 80, y, card, True)
        if not self.community:
            placeholder = self.small_font.render("Community cards will appear here", True, (255, 255, 255))
            self.screen.blit(placeholder, (360, 310))

    def draw_sidebar(self):
        sidebar = pygame.Rect(WIDTH - 260, 90, 200, HEIGHT - 220)
        pygame.draw.rect(self.screen, (45, 35, 25), sidebar, border_radius=15)
        pygame.draw.rect(self.screen, (255, 255, 255), sidebar, 2, border_radius=15)
        heading = self.font.render("Game Log", True, (255, 255, 255))
        self.screen.blit(heading, (WIDTH - 220, 115))
        for i, line in enumerate(self.log_lines[-8:]):
            text = self.small_font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (WIDTH - 235, 155 + i * 55))

        if self.game_over and self.winner:
            result = self.font.render(f"Winner: {self.winner}", True, (255, 255, 255))
            self.screen.blit(result, (WIDTH - 235, HEIGHT - 180))

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen, self.small_font)

    def draw_card(self, x, y, card, face_up):
        rect = pygame.Rect(x, y, 60, 85)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, border_radius=8)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2, border_radius=8)
        if face_up:
            rank_text = self.small_font.render(str(card), True, (0, 0, 0))
            self.screen.blit(rank_text, (x + 12, y + 10))
        else:
            pygame.draw.rect(self.screen, (40, 80, 140), rect, border_radius=8)
            pygame.draw.line(self.screen, (255, 255, 255), (x + 16, y + 16), (x + 44, y + 69), 2)
            pygame.draw.line(self.screen, (255, 255, 255), (x + 44, y + 16), (x + 16, y + 69), 2)


def hand_rank(cards):
    cards = list(cards)

    if len(cards) < 5:
        ranks = sorted([card.rank for card in cards], reverse=True)
        counts = Counter(ranks)
        if len(cards) >= 2 and sorted(counts.values(), reverse=True)[0] == 2:
            pair = max(rank for rank, count in counts.items() if count == 2)
            kickers = sorted([rank for rank, count in counts.items() if count == 1], reverse=True)
            return (1, pair, *kickers)
        return (0, *ranks)

    def evaluate_five(cards5):
        ranks = sorted([card.rank for card in cards5], reverse=True)
        counts = Counter(ranks)
        sorted_counts = sorted(counts.values(), reverse=True)
        is_flush = len({card.suit for card in cards5}) == 1

        def straight_high(ranks_list):
            unique = sorted(set(ranks_list), reverse=True)
            if len(unique) < 5:
                return None
            for i in range(len(unique) - 4):
                window = unique[i:i + 5]
                if window[0] - window[-1] == 4:
                    return window[0]
            if set([14, 5, 4, 3, 2]).issubset(set(ranks_list)):
                return 5
            return None

        straight = straight_high(ranks)
        if is_flush and straight is not None:
            return (8, straight)
        if sorted_counts == [4, 1]:
            quad = max(rank for rank, count in counts.items() if count == 4)
            kicker = max(rank for rank, count in counts.items() if count == 1)
            return (7, quad, kicker)
        if sorted_counts == [3, 2]:
            trip = max(rank for rank, count in counts.items() if count == 3)
            pair = max(rank for rank, count in counts.items() if count == 2)
            return (6, trip, pair)
        if is_flush:
            return (5, *ranks)
        if straight is not None:
            return (4, straight)
        if sorted_counts == [3, 1, 1]:
            trip = max(rank for rank, count in counts.items() if count == 3)
            kickers = sorted([rank for rank, count in counts.items() if count == 1], reverse=True)
            return (3, trip, *kickers)
        if sorted_counts == [2, 2, 1]:
            pairs = sorted([rank for rank, count in counts.items() if count == 2], reverse=True)
            kicker = max(rank for rank, count in counts.items() if count == 1)
            return (2, *pairs, kicker)
        if sorted_counts == [2, 1, 1, 1]:
            pair = max(rank for rank, count in counts.items() if count == 2)
            kickers = sorted([rank for rank, count in counts.items() if count == 1], reverse=True)
            return (1, pair, *kickers)
        return (0, *ranks)

    best = None
    for combo in combinations(cards, 5):
        score = evaluate_five(combo)
        if best is None or score > best:
            best = score
    return best


def compare_hands(left, right):
    return left > right


if __name__ == "__main__":
    game = PokerGame()
    game.run()
