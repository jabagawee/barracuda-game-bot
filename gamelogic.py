# /usr/bin/env python

discard_pile = []

# to the pain
def ping(x):
    return 'pong' if x == 'ping' else 'what in the fuck?'

# in all of these functions, stuff is a dictionary
#
# the input section of the docstring will detail how the
# dictionary is structured

def start_game(stuff):
    '''
    The start_game function will be called at the beginning
    of a game, giving you the opportunity to initialize any
    state you may need.

    Input (struct):
    game_id         -- an integer representing the current game
    player_id       -- an zero-indexed integer indicating which
                       player you are
    initial_discard -- an integer of the first card in the
                       discard pile
    other_player_id -- an integer indicating the team ID of the
                       opponent

    Output:
    an empty string
    '''
    discard_pile.append(stuff['initial_discard'])
    return ''

def get_move(stuff):
    '''
    The get_move function will be called to obtain the move
    your player wishes to make.

    Input (struct):
    game_id -- an integer representing the current game
    rack -- a list of 20 integers representing your rack
    discard -- an integer of the first card in the discard pile
    remaining_microseconds -- an integer that no one gives a fuck about
    other_player_moves     -- an empty array if you're player 0 on move 1
                              otherwise, it's an array of an array of...
                              [ an integer representing opponent's index,
                                { 'move'   : 'take_discard' /
                                             'take_deck' / 
                                             'no_move' /
                                             'illegal' /
                                             'timed_out',
                                  'idx'    : an integer index for
                                             'take_discard' and 'take_deck',
                                  'reason' : a reason for illegality }]
    Output (struct):
    move -- 'request_discard' or 'request_deck'
    idx  -- an integer index for which rack position you want to swap
            with the discard pile for
    '''
    my_rack = stuff['rack']
    
    raise NotImplementedError

def get_deck_exchange(stuff):
    raise NotImplementedError

def move_result(stuff):
    raise NotImplementedError

def move_game(stuff):
    raise NotImplementedError

def game_result(stuff):
    raise NotImplementedError
