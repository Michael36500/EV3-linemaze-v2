#!/usr/bin/env pybricks-micropython

# from simuation import Robot
from robot import Robot

# from dataclasses import dataclass
from time import sleep
import random, sys


# @dataclass
# class Policko:
#     up:     int = 0
#     right:  int = 0
#     down:   int = 0
#     left:   int = 0


class Policko:
    def __init__(self) -> None:
        self.up = 0
        self.right = 0
        self.down = 0
        self.left = 0


def pprint_maze(mapa: list) -> None:
    for line in mapa:
        for char in line:
            print(char, end="")
            if char in "─ ┌ ├ └ ┬ ┴ ┼ ╶":
                print("─", end="")
            else:
                print(" ", end="")

        print()


def dot_if_zero(num: int) -> str:
    if num == 0 or num == ".":
        return " "
    return str(num)


bolden_characters = {
    "─": "━",
    "│": "┃",
    "┌": "┏",
    "┐": "┓",
    "┘": "┛",
    "├": "┣",
    "└": "┗",
    "┤": "┫",
    "┬": "┳",
    "┴": "┻",
    "┼": "╋",
    "■": "█",
    "╴": "╸",
    "╵": "╹",
    "╶": "╺",
    "╷": "╻",
    " ": " ",
}


def bolden_char(char: str) -> str:
    return bolden_characters[char]


maze_chars_around = {
    "─": {"up": " ", "down": " ", "left": "─", "right": "─"},
    "│": {"up": "│", "down": "│", "left": " ", "right": " "},
    "┌": {"down": "│", "right": "─", "default": " "},
    "┐": {"down": "│", "left": "─", "default": " "},
    "└": {"up": "│", "right": "─", "default": " "},
    "┘": {"up": "│", "left": "─", "default": " "},
    "├": {"up": "│", "down": "│", "right": "─", "default": " "},
    "┤": {"up": "│", "down": "│", "left": "─", "default": " "},
    "┬": {"left": "─", "right": "─", "down": "│", "default": " "},
    "┴": {"left": "─", "right": "─", "up": "│", "default": " "},
    "┼": {"up": "│", "down": "│", "left": "─", "right": "─", "default": " "},
    "■": {"default": " "},
    "╴": {"left": "─", "default": " "},
    "╵": {"up": "│", "default": " "},
    "╶": {"right": "─", "default": " "},
    "╷": {"down": "│", "default": " "},
    "default": {"default": " "},
}


def charing(dot: str, maze_char: str, direction: str) -> str:
    try:
        dot = int(dot)
        if dot > 10:
            return "X"
        else:
            return str(dot)
    except:
        try:
            return maze_chars_around[maze_char][direction]
        except:
            return " "
        # return dot


def pprint_map(map: list, maze: list, pos) -> None:
    y = -1
    for line_map, line_maze in zip(map, maze):
        y += 1
        if (
            str(line_maze)
            .replace(" ", "")
            .replace(".", "")
            .replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace(",", "")
            == ""
            and y > 6
        ):
            continue

        top = ""
        mid = ""
        bot = ""

        x = -1
        for policko, maze_char in zip(line_map, line_maze):
            x += 1
            if pos.x == x and pos.y == y:
                top += "   " + charing(dot_if_zero(policko.up), maze_char, "up") + "   "
                mid += (
                    " "
                    + charing(dot_if_zero(policko.left), maze_char, "left")
                    + " \033[1m\033[91mX\033[0m "
                    + charing(dot_if_zero(policko.right), maze_char, "right")
                    + " "
                )
                bot += (
                    "   "
                    + charing(dot_if_zero(policko.down), maze_char, "down")
                    + "   "
                )

            else:
                top += "   " + charing(dot_if_zero(policko.up), maze_char, "up") + "   "
                mid += (
                    " "
                    + charing(dot_if_zero(policko.left), maze_char, "left")
                    + " "
                    + bolden_char(dot_if_zero(maze_char))
                    + " "
                    + charing(dot_if_zero(policko.right), maze_char, "right")
                    + " "
                )
                bot += (
                    "   "
                    + charing(dot_if_zero(policko.down), maze_char, "down")
                    + "   "
                )

        if mid.strip() == "":
            continue
        print(top)
        print(mid)
        print(bot)


