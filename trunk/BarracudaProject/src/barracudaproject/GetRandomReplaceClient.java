/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package barracudaproject;

/**
 *
 * @author Stephen
 */
public class GetRandomReplaceClient extends Client{
    public GetRandomReplaceClient(String name) {
        super(name);
    }
    
    public Move get_move(int game_id, int[] rack, int discard, int remaining_microseconds, Move other_player_moves) {
        if(BarracudaProject.WRITE_OUTPUT)
            printRack(rack);
        return new Move(0, "request_deck", 0, "bah");
    }
    
    public int get_deck_exchange(int game_id, int remaining_microseconds, int[] rack, int card) {
        int index = (card-1)/4;
        return index;
    }
}
