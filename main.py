from robot import Robot
from dataclasses import dataclass
from time import sleep
import random, sys


@dataclass
class Policko:
    up:     int = 0
    right:  int = 0
    down:   int = 0
    left:   int = 0


def pprint_map(mapa: list) -> None:
    for line in mapa:
        for char in line:
            print(char, end='')
            if char in '─ ┌ ├ └ ┬ ┴ ┼ ╶':   print('─', end='')
            else:                           print(' ', end='')

        print()
def tremaux(robot: Robot) -> None:
    seed = random.randrange(sys.maxsize)
    random.seed(seed)
    print(f'Seed: {seed}', file=open('seed', 'w'))

    my_map = [[Policko() for _ in range(10)] for _ in range(10)]
    my_maze = [['.' for _ in range(10)] for _ in range(10)]

    robot.forward()
    
    while True:
        current = robot.where_am_i()
        my_maze[robot.pos.y][robot.pos.x] = current
        print('------')
        print(f'pos: {robot.pos.x}, {robot.pos.y}')
        print(f'orient: {robot.orientation.str_orient}')
        print(f'current: {current}')
        print()
        
        # on a straight line
        if current in '─│':
            pass

        # in a turn
        elif current in '┌┐└┘':
            match current:
                case '┌':
                    if robot.orientation.str_orient == 'up':          robot.turn_right()
                    elif robot.orientation.str_orient == 'left':        robot.turn_left()
                    else:       raise ValueError(f'Invalid turn: {robot.orientation.str_orient}')
                case '┐':
                    if robot.orientation.str_orient == 'up':          robot.turn_left()
                    elif robot.orientation.str_orient == 'right':       robot.turn_right()
                    else:       raise ValueError(f'Invalid turn: {robot.orientation.str_orient}')
                case '└':
                    if robot.orientation.str_orient == 'down':        robot.turn_left()
                    elif robot.orientation.str_orient == 'left':        robot.turn_right()
                    else:       raise ValueError(f'Invalid turn: {robot.orientation.str_orient}')
                case '┘':
                    if robot.orientation.str_orient == 'down':        robot.turn_right()
                    elif robot.orientation.str_orient == 'right':       robot.turn_left()
                    else:       
                        raise ValueError(f'Invalid turn: {robot.orientation.str_orient}')
        
        elif current in '╴╵╶╷':
            robot.turn_around()

        elif current in '├┤┬┴┼':
            # apply logic
            # firsly, mark the current field
            my_map[robot.pos.y][robot.pos.x].__dict__[
                robot.orientation.num2str(
                    (robot.orientation.int_orient + 2) %4
                )
            ] += 1

            # choose the direction
            policko = my_map[robot.pos.y][robot.pos.x]
            ## try to pick unmarked path
            marked_0 = []
            marked_1 = []
            dict_policko = policko.__dict__.copy()

            
            if current == '├':  dict_policko.pop('left')
            if current == '┤':  dict_policko.pop('right')
            if current == '┬':  dict_policko.pop('up')
            if current == '┴':  dict_policko.pop('down')

            for key, value in dict_policko.items():
                if value == 0: marked_0.append(key)
                if value == 1: marked_1.append(key)

            random.shuffle(marked_0)
            random.shuffle(marked_1)  

            if marked_0 != []:
                print(marked_0)
                robot.turn_absolute(marked_0[0])

            elif marked_0 == []:
                if marked_1 != []:
                    print(marked_1)
                    robot.turn_absolute(marked_1[0])

                elif marked_1 == []:
                    robot.turn_around()
            

                

            print(my_map[robot.pos.y][robot.pos.x].__dict__)
            print(f'heading: {robot.orientation.str_orient}')
            my_map[robot.pos.y][robot.pos.x].__dict__[robot.orientation.str_orient] += 1

            print(policko.__dict__)

        elif current == '■':
            print('┌─────────────────┐')
            print('| End of the maze |')
            print('└─────────────────┘')

            pprint_map(my_maze)
            exit(0)
            # robot.turn_around()
            # robot.forward()


            # sleep(1)

    
        robot.forward() 
                    
    


def main():
    map_size = 10
    robot = Robot()
    tremaux(robot)



if __name__ == '__main__':
    main()
