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
    print "New game started."
    global top_discard
    top_discard = s['initial_discard']
    print "Top discard card: %s" %(top_discard)
    if s['player_id'] == 0:
        game_just_started = True
    print "We are player %s." %(0 if game_just_started else 1)
    return ''

turn_count = 1
def get_move(s):
    global game_just_started
    if game_just_started:
        game_just_started = False

    global turn_count
    if turn_count <= 10:
        turn_count += 1
        return {'move' : 'request_deck'}
    turn_count += 1

    partOfRunLength = [0] * 20
    i = 0
    rack = s['rack']
    discard = s['discard']
    while i < len(rack):
        partOfRunLength[i] = 0
        i += 1
    lastValue = rack[0]
    runLength = 1
    i = 1
    while i < len(rack):
        if rack[i] == lastValue + 1:
            runLength += 1
            if inQuadrant(rack[i], i): 
                j = 0
                while j < runLength:
                    partOfRunLength[i - j] = 0
                    j += 1
                
                partOfRunLength[i - runLength + 1] = runLength
            
        else:
            runLength = 1
        lastValue = rack[i]
        i+=1
    
    i = 0
    while i < len(partOfRunLength):
        rl = partOfRunLength[i]
        if rl > 1:
            if i - 1 > 0 and discard == rack[i] - 1:
                return {'move': "request_discard", 'idx' : i - 1}
            if i + rl < len(rack) and discard == rack[i + rl - 1] + 1:
                return {'move': "request_discard", 'idx' : i+rl}
        
        i += 1
    
    
    divideByFour = (discard-1)/4
    rlIndex = inRunLength(partOfRunLength, divideByFour)
    if rlIndex > -1:
        lowerBound = rack[rlIndex]
        if rlIndex == 0:
            return {'move': "request_discard", 'idx' : 0}
        if rlIndex + partOfRunLength[rlIndex] - 1 > 19:
            return {'move': "request_discard", 'idx' : 19}
        if discard < lowerBound:
            return {'move': "request_discard", 'idx' : rlIndex-1}
        else:
            return {'move': "request_discard", 'idx' : rlIndex + partOfRunLength[rlIndex] - 1}
    
    return {'move' : 'request_deck'}

def get_deck_exchange(s):
    return (s['card']-1)/4
    
def inQuadrant(num, position) :
    upperBound = (num-1)/4 + 3
    lowerBound = (num-1)/4 - 3
    if position < upperBound and position > lowerBound :
        return True
    return False


def inRunLength(runLengths, index):
    i=0
    while i < len(runLengths):
        if runLengths[i] > 0 : #run length
            if index >= i and index < (i+runLengths[i]):
                return i
        i += 1
    return -1


def discardIsGood (rack, discard) :
    placement = (discard-1)/4
    if placement+1>=rack.length or rack[placement+1] > discard :
        return True
    return False

def getBlocked(rack) :
    blocks = []
    lastValue = rack[0]
    run = 1
    i=1
    while i< len(rack) :
        if rack[i] == lastValue+1:
            run+=1
        elif run > 1 :
            j=0
            while(j<run):
                blocks.append(i-j)
                j+=1
            run = 1
        i+=1
    return blocks


# locked
def move_result(s):
    print "Move result: %s" %(s['move'])
    return ''

# locked
def game_result(s):
    print "Game over because %s.\nYour score:  %s\nTheir score: %s" %(s['reason'], s['your_score'], s['other_score'])
    print
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
