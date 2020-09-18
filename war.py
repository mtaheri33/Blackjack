'''
This allows you to see the card game "War".
'''

import random
from IPython.display import clear_output


RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
SUITS = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
VALUES = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
          'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}


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
    of all 52 cards from the Card class.
    '''

    def __init__(self):
        self.deck = []
        for rank in RANKS:
            for suit in SUITS:
                self.deck.append(Card(rank, suit))

    def __str__(self):
        return f'The deck has {len(self.deck)} cards.'

    def shuffle_deck(self):
        '''
        This will shuffle the deck list.
        '''
        random.shuffle(self.deck)

    def deal_deck(self, player_1_hand, player_2_hand):
        '''
        This will deal half of the deck to each player.
        '''
        for _ in range(26):
            player_1_hand.hand.append(self.deck.pop(0))
            player_2_hand.hand.append(self.deck.pop(0))


class Hand:
    '''
    The object instance of this class will have a .hand attribute that is a list
    of the card objects they possess.
    '''

    def __init__(self, player_name):
        self.player_name = player_name
        self.hand = []

    def __str__(self):
        return f'{self.player_name} has {len(self.hand)} cards in his/her hand.'

    def play_card(self, board):
        '''
        This will play the top (index=0) card in the hand on the board.
        '''
        board.append(self.hand.pop(0))

    def take_cards(self, board_1, board_2):
        '''
        This will take the cards from both boards and then clear the boards.
        '''
        self.hand.extend(board_1)
        self.hand.extend(board_2)
        board_1.clear()
        board_2.clear()


def compare_boards(player_1_board, player_1_hand, player_2_board, player_2_hand):
    '''
    This will compare the value of the last card in each player's board.
    If there is a winner, that player will take all of the cards.
    If the cards are equal, war is needed.
    '''

    if player_1_board[-1].value > player_2_board[-1].value:
        print('Player 1 wins the round.')
        player_1_hand.take_cards(player_1_board, player_2_board)
        return False

    if player_1_board[-1].value < player_2_board[-1].value:
        print('Player 2 wins the round.')
        player_2_hand.take_cards(player_2_board, player_1_board)
        return False

    print('War:')
    return True



while True:
    INPUT_1 = input('Would you like to see a game of war played?  Enter yes or no:')
    if INPUT_1.lower() in ['yes', 'y']:
        KEEP_PLAYING = True
        break
    if INPUT_1.lower() in ['no', 'n']:
        KEEP_PLAYING = False
        break
    print('Please enter yes or no.')


# This loop continues until the user does not want to see any more games of War.
while KEEP_PLAYING:

    # This will set up the game at the beginning.
    PLAYER_1_HAND = Hand('Player 1')
    PLAYER_2_HAND = Hand('Player 2')
    PLAYER_1_BOARD = []
    PLAYER_2_BOARD = []
    DECK = Deck()
    DECK.shuffle_deck()
    DECK.deal_deck(PLAYER_1_HAND, PLAYER_2_HAND)
    print(PLAYER_1_HAND)
    print(PLAYER_2_HAND)


    # This loop continues until a player has zero cards or does not have enough cards for war.
    PLAYING = True
    ROUND = 0
    while PLAYING:

        '''
        The first turn.
        If there is a winner, it skips over the while NEED_WAR block below and
        prints the new card total for each player's hand.
        If the cards are equal, war is needed.
        '''
        ROUND += 1
        PLAYER_1_HAND.play_card(PLAYER_1_BOARD)
        PLAYER_2_HAND.play_card(PLAYER_2_BOARD)
        print(f'\nRound {ROUND}')
        print('{0:^18}    {1:^18}'.format("Player 1's card:", "Player 2's card:"))
        print('{0:^18}    {1:^18}'.format(str(PLAYER_1_BOARD[-1]), str(PLAYER_2_BOARD[-1])))
        NEED_WAR = compare_boards(PLAYER_1_BOARD, PLAYER_1_HAND, PLAYER_2_BOARD, PLAYER_2_HAND)


        '''
        This loop runs if the first turn of the round has equal cards.
        It will repeat if the latest war results in equal cards again, or else it stops.
        '''
        while NEED_WAR:

            if len(PLAYER_1_HAND.hand) < 4:
                print('Player 1 does not have enough cards left for war.')
                break
            if len(PLAYER_2_HAND.hand) < 4:
                print('Player 2 does not have enough cards left for war.')
                break

            for _ in range(3):
                PLAYER_1_HAND.play_card(PLAYER_1_BOARD)
                PLAYER_2_HAND.play_card(PLAYER_2_BOARD)
                print('{0:^18}    {1:^18}'.format('Face-down card', 'Face-down card'))
            PLAYER_1_HAND.play_card(PLAYER_1_BOARD)
            PLAYER_2_HAND.play_card(PLAYER_2_BOARD)
            print('{0:^18}    {1:^18}'.format(str(PLAYER_1_BOARD[-1]), str(PLAYER_2_BOARD[-1])))
            NEED_WAR = compare_boards(PLAYER_1_BOARD, PLAYER_1_HAND, PLAYER_2_BOARD, PLAYER_2_HAND)


        print(PLAYER_1_HAND)
        print(PLAYER_2_HAND)


        '''
        This if statement is only triggered when war was needed,
        but a player did not have enough cards.
        The check for having at least 4 cards is repeated in order to
        print the correct player who won.
        This print statement was not included in the NEED_WAR loop because if it was,
        it would then print how many cards each player has after it.
        Ex:
        Player 2 has won.
        Player 1 has ... cards.
        Player 2 has ... cards.
        In addition, if it was included and the player used their last card
        which triggered war, it would print the other player won.  Since
        the player now has zero cards, it would print the other player won again.
        Ex:
        Player 2 has won.
        Player 1 has 0 cards.
        Player 2 has 50 cards.
        Player 2 has won.
        This way, the player who won statement is always the last line,
        and it is only printed once.
        '''
        if NEED_WAR:

            if len(PLAYER_1_HAND.hand) < 4:
                print('\nPlayer 2 has won.\n')
                PLAYING = False
            else:
                print('\nPlayer 1 has won.\n')
                PLAYING = False


        if len(PLAYER_1_HAND.hand) == 0:
            print('\nPlayer 2 has won.\n')
            PLAYING = False
        elif len(PLAYER_2_HAND.hand) == 0:
            print('\nPlayer 1 has won.\n')
            PLAYING = False


    while True:
        INPUT_2 = input('Would you like to see another game of war played?  Enter yes or no:')
        if INPUT_2.lower() in ['yes', 'y']:
            KEEP_PLAYING = True
            clear_output()
            break
        if INPUT_2.lower() in ['no', 'n']:
            KEEP_PLAYING = False
            break
        print('Please enter yes or no.')
