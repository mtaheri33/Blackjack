'''
This allows you to play the card game "Blackjack".
An added feature allows you to see the "count" as cards are dealt
to adjust your betting strategy.
The code has not been thoroughly reviewed and tested.
'''

import random

RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
SUITS = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
VALUES = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
          'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

class Card:
    '''
    Each card will be its own object, an instance of this class.
    '''

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = VALUES[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    '''
    The object instance of this class will have a .deck attribute that is a list
    of 2 complete decks, so 104 cards from the Card class.
    '''

    def __init__(self):
        '''
        When the deck object is created, it will add all 52 cards
        from a standard deck to a list.
        It then does this again for a total of 104 cards.
        '''
        self.deck = []
        for _ in range(2):
            for rank in RANKS:
                for suit in SUITS:
                    self.deck.append(Card(rank, suit))

    def __str__(self):
        return f'The deck has {len(self.deck)} card(s).'

    def shuffle_deck(self):
        '''
        This will shuffle the deck list.
        '''
        random.shuffle(self.deck)

    def deal_card(self, cards):
        '''
        This will deal a card by adding the first(top) card in the deck
        to a list.
        After dealing a card, if the deck is empty it will refill.
        '''
        card_ = self.deck.pop(0)
        cards.append(card_)
        if len(self.deck) == 0:
            for _ in range(2):
                for rank in RANKS:
                    for suit in SUITS:
                        self.deck.append(Card(rank, suit))
            self.shuffle_deck()
            print(f'The last card in the deck is the {card_}.  Now there is a new deck.\n')

class Player:
    '''
    The player's cards, car ranks, bet(s), and chips will be under this class.
    He/she starts out with $1000.
    '''

    def __init__(self):
        self.cards = []
        self.card_ranks = []
        self.split_cards = []
        self.split_card_ranks = []
        self.bet = 0
        self.split_bet = 0
        self.chips = 1000

    def __str__(self):
        return f'Chip total: ${self.chips}'

def change_count(last_card, count, deck):
    '''
    This will change the count based on the last card dealt.
    If there is a new deck, the count gets reset to 0.
    '''

    if len(deck.deck) == 104:
        return 0

    if last_card.rank in ('Two', 'Three', 'Four', 'Five', 'Six'):
        return count + 1

    if last_card.rank in ('Seven', 'Eight', 'Nine'):
        return count

    # It is a high card.
    return count - 1

def cards_total(cards):
    '''
    This will determine the total value of a list of cards.
    If it is over 21, it will return 'Bust'.
    If it is 21 or under, it will return the total value.
    '''

    total = 0
    for card_ in cards:
        total += card_.value

    aces = 0
    for card_ in cards:
        if card_.rank == 'Ace':
            aces += 1

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    if total > 21:
        return 'bust'

    # The player did not bust.
    return total

def display_cards(header, cards):
    '''
    This will display the dealer's or player's cards.
    '''

    print(header)

    for card_ in cards:
        print(f'  {str(card_)}')

    print('')

def keep_going(chips):
    '''
    If the player has less than the minimum bet, he/she can no longer play.
    If not, it will ask the player if he/she wants to play another hand.
    It will be used whenever the round is over, such as
    when a player gets blackjack, player busts, dealer busts, etc.
    '''

    if chips < 50:
        return False

    while True:
        choice = input('Would you like to play another hand?  Enter yes or no:')
        if choice.lower() in ['yes', 'y', 'no', 'n']:
            print('')
            break
        print("Enter 'yes', 'y', 'no', or 'n' without quotes.")

    if choice.lower() in ['yes', 'y']:
        return True

    # The player picked no.
    return False


while True:

    INPUT_1 = input('Would you like to play blackjack?  Enter yes or no:')
    if INPUT_1.lower() in ['yes', 'y']:
        KEEP_PLAYING = True
        break
    if INPUT_1.lower() in ['no', 'n']:
        KEEP_PLAYING = False
        break
    print("Enter 'yes', 'y', 'no', or 'n' without quotes.")

# This loop continues until the player does not want to play anymore.
while KEEP_PLAYING:

    # This will set up the game at the beginning.
    DEALER_CARDS = []
    DEALER_CARD_RANKS = []
    COUNT = 0
    PLAYER = Player()
    DECK = Deck()
    DECK.shuffle_deck()

    # This loop continues until the player leaves or does not have enough chips.
    PLAYING = True
    while PLAYING:

        # This will reset the player and dealer lists that are appended to each hand.
        DEALER_CARDS.clear()
        DEALER_CARD_RANKS.clear()
        PLAYER.cards.clear()
        PLAYER.card_ranks.clear()
        PLAYER.split_cards.clear()
        PLAYER.split_card_ranks.clear()
        TOTAL = 0
        SPLIT_TOTAL = 0

        print(f'Count: {COUNT}')

        # This will give a recommended bet.
        if COUNT <= 1:
            print('Recommended bet: $50')
        elif COUNT == 2:
            print('Recommended bet: $100')
        elif COUNT == 3:
            print('Recommended bet: $150')
        elif COUNT == 4:
            print('Recommended bet: $200')
        elif COUNT == 5:
            print('Recommended bet: $250')
        elif COUNT >= 6:
            print('Recommended bet: $300')

        print(PLAYER)

        # This will ask for and save the player's bet.
        while True:
            try:
                PLAYER.bet = int(input('How much would you like to bet?  \
Enter a multiple of 10, and the minimum bet is $50.'))
            except ValueError:
                print('Enter a number.  Do not use $.')
            else:
                if PLAYER.bet < 50:
                    print('The minimum bet is $50.')
                elif PLAYER.bet % 10 != 0:
                    print('Enter a multiple of 10.')
                else:
                    print('')
                    break

        '''
        This will deal a card to the player and then a face-up card to the dealer.
        It will then deal another card to the player and then a face-down card to the dealer.
        As a result, the count is only updated based on the first three cards dealt.
        '''
        DECK.deal_card(PLAYER.cards)
        COUNT = change_count(PLAYER.cards[-1], COUNT, DECK)
        DECK.deal_card(DEALER_CARDS)
        COUNT = change_count(DEALER_CARDS[-1], COUNT, DECK)
        DECK.deal_card(PLAYER.cards)
        COUNT = change_count(PLAYER.cards[-1], COUNT, DECK)
        DECK.deal_card(DEALER_CARDS)

        # This will display the cards and the updated count.
        display_cards("Dealer's cards:", [DEALER_CARDS[0], 'Face-down card'])
        display_cards("Player's cards:", PLAYER.cards)
        print(f'Count: {COUNT}\n')

        # This will create a list of card ranks for the player and dealer.
        for card in PLAYER.cards:
            PLAYER.card_ranks.append(card.rank)
        for card in DEALER_CARDS:
            DEALER_CARD_RANKS.append(card.rank)

        # This will check if the player has blackjack.
        if 'Ace' in PLAYER.card_ranks and ('Ten' in PLAYER.card_ranks
                                           or 'Jack' in PLAYER.card_ranks
                                           or 'Queen' in PLAYER.card_ranks
                                           or 'King' in PLAYER.card_ranks):
            # This will check if the dealer also has blackjack.
            if 'Ace' in DEALER_CARD_RANKS and ('Ten' in DEALER_CARD_RANKS
                                               or 'Jack' in DEALER_CARD_RANKS
                                               or 'Queen' in DEALER_CARD_RANKS
                                               or 'King' in DEALER_CARD_RANKS):
                COUNT = change_count(DEALER_CARDS[-1], COUNT, DECK)
                display_cards("Dealer's cards:", DEALER_CARDS)
                display_cards("Player's cards:", PLAYER.cards)
                print(f'Count: {COUNT}\n')
                print('Push\n')
                PLAYING = keep_going(PLAYER.chips)
                continue
            # This will run if the player has blackjack and the dealer does not.
            COUNT = change_count(DEALER_CARDS[-1], COUNT, DECK)
            display_cards("Dealer's cards:", DEALER_CARDS)
            display_cards("Player's cards:", PLAYER.cards)
            print(f'Count: {COUNT}\n')
            print(f'Player has blackjack and wins ${int(1.5*PLAYER.bet)}.\n')
            PLAYER.chips += int(1.5 * PLAYER.bet)
            PLAYING = keep_going(PLAYER.chips)
            continue

        # This will check if the dealer has blackjack.
        if DEALER_CARD_RANKS[0] in ('Ten', 'Jack', 'Queen', 'King', 'Ace'):
            print('Checking if the dealer has blackjack...')
            if 'Ace' in DEALER_CARD_RANKS and ('Ten' in DEALER_CARD_RANKS
                                               or 'Jack' in DEALER_CARD_RANKS
                                               or 'Queen' in DEALER_CARD_RANKS
                                               or 'King' in DEALER_CARD_RANKS):
                COUNT = change_count(DEALER_CARDS[-1], COUNT, DECK)
                display_cards("Dealer's cards:", DEALER_CARDS)
                display_cards("Player's cards:", PLAYER.cards)
                print(f'Count: {COUNT}\n')
                print(f'Dealer has blackjack and player loses ${PLAYER.bet}.\n')
                PLAYER.chips -= PLAYER.bet
                PLAYING = keep_going(PLAYER.chips)
                continue
            print('Dealer does not have blackjack.\n')

        # This will ask for and store the player's next decision.
        if PLAYER.card_ranks[0] == PLAYER.card_ranks[1]:
            while True:
                INPUT_2 = input('Would you like to hit, stand, double down, or split?')
                if INPUT_2.lower() in ['hit', 'h', 'stand', 's', 'double down',
                                       'doubledown', 'double-down', 'dd', 'split']:
                    print('')
                    break
                print("Enter 'hit' or 'h' without quotes if you want to hit.")
                print("Enter 'stand' or 's' without quotes if you want to stand.")
                print("Enter 'double down' or 'dd' without quotes if you want to double down.")
                print("Enter 'split' without quotes if you want to split.")
        else:
            while True:
                INPUT_2 = input('Would you like to hit, stand, or double down?')
                if INPUT_2.lower() in ['hit', 'h', 'stand', 's', 'double down',
                                       'doubledown', 'double-down', 'dd']:
                    print('')
                    break
                print("Enter 'hit' or 'h' without quotes if you want to hit.")
                print("Enter 'stand' or 's' without quotes if you want to stand.")
                print("Enter 'double down' or 'dd' without quotes if you want to double down.")

        '''
        This will start with the player's first hand and deal a card.
        It will check if he/she has blackjack.
        If not, the player will be able to hit until he/she busts or stands.
        This then repeats for the second hand.
        '''
        INPUT_3 = ''
        INPUT_4 = ''
        if INPUT_2.lower() == 'split':
            # This will transfer one card to the second hand.
            PLAYER.split_cards.append(PLAYER.cards.pop())
            PLAYER.split_bet = PLAYER.bet
            # This will deal a card to the first hand and display the cards.
            DECK.deal_card(PLAYER.cards)
            COUNT = change_count(PLAYER.cards[-1], COUNT, DECK)
            display_cards("Dealer's cards:", [DEALER_CARDS[0], 'Face-down card'])
            display_cards("Player's cards:", PLAYER.cards)
            display_cards("Player's split cards:", PLAYER.split_cards)
            print(f'Count: {COUNT}\n')
            # This will check if the first hand is a blackjack.
            FIRST_HAND = True
            PLAYER.card_ranks.clear()
            for card in PLAYER.cards:
                PLAYER.card_ranks.append(card.rank)
            if 'Ace' in PLAYER.card_ranks and ('Ten' in PLAYER.card_ranks
                                               or 'Jack' in PLAYER.card_ranks
                                               or 'Queen' in PLAYER.card_ranks
                                               or 'King' in PLAYER.card_ranks):
                print(f'Player has blackjack and wins ${int(1.5*PLAYER.bet)}.\n')
                PLAYER.chips += int(1.5 * PLAYER.bet)
                FIRST_HAND = False
            # The first hand is not blackjack, and FIRST_HAND still equals True.
            while FIRST_HAND:
                while True:
                    INPUT_3 = input("Would you like to hit or stand on Player's cards?")
                    if INPUT_3.lower() in ['hit', 'h', 'stand', 's']:
                        print('')
                        break
                    print("Enter 'hit' or 'h' without quotes if you want to hit.")
                    print("Enter 'stand' or 's' without quotes if you want to stand.")
                # The player chose to stand.
                if INPUT_3.lower() in ['stand', 's']:
                    break
                # The player chose to hit.
                DECK.deal_card(PLAYER.cards)
                COUNT = change_count(PLAYER.cards[-1], COUNT, DECK)
                display_cards("Dealer's cards:", [DEALER_CARDS[0], 'Face-down card'])
                display_cards("Player's cards:", PLAYER.cards)
                display_cards("Player's split cards:", PLAYER.split_cards)
                print(f'Count: {COUNT}\n')
                TOTAL = cards_total(PLAYER.cards)
                if TOTAL == 'bust':
                    print(f'Player busts and loses ${PLAYER.bet}.\n')
                    PLAYER.chips -= PLAYER.bet
                    break
                '''
                The player did not bust, so the loop repeats
                and he/she can choose to hit again or stand.
                '''
            # Most of this is copied from above and applies to the second hand.
            DECK.deal_card(PLAYER.split_cards)
            COUNT = change_count(PLAYER.split_cards[-1], COUNT, DECK)
            display_cards("Dealer's cards:", [DEALER_CARDS[0], 'Face-down card'])
            if INPUT_3.lower() in ['stand', 's']:
                display_cards("Player's cards:", PLAYER.cards)
            display_cards("Player's split cards:", PLAYER.split_cards)
            print(f'Count: {COUNT}\n')
            SECOND_HAND = True
            for card in PLAYER.split_cards:
                PLAYER.split_card_ranks.append(card.rank)
            if 'Ace' in PLAYER.split_card_ranks and ('Ten' in PLAYER.split_card_ranks
                                                     or 'Jack' in PLAYER.split_card_ranks
                                                     or 'Queen' in PLAYER.split_card_ranks
                                                     or 'King' in PLAYER.split_card_ranks):
                print(f'Player has blackjack and wins ${int(1.5*PLAYER.split_bet)}.\n')
                PLAYER.chips += int(1.5 * PLAYER.split_bet)
                SECOND_HAND = False
            # This is an opportunity for the round to be over.
            if INPUT_3.lower() not in ['stand', 's'] and not SECOND_HAND:
                COUNT = change_count(DEALER_CARDS[-1], COUNT, DECK)
                display_cards("Dealer's cards:", DEALER_CARDS)
                print(f'Count: {COUNT}\n')
                PLAYING = keep_going(PLAYER.chips)
                continue
            while SECOND_HAND:
                while True:
                    INPUT_4 = input("Would you like to hit or stand on Player's split cards?")
                    if INPUT_4.lower() in ['hit', 'h', 'stand', 's']:
                        print('')
                        break
                    print("Enter 'hit' or 'h' without quotes if you want to hit.")
                    print("Enter 'stand' or 's' without quotes if you want to stand.")
                if INPUT_4.lower() in ['stand', 's']:
                    break
                DECK.deal_card(PLAYER.split_cards)
                COUNT = change_count(PLAYER.split_cards[-1], COUNT, DECK)
                display_cards("Dealer's cards:", [DEALER_CARDS[0], 'Face-down card'])
                if INPUT_3.lower() in ['stand', 's']:
                    display_cards("Player's cards:", PLAYER.cards)
                display_cards("Player's split cards:", PLAYER.split_cards)
                print(f'Count: {COUNT}\n')
                SPLIT_TOTAL = cards_total(PLAYER.split_cards)
                if SPLIT_TOTAL == 'bust':
                    print(f'Player busts and loses ${PLAYER.split_bet}.\n')
                    PLAYER.chips -= PLAYER.split_bet
                    break
            # Both hands are now finished, but the round may already be over.
            if INPUT_3.lower() not in ['stand', 's'] and INPUT_4.lower() not in ['stand', 's']:
                COUNT = change_count(DEALER_CARDS[-1], COUNT, DECK)
                display_cards("Dealer's cards:", DEALER_CARDS)
                print(f'Count: {COUNT}\n')
                PLAYING = keep_going(PLAYER.chips)
                continue

        # This will run if the player chose to hit.
        while INPUT_2.lower() in ['hit', 'h']:
            DECK.deal_card(PLAYER.cards)
            COUNT = change_count(PLAYER.cards[-1], COUNT, DECK)
            display_cards("Dealer's cards:", [DEALER_CARDS[0], 'Face-down card'])
            display_cards("Player's cards:", PLAYER.cards)
            print(f'Count: {COUNT}\n')
            TOTAL = cards_total(PLAYER.cards)
            if TOTAL == 'bust':
                print(f'Player busts and loses ${PLAYER.bet}.\n')
                PLAYER.chips -= PLAYER.bet
                break
            # The player did not bust, so he/she can choose to hit again or stand.
            while True:
                INPUT_2 = input('Would you like to hit or stand?')
                if INPUT_2.lower() in ['hit', 'h', 'stand', 's']:
                    print('')
                    break
                print("Enter 'hit' or 'h' without quotes if you want to hit.")
                print("Enter 'stand' or 's' without quotes if you want to stand.")
            # The player chose to stand.
            if INPUT_2.lower() in ['stand', 's']:
                break
            # The player chose to hit again and the loop repeats.
        # If the player busted, so the round is over.
        if TOTAL == 'bust':
            COUNT = change_count(DEALER_CARDS[-1], COUNT, DECK)
            display_cards("Dealer's cards:", DEALER_CARDS)
            print(f'Count: {COUNT}\n')
            PLAYING = keep_going(PLAYER.chips)
            continue

        # This will run if the player chose to double down.
        if INPUT_2.lower() in ['double down', 'doubledown', 'double-down', 'dd']:
            PLAYER.bet = 2 * PLAYER.bet
            DECK.deal_card(PLAYER.cards)
            COUNT = change_count(PLAYER.cards[-1], COUNT, DECK)
            display_cards("Dealer's cards:", [DEALER_CARDS[0], 'Face-down card'])
            display_cards("Player's cards:", PLAYER.cards)
            print(f'Count: {COUNT}\n')
            TOTAL = cards_total(PLAYER.cards)
            if TOTAL == 'bust':
                print(f'Player busts and loses ${PLAYER.bet}.\n')
                PLAYER.chips -= PLAYER.bet
                COUNT = change_count(DEALER_CARDS[-1], COUNT, DECK)
                display_cards("Dealer's cards:", DEALER_CARDS)
                print(f'Count: {COUNT}\n')
                PLAYING = keep_going(PLAYER.chips)
                continue
            # The player did not bust, and his/her hand is finished.

        #It is now the dealer's turn.

        # The player chose to stand with both the hand and split hand.
        DEALER_TURN = True
        while INPUT_3.lower() in ['stand', 's'] and INPUT_4.lower() in ['stand', 's']:
            COUNT = change_count(DEALER_CARDS[-1], COUNT, DECK)
            display_cards("Dealer's cards:", DEALER_CARDS)
            display_cards("Player's cards:", PLAYER.cards)
            display_cards("Player's split cards:", PLAYER.split_cards)
            print(f'Count: {COUNT}\n')
            DEALER_TOTAL = cards_total(DEALER_CARDS)
            # The dealer busts after drawing at least one other card.
            if DEALER_TOTAL == 'bust':
                print(f'Dealer busts and player wins ${PLAYER.bet + PLAYER.split_bet}.\n')
                PLAYER.chips += PLAYER.bet + PLAYER.split_bet
                DEALER_TURN = False
                break
            # The total is less than 17, so the dealer needs to draw another card.
            if DEALER_TOTAL < 17:
                DECK.deal_card(DEALER_CARDS)
                continue
            # The total is 17 or greater.
            if DEALER_TOTAL >= 17:
                # These if statements are for scenarios only involving the first hand.
                if TOTAL > DEALER_TOTAL:
                    print(f'Player has a higher total and wins {PLAYER.bet}.')
                    PLAYER.chips += PLAYER.bet
                elif TOTAL == DEALER_TOTAL:
                    print('Push')
                else:
                    print(f'Player has a lower total and loses {PLAYER.bet}.')
                    PLAYER.chips -= PLAYER.bet
                # These if statements are for scenarios only involving the second hand.
                if SPLIT_TOTAL > DEALER_TOTAL:
                    print(f'Player has a higher split total and wins {PLAYER.split_bet}.\n')
                    PLAYER.chips += PLAYER.split_bet
                elif SPLIT_TOTAL == DEALER_TOTAL:
                    print('Push\n')
                else:
                    print(f'Player has a lower split total and loses {PLAYER.split_bet}.\n')
                    PLAYER.chips -= PLAYER.split_bet
                DEALER_TURN = False
                break

        # The player chose to stand with only the split hand.
        while INPUT_3.lower() not in ['stand', 's'] and INPUT_4.lower() in ['stand', 's']:
            COUNT = change_count(DEALER_CARDS[-1], COUNT, DECK)
            display_cards("Dealer's cards:", DEALER_CARDS)
            display_cards("Player's split cards:", PLAYER.split_cards)
            print(f'Count: {COUNT}\n')
            DEALER_TOTAL = cards_total(DEALER_CARDS)
            # The dealer busts after drawing at least one other card.
            if DEALER_TOTAL == 'bust':
                print(f'Dealer busts and player wins ${PLAYER.split_bet}.\n')
                PLAYER.chips += PLAYER.split_bet
                DEALER_TURN = False
                break
            # The total is less than 17, so the dealer needs to draw another card.
            if DEALER_TOTAL < 17:
                DECK.deal_card(DEALER_CARDS)
                continue
            # The total is 17 or greater.
            if DEALER_TOTAL >= 17:
                if SPLIT_TOTAL > DEALER_TOTAL:
                    print(f'Player has a higher split total and wins {PLAYER.split_bet}.\n')
                    PLAYER.chips += PLAYER.split_bet
                elif SPLIT_TOTAL == DEALER_TOTAL:
                    print('Push\n')
                else:
                    print(f'Player has a lower split total and loses {PLAYER.split_bet}.\n')
                    PLAYER.chips -= PLAYER.split_bet
                DEALER_TURN = False
                break

        # The player only has one hand.
        while DEALER_TURN:
            COUNT = change_count(DEALER_CARDS[-1], COUNT, DECK)
            display_cards("Dealer's cards:", DEALER_CARDS)
            display_cards("Player's cards:", PLAYER.cards)
            print(f'Count: {COUNT}\n')
            DEALER_TOTAL = cards_total(DEALER_CARDS)
            # The dealer busts after drawing at least one other card.
            if DEALER_TOTAL == 'bust':
                print(f'Dealer busts and player wins ${PLAYER.bet}.\n')
                PLAYER.chips += PLAYER.bet
                break
            # The total is less than 17, so the dealer needs to draw another card.
            if DEALER_TOTAL < 17:
                DECK.deal_card(DEALER_CARDS)
                continue
            # The total is 17 or greater.
            if DEALER_TOTAL >= 17:
                if TOTAL > DEALER_TOTAL:
                    print(f'Player has a higher total and wins {PLAYER.bet}.\n')
                    PLAYER.chips += PLAYER.bet
                elif TOTAL == DEALER_TOTAL:
                    print('Push\n')
                else:
                    print(f'Player has a lower total and loses {PLAYER.bet}.\n')
                    PLAYER.chips -= PLAYER.bet
                break

        # The round is now over.
        PLAYING = keep_going(PLAYER.chips)

    print(PLAYER)
    print('')

    while True:
        INPUT_5 = input('Would you like to play a new game?  Enter yes or no:')
        if INPUT_5.lower() in ['yes', 'y']:
            KEEP_PLAYING = True
            break
        if INPUT_5.lower() in ['no', 'n']:
            KEEP_PLAYING = False
            break
        print("Enter 'yes', 'y', 'no', or 'n' without quotes.")
