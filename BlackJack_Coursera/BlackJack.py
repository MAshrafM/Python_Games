# Mini-project #6 - Blackjack

import simplegui
import random

title = "Blackjack"
# Title with more Pizzaz!
# Commented out as the instructions state the title specifically
#title = "BlackJack 21!"

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
MIN_CARDS = 13	# Minimum number of cards to start a round

SHADOW_SIZE = (2,2)
TITLE_FONT = 60
VALUE_FONT = 20
SCORE_FONT = 30
NAME_FONT = 40
OUTCOME_FONT = 40
HINT_FONT = 30

TITLE_COLOR = "black"
SHADOW_COLOR = "white"
NAME_COLOR = "white"
VALUE_COLOR = "white"
SCORE_COLOR = "white"
NEG_SCORE_COLOR = "red"
POS_SCORE_COLOR = "white"
OUTCOME_COLOR = "yellow"
HINT_COLOR = "yellow"

TITLE_POS = (50, 70)
SCORE_POS = (450, 65)

DEALER_NAME_POS = (70, 150)
DEALER_VALUE_POS = (30, 240)
DEALER_POS = (70, 180)

PLAYER_NAME_POS = (70, 350)
PLAYER_VALUE_POS = (30, 440)
PLAYER_POS = (70, 380)

OUTCOME_POS = (150, 550)
HINT_POS = (300, 350)

CARD_SPACING = CARD_SIZE[0] + 20

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# Control debugging output
DEBUG = False
def debug(text):
    if (DEBUG):
        print(text)
        
# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    # added the ability to draw the card face down
    def draw(self, canvas, pos, face_down=False):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        if (face_down):
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        else:
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        s = "Value=" + str(self.get_value())
        for card in self.cards:
            s += " " + str(card)            
        return s

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        has_ace = False
        for card in self.cards:
            value += VALUES[card.rank]
            if (card.rank == 'A'):
                has_ace = True
        # adjust value for ace
        if (has_ace and value <= 11):
            value += 10
        return value
    
    # Since this is a blackjack specific hand class
    # I added the ability to hide the hole card for the dealer
    def draw(self, canvas, pos, hide_first=False):
        # draw a hand on the canvas, use the draw method for cards
        card_pos = [pos[0], pos[1]]
        first = hide_first
        for card in self.cards:
            card.draw(canvas, card_pos, first)
            card_pos[0] += CARD_SPACING
            first = False
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        debug("new deck")
        self.shuffle()

    def shuffle(self):
        # Put all cards back in the deck
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
        if (len(self.cards) != 52):
            print("Error in deck: " + str(self))
            return
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def get_card_count(self):
        return len(self.cards)
    
    def is_empty(self):
        return self.get_card_count() == 0
    
    def __str__(self):
        # return a string representing the deck
        s = "Card count=" + str(self.get_card_count())
        for card in self.cards:
            s += " " + str(card)
        return s

# Define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, hint, score

    # Player loses if round was in progress
    if (in_play):
        score -= 1
        outcome = "You Forfeited! Dealer Wins!"
    else:
        outcome = ""
        
    debug("")
    debug("New deal...")
    hint = "Hit or Stand?"
    
    # -- Enhancement - commented out since instructions say
    # to make a new deck for every deal -
    # continue to use the same deck until there are not
    #  enough cards for a round
    #if (deck.get_card_count() < MIN_CARDS):
    #    deck.shuffle()
    
    deck.shuffle()
    
    # For test, print the deck
    debug("Deck: " + str(deck))
    # For test, deal out the whole deck
    #count = 1
    #while not deck.is_empty():
    #    print(str(count) + "=" + str(deck.deal_card()))
    #    count += 1
        
    # Create the hands
    player_hand = Hand()
    debug("Initial Player Hand = " + str(player_hand))
    dealer_hand = Hand()
    debug("Initial Dealer Hand = " + str(dealer_hand))
    for i in range(2):
        # part of enhancement (keep dealing until deck is exhausted)
        if (deck.is_empty()):
            print("Out of cards")
            return
        # Add a card to the player's hand
        player_hand.add_card(deck.deal_card())
        # part of enhancement (keep dealing until deck is exhausted)
        if (deck.is_empty()):
            print("Out of cards")
            return
        # Add a card to the dealer's hand
        dealer_hand.add_card(deck.deal_card())
    
    debug("Player = " + str(player_hand))
    debug("Dealer = " + str(dealer_hand))
        
    in_play = True

