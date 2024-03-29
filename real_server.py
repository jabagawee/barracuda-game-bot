from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("172.16.73.133", 8000), requestHandler=RequestHandler)
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
    global top_discard
    top_discard = s['initial_discard']
    if s['player_id'] == 0:
        game_just_started = True
    return ''

def get_move(s):
    pass

def get_deck_exchange(s):
    pass

# locked
def move_result(s):
    print "Move result: %s" %(s['move'])
    return ''

# locked
def game_result(s):
    print "Game over because %s.\nYour score: %s\nOther score:%s" %(s['reason'], s['your_score'], s['other_score'])
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
