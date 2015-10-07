# ai3202
Jared Jolton / Repository for Fall 2015 CSCI-3202 coursework at CU Boulder

<p>This repository currently contains the files for assignment 3, A* pathfinding. 
Run the code with 2 command line arguments:</p>
  <p>1) The world to explore (either World1.txt or World2.txt)<br>
  2) The heuristic to use (1, 2, 3, or 4). These heuristics are explained below.</p>
<p>A* pathfinding uses the estimated distance to the goal (heuristic) to determine what path to follow.
My particular implementation of A* is capable of using 4 different heuristics:</p>
  <p>1) Manhattan Distance:</p>
    <p>a) this heuristic adds the horizontal and vertical locations to the goal<br>
    b) for world1, it finds a suboptimal path cost of 156, with 12 locations in the path<br>
    c) for world2, it finds a suboptimal path cost of 152, with 10 locations in the path</p>
  <p>2) Approximate Diagonal Distance:</p>
    <p>a) this heuristic computes the straight line distance to the goal using the pythagorean theorem<br>
    b) for world1, it finds a suboptimal path cost of 166, with 14 locations in the path<br>
    c) for world2, it finds a suboptimal path cost of 152, with 10 locations in the path</p>
  3) Diagonal Shortcut:</p>
    <p>a) this heuristic computes the cost of moving diagonally even if it is not possible, so the path is always directed at the goal<br>
    b) for world1, it finds an OPTIMAL path cost of 130, with 11 locations in the path<br>
    c) for world2, it finds an OPTIMAL path cost of 144, with 10 locations in the path</p>
  4) Chebyshev Distance:</p>
    <p>a) this heuristic computes the cost of moving if diagonal moves are impossible, and subtracts the cost of actually moving diagonally<br>
    b) for world1, it finds an OPTIMAL path cost of 130, with 11 locations in the path<br>
    c) for world2, it finds an OPTIMAL path cost of 144, with 10 locations in the path</p>
