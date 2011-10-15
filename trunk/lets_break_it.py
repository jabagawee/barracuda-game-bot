#! /usr/bin/env python

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import random
import sys
import time

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("172.16.73.133", int(sys.argv[1])), requestHandler=RequestHandler)
server.register_introspection_functions()

partOfRunLength = []
distanceFromOptimal = []

discards = []
opponentKnownCards = set()

deckSize = 39
discardSize = 1

turnNum = 0

notTurnNumed = True

focus = None

def ping(x):
    return 'pong' if x == 'ping' else 'fuck you'

def start_game(s):
    global turnNum
    turnNum = 0
    discards.append(s['initial_discard'])
    return ''

def get_move(s):
    global turnNum
    global deckSize
    global discardSize
    global discards
    global partOfRunLength
    global distanceFromOptimal
    turnNum += 1

    # if turnNum <= sys.argv[3]:
     #   return makeMove('request_deck', 0, s['rack'])

    if s['other_player_moves'] != [] and s['other_player_moves'][0][1]['move'] == 'take_deck':
        deckSize -= 1
        discardSize += 1

    if deckSize == 0:
        deckSize = 39
        discardSize = 1
        # topDiscard = discards.pop()
        discards = [discards.pop()]

    if s['other_player_moves'] != [] and s['other_player_moves'][0][1]['move'] == 'take_discard':
        opponentKnownCards.add(discards.pop())

    if s['other_player_moves'] != []:
        discards.append(s['discard'])

    if s['discard'] in opponentKnownCards:
        opponentKnownCards.remove(s['discard'])
    
    partOfRunLength = [1] * 20
    lastValue = s['rack'][0]
    runLength = 1
    for i in xrange(1, 20):
        if s['rack'][i] == lastValue + 1:
            runLength += 1
            if inQuadrant(s['rack'][i], i): # not necessarily needed
                for j in xrange(runLength):
                    partOfRunLength[i - j] = 0
                partOfRunLength[i - runLength + 1] = runLength
        else:
            runLength = 1
        lastValue = s['rack'][i]


    # if max(partOfRunLength) >= 5:
        # new mode

    '''
    for i in xrange(20):
        print 'loop %s' %(i)
        print partOfRunLength
        right_adjacent, left_adjacent = 20, 20
        if partOfRunLength[i] > 1:
            if i + partOfRunLength[i] < 20:
                right_adjacent = partOfRunLength[i+partOfRunLength[i]]
            print 'right_adjacent: %s' %(right_adjacent)
            j = i - 1
            while j >= 0 and partOfRunLength[j] == 0:
                j -= 1
            left_adjacent =  partOfRunLength[j]
            if partOfRunLength[i] > right_adjacent:
                for k in xrange(right_adjacent):
                    partOfRunLength[i+partOfRunLength[i]+k] = 1
            if partOfRunLength[i] > left_adjacent:
                for k in xrange(j):
                    partOfRunLength[i-k] = 1
    '''

    totalDistance = 0
    distanceFromOptimal = [0] * 20
    for i in xrange(20):
        distanceFromOptimal[i] = abs(i - (s['rack'][i] - 1) / 4)
        totalDistance += distanceFromOptimal[i]

    rlFound = 1
    # if isInOrder(s['rack']):
    if countRedSquares(s['rack']) < int(sys.argv[2]):
        if focus != None:
            if s['discard'] == s['rack'][focus] - 1 and focus > 0:
                if inRunLength(partOfRunLength, focus - 1) <= partOfRunLength[focus]:
                    return makeMove('request_discard', focus - 1, s['rack'])
            if s['discard'] == s['rack'][focus + partOfRunLength[focus] - 1] + 1 and focus + partOfRunLength[focus] < 20:
                if inRunLength(partOfRunLength, focus + partOfRunLength[focus]) <= partOfRunLength[focus]:
                    return makeMove('request_discard', focus + partOfRunLength[focus], s['rack'])

        for i in xrange(20):
            if partOfRunLength[i] > 0:
                rlFound = max(rlFound, partOfRunLength[i])
                thing = True
                '''
                if partOfRunLength[i] == 1:
                    for x in xrange(-5, 6):
                        if i+x < 0 or i+x>19 or x == 0:
                            continue
                        if partOfRunLength[i+x] > 1:
                            thing = False

                    for x in xrange(-2, 3):
                        if i+x < 0 or i+x > 19 or x == 0:
                            continue
                        if inRunLength(partOfRunLength, i+x) > 1:
                            thing = False
                '''


                if s['discard'] == s['rack'][i] - 1 and i > 0:
                    if thing and inRunLength(partOfRunLength, i - 1) <= partOfRunLength[i]:
                        return makeMove('request_discard', i - 1, s['rack'])
                if s['discard'] == s['rack'][i + partOfRunLength[i] - 1] + 1 and i + partOfRunLength[i] < 20:
                    if thing and inRunLength(partOfRunLength, i + partOfRunLength[i]) <= partOfRunLength[i]:
                        return makeMove('request_discard', i + partOfRunLength[i], s['rack'])

        if rlFound > 1: # and turnNum > 25:
            for i in xrange(20):
                new_rack = s['rack'][:]
                new_rack[i] = s['discard']
                if isInOrder(new_rack) and inRunLength(partOfRunLength, i) < 2:
                    return makeMove('request_discard', i, s['rack'])

        return makeMove('request_deck', 0, s['rack'])
        
    if distanceFromOptimal[(s['discard'] - 1) / 4] == 0:
        return makeMove('request_deck', 0, s['rack']);
    else:
        return makeMove('request_discard', (s['discard'] - 1) / 4, s['rack'])
    
