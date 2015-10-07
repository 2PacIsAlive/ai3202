# Markov Decision Processes and Value Iteration

<h3>Instructions:</h3>
<p>Run the code with two command line arguments:<br>
<ul type="square">
    <li>1: The name of the world file (e.g. World1MDP.txt)</li>
    <li>2: The value of epsilon (involved in calculating the maximum allowable error)</li>
</ul>
The code will output the number of iterations required for convergence, the path taken by the algorithm (as displayed on a convenient world map), and the utilities associated with each step in the path.</p>

<h3>Observations:</h3>
<p>Running the code with different values for epsilon produces different outputs. 
This is a direct result of the convergence threshold being raised or lowered.
The value iteration algorithm converges when the largest change in utility is smaller than this threshold. 
When the change is very small, the algorithm is no longer producing significant changes in the utilities of the states,
and should terminate.
The threshold is computed by multiplying epsilon by 1-gamma/gamma, where gamma is the discount factor (in this case gamma = 0.9) 
Gamma reflects the notion that rewards are worth less over time.<br>
When epsilon is increased, the convergence threshold is lowered, and it takes fewer iterations to reach the goal. 
The utilities produced in this circumstance are <b>less</b> "accurate".<br>
When epsilon is decreased, the convergence threshold is raised, and it takes more iterations to reach the goal.
The utilities produced in this circumstance are <b>more</b> "accurate".</p>
<p>Here are several examples of this difference:</p>
<ul type="square">
    <li>Epsilon = 0.5 (default)</li>
    <li>Epsilon = 0.1</li>
</ul>
