package matchup.g8;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

import matchup.sim.Simulator;
import matchup.sim.utils.*;

public class Player implements matchup.sim.Player {
	private List<Integer> skills;
	private List<Integer> PrevSkills;
	private List<List<Integer>> distribution;

	private List<Integer> availableRows;
	private PlayerData Opponent, Self;
	private int Opponent_score,Self_score,tie;
	private Random rand;
	private boolean playHome, WonLast, first_game, counter_strategy;
	private Integer lossStreak;
	public Player() {
		Opponent_score = 0;
		Self_score = 0;
		tie=0;
		rand = new Random();
		skills = new ArrayList<Integer>();
		PrevSkills = new ArrayList<Integer>();
		distribution = new ArrayList<List<Integer>>();
		availableRows = new ArrayList<Integer>();
		WonLast=true;
		first_game = true;
		counter_strategy=true;
		lossStreak = 0;
		for (int i=0; i<3; ++i) availableRows.add(i);
	}
	
    public void init(String opponent) {
    }



	private List<Integer> playSevens()
	{
		List<Integer> skillset = new ArrayList<Integer>();
		for(int i=0;i<10;i++) skillset.add(7);
		for(int i=0;i<3;i++) skillset.add(5);
		skillset.add(3);
		skillset.add(2);
		return skillset;		
	}

	private List<Integer> playAntiSevens()
	{
		List<Integer> skillset = new ArrayList<Integer>();
		for(int i=0;i<8;i++) skillset.add(5);
		for(int i=0;i<3;i++) skillset.add(10);
		skillset.add(7);
		skillset.add(7);
		skillset.add(5);
		skillset.add(1);
		return skillset;		
	}

	private List<Integer> playBalanced()
	{
		List<Integer> skillset = new ArrayList<Integer>();
		for(int i=0;i<4;i++) skillset.add(9);
		for(int i=0;i<3;i++) skillset.add(7);
		for(int i=0;i<3;i++) skillset.add(5);
		for(int i=0;i<4;i++) skillset.add(4);
		skillset.add(2);
		return skillset;		
	}

	private List<Integer> playNines()
	{
		List<Integer> skillset = new ArrayList<Integer>();
		for(int i=0;i<5;i++) skillset.add(9);
		for(int i=0;i<5;i++) skillset.add(8);
		for(int i=0;i<5;i++) skillset.add(1);
		//for(int i=0;i<4;i++) skillset.add(4);
		//skillset.add(2);
		return skillset;		
	}


	private void Analyze()
	{

		List<Game> hist  = Simulator.getGames();
		if(hist.size()>=2 && hist.get(hist.size()-1).playerA.name.equals("g8"))
		{
			Opponent = hist.get(hist.size()-1).playerB;
			Opponent_score = hist.get(hist.size()-1).playerB.score + hist.get(hist.size()-2).playerB.score;
			Self = hist.get(hist.size()-1).playerA;
			Self_score = hist.get(hist.size()-1).playerA.score + hist.get(hist.size()-2).playerA.score;
		}
		else if(hist.size()>=2)
			{
				Opponent = hist.get(hist.size()-1).playerA;
				Opponent_score = hist.get(hist.size()-1).playerA.score + hist.get(hist.size()-2).playerA.score;
				Self = hist.get(hist.size()-1).playerB;
				Self_score = hist.get(hist.size()-1).playerB.score + hist.get(hist.size()-2).playerB.score;
			}


		if(hist.size()>=5)
		{
		
		}

		if(Opponent!=null) 
		{
			if(Opponent_score> Self_score)
				{
					WonLast  = false;
					lossStreak++;
					tie=0;
				}

			else if(Opponent_score == Self_score)
			{
				tie++;
				System.out.println("last game was a tie thus keeping previous team");
				System.out.println(Integer.toString(tie));
				if(tie>=3) 
				{
					WonLast = false;
					lossStreak = tie;
				}
				else WonLast = true; 
			}
			else
				{
					WonLast = true;
					lossStreak = 0;
					tie=0;
				}
		}
	}