def is_there_zero(policko: Policko) -> bool:
    if policko.up == 0:
        return True
    if policko.right == 0:
        return True
    if policko.down == 0:
        return True
    if policko.left == 0:
        return True
    return False


# def lenght_to_zero(key: str, pos, my_map) -> int:
#     x = pos.x
#     y = pos.y
#     if key == "up":
#         y -= 1
#     elif key == "right":
#         x += 1
#     elif key == "down":
#         y += 1
#     elif key == "left":
#         x -= 1

#     policko = my_map[y][x]
#     if is_there_zero(policko):
#         return 1
#     if policko == "─":
#         return min(
#             lenght_to_zero("left", pos, my_map) + 1,
#             lenght_to_zero("right", pos, my_map + 1),
#         )
#     elif policko == "│":
#         return min(
#             lenght_to_zero("up", pos, my_map) + 1,
#             lenght_to_zero("down", pos, my_map + 1),
#         )
#     elif policko == "┌":
#         return min(
#             lenght_to_zero("right", pos, my_map) + 1,
#             lenght_to_zero("down", pos, my_map + 1),
#         )
#     elif policko == "┐":
#         return min(
#             lenght_to_zero("left", pos, my_map) + 1,
#             lenght_to_zero("down", pos, my_map + 1),
#         )
#     elif policko == "┘":
#         return min(
#             lenght_to_zero("left", pos, my_map) + 1,
#             lenght_to_zero("up", pos, my_map + 1),
#         )
#     elif policko == "├":
#         return min(
#             lenght_to_zero("up", pos, my_map) + 1,
#             lenght_to_zero("right", pos, my_map) + 1,
#             lenght_to_zero("down", pos, my_map + 1),
#         )
#     elif policko == "└":
#         return min(
#             lenght_to_zero("up", pos, my_map) + 1,
#             lenght_to_zero("right", pos, my_map) + 1,
#         )
#     elif policko == "┤":
#         return min(
#             lenght_to_zero("up", pos, my_map) + 1,
#             lenght_to_zero("left", pos, my_map) + 1,
#             lenght_to_zero("down", pos, my_map + 1),
#         )
#     elif policko == "┬":
#         return min(
#             lenght_to_zero("left", pos, my_map) + 1,
#             lenght_to_zero("right", pos, my_map) + 1,
#             lenght_to_zero("down", pos, my_map + 1),
#         )
#     elif policko == "┴":
#         return min(
#             lenght_to_zero("left", pos, my_map) + 1,
#             lenght_to_zero("right", pos, my_map) + 1,
#             lenght_to_zero("up", pos, my_map + 1),
#         )
#     elif policko == "┼":
#         return min(
#             lenght_to_zero("left", pos, my_map) + 1,
#             lenght_to_zero("right", pos, my_map) + 1,
#             lenght_to_zero("up", pos, my_map) + 1,
#             lenght_to_zero("down", pos, my_map + 1),
#         )
#     else:
#         return 10000


