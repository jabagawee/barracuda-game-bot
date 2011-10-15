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

        int j=0;

        for(int i=0; i<20; i++){
            ranges[i][0]=j;
            j+=20;
            ranges[i][1]=j;

            //get range average for each slot in rack
            averages[i]=(ranges[i][0]+ranges[i][1])/2;
            differences[i]=rack[i]-averages[i];

            //values in rack slots that are too far away from range average are deleted
            if(differences[i]>=10){
                ratings[i]=0;
            }

            //gets intervals between each slot in rack
            for(int k=0; k<19;k++){
                intervals[k]=rack[i+1]-rack[i];
            }
        }
        
      return new Move(0, "request_discard", 0, "bah");
    }
    
}