	public List<Integer> getNew()
	{
		List<Integer> oppSkills = new ArrayList<Integer>();
		for(int i=0;i<Opponent.skills.size();i++)
		{
			oppSkills.add(Opponent.skills.get(i));
		}
		Collections.sort(oppSkills);
		Integer Count[] = new Integer[11];
		for(int i=0;i<11;i++) Count[i] =0;
		
		for(int i=0;i<oppSkills.size();i++)
		{
			Count[oppSkills.get(i)-1]++;
		}
		if(Count[9] + Count[10] <= 4 && Count[4] + Count[6] + Count[7] <= 10) /// Mostly 9's are highest 
			oppSkills = playSevens();
		else if(Count[6]>=8) 					///opponent using the sevens strategy
			oppSkills = playAntiSevens();
		else if(Count[8] + Count[7] <= 6)			/// If somewhat balanced
			oppSkills = playBalanced();
		else 							/// improve upon opponent's distribution
		for(int i=0;i<15;i++)
		{
			if(i<6)
				oppSkills.set(i,oppSkills.get(i)+3);
			else
				oppSkills.set(i,oppSkills.get(i)-2);
		}

		
		return oppSkills;
	}

	private void improveSkills()
	{
			Collections.sort(skills);
			if(lossStreak>4) counter_strategy = !counter_strategy;

			for(int i=0;i<15;i++)
			{
			if(i<6)
				skills.set(i,skills.get(i)+3);
			else
				skills.set(i,skills.get(i)-2);
			}
			   
	}

	private void counterSkills()
	{
		List<Integer> oppSkills = new ArrayList<Integer>();
		for(int i=0;i<Opponent.skills.size();i++)
		{
			oppSkills.add(Opponent.skills.get(i));
		}
		Collections.sort(oppSkills);
		Integer Count[] = new Integer[11];
		for(int i=0;i<11;i++) Count[i] =0;
		
		for(int i=0;i<oppSkills.size();i++)
		{
			Count[oppSkills.get(i)-1]++;
		}
		if(Count[9] + Count[10] >= 5) /// Mostly 9's are highest 
			oppSkills = playSevens();
		else if(Count[6]>=8) 					///opponent using the sevens strategy
			oppSkills = playNines();
		else if(Count[8] + Count[7] >= 6)			/// If somewhat balanced
			oppSkills = playNines();
		else 							/// improve upon opponent's distribution
		for(int i=0;i<15;i++)
		{
			if(i<6)
				oppSkills.set(i,oppSkills.get(i)+3);
			else
				oppSkills.set(i,oppSkills.get(i)-2);
		}

		skills = oppSkills;
		//return oppSkills;
		
		
	}
	public List<Integer> getSkills() {	
             
		skills.clear();

		if(!first_game)
		for(int i=0;i<15;i++) skills.add(PrevSkills.get(i));


		Analyze();

		
		if(!WonLast && lossStreak<2)
		  skills = getNew();

		else if(lossStreak>=2)
	          improveSkills();

		else if(!first_game && tie==0 && counter_strategy)	
		 {
			counterSkills();
		}
		else if(!first_game)
			skills = getNew();
		
		if(first_game)
		{
			skills.add(9);
			skills.add(9);
			skills.add(9);
			skills.add(9);
			skills.add(7);
			skills.add(7);
			skills.add(7);
			skills.add(5);
			skills.add(5);
			skills.add(5);
			skills.add(4);
			skills.add(4);
			skills.add(4);
			skills.add(4);
			skills.add(2);
			first_game = false;
		}

		PrevSkills.clear();
		for(int i=0;i<skills.size();i++) PrevSkills.add(skills.get(i));
		

		Collections.shuffle(skills);
		return skills;
	}

    public List<List<Integer>> getDistribution(List<Integer> opponentSkills, boolean isHome) {
    	List<Integer> row1 = new ArrayList<Integer>();
	List<Integer> row2 = new ArrayList<Integer>();
	List<Integer> row3 = new ArrayList<Integer>();
	playHome = isHome;
	Collections.sort(skills);
	if(isHome)
    	{
	row1.add(skills.get(14));
    	row1.add(skills.get(13));
    	row1.add(skills.get(10));
    	row1.add(skills.get(9));
    	row1.add(skills.get(0));

    	
    	row2.add(skills.get(12));
    	row2.add(skills.get(8));
    	row2.add(skills.get(6));
    	row2.add(skills.get(4));
    	row2.add(skills.get(1));

    	
    	row3.add(skills.get(11));
    	row3.add(skills.get(7));
    	row3.add(skills.get(5));
    	row3.add(skills.get(3));
    	row3.add(skills.get(2));
	}

	else
	{
	row1.add(skills.get(14));
    	row1.add(skills.get(13));
    	row1.add(skills.get(12));
    	row1.add(skills.get(11));
    	row1.add(skills.get(10));

    	
    	row2.add(skills.get(9));
    	row2.add(skills.get(8));
    	row2.add(skills.get(7));
    	row2.add(skills.get(6));
    	row2.add(skills.get(5));

    	
    	row3.add(skills.get(4));
    	row3.add(skills.get(3));
    	row3.add(skills.get(2));
    	row3.add(skills.get(1));
    	row3.add(skills.get(0));
		
	}

    	distribution = new ArrayList<List<Integer>>();

    	distribution.add(row1);
    	distribution.add(row2);
    	distribution.add(row3);

    	return distribution;
    }


