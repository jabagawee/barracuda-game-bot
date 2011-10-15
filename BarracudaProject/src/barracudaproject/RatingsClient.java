/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package barracudaproject;

/**
 *
 * @author Peter Gao
 */
public class RatingsClient extends Client {
    public RatingsClient(String name) {
        super(name);
    }
    
    public Move get_move(int game_id, int[] rack, int discard, int remaining_microseconds, Move other_player_moves) {

        int[][] ranges = new int[20][2];
        int[] averages = new int[20];
        int[] differences = new int[20];
        int[] ratings = new int[20];
        int[] intervals= new int[19];

        int rangecounter=0;
        int closest=80;
        int closestindex=0;

        for(int i=0; i<20; i++){
            ranges[i][0]=rangecounter;
            rangecounter+=20;
            ranges[i][1]=rangecounter;

            //get range average for each slot in rack
            averages[i]=(ranges[i][0]+ranges[i][1])/2;
            differences[i]=rack[i]-averages[i];

            //values in rack slots that are too far away from range average are marked for replacement
            if(differences[i]>=10){
                ratings[i]=0;
            }

            //gets intervals between each slot in rack
            for(int k=0; k<19; k++){
                intervals[k]=rack[k+1]-rack[k];
            }
            
            //closest slot with range average closest to discard value
            int tempclosest=discard-averages[i];
            if(tempclosest<closest){
                closest=tempclosest;
                closestindex=i;
            }
            
        }
        
        if(ratings[closestindex]==0){
            return new Move(0, "request_discard", closestindex, "bah");
        }
        
        int index = (discard-1)/4;
        if(BarracudaProject.WRITE_OUTPUT)
            printRack(rack);
        return new Move(0, "request_discard", index, "bah");
    }
}
