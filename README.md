# Line maze solving robot
This is a code for my line-maze solving robot.

## What is an Line Maze?
Line maze is a robotics discipline, that involves solving, you guessed it, a line maze, such as this one:

![line maze image](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.5IgMjDqidQk2i5VfR3WRxQHaFj%26pid%3DApi&f=1&ipt=57869ebd42321d696badb4720392bb809baa4c457bbe52a37f5e557543692111&ipo=images)

The robot goes from the start (on the left) to the end (on the right). He's allowed multiple attempts and can "remember" the path. Usually on the first run robot "scouts" the maze, then finds the fastest route and on the second run he tries to go as fast as possible.

## My approach
I decided (after having some probles with algorithm for traversing the maze) to firstly write a simulator, in [simulation.py](simulation.py) is code for "digital" version of my robot.

Then, in [robot.py](robot.py) is the actual code for the robot, how he should move and etc.

Last, but not least, in [main.py](main.py) is the main algorithm for finding the route. I am using [Trémaux's algorithm](https://en.wikipedia.org/wiki/Maze-solving_algorithm#Tr%C3%A9maux's_algorithm) for it's simplicity. Still, I have struggle with the implementation.

## Current state of the project
I've completed the simulation part, you can run it by cloning the project and executing [main.py](main.py). I've also completed the hardware part of robot, although I was limited by bricks and I'm planning on rebuilding.

The biggest struggle right now is with software part of robot. For some reason, even on the same track, simulation code and "real" code behaves very differently. Simulation searches through the maze quite fast, but real robot is acting random. No, it's worse than random, he *purpusefully* goes in the wrong direction every time. 

## Showcase
### How it works (in the current state)
[how it works](vids/how_it_works.mp4)

### How it should work
[how it should work](vids/how_it_should_work.mp4)

### Simulation showcase
Sadly, it was recorded with night-mode enabled... >:(

[sim showcase](vids/simulation_video.webm)

## Future plans
- [ ] - make robot working
- [ ] - add some optimalizations
  - [ ] like cutting corners to save time 
  - [ ] or prefering straight paths with less turns
  - [ ] and accelerating more on long straights
- [ ] - add some kind of ui to the robot