    public int canWin(int score,List<Integer> round,int j)
    {

	for(int i=j;i<round.size();i++)
		if(round.get(i) - score > 2)
		 	return i;
		return -1;
    }

    public int canTie(int score,List<Integer> round,int j)
    {
	for(int i=j;i<round.size();i++)
		if(Math.abs(score - round.get(i)) < 3)
		 	return i;
		return -1;
    }

    public List<Integer> playRound(List<Integer> opponentRound) {
 

	

	List<Integer> round = null;
	if (opponentRound==null) {
//	System.out.println("mid row is" + Integer.toString(mid_row));
    	round = distribution.get(0);
    	availableRows.remove(0);
    	return round;

	}

//	System.out.println("rational playing home strategy");
	int n = availableRows.size();
        int[] score = new int[n];
	int[] sum = new int[n];
        ArrayList<List<Integer>> Candidates = new ArrayList<List<Integer>>();
	for(int i=0;i<n;i++)
	{
		round = new ArrayList<Integer>(distribution.get(availableRows.get(i)));
		
		Collections.sort(round);
		sum[i] =0;
		for(int j=0;j<opponentRound.size();j++)
		{
			
/// try to win
			int idx_win = canWin(opponentRound.get(j),round,j);
			if(idx_win>0)
			{
				sum[i] += round.get(idx_win);
				Collections.swap(round,j,idx_win);
				if(j<opponentRound.size()-1)
				Collections.sort(round.subList(j+1,round.size()));
				score[i]++;
				continue;
			}
							
/// try to tie
			int idx_tie = canTie(opponentRound.get(j),round,j);
			if(idx_tie>0)
			{
				sum[i] += round.get(idx_tie);
				Collections.swap(round,j,idx_tie);
				if(j<opponentRound.size()-1)
				Collections.sort(round.subList(j+1,round.size()));
				continue;
			}

/// try to lose with least
			score[i]--;
			sum[i] += round.get(i);
			
		}
		
		Candidates.add(round);

	}

//		System.out.println("Candidates populated");
//		System.out.println(Candidates);	

/// decide which row to play

	int min_win = 100000;
	int min_loss = -100000;
	int win_choice =-1;
	int tie_choice = -1;
	int loss_choice = -1;

	for(int i=0;i<n;i++)
	{
		if(sum[i]<min_win && score[i]>0)
		{
			min_win = sum[i];
			win_choice = i;
		}

		else if(score[i] == 0) tie_choice = i;

		else if(score[i] > min_loss && score[i]<0)
		{
			min_loss = score[i];
			loss_choice = i;
		}
	}

//	for(int i=0;i<n;i++) System.out.println("scores are " + Integer.toString(score[i]));
	
	int fin_choice = -1;

	if(win_choice >= 0)
		{
//			System.out.println("winning this matchup");
			fin_choice = win_choice;
			availableRows.remove(win_choice);
		}
	else if(tie_choice >= 0)
		{
//			System.out.println("tying this matchup");
			fin_choice = tie_choice;
			availableRows.remove(tie_choice);
		}
	else
		{
//			System.out.println("losing this matchup");
			fin_choice = loss_choice;
			System.out.println(fin_choice);
			availableRows.remove(loss_choice);
		}

//	System.out.println("Determine final choice");
        List<Integer> PlayedRow = new ArrayList<Integer>(Candidates.get(fin_choice));
	
    	return PlayedRow;
    }

    public void clear() {
    	availableRows.clear();
    	for (int i=0; i<3; ++i) availableRows.add(i);
    }
}
