/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package barracudaproject;

import java.util.Random;

/**
 *
 * @author Stephen
 */
public class Client {
    private int id;
    private int turnOrder; //0 if going first, 1 if going second
    private int currentTopDiscard; //Current discard card on top
    private int otherPlayerID; //Other player's ID
    
    private String name;
    
    public Client(String name) {
        Random random = new Random();
        id = random.nextInt();
        this.name = name;
    }
    
    public int getID() {
        return id;
    }
    
    public String start_game(int game_id, int player_id, int initial_discard, int other_player_id) {
        turnOrder = player_id;
        currentTopDiscard = initial_discard;
        otherPlayerID = other_player_id;
        return "";
    }
    
    public Move get_move(int game_id, int[] rack, int discard, int remaining_microseconds, Move other_player_moves) {
        int index = 0;
        return new Move(0, "request_discard", index, "bah");
    }
    
    public String move_result(int game_id, String move, String reason) {
        if(move == "move_ended_game") {
            System.out.println(id+": I win! ("+name+")");
        }
        if(move == "next_player_move") {
            //System.out.println(id+": Successfully finished turn. ("+name+")");
        }
        if(!reason.equals("")) {
            System.out.println("Reason: "+reason);
        }
        return "";
    }
    
    public int get_deck_exchange(int game_id, int remaining_microseconds, int[] rack, int card) {
        return 0;
    }
    
    public String game_result(int game_id, int your_score, int other_score, String reason) {
        if(BarracudaProject.WRITE_OUTPUT) {
            System.out.println(id+": Game over. Reason: "+reason+" ("+name+")");
            System.out.println("My Score: "+your_score);
            System.out.println("Their score: "+other_score);
        }
        return "";
    }
    
    protected void printRack(int[] rack) {
        System.out.print(name+"'s Rack: [");
        for(int i = 0; i<rack.length; i++) {
            if(rack[i]/10 == 0)
                System.out.print(0);
            System.out.print(rack[i]+",");
        }
        System.out.println("]");
    }
}
