import sys

from calvin_blackjack import get_bet, get_deck, show_hands, get_hand_value, get_move
from terminal_colourer import Colour
import settings

def main():
    print('''\n\n\n\n
< Blackjack >

  Rules:
    Try to get as close to 21 without going over.
    Kings, Queens, and Jacks are worth 10 points.
    Aces are worth 1 or 11 points.
    Cards 2 through 10 are worth their face value.
    (H)it to take another card.
    (S)tand to stop taking cards.
    On your first play, you can (D)ouble down to increase your bet
    but must hit exactly one more time before standing.
    In case of a tie, the bet is returned to the player.
    The dealer stops hitting at 17.
    (This version doesn't have splitting or insurance.)
          ''')
    
    # Initialise game
    credits = settings.INITIAL_CREDITS

    # Main game loop
    while True:
        # Check that the player has enough credits remaining to continue
        if credits <= settings.MIN_BET:
            if credits <= 0:
                print(Colour.red(f'GAME OVER'))
                print(Colour.red(f'Credits left: {credits} credits'))
                print(Colour.red('You\'re broke! Good thing you weren\'t playing with real money!'))
                sys.exit()
            elif 0 < credits < settings.MIN_BET:
                print(Colour.red(f'''GAME OVER
                        Credits left: {credits} credits
                        You no longer have enough credits for the minimum bet ({settings.MIN_BET} credits)
                '''))
        
        # Let the player bet an amount of credits for the round
        print(Colour.green(f'Credits left: {credits}'))
        bet = int(get_bet(max_bet=credits))

        # Give the player and dealer 2 cards from their deck each
        deck = get_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        # Handles player actions
        print(Colour.bold(f'\nBet: {bet} credits'))

        while True: # Keep looping until the player stands or busts
            show_hands(player_hand, dealer_hand, show_dealer_hand=False)
            print()

            # Check if the player has bust
            if get_hand_value(player_hand) > 21:
                break

            # Gets the player's move ('H', 'S' or 'D')
            player_move = get_move(player_hand, bet, credits - int(bet))

            if player_move == 'D':
                bet += min(bet, (credits - int(bet)))
                print(Colour.bold(f'Bet increased to: {bet} credits.'))
            
            if player_move in ('H', 'D'):
                # Draw another card for the player
                new_card = deck.pop() # Pop a (rank, suit) card from deck (list of cards remaining)
                rank, suit = new_card
                print(Colour.bold(f'\nYou drew a {rank} of {suit}'))
                player_hand.append(new_card)
                
                if get_hand_value(player_hand) > 21:
                    # Player has busted, handled in above break and later
                    continue
            
            if player_move == 'S':
                # Stand/doubling down stops the player's turn.
                print(Colour.bold('You stand.'))
                break
            elif player_move == 'D':
                print(Colour.bold('You double down.'))
                break
    
        # Handles dealer's actions
        '''The dealer must continue hitting until the player busts or their hand value reaches 17 and above or busts'''
        if get_hand_value(player_hand) <= 21:
            while get_hand_value(dealer_hand) < 17:
                # The dealer hits
                print(Colour.bold('\n\nDealer hits...'))
                dealer_hand.append(deck.pop())
                show_hands(player_hand, dealer_hand, show_dealer_hand=False)

                if get_hand_value(dealer_hand) > 21:
                    # The dealer has busted, show later
                    break

                input('Press Enter to continue...')
                print('\n\n')
        
        # Show final hands
        show_hands(player_hand, dealer_hand, show_dealer_hand=True)

        player_value = get_hand_value(player_hand)
        dealer_value = get_hand_value(dealer_hand)

        # Handle whether the player won, lost or tied
        if dealer_value > 21:
            print(Colour.bold(f'Dealer busts! You win {bet} credits!'))
            credits += bet
        elif player_value > 21 or player_value < dealer_value:
            print(Colour.yellow(f'\nYou lost {bet} credits!'))
            credits -= bet
        elif player_value > dealer_value:
            print(Colour.green(f'You won {bet} credits!'))
            credits += bet
        elif player_value == dealer_value:
            print(Colour.bold(f'It\'s a tie! Your credits are returned to you.'))
        
        input('Press Enter to continue...')
            

if __name__ == '__main__':
    main()