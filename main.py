from robot import Robot
from dataclasses import dataclass


@dataclass
class Policko:
    up:     int = 0
    right:  int = 0
    down:   int = 0
    left:   int = 0


def tremaux(robot: Robot) -> None:
    my_map = [[Policko() for _ in range(10)] for _ in range(10)]
    robot.forward()
    
    while True:
        current = robot.where_am_i()

        print()
        print(f'pos: {robot.pos.x}, {robot.pos.y}')
        print(f'orient: {robot.orientation.str_orient}')
        print(f'current: {current}')
        print()
        
        # on a straight line
        if current in '─│':
            robot.forward()
            continue

        # in a turn
        if current in '┌┐└┘':
            match current:
                case '┌':
                    if robot.direction.str_orient == 'up':          robot.turn_right()
                    if robot.direction.str_orient == 'left':        robot.turn_left()
                    else:       raise ValueError(f'Invalid turn: {robot.direction.str_orient}')
                case '┐':
                    if robot.direction.str_orient == 'up':          robot.turn_left()
                    if robot.direction.str_orient == 'right':       robot.turn_right()
                    else:       raise ValueError(f'Invalid turn: {robot.direction.str_orient}')
                case '└':
                    if robot.direction.str_orient == 'down':        robot.turn_left()
                    if robot.direction.str_orient == 'left':        robot.turn_right()
                    else:       raise ValueError(f'Invalid turn: {robot.direction.str_orient}')
                case '┘':
                    if robot.direction.str_orient == 'down':        robot.turn_right()
                    if robot.direction.str_orient == 'right':       robot.turn_left()
                    else:       raise ValueError(f'Invalid turn: {robot.direction.str_orient}')
            robot.forward()
        
        if current in '╴╵╶╷':
            robot.turn_around()
            robot.forward()

        if current in '├┤┬┴┼':
            # apply logic
            # firsly, mark the current field
            my_map[robot.pos.y][robot.pos.x].__dict__[robot.orientation.str_orient] += 1

            # choose the direction
            policko = my_map[robot.pos.y][robot.pos.x]
            ## try to pick unmarked path
            marked_0 = []
            marked_1 = []
            for key, value in policko.__dict__.items():
                if value == 0: marked_0.append(key)
                if value == 1: marked_1.append(key)

            if marked_0 != []:
                print()
                robot.turn_absolute(marked_0[0])
                robot.forward()

            if marked_0 == []:
                if marked_1 != []:
                    robot.turn_absolute(marked_1[0])
                    robot.forward()
                
                if marked_1 == []:
                    robot.turn_around()
            


            # lastly, mark the exit
            my_map[robot.pos.y][robot.pos.x].__dict__[robot.orientation.str_orient] += 1
            continue
            

                 

                    
    


def main():
    map_size = 10
    robot = Robot()
    tremaux(robot)



if __name__ == '__main__':
    main()
