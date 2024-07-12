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


def pprint_maze(mapa: list) -> None:
    for line in mapa:
        for char in line:
            print(char, end='')
            if char in '─ ┌ ├ └ ┬ ┴ ┼ ╶':   print('─', end='')
            else:                           print(' ', end='')

        print()


def dot_if_zero(num: int) -> str:
    if num == 0 or num == '.': return ' '
    return str(num)

def bolden_char(char: str) -> str:
    match char:
        case '─':       return '━'
        case '│':       return '┃'
        case '┌':       return '┏'
        case '┐':       return '┓'
        case '┘':       return '┛'
        case '├':       return '┣'
        case '└':       return '┗'
        case '┤':       return '┫'
        case '┬':       return '┳'
        case '┴':       return '┻'
        case '┼':       return '╋'
        case '■':       return '█'
        case '╴':       return '╸'
        case '╵':       return '╹'
        case '╶':       return '╺'
        case '╷':       return '╻'
        case ' ':       return ' '

def charing(dot: str, maze_char: str, direction: str) -> str:
    try:
        dot = int(dot)
        if dot > 10: return 'X'
        else: return str(dot)
    except:
        match maze_char:
            case '─':
                if direction == 'up' or direction == 'down': return ' '
                elif direction == 'left' or direction == 'right': return '─'
            case '│':
                if direction == 'up' or direction == 'down': return '│'
                elif direction == 'left' or direction == 'right': return ' '
            case '┌':
                if direction == 'down': return '│'
                elif direction == 'right': return '─'
                else: return ' '
            case '┐':
                if direction == 'down': return '│'
                elif direction == 'left': return '─'
                else: return ' '
            case '└':
                if direction == 'up': return '│'
                elif direction == 'right': return '─'
                else: return ' '
            case '┘':
                if direction == 'up': return '│'
                elif direction == 'left': return '─'
                else: return ' '
            case '├':
                if direction == 'up' or direction == 'down': return '│'
                elif direction == 'right': return '─'
                else: return ' '
            case '┤':
                if direction == 'up' or direction == 'down': return '│'
                elif direction == 'left': return '─'
                else: return ' '
            case '┬':
                if direction == 'left' or direction == 'right': return '─'
                elif direction == 'down': return '│'
                else: return ' '
            case '┴':
                if direction == 'left' or direction == 'right': return '─'
                elif direction == 'up': return '│'
                else: return ' '
            case '┼':
                if direction == 'up' or direction == 'down': return '│'
                elif direction == 'left' or direction == 'right': return '─'
                else: return ' '
            case '■':
                return ' '
            case '╴':
                if direction == 'left': return '─'
                else: return ' '
            case '╵':
                if direction == 'up': return '│'
                else: return ' '
            case '╶':
                if direction == 'right': return '─'
                else: return ' '
            case '╷':
                if direction == 'down': return '│'
                else: return ' '
            case _:
                return ' '
    

def pprint_map(map: list, maze: list, pos) -> None:
    y = -1
    for line_map, line_maze in zip(map, maze):
        y += 1
        if str(line_maze)\
            .replace(' ', '')\
            .replace('.', '')\
            .replace('[', '')\
            .replace(']', '')\
            .replace('\'', '')\
            .replace(',', '')\
            == '' and y > 6: continue

        top: str = ''
        mid: str = ''
        bot: str = ''

        x = -1 
        for policko, maze_char in zip(line_map, line_maze): 
            x += 1 
            if pos.x == x and pos.y == y:
                top += f'   {charing(dot_if_zero(policko.up), maze_char, "up")}   '
                mid += f' {charing(dot_if_zero(policko.left), maze_char, "left")} \033[1m\033[91mX\033[0m {charing(dot_if_zero(policko.right), maze_char, "right")} '
                bot += f'   {charing(dot_if_zero(policko.down), maze_char, "down")}   '

            else:
                top += f'   {charing(dot_if_zero(policko.up), maze_char, "up")}   '
                mid += f' {charing(dot_if_zero(policko.left), maze_char, "left")} {bolden_char(dot_if_zero(maze_char))} {charing(dot_if_zero(policko.right), maze_char, "right")} '
                bot += f'   {charing(dot_if_zero(policko.down), maze_char, "down")}   '

        print(top)
        print(mid)
        print(bot)




def tremaux(robot: Robot) -> None:
    seed = random.randrange(sys.maxsize)
    random.seed(seed)
    print(f'Seed: {seed}', file=open('seed', 'w'))

    my_map = [[Policko() for _ in range(10)] for _ in range(10)]
    my_maze = [['.' for _ in range(10)] for _ in range(10)]

    robot.forward()

    itera = 0
    number_of_zeroes = 0
 
    while True:
        itera += 1
        # print(f'Itera: {itera}')
        current = robot.where_am_i()
        my_maze[robot.pos.y][robot.pos.x] = current
        # print('------')
        # print(f'pos: {robot.pos.x}, {robot.pos.y}')
        # print(f'orient: {robot.orientation.str_orient}')
        # print(f'current: {current}')
        # print()
        
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
            dict_policko = policko.__dict__.copy()




            
            if current == '├':  dict_policko.pop('left')
            if current == '┤':  dict_policko.pop('right')
            if current == '┬':  dict_policko.pop('up')
            if current == '┴':  dict_policko.pop('down')

            # if sum(dict_policko.values()) == 0:
            #     number_of_zeroes += len(dict_policko)

            list_mini = [key for key, value in dict_policko.items() if value == min(dict_policko.values())]
            random.shuffle(list_mini)
            robot.turn_absolute(list_mini[0]) 

            # for key, value in dict_policko.items():
            #     if value == 0: marked_0.append(key)
            #     if value == 1: marked_1.append(key)

            # random.shuffle(marked_0)
            # random.shuffle(marked_1)  

            # if marked_0 != []:
            #     # print(marked_0)
            #     robot.turn_absolute(marked_0[0])

            # elif marked_0 == []:
            #     if marked_1 != []:
            #         # print(marked_1)
            #         robot.turn_absolute(marked_1[0])

            #     elif marked_1 == []:
            #         robot.turn_around()

            

                

            # print(my_map[robot.pos.y][robot.pos.x].__dict__)
            # print(f'heading: {robot.orientation.str_orient}')
            my_map[robot.pos.y][robot.pos.x].__dict__[robot.orientation.str_orient] += 1

            # print(policko.__dict__)

        elif current == '■':
            print('┌─────────────────┐')
            print('| End of the maze |')
            print('└─────────────────┘')

            # pprint_maze(my_maze)
            # pprint_map(my_map, my_maze)
            # exit(0)
            robot.turn_around()
            # robot.forward()


            # sleep(1)

        if number_of_zeroes == 0:
            print('┌──────────────────────────┐')
            print('| All of the maze searched |')
            print('└──────────────────────────┘')
            print('Iterations:', itera)
            exit(0)

    
        robot.forward() 
        # pprint_map(my_map, my_maze, robot.pos)
        # sleep(0.2)
                    
    


def main():
    map_size = 10
    robot = Robot()
    tremaux(robot)



if __name__ == '__main__':
    main()
