/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package barracudaproject;

import java.util.ArrayList;

/**
 *
 * @author Stephen
 */
public class StephenClient extends Client{
    public StephenClient(String name) {
        super(name);
    }
    
    public Move get_move(int game_id, int[] rack, int discard, int remaining_microseconds, Move other_player_moves) {
        int[] partOfRunLength = new int[20];
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
        //printRack(rack);
        //printRack(partOfRunLength);
        
        for(int i = 0; i<partOfRunLength.length; i++) {
            int rl = partOfRunLength[i];
            if(rl > 1) { //runlength > 1
                if(i-1>0 && discard == rack[i]-1)
                    return new Move(0, "request_discard", i-1, "bah");
                if(i+rl<rack.length && discard == rack[i+rl-1]+1)
                    return new Move(0, "request_discard", i+rl, "bah");
            }
        }
        
        int divideByFour = (discard-1)/4;
        int rlIndex = inRunLength(partOfRunLength, divideByFour);
        if(rlIndex > -1) {
            int lowerBound = rack[rlIndex];
            if(rlIndex == 0)
                return new Move(0, "request_discard", 0, "bah");
            if(rlIndex+partOfRunLength[rlIndex]-1 > 19)
                return new Move(0, "request_discard", 19, "bah");
            if(discard < lowerBound)
                return new Move(0, "request_discard", rlIndex-1, "bah");
            else
                return new Move(0, "request_discard", rlIndex+partOfRunLength[rlIndex]-1, "bah");
        }
        
        return new Move(0, "request_discard", (discard-1)/4, "bah");
    }
    
    public int get_deck_exchange(int game_id, int remaining_microseconds, int[] rack, int card) {
        int index = (card-1)/4;
        while(index<rack.length-1 && rack[index+1] < index)
            index++;
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
    
    private Boolean discardIsGood(int[] rack, int discard) {
        int placement = (discard-1)/4;
        if(placement+1>=rack.length || rack[placement+1] > discard)
            return true;
        return false;
    }
    
    private ArrayList<Integer> getBlocked(int[] rack) {
        ArrayList<Integer> blocks = new ArrayList<Integer>();
        int lastValue = rack[0];
        int run = 1;
        for(int i = 1; i<rack.length; i++) {
            if(rack[i] == lastValue+1)
                run++;
            else if(run > 1){
                for(int j = 0; j<run; j++) {
                    blocks.add(i-j);
                }
                run = 1;
            }
        }
        return blocks;
    }
}