def tremaux(robot: Robot, debug=True) -> None:
    seed = random.randrange(sys.maxsize)
    # seed = 2548946025440068861
    random.seed(seed)
    print("Seed:", seed, file=open("seed", "w"))

    my_map = [[Policko() for _ in range(10)] for _ in range(10)]
    my_maze = [["." for _ in range(10)] for _ in range(10)]

    robot.forward()

    itera = 0
    number_of_zeroes = 1

    robot.ev3.speaker.beep()
    input("continue?")

    while True:
        itera += 1
        # print(f'Itera: {itera}')
        current = robot.where_am_i()
        my_maze[robot.pos.y][robot.pos.x] = current
        if debug:
            print("------")
            print("pos:", robot.pos.x, ",", robot.pos.y)
            print("orient:", robot.orientation.str_orient)
            print("current:", current)
            print()

        # on a straight line
        if current in "─│":
            pass

        # in a turn
        elif current in "┌┐└┘":
            if current == "┌":
                if robot.orientation.str_orient == "up":
                    robot.turn_right()
                elif robot.orientation.str_orient == "left":
                    robot.turn_left()
                else:
                    raise ValueError("Invalid turn:", robot.orientation.str_orient)
            elif current == "┐":
                if robot.orientation.str_orient == "up":
                    robot.turn_left()
                elif robot.orientation.str_orient == "right":
                    robot.turn_right()
                else:
                    raise ValueError("Invalid turn:", robot.orientation.str_orient)
            elif current == "└":
                if robot.orientation.str_orient == "down":
                    robot.turn_left()
                elif robot.orientation.str_orient == "left":
                    robot.turn_right()
                else:
                    raise ValueError("Invalid turn:", robot.orientation.str_orient)
            elif current == "┘":
                if robot.orientation.str_orient == "down":
                    robot.turn_right()
                elif robot.orientation.str_orient == "right":
                    robot.turn_left()
                else:
                    raise ValueError("Invalid turn:", robot.orientation.str_orient)
        elif current in "╴╵╶╷":
            robot.turn_around()

        elif current in "├ ┤ ┬ ┴ ┼":
            # apply logic
            # firsly, mark the current field
            if (
                my_map[robot.pos.y][robot.pos.x].__dict__[
                    robot.orientation.num2str((robot.orientation.int_orient + 2) % 4)
                ]
                == 0
            ):
                number_of_zeroes -= 1

            # choose the direction
            policko = my_map[robot.pos.y][robot.pos.x]
            ## try to pick unmarked path
            dict_policko = policko.__dict__.copy()
            if current == "├":
                dict_policko.pop("left")
            if current == "┤":
                dict_policko.pop("right")
            if current == "┬":
                dict_policko.pop("up")
            if current == "┴":
                dict_policko.pop("down")

            if sum(dict_policko.values()) == 0:
                number_of_zeroes += len(dict_policko)

            my_map[robot.pos.y][robot.pos.x].__dict__[
                robot.orientation.num2str((robot.orientation.int_orient + 2) % 4)
            ] += 1

            dict_policko = policko.__dict__.copy()
            if current == "├":
                dict_policko.pop("left")
            if current == "┤":
                dict_policko.pop("right")
            if current == "┬":
                dict_policko.pop("up")
            if current == "┴":
                dict_policko.pop("down")

            list_mini = [
                key
                for key, value in dict_policko.items()
                if value == min(dict_policko.values())
            ]
            random.shuffle(list_mini)
            print(list_mini)
            # dict_length = {}
            # for key in list_mini:
            #     dict_length[key] = lenght_to_zero(key, robot.pos, my_map)
            # print(dict_length)
            # list_mini = [key for key, value in zip(list_mini, dict_length.items) if value == min(list_lenght)]

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
            if (
                my_map[robot.pos.y][robot.pos.x].__dict__[robot.orientation.str_orient]
                == 0
            ):
                number_of_zeroes -= 1
            my_map[robot.pos.y][robot.pos.x].__dict__[robot.orientation.str_orient] += 1

            # print(policko.__dict__)

        elif current == "■":
            if debug:
                print("┌─────────────────┐")
                print("| End of the maze |")
                print("└─────────────────┘")

            # pprint_maze(my_maze)
            # pprint_map(my_map, my_maze)
            # exit(0)
            robot.turn_around()
            robot.forward()

            # sleep(1)

        robot.forward()
        if debug:
            print("Number of zeroes:", number_of_zeroes)
            pprint_map(my_map, my_maze, robot.pos)
            sleep(0.1)

        if number_of_zeroes == 0:
            if debug:
                print("┌──────────────────────────┐")
                print("| All of the maze searched |")
                print("└──────────────────────────┘")
                print("Iterations:", itera)
            # print(itera, file=open('iterations', 'a'))
            return itera
            # exit(0)


def main(debug=True) -> None:
    map_size = 10
    robot = Robot()
    return tremaux(robot, debug)


if __name__ == "__main__":
    main()
