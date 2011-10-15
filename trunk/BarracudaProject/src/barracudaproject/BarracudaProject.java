/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package barracudaproject;

/**
 *
 * @author Stephen
 */
public class BarracudaProject {
    
    public static final Boolean WRITE_OUTPUT = false;

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        int trials = 100000;
        int p1scoreTot = 0;
        int p2scoreTot = 0;
        
        Client player1 = new RatingsClient("grc1");
        Client player2 = new DivideFourClient("sjcc2");
        
        for(int i = 0; i < trials; i++) {
            Game newGame1 = new Game(player1, player2);
            while(!newGame1.stepForwards());
            p1scoreTot += newGame1.getScore0();
            p2scoreTot += newGame1.getScore1();
            
            Game newGame2 = new Game(player2, player1);
            while(!newGame2.stepForwards());
            p1scoreTot += newGame2.getScore1();
            p2scoreTot += newGame2.getScore0();
        }
        System.out.println("Player 1's Avg Score: "+((double)p1scoreTot/(trials*2)));
        System.out.println("Player 2's Avg Score: "+((double)p2scoreTot/(trials*2)));
    }
}
