/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package barracudaproject;

/**
 *
 * @author Stephen
 */
public class DivideFourClient extends Client {
    public DivideFourClient(String name) {
        super(name);
    }
    
    public Move get_move(int game_id, int[] rack, int discard, int remaining_microseconds, Move other_player_moves) {
        int index = (discard-1)/4;
        //System.out.println("Got int "+discard+" replace index "+index);
        if(BarracudaProject.WRITE_OUTPUT)
            printRack(rack);
        return new Move(0, "request_discard", index, "bah");
    }
}