def makeMove(move, idx, rack):
    global discards

    if move == 'request_discard':
        discards.pop()
        discards.append(rack[idx])
        return {'move' : move, 'idx' : idx}

    return {'move' : move}
    
def get_deck_exchange(s):
    global partOfRunLength
    global focus

    # if turnNum <= sys.argv[3]:
    #     return deckExchange((s['card']-1)/4, s['rack'])

    rlFound = 1

    if countRedSquares(s['rack']) < int(sys.argv[2]):
        if focus != None:
            if s['card'] == s['rack'][focus] - 1 and focus > 0:
                if inRunLength(partOfRunLength, focus - 1) <= partOfRunLength[focus]:
                    return deckExchange(focus - 1, s['rack'])
            if s['card'] == s['rack'][focus + partOfRunLength[focus] - 1] + 1 and focus + partOfRunLength[focus] < 20:
                if inRunLength(partOfRunLength, focus + partOfRunLength[focus]) <= partOfRunLength[focus]:
                    return deckExchange(focus + partOfRunLength[focus], s['rack'])
        for i in xrange(20):
            if partOfRunLength[i] > 0:
                thing = True
                '''
                if partOfRunLength[i] == 1:
                    for x in xrange(-5, 6):
                        if i+x < 0 or i+x>19 or x == 0:
                            continue
                        if partOfRunLength[i+x] > 1:
                            thing = False

                    for x in xrange(-2, 3):
                        if i+x < 0 or i+x > 19 or x == 0:
                            continue
                        if inRunLength(partOfRunLength, i+x) > 1:
                            thing = False
                '''

                rlFound = max(rlFound, partOfRunLength[i])
                if s['card'] == s['rack'][i] - 1 and i > 0:
                    if thing and inRunLength(partOfRunLength, i - 1) <= partOfRunLength[i]:
                        return deckExchange(i - 1, s['rack'])
                if s['card'] == s['rack'][i + partOfRunLength[i] - 1] + 1 and i + partOfRunLength[i] < 20:
                    if thing and inRunLength(partOfRunLength, i + partOfRunLength[i]) <= partOfRunLength[i]:
                        return deckExchange(i + partOfRunLength[i], s['rack'])

    for i in xrange(20):
        new_rack = s['rack'][:]
        new_rack[i] = s['card']
        if isInOrder(new_rack) and inRunLength(partOfRunLength, i) < 2:
            return deckExchange(i, s['rack'])

    for i in xrange(20):
        new_rack = s['rack'][:]
        new_rack[i] = s['card']
        if countRedSquares(new_rack) == countRedSquares(s['rack']) and inRunLength(partOfRunLength, i) < 2:
            return deckExchange(i, s['rack'])

    for i in xrange(20):
        new_rack = s['rack'][:]
        new_rack[i] = s['card']
        if isInOrder(new_rack):
            return deckExchange(i, s['rack'])

    for i in xrange(20):
        new_rack = s['rack'][:]
        new_rack[i] = s['card']
        if countRedSquares(new_rack) == countRedSquares(s['rack']):
            return deckExchange(i, s['rack'])

    print "OHMYGOD YOU SHOULD NEVER BE HERE WTFFFFFFFFFF"
    return deckExchange((s['card']) / 4, s['rack'])

def deckExchange(index, rack):
    global discards
    discards.pop()
    discards.append(rack[index])
    return index

def inQuadrant(num, position):
    upperBound = (num - 1) / 4 + 4
    lowerBound = (num - 1) / 4 - 4
    return position < upperBound and position > lowerBound
    
def inRunLength(runLengths, index):
    for i in xrange(len(runLengths)):
        if runLengths[i] > 0:
            if index >= i and index < i + runLengths[i]:
                return runLengths[i]
    return -1

def getPossibleCardsInDeck(myCards):
    possibles = set()
    for i in xrange(1, 81):
        iHaveCard = i in myCards

        if i not in discards and i not in opponentKnownCards and not iHaveCard:
            possibles.add(i)
    return possibles

def isInOrder(rack):
    lastValue = rack[0]
    for i in xrange(1, len(rack)):
        if rack[i] < lastValue:
            return False
        lastValue = rack[i]
    return True

def countRedSquares(rack):
    a = 0
    lastValue = rack[0]
    for i in xrange(1, len(rack)):
        if rack[i] < lastValue:
            a += 1
        lastValue = rack[i]
    return a

def distance(rack):
    totalDistance = 0
    for i in xrange(20):
        totalDistance += abs(i - (rack[i] - 1) / 4)
    return totalDistance

def h(rack):
    return 50 * countRedSquares(rack) - distance(rack)

def move_result(s):
    print "Move result: %s." %(s['move'])
    return ''

def game_result(s):
    print 'turnNum: %s' %(turnNum)
    print "Game over because: %s.\nOur score: %s\nTheir score: %s\n\n" %(s['reason'], s['your_score'], s['other_score'])
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
