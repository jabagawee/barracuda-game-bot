package rackplayer;

public class Player {
	

	public struct get_move(XMLRPC struct vals){
		
		currentRack=vals.rack;
		
		int[] ranges = new int[20];
		int[] differences = new int[20];
		int[] ratings = new int[20];
		
		int j=0;
		
		for(int i=0; i<20; i++){
			ranges[i][0]=j;
			j+=20;
			ranges[i][1]=j;
			
			int avg=(ranges[i][0]+ranges[i][1])/2;
			differences[i]=vals[i]-avg;
			
			if(differences[i]>=10){
				ratings[i]=0;
			}
		}
		
		
		
	}

	public struct move(){
		
	}

}