def hit():
    global in_play, outcome, score, hint
    # if the hand is in play, hit the player
    if (not in_play):
        return
    
    debug("Hit")
    # part of enhancement (keep dealing until deck is exhausted)
    if (deck.is_empty()):
        print("Out of cards")
        return
    player_hand.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
    value = player_hand.get_value()
    if (value > 21):
        outcome = "You Busted!  Dealer Wins!"
        hint = "New deal?"
        in_play = False
        score -= 1
        
    debug("Player = " + str(player_hand))
    debug("Dealer = " + str(dealer_hand))
    debug(outcome)
    debug("Score=" + str(score))
    
def stand():
    global in_play, outcome, score, hint
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if (not in_play):
        return
    debug("Stand")
    in_play = False
    
    # Deal cards to dealer until 17 is reached
    while (dealer_hand.get_value() < 17):
        debug("Dealer hit")
        # part of enhancement (keep dealing until deck is exhausted)
        if (deck.is_empty()):
            print("Out of cards")
            return
        dealer_hand.add_card(deck.deal_card())
        debug("Player = " + str(player_hand))
        debug("Dealer = " + str(dealer_hand))
        
    # assign a message to outcome, update in_play and score
    value = dealer_hand.get_value()
    if (value > 21):
        outcome = "Dealer Busted!  You Win!"
        score += 1
    elif (value >= player_hand.get_value()):
        # dealer wins a push
        outcome = "Dealer Wins!"
        score -= 1
    else:
        outcome = "You Win!"
        score += 1
    hint = "New deal?"
    debug(outcome)
    debug("Score=" + str(score))
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])

    # Draw the Title
    canvas.draw_text(title, (TITLE_POS[0] + SHADOW_SIZE[0], TITLE_POS[1] + SHADOW_SIZE[1]), TITLE_FONT, SHADOW_COLOR)
    canvas.draw_text(title, TITLE_POS, TITLE_FONT, TITLE_COLOR)
    
    # Draw the score
    canvas.draw_text("Score: ", SCORE_POS, SCORE_FONT, SCORE_COLOR)
    if (score < 0):
        color = NEG_SCORE_COLOR
    else:
        color = POS_SCORE_COLOR        
    canvas.draw_text(str(score), (SCORE_POS[0] + frame.get_canvas_textwidth("Score: ", SCORE_FONT), SCORE_POS[1]), SCORE_FONT, color)

    # Draw the Dealer Hand    
    canvas.draw_text("Dealer", DEALER_NAME_POS, NAME_FONT, NAME_COLOR)
    if (DEBUG and not in_play):
        canvas.draw_text(str(dealer_hand.get_value()), DEALER_VALUE_POS, VALUE_FONT, VALUE_COLOR)
    dealer_hand.draw(canvas, DEALER_POS, in_play)

    # Draw the Player Hand
    canvas.draw_text("Player", PLAYER_NAME_POS, NAME_FONT, NAME_COLOR)
    if (DEBUG):
        canvas.draw_text(str(player_hand.get_value()), PLAYER_VALUE_POS, VALUE_FONT, VALUE_COLOR)
    player_hand.draw(canvas, PLAYER_POS)
    
    # Draw the hint for the player
    canvas.draw_text(hint, HINT_POS, HINT_FONT, HINT_COLOR)
    
    # Center the outcome
    left = (CANVAS_WIDTH - frame.get_canvas_textwidth(outcome, OUTCOME_FONT))/2
    canvas.draw_text(outcome, (left, OUTCOME_POS[1]), OUTCOME_FONT, OUTCOME_COLOR)
    
# initialization frame
frame = simplegui.create_frame(title, CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
# Start with a new deck
deck = Deck()
deal()
frame.start()

# remember to review the grading rubric