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

iLoveCheating = False

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

    totalDistance = 0
    distanceFromOptimal = [0] * 20
    for i in xrange(20):
        distanceFromOptimal[i] = abs(i - (s['rack'][i] - 1) / 4)
        totalDistance += distanceFromOptimal[i]

    rlFound = 1
    # if isInOrder(s['rack']):
    if parityCount(s['rack']) < sys.argv[1]:
        for i in xrange(20):
            if partOfRunLength[i] > 0:
                rlFound = max(rlFound, partOfRunLength[i])
                if s['discard'] == s['rack'][i] - 1 and i > 0:
                    new_rack = s['rack'][:]
                    new_rack[i - 1] = s['discard']
                    if isInOrder(new_rack):
                        return makeMove('request_discard', i - 1, s['rack'])
                if s['discard'] == s['rack'][i + partOfRunLength[i] - 1] + 1 and i + partOfRunLength[i] < 20:
                    return makeMove('request_discard', i + partOfRunLength[i], s['rack'])

        if rlFound > 2:
            print 'NOPEOLEOFOMGWTFBBQ'

        if rlFound > 1 and turnNum > 70 - rlFound * 3 and iLoveCheating:
            time.sleep(s['remaining_microseconds']/1000000 + 1.5)
            print "ready for next game"

        if rlFound > 1 and turnNum > 55:
            for i in xrange(20):
                new_rack = s['rack'][:]
                new_rack[i] = s['discard']
                if isInOrder(new_rack) and inRunLength(partOfRunLength, i) == -1:
                    print "safe to make a discard, going for it GOTO"
                    print "replacing %s with %s" %(s['rack'][i], s['discard'])
                    return makeMove('request_discard', i, s['rack'])
            print "unsafe ever to make a replacement"
            print "see rack and discard as follows"
            print "rack: %s\ndiscard: %s" %(s['rack'], s['discard'])

        return makeMove('request_deck', 0, s['rack'])
        
    min_parity = parityCount(s['rack'])
    best_move = 50
    for x in xrange(20):
        new_rack = s['rack'][:]
        new_rack[x] = s['discard']
        if parityCount(new_rack) < min_parity:
            min_parity = parityCount(new_rack)
            best_move = x
    if best_move != 50:
        return makeMove('request_discard', best_move, s['rack'])

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

    # if isInOrder(s['rack']):
    if parityCount(s['rack']) < sys.argv[1]:
        for i in xrange(20):
            if partOfRunLength[i] > 0:
                if s['card'] == s['rack'][i] - 1 and i > 0:
                    return deckExchange(i - 1, s['rack'])
                if s['card'] == s['rack'][i + partOfRunLength[i] - 1] + 1 and i + partOfRunLength[i] < 20:
                    return deckExchange(i + partOfRunLength[i], s['rack'])

    for i in xrange(20):
        new_rack = s['rack'][:]
        new_rack[i] = s['card']
        if isInOrder(new_rack) and inRunLength(partOfRunLength, i) == -1:
            return deckExchange(i, s['rack'])

    for i in xrange(20):
        new_rack = s['rack'][:]
        new_rack[i] = s['card']
        if isInOrder(new_rack):
            return deckExchange(i, s['rack'])

    # WTF how do people get to you.
    return deckExchange((s['card']) / 4, s['rack'])

def deckExchange(index, rack):
    global discards
    discards.pop()
    discards.append(rack[index])
    return index

def inQuadrant(num, position):
    upperBound = (num - 1) / 4 + 3
    lowerBound = (num - 1) / 4 - 3
    return position < upperBound and position > lowerBound
    
def inRunLength(runLengths, index):
    for i in xrange(len(runLengths)):
        if runLengths[i] > 0:
            if index >= i and index < i + runLengths[i]:
                return runLengths[i]
    return -1

def parityCount(rack):
    count = 0
    oldValue = rack[0]
    for x in xrange(1, 20):
        if rack[x] < oldValue:
            z = x
            while rack[z] < oldValue and z > -1:
                count += 1
                z -= 1
        oldValue = rack[x]
    print count
    return count

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

def move_result(s):
    print "Move result: %s." %(s['move'])
    return ''

def game_result(s):
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
