from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import random
import sys

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("172.16.73.133", int(sys.argv[1])), requestHandler=RequestHandler)
server.register_introspection_functions()

# Variables to store state
top_discard, not_top_discard = 0, set()
opponent_range = set(range(1,80+1))
opponent_rack = [0] * 20
game_just_started = False

# locked
def ping(x):
    return 'pong' if x == 'ping' else 'what in the fuck'

# half locked
def start_game(s):
    print "New game started.\n"
    global top_discard
    top_discard = s['initial_discard']
    print "Top discard card: %s.\n" %(top_discard)
    if s['player_id'] == 0:
        game_just_started = True
    print "We are player %s.\n" %(0 if game_just_started else 1)
    return ''

def get_move(s):
    # return {'move' : 'request_discard', 'idx' : -1}
    global game_just_started
    if game_just_started:
        game_just_started = False
        return {'move' : 'request_discard', 'idx' : random.randint(0, 19)}
    d = s['discard']
    r = s['rack']
    if d - 1 in r and r.index(d - 1) < 19 and abs((r.index(d - 1) + 1) * 4 - d) < 3:
        print 'request_discard @ %s' %(r.index(d-1)+1)
        return {'move' : 'request_discard', 'idx' : r.index(d-1) + 1}
    elif d - 2 in r and r.index(d - 2) < 18 and abs((r.indx(d - 1) + 1) * 4 - d) < 3:
        print 'request_discard @ %s' %(r.index(d-2)+2)
        return {'move' : 'request_discard', 'idx' : r.index(d-2) + 2}
    # elif d - 3 in r and r.index(d - 3) < 17:
    #     return {'move' : 'request_discard', 'idx' : r.index(d-3) + 3}
    else:
        print 'going to request_deck'
        return {'move' : 'request_deck'}

def get_deck_exchange(s):
    r = s['rack'] # [int] * 20
    c = s['card'] # int
    if c - 1 in r and r.index(c - 1) < 19 and abs((r.index(c - 1) + 1) * 4 - c) < 3:
        print 'request_deck @ %s' %(r.index(c-1)+1)
        return r.index(c - 1) + 1
    elif c - 2 in r and r.index(c - 2) < 18 and abs((r.index(c - 1) + 1) * 4 - c) < 3:
        print 'request_deck @ %s' %(r.index(c-2)+2)
        return r.index(c - 2) + 2
    # elif c - 3 in r and r.index(c - 3) < 17:
    #     return r.index(c - 3) + 3
    else:
        print 'request_deck @ %s' %((c-1)/4)
        return (c - 1) / 4

# locked
def move_result(s):
    print "Move result: %s.\n" %(s['move'])
    if s['move'] == 'move_ended_game':
        print s['reason']
    return ''

# locked
def game_result(s):
    print "Game over because %s.\nYour score:  %s\nTheir score: %s\n\n" %(s['reason'], s['your_score'], s['other_score'])
    return ''

# functions that are defined in gamelogic.py
server.register_function(ping)
server.register_function(start_game)
server.register_function(get_move)
server.register_function(get_deck_exchange)
server.register_function(move_result)
server.register_function(game_result)

# Run the server's main loop
server.serve_forever()
