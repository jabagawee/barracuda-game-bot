#! /usr/bin/env python

partOfRunLength = []
distanceFromOptimal = []

discards = []
opponentKnownCards = set()

deckSize = 39
discardSize = 1

turnNum = 0

notTurnNumed = True

def start_game(s):
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

    if s['other_player_moves'] != [[]] and s['other_player_moves']['move'] == 'take_deck':
        deckSize -= 1
        discardSize += 1

    if deckSize == 0:
        deckSize = 39
        discardSize = 1
        # topDiscard = discards.pop()
        discards = [discards.pop()]

    if s['other_player_moves'] != [[]] and s['other_player_moves']['move'] == 'take_discard':
        opponentKnownCards.add(discards.pop())

    if s['other_player_moves'] != [[]]:
        discards.append(s['discard'])

    if s['discard'] in opponentKnownCards:
        opponentKnownCards.remove(s['discard'])

    partOfRunLength = [0] * 20
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
    for i in xrange(20):
        distanceFromOptimal[i] = abs(i - (s['rack'][i] - 1) / 4)
        totalDistance += distanceFromOptimal[i]

    if isInOrder(s['rack']):
        rlFound = False
        for i in xrange(20):
            if partOfRunLength[i] > 1:
                rlFound = True
                if s['discard'] == s['rack'] - 1 and i > 0:
                    return makeMove(0, 'request_discard', i - 1, s['rack'])
                if s['discard'] == s['rack'][i + partOfRunLength[i] - 1] + 1 and i + partOfRunLength[i] < 20:

    public Move get_move(int game_id, int[] rack, int discard, int remaining_microseconds, Move other_player_moves) {
        turnNum++;
        if(other_player_moves != null && other_player_moves.move.equals("take_deck")) {
            deckSize--;
            discardSize++;
        }
        if(deckSize == 0) {
            deckSize = 39;
            discardSize = 1;
            int topDiscard = discards.get(0);
            discards = new ArrayList<Integer>();
            discards.add(topDiscard);
        }
        if(other_player_moves != null && other_player_moves.move.equals("take_discard")) {
            if(!opponentKnownCards.contains(discards.get(0)))
                opponentKnownCards.add(discards.remove(0));
            Collections.sort(opponentKnownCards);
        }
        if(other_player_moves != null)
            discards.add(0, discard);
        if(opponentKnownCards.contains(discard)) {
            opponentKnownCards.remove(new Integer(discard));
            /*for(int i = 0; i<opponentKnownCards.size(); i++) {
                if(opponentKnownCards.get(i) == discard) {
                    System.out.println(opponentKnownCards.remove(i));
                    i = opponentKnownCards.size();
                }
            }*/
        }
        
        partOfRunLength = new int[20];
        for(int i = 0; i<rack.length; i++)
            partOfRunLength[i] = 0;
        int lastValue = rack[0];
        int runLength = 1;
        for(int i = 1; i<rack.length; i++) {
            if(rack[i] == lastValue+1) {
                runLength++;
                if(inQuadrant(rack[i], i)) {
                    for(int j = 0; j<runLength; j++) {
                        partOfRunLength[i-j] = 0;
                    }
                    partOfRunLength[i-runLength+1] = runLength;
                }
            } else
                runLength = 1;
            lastValue = rack[i];
        }
        
        distanceFromOptimal = new int[20];
        int totalDistance = 0;
        for(int i = 0; i<rack.length; i++) {
            distanceFromOptimal[i] = Math.abs(i-(rack[i]-1)/4);
            totalDistance += distanceFromOptimal[i];
        }
        
        if(isInOrder(rack) && notTurnNumed) {
            notTurnNumed = false;
            //System.out.println(turnNum);
        }
        
        if(isInOrder(rack)) {
            Boolean rlFound = false;
            for(int i = 0; i<partOfRunLength.length; i++) { //Loop through run lengths now that we have in order
                if(partOfRunLength[i]>1) { //We have a run length > 1!
                    rlFound = true;
                    if(discard == rack[i]-1 && i>0) { //We have a discard card that's 1 less than the run length!!
                        return makeMove(0, "request_discard", i-1, "bah", rack);
                    }
                    if(discard == rack[i+partOfRunLength[i]-1]+1 && i+partOfRunLength[i] < partOfRunLength.length) { //We have a discard 1 more than run length
                        return makeMove(0, "request_discard", i+partOfRunLength[i], "bah", rack);
                    }
                }
            }
            if(!rlFound) { //WTF NO RUNLENGTHS AT ALL?
                
            }
            //No run length found to match discard. Draw a deck.
            return makeMove(0, "request_deck", 0, "bah", rack);
            
        }
        
        if(distanceFromOptimal[(discard-1)/4] == 0)
            return makeMove(0, "request_deck", 0, "bah", rack);
        else
            return makeMove(0, "request_discard", (discard-1)/4, "bah", rack);
    }
    
    private Move makeMove(int gameID, String move, int idx, String result, int[] rack) {
        if(move.equals("request_discard")) {
            discards.remove(0);
            discards.add(0, rack[idx]);
        }
        return new Move(gameID, move, idx, result);
    }
    
    public int get_deck_exchange(int game_id, int remaining_microseconds, int[] rack, int card) {
        int index = (card-1)/4;
        if(isInOrder(rack)) { //If in order already, do run-length stuff.
            Boolean rlFound = false;
            for(int i = 0; i<partOfRunLength.length; i++) { //Loop through run lengths now that we have in order
                if(partOfRunLength[i]>1) { //We have a run length > 1!
                    rlFound = true;
                    if(card == rack[i]-1 && i>0) { //We have a discard card that's 1 less than the run length!!
                        return deckExchange(i-1, rack);
                    }
                    if(card == rack[i+partOfRunLength[i]-1]+1 && i+partOfRunLength[i] < partOfRunLength.length) { //We have a discard 1 more than run length
                        return deckExchange(i+partOfRunLength[i], rack);
                    }
                }
            }
            if(!rlFound) { //WTF NO RUNLENGTHS AT ALL?
                
            }
            //No run length found to match discard. Damn.        
        }
        return deckExchange(index, rack);
    }
    
    private int deckExchange(int index, int[] rack) {
        discards.remove(0);
        discards.add(0, rack[index]);
        return index;
    }
    
    private Boolean inQuadrant(int num, int position) {
        int upperBound = (num-1)/4 + 3;
        int lowerBound = (num-1)/4 - 3;
        if(position < upperBound && position > lowerBound)
            return true;
        return false;
    }
    
    private int inRunLength(int[] runLengths, int index) {
        for(int i = 0; i<runLengths.length; i++) {
            if(runLengths[i] > 0) { //run length
                if(index >= i && index < (i+runLengths[i]) )
                    return i;
            }
        }
        return -1;
    }
    
    private ArrayList<Integer> getPossibleCardsInDeck(int[] myCards) {
        ArrayList<Integer> possibles = new ArrayList<Integer>();
        for(int i = 1; i<81; i++) {
            boolean iHaveCard = false;
            for(int j = 0; j<myCards.length; j++) {
                if(myCards[j] == i) {
                    iHaveCard = true;
                    j = myCards.length;
                }
            }
            if(!discards.contains(i) && !opponentKnownCards.contains(i) && !iHaveCard) {
                possibles.add(i);
            }
        }
        return possibles;
    }
    
    private Boolean isInOrder(int[] rack) {
        int lastValue = rack[0];
        for(int i = 1; i<rack.length; i++) {
            if(rack[i]<lastValue)
                return false;
            lastValue = rack[i];
        }
        return true;
    }
}
