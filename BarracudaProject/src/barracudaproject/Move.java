/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package barracudaproject;

/**
 *
 * @author Stephen
 */
public class Move {
    public int otherPlayer;
    public String move;
    public int idx;
    public String reason;
    public Move(int otherPlayer, String move, int idx, String reason) {
        this.otherPlayer = otherPlayer;
        this.move = move;
        this.idx = idx;
        this.reason = reason;
    }
}
