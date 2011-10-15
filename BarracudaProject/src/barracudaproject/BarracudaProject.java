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
        for(int i = 0; i < trials; i++) {
            Game newGame = new Game(new GetRandomReplaceClient("grc1"), new DivideFourClient("dfc2"));
            while(!newGame.stepForwards());
            p1scoreTot += newGame.getScore0();
            p2scoreTot += newGame.getScore1();
        }
        System.out.println("Player 1's Avg Score: "+((double)p1scoreTot/trials));
        System.out.println("Player 2's Avg Score: "+((double)p2scoreTot/trials));
    }
}
