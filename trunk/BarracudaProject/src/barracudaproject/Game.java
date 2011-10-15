/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package barracudaproject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

/**
 *
 * @author Stephen
 */
public class Game {
    
    private int gameID;
    
    private static final int START_GAME = 0;
    private static final int GET_MOVE = 1;
    private static final int GAME_OVER = 2;
    
    private int currentState = START_GAME;
    private int currentTurn = 0; //Start with player 0.
    
    private Client player0;
    private Client player1;
    
    private int[] firstPlayerHand = new int[20];
    private int[] secondPlayerHand = new int[20];
    
    private ArrayList<Integer> deck = new ArrayList<Integer>();
    private ArrayList<Integer> discard = new ArrayList<Integer>();
    
    private Move previousMove = null;
    
    private int currentMoveNum = 0;
    private String gameOverReason = "";
    
    private int score0 = 0;
    private int score1 = 0;
        
    public Game(Client client0, Client client1) {
        player0 = client0;
        player1 = client1;
        for(int i = 1; i<81; i++) {
            deck.add(i);
        }
        Collections.shuffle(deck);
        Random random = new Random();
        gameID = random.nextInt();
        discard.add(getTopDeckCard());
        for(int i = 0; i < firstPlayerHand.length; i++) {
            firstPlayerHand[i] = getTopDeckCard();
            secondPlayerHand[i] = getTopDeckCard();
        }
    }
    
    public Boolean stepForwards() { //returns False if game not over, true if game over.
        switch(currentState) {
            case START_GAME:
                player0.start_game(gameID, 0, getTopDiscard(), player1.getID());
                player1.start_game(gameID, 0, getTopDiscard(), player0.getID());
                currentState = GET_MOVE;
                break;
            case GET_MOVE:
                Move requestedMove;
                if(currentTurn == 0) { //First player
                    requestedMove = player0.get_move(gameID, firstPlayerHand, getTopDiscard(), 0, previousMove);
                } else { //Second player
                    requestedMove = player1.get_move(gameID, secondPlayerHand, getTopDiscard(), 0, previousMove);
                }
                
                if(requestedMove.move.equals("request_discard")) { //requesting discard
                    int discardedCard;
                    boolean gameOver;
                    if(currentTurn == 0) { // First Player
                        discardedCard = firstPlayerHand[requestedMove.idx];
                        firstPlayerHand[requestedMove.idx] = discard.remove(0);
                        discard.add(0, discardedCard);
                        gameOver = checkWin(firstPlayerHand);
                        if(gameOver) {
                            player0.move_result(gameID, "move_ended_game", "Game is over! You win!");
                            currentState = GAME_OVER;
                            gameOverReason = "Player 1 Wins";
                        } else {
                            player0.move_result(gameID, "next_player_move", "");
                        }
                        previousMove = new Move(1, "take_discard", requestedMove.idx, "");
                    } else { // Second player
                        discardedCard = secondPlayerHand[requestedMove.idx];
                        secondPlayerHand[requestedMove.idx] = discard.remove(0);
                        discard.add(0, discardedCard);
                        gameOver = checkWin(secondPlayerHand);
                        if(gameOver) {
                            player1.move_result(gameID, "move_ended_game", "Game is over! You win!");
                            currentState = GAME_OVER;
                            gameOverReason = "Player 2 Wins";
                        } else {
                            player1.move_result(gameID, "next_player_move", "");
                        }
                        previousMove = new Move(0, "take_discard", requestedMove.idx, "");
                    }
                }
                if(requestedMove.move.equals("request_deck")) {
                    int topCard = getTopDeckCard();
                    boolean gameOver;
                    if(currentTurn == 0) { //first player
                        int index = player0.get_deck_exchange(gameID, 0, firstPlayerHand, topCard);
                        discard.add(0, firstPlayerHand[index]);
                        firstPlayerHand[index] = topCard;
                        gameOver = checkWin(firstPlayerHand);
                        if(gameOver) {
                            player0.move_result(gameID, "move_ended_game", "Game is over! You win!");
                            currentState = GAME_OVER;
                            gameOverReason = "Player 1 Wins";
                        } else {
                            player0.move_result(gameID, "next_player_move", "");
                        }
                        previousMove = new Move(0, "take_deck", requestedMove.idx, "");
                    } else { //second player
                        int index = player1.get_deck_exchange(gameID, 0, firstPlayerHand, topCard);
                        discard.add(0, secondPlayerHand[index]);
                        secondPlayerHand[index] = topCard;
                        gameOver = checkWin(secondPlayerHand);
                        if(gameOver) {
                            player1.move_result(gameID, "move_ended_game", "Game is over! You win!");
                            currentState = GAME_OVER;
                            gameOverReason = "Player 2 Wins";
                        } else {
                            player1.move_result(gameID, "next_player_move", "");
                        }
                        previousMove = new Move(1, "take_deck", requestedMove.idx, "");
                    }
                }
                currentMoveNum++;
                if(currentMoveNum > 150) {
                    currentState = GAME_OVER;
                    gameOverReason = "Move limit exceeded";
                }
                if(currentTurn == 0)
                    currentTurn = 1;
                else
                    currentTurn = 0;
                break;
                
        }
        if(currentState == GAME_OVER) {
            if(BarracudaProject.WRITE_OUTPUT)
                System.out.println("SERVER: Game over. Reason: "+gameOverReason);
            if(gameOverReason.equals("Player 1 Wins")) {
                score0 = 150;
                score1 = calcScoreLost(secondPlayerHand);
            }
            if(gameOverReason.equals("Player 2 Wins")) {
                score1 = 150;
                score0 = calcScoreLost(firstPlayerHand);
            }
            if(gameOverReason.equals("Move limit exceeded")) {
                score0 = calcScoreScored(firstPlayerHand);
                score1 = calcScoreScored(secondPlayerHand);
            }
            
            player0.game_result(gameID, score0, score1, gameOverReason);
            player1.game_result(gameID, score1, score0, gameOverReason);
            return true;
        }
        return false;
    }
    
