README for BlockBots

Author: Andrew Ellison

Dependencies:
- Python 3: https://www.python.org/downloads/
- Pyglet: https://bitbucket.org/pyglet/pyglet/wiki/Home

The idea of this game is to program robots to manage a warehouse. Boxes are delivered via Delivery Blocks and must be moved to the correct Delivery blocks at the correct times to win points. Given an infinitely sized warehouse, this game should be Turing Complete.


Programs for robots are essentially Finite State Machines with output being robot movement and input being the presence or absence of boxes in adjacent squares. The programs themselves are collections of instructions of the format (instruction_name,actions,transition_1/transition_n). As many of these instructions as necessary may be used to build a program.

Instructions may be named any string or character except for brackets and commas.

Actions are strings of w, a, s, and d. Each character commands the robot to move once in that direction. The condition(s) are evaluated once every action in the string has been completed.

Transitions change the instruction currently being followed by the robot, they are made up of a condition and a destination (condition->next_instruction) and are delimited by a forward slash (/). Conditions and their destination instruction are delimited by an arrow (->).

Conditions are strings comprised of the same characters as actions, except they each refer to a sensor telling whether or not there is a box in the adjacent square denoted by the character. These sensor readings must be joined with logical "and" (&) or logical "or" (|). The result of the sensor readings for each condition determines whether the transition is succesful. An empty condition is always succesful, and if every condition fails, the instruction is looped.

The next_instruction part of the condition is simply the instruction_name of any instruction in the program.

eg.(1,,w->2/a->3/s->4/d->5)(2,w,)(3,a,)(4,s,)(5,d,) is the default robot program. It stays still until it senses a box adjacent to it, then moves indefinitely in that direction, pushing the box.


Gameplay is pretty basic at the moment. All interaction is via mouse and console. When the command word is entered in the console, that command is carried out at the position of every left mouse click. Arguments are delimited by a single space from the command and each other.

Console Commands:
- box
- programmer
- conveyor
- robot
- delivery
- delete
- program_visualiser

box: Takes no arguments, simply places a blue box in the warehouse at each mouse click. These boxes can be pushed by robots, conveyor belts and other boxes

programmer: Takes program as argument, places white square at mouse click which will reprogram any robot that drives over it.

conveyor: Takes direction (w, a, s, or d) as argument, places yellow conveyor belt section at mouse click, pushes any box or robot that travels over it in given direction.

robot: Takes no argument, places green robot square that will run according to ts' program and can push boxes.

delivery: Takes two arguments, delivers and time. A grey square that, when placed, delivers or takes away blue boxes according to its' arguments. Delivers is boolean, 1 means it places boxes every update, 0 takes them away every update. Time is in seconds, the time period between updates.

delete: Deletes objects at mouse click.

program_visualiser: Takes a program as argument, at click places a program visualiser which outlines all possible paths of that program from that point in purple squares.