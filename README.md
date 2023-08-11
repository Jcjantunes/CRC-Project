# CRC-Project
Network Science (CRC) Course Project (Grade: 17.5/20) - IST - 2020/2021

# CRC
Evolution of Fairness in Different Networks

The project.py code contains an implementation of the Ultimatum Game:
	- In each generation, each player will play either with every other player (in the baseline model) or play with all 
	  its neighbours (in a network environment), as both the proposer and the receiver.
	- After all players have exchanged with each other, the payoff of each player is calculated. 
	- At the end of each generation the strategies (the p and q values of each player) will be propagated 
	  through the next generation proportionally to their payoff levels. 
	  The update of these strategies will also take into account the mutation error that will choose the p and q values randomly 
	  within the given error interval centered around the previous generation’s p and q values.

The project depends on:
	- Python3
	- NetworkX: version 2.6.3 was what was used when creating the project. Can be easily installed via "pip install networkx"
	- Numpy: version 1.21.2 was what was used when creating the project. Can be easilty installed with pip via "pip install numpy"

The provided code has the following parameters: N m generations prob network_type mutation_error lowOffersPenaltyFlag
	N: Number of players.
	m: Number of initial links of a player.
	generations: Determines how many times the model is executed.
	prob: Probability of creating a link between players (its value must be between 0 and 1).
	network_type: Defines the type of network the graph will have, it can be the following:
					- "none": Baseline model where there is no network type and every player plays whith everyone else, this model will ignore the 
							  provided m and prob parameters.
					- "ba": The graph will be a Albert-Barabasi network, this network will ignore the provided prob parameter.
					- "rand": The graph will be a Random network, this network will ignore the provided m parameter.
					- "wt": The graph will be a Watts-Strogatz network.
	mutation_error: Decimal value (between 0 and 1) that adds more random values to players strategies.
	lowOffersPenaltyFlag: Determines if the model will apply penalties, it can be either:
							- "0": Penalties will not be applied.
							- "1": Penalties will be applied.

In order to run this code please run the project.py in any IDE with the previous parameters.

Alternatively, it is possible to use the terminal to run the project: 
	- python3 project.py <N> <m> <generations> <prob> <network_type> <mutation_error> <low_offers_penalty_flag>

Once the system is running, the results will be printed to 4 different files: p_qFile.txt, timeFile.txt, fairFile.txt and payoffFile.txt.
These files have the following format (by column):
	- p_qFile: "generation pValue qValue\n"
		- generation: The number of the generation where the pValue and qValue is assossiated to.
		- pValue: The average p value of all players of a generation.
		- qValue: The average q value of all players of a generation.
	- timeFile: "generation timestamp\n"
		- generation: The number of the generation where the timestamp is assossiated to.
		- timestamp: The logaritmic timestamp of a generation. This timestamp is accoring the 
					 the noisy logaritmic convergence scale.
	- fairFile: "generation fairPercentage\n"
		- generation: The number of the generation where the fairPercentage is assossiated to.
		- fairPercentage: The percentage of the number of fair plays executed of a generation.
	- payoffFile: "generation payoff"
		- generation: The number of the generation where the payoff is assossiated to.
		- payoff: The average payoff of all players of a generation.

At the end of the simulation it will be printed to the terminal "Simulation Complete"

Disclaimer: 
 	The provided code can take a very long time to be executed according to the number of generations 
 	(for instance 10000 generations can take up to 50 minutes to be excuted) and along the simulation 
 	the current generation number will be printed to the terminal in order to keep track on which generation 
 	the simulation it is currently on.

 	In the timeFile.txt the initial values of the timestamp have negative values and 
 	in order to generate the graphs starting from 0, it was added to each timestamp the 
 	timestamp of the first line of the file.
