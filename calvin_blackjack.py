import sys
import random

from terminal_colourer import Colour
import settings

# Set up the Unicode chr constants:
HEARTS   = chr(9829) # ♥
DIAMONDS = chr(9830) # ♦
SPADES   = chr(9824) # ♠
CLUBS    = chr(9827) # ♣

BACKSIDE = 'backside'

def get_bet(max_bet):
     while True: # Keep asking until they enter a valid amount
        print(Colour.bold(f'How much do you want to bet? Minimum bet: {settings.MIN_BET} credits.'))
        bet = input(' > ').upper().strip()

        if bet[0] == 'Q':
            print('Game ended. Thanks for playing!')
            sys.exit()

        if int(bet) < settings.MIN_BET:
            print(f'Error: Minimum bet is {settings.MIN_BET} credits.')

        if int(bet) > max_bet:
            print('Error: You do not have enough credits.')

        if not bet.isdecimal():
            print('Error: Please enter an integer amount.')
            continue

        # Player entered a valid bet
        if settings.MIN_BET <= int(bet) <= max_bet:
            return bet

def get_deck():
    '''Return a list of (rank, suit) tuples for all 52 cards.'''
    deck = []

    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        # Add the numbered cards.
        for rank in range(2,11):
            deck.append((str(rank), suit))
        # Add the face and ace cards.
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
        
    # Return shuffled deck
    random.shuffle(deck)
    return deck

def show_hands(player_hand, dealer_hand, show_dealer_hand):
    '''Show the player's and dealer's cards.
       Hide the dealer's first card if showDealerHand is False.'''
    
    print()
    if show_dealer_hand:
        print(Colour.purple(f'DEALER: {get_hand_value(dealer_hand)}'))
        show_cards(dealer_hand)
    elif not show_dealer_hand:
        print(Colour.purple('DEALER: ???'))
        # Hide the dealer's first card
        show_cards([BACKSIDE] + dealer_hand[1:])
    
    # Show player's hand
    print(Colour.cyan(f'PLAYER: {get_hand_value(player_hand)}'))
    show_cards(player_hand)

def get_hand_value(cards):
    '''Return total value of cards in a certain hand.
       Face cards are worth 10, aces are worth 11 or 1 (this function picks the most suitable ace value)'''
    
    hand_value = 0
    ace_count = 0

    # Add value for non-Ace cards
    for card in cards:
        rank = card[0]  # Each card is a (rank, suit) tuple
        if rank == 'A':
            ace_count += 1
        elif rank in ['J', 'Q', 'K']:
            hand_value += 10 # Face cards are worth 10 points
        else:
            hand_value += int(rank) # Numbered cards are worth their number
    
    # Add value for Ace cards
    hand_value += ace_count # Add 1 per Ace first
    for ace in range(ace_count):
        # If another 10 can be added without busting, do so
        if hand_value + 10 <= 21:
            hand_value + 10
    
    return hand_value

def show_cards(cards):
    '''Show any number of specific cards'''
    rows = ['',
            '',
            '',
            '',
            ''] # Text to be displayed on each row

    for rank, card in enumerate(cards): # Cards is a list of (rank, suit) cards
        rows[0] += ' ___  '  # Print the top line of each card
        if card == BACKSIDE:
            # Print a card's backside
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Print the card's front:
            rank, suit = card  # The card is a (rank, suit) tuple data structure.
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    # Finally, print each row on the screen, for 1x instance of showing cards
    for row in rows:
        print(row)
    
def get_move(player_hand, bet, credits):
    '''Asks the player for their move, 
       and returns 'H' for hit, 'S' for stand, and 'D' for double down'''
    while True:  # Keep looping until the player enters a suitable move
        suitable_moves = ['(H)it', '(S)tand']
        # The player can only double down on their first move, 
        # which we can tell because they'll have exactly two cards:
        if len(player_hand) == 2 and credits > int(bet):
            suitable_moves.append('(D)ouble down')
        # Get the player's move
        movePrompt = ', '.join(suitable_moves) + '?'
        player_move = input(f'{movePrompt}\n > ').upper()
        if player_move[0] in ('H', 'S'):
            return player_move[0]
        if player_move[0] == 'D' and '(D)ouble down' in suitable_moves:
            return player_move[0]
