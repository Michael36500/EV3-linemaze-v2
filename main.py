from functools import wraps
from robot import Robot




def tremaux(robot: Robot) -> None:
    my_map = [['.' for _ in range(10)] for _ in range(10)]
    print(robot.where_am_i())
    


def main():
    robot = Robot()
    tremaux(robot)



if __name__ == '__main__':
    main()
