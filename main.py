from functools import wraps
from robot import Robot




def tremaux(robot: Robot) -> None:
    my_map = [['0' for _ in range(10)] for _ in range(10)]
    
    while True:
        current = robot.where_am_i()
        
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

        # if current in '├┤┬┴':
        #     # apply logic

                 

                    
    


def main():
    map_size = 10
    robot = Robot()
    tremaux(robot)



if __name__ == '__main__':
    main()
