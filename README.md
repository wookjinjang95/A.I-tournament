# A.I-tournament

This is A-I tournament I created in a group of two people during my artificial intelligence course. To run this file of the
result, please follow the command below.

  python capture.py -r baselineTeam -b myTeam
  
  
If you run the code above, you will be able to see red team and blue team. Blue team is the A.I pacman that I created and
redTeam is the baseline A.I that I have to go against.

## Files

### Key files to read:
  #### capture.py	
  The main file that runs games locally. This file also describes the new capture the flag GameState type and rules.
  
  #### captureAgents.py	
  Specification and helper methods for capture agents.
  
  #### baselineTeam.py	
  Example code that defines two very basic reflex agents, to help you get started.
  
  #### myTeam.py	
  This is where you define your own agents for inclusion in the nightly tournament. (This is the only file that you submit.) 
  Currently, there is a Dummy Agent defined to help you get started.

### Supporting files (do not modify):
  #### game.py
  The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.
  
  #### util.py
  Useful data structures for implementing search algorithms.

  #### distanceCalculator.py
  Computes shortest paths between all maze positions.
  
  #### graphicsDisplay.py	
  Graphics for Pacman

  #### graphicsUtils.py	
  Support for Pacman graphics
  
  #### textDisplay.py	
  ASCII graphics for Pacman
  
  #### keyboardAgents.py	
  Keyboard interfaces to control Pacman
  
  #### layout.py
  Code for reading layout files and storing their contents
