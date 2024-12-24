import random
from data import get_db_connection

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class CardDeck:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None

class PlayerHand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces_count = 0

    def add_card(self, card):
        self.cards.append(card)
        if card.rank in ['Jack', 'Queen', 'King']:
            self.value += 10
        elif card.rank == 'Ace':
            self.value += 11
            self.aces_count += 1
        else:
            self.value += int(card.rank)
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces_count:
            self.value -= 10
            self.aces_count -= 1

class Blackjack:
    def __init__(self):
        self.deck = CardDeck()
        self.player_hand = PlayerHand()
        self.dealer_hand = PlayerHand()
        self.is_game_over = False
        self.game_result = ""

    def start_new_round(self):
        self.deck = CardDeck() 
        self.player_hand = PlayerHand()  
        self.dealer_hand = PlayerHand()  
        self.is_game_over = False  
        self.game_result = "" 
        self.deal_initial_cards()


    def deal_initial_cards(self):
        for _ in range(2):
            self.player_hand.add_card(self.deck.deal_card())
            self.dealer_hand.add_card(self.deck.deal_card())

    def hit_card(self):
        if not self.is_game_over:
            self.player_hand.add_card(self.deck.deal_card())
            if self.player_hand.value > 21: 
                self.is_game_over = True
                self.game_result = "User busts! Dealer wins."
                return self.get_game_state()
        return self.get_game_state()

    def stand_player(self):
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
            if self.dealer_hand.value > 21: 
                self.is_game_over = True
                self.game_result = "Dealer busts! User wins."
                return "win"
        
        if self.player_hand.value > self.dealer_hand.value:
            self.is_game_over = True
            self.game_result = "User wins."
            return "win"
        elif self.player_hand.value < self.dealer_hand.value:
            self.is_game_over = True
            self.game_result = "Dealer wins."
            return "lose"
        else:
            self.is_game_over = True
            self.game_result = "It's a draw."
            return "draw"

    def card_to_string(self, card):
        suits = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
        ranks = {'Jack': 'J', 'Queen': 'Q', 'King': 'K', 'Ace': 'A'}
        rank = ranks.get(card.rank, card.rank)  
        suit = suits[card.suit]  
        return f"{rank}{suit}"

    def get_game_state(self):
        return {
            'user_hand': [self.card_to_string(card) for card in self.player_hand.cards],
            'dealer_hand': [self.card_to_string(card) for card in self.dealer_hand.cards] if self.is_game_over else [self.card_to_string(self.dealer_hand.cards[0]), "🂠"],
            'user_value': self.player_hand.value,
            'dealer_value': self.dealer_hand.value if self.is_game_over else "?",
            'result': self.game_result,
            'game_over': self.is_game_over
        }
    def card_to_string(self, card):
        suits = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
        ranks = {'Jack': 'J', 'Queen': 'Q', 'King': 'K', 'Ace': 'A'}
        rank = ranks.get(card.rank, card.rank)
        suit = suits[card.suit]
        return f"{rank}{suit}"
