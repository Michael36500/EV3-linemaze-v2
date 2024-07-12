from functools import wraps
from robot import Robot




def tremaux(robot: Robot) -> None:
    my_map = [['.' for _ in range(10)] for _ in range(10)]
    
    while True:
        current = robot.where_am_i()
        
        # on a straight line
        if current in '─│':
            robot.forward()
            continue

        # in a turn
        # if current in '┌┐└┘':
        #     robot.forward()
        #     continue
    


def main():
    map_size = 10
    robot = Robot()
    tremaux(robot)



if __name__ == '__main__':
    main()