    private int calcScoreLost(int[] hand) {
        int lastValue = hand[0];
        int points = 5;
        for(int i = 1; i<hand.length; i++) {
            if(hand[i]>lastValue) {
                points += 5;
            } else {
                i = hand.length;
            }
            lastValue = hand[i];
        }
        return points;
    }
    
    private int calcScoreScored(int[] hand) {
        int lastValue = hand[0];
        int points = 5;
        boolean all20Good = true;
        for(int i = 1; i<hand.length; i++) {
            if(hand[i]>lastValue) {
                points += 5;
            } else {
                all20Good = false;
                i = hand.length-1;
            }
            lastValue = hand[i];
        }
        lastValue = hand[0];
        int sequence = 1;
        int maxSequence = 1;
        if(all20Good) {
            for(int i = 1; i<hand.length; i++) {
                if(hand[i] == lastValue+1) {
                    sequence++;
                } else {
                    maxSequence = Math.max(sequence, maxSequence);
                    sequence = 1;
                }
                lastValue = hand[i];
            }
            points += maxSequence*10;
        }
        return points;
    }
    
    private Boolean checkWin(int[] hand) {
        int consecutive = 1;
        int lastValue = hand[0];
        Boolean fiveReached = false;
        for(int i = 1; i < hand.length; i++) {
            int val = hand[i];
            if(val > lastValue)
                return false;
            if(val == (lastValue + 1)) {
                consecutive++;
                if(consecutive > 4)
                    fiveReached = true;
            } else
                consecutive = 1;
        }
        return fiveReached;
    }
    
    public ArrayList<Integer> getDeck() {
        return deck;
    }
    
    public int getTopDiscard() {
        return discard.get(0);
    }
    
    public int getScore0() {
        return score0;
    }
    
    public int getScore1() {
        return score1;
    }

    //Utils
    private int getTopDeckCard() {
        if(deck.size() == 0) {
            int topDiscard = discard.remove(0);
            deck = new ArrayList(discard);
            discard = new ArrayList();
            discard.add(topDiscard);
        }
        return deck.remove(0);
    }
}
