from typing import *

# from dataclasses import dataclass
# from pydantic import BaseModel


class Position:
    # @enforce_types
    def __init__(slef, x: int, y: int) -> None:
        slef.x = x
        slef.y = y


class Orientation:
    def num2str(slef, num: int) -> str:
        if num == 0:
            return "up"
        if num == 1:
            return "right"
        if num == 2:
            return "down"
        if num == 3:
            return "left"

    def str2num(slef, stri: str) -> int:
        if stri == "up":
            return 0
        if stri == "right":
            return 1
        if stri == "down":
            return 2
        if stri == "left":
            return 3

    def __init__(slef, starting: str) -> None:
        if starting not in ["up", "right", "down", "left"]:
            raise ValueError("Invalid orientation")

        slef.str_orient = starting
        slef.int_orient = slef.str2num(starting)

    def left(slef) -> None:
        slef.int_orient = (slef.int_orient - 1) % 4
        slef.str_orient = slef.num2str(slef.int_orient)

    def right(slef) -> None:
        slef.int_orient = (slef.int_orient + 1) % 4
        slef.str_orient = slef.num2str(slef.int_orient)


class Robot:
    def load_mapa(_) -> List[List[str]]:
        mapa = []
        with open("maze") as f:
            for line in f:
                lin = []
                for char in line:
                    char = char.strip()
                    if char == "":
                        char = " "
                    lin.append(char)
                mapa.append(lin)
        return mapa

    def where_am_i(slef) -> str:
        return slef.secret_mapa[slef.pos.y][slef.pos.x]

    def forward(slef) -> None:
        # check if all alrigh
        ## check if orient is valid
        if slef.orientation.str_orient not in ["up", "right", "down", "left"]:
            raise ValueError(f"Invalid orientation: {slef.orientation.str_orient}")

        ## check if out of bounds
        if slef.orientation.str_orient == "up" and slef.pos.y - 1 < -1:
            raise ValueError(
                f"Out of bounds: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}"
            )
        if slef.orientation.str_orient == "right" and slef.pos.x == len(
            slef.secret_mapa[0]
        ):
            raise ValueError(
                f"Out of bounds: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}"
            )
        if slef.orientation.str_orient == "down" and slef.pos.y == len(
            slef.secret_mapa
        ):
            raise ValueError(
                f"Out of bounds: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}"
            )
        if slef.orientation.str_orient == "left" and slef.pos.x - 1 < -1:
            raise ValueError(
                f"Out of bounds: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}"
            )

        ## check if wall
        current: str = slef.secret_mapa[slef.pos.y][slef.pos.x]
        match current:
            case "╴":
                # print(slef.orientation.str_orient != 'left')
                if slef.orientation.str_orient != "left":
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "╵":
                if slef.orientation.str_orient != "up":
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "╶":
                if slef.orientation.str_orient != "right":
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "╷":
                if slef.orientation.str_orient != "down":
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "─":
                if (
                    slef.orientation.str_orient == "up"
                    or slef.orientation.str_orient == "down"
                ):
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "│":
                if (
                    slef.orientation.str_orient == "right"
                    or slef.orientation.str_orient == "left"
                ):
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "┌":
                if (
                    slef.orientation.str_orient == "left"
                    or slef.orientation.str_orient == "up"
                ):
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "┐":
                if (
                    slef.orientation.str_orient == "right"
                    or slef.orientation.str_orient == "up"
                ):
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "└":
                if (
                    slef.orientation.str_orient == "left"
                    or slef.orientation.str_orient == "down"
                ):
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "┘":
                if (
                    slef.orientation.str_orient == "right"
                    or slef.orientation.str_orient == "down"
                ):
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "├":
                if slef.orientation.str_orient == "left":
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "┤":
                if slef.orientation.str_orient == "right":
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "┬":
                if slef.orientation.str_orient == "up":
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "┴":
                if slef.orientation.str_orient == "down":
                    raise ValueError(
                        f"Wall: {slef.pos.x}, {slef.pos.y}, {slef.orientation.str_orient}. {current}"
                    )
            case "┼":
                pass
            case "■":
                if not slef.found_end:
                    slef.found_end = True
                    return "end"
                else:
                    # print('End already found')
                    pass
            case _:
                raise ValueError(
                    f"Invalid character: {current} at {slef.pos.x}, {slef.pos.y}"
                )

        if slef.orientation.str_orient == "up":
            slef.pos.y -= 1
        if slef.orientation.str_orient == "right":
            slef.pos.x += 1
        if slef.orientation.str_orient == "down":
            slef.pos.y += 1
        if slef.orientation.str_orient == "left":
            slef.pos.x -= 1

    def turn_left(slef) -> None:
        slef.orientation.left()

    def turn_right(slef) -> None:
        slef.orientation.right()

    def turn_around(slef) -> None:
        slef.turn_left()
        slef.turn_left()

    def turn_absolute(slef, orient: str) -> None:
        start = slef.orientation.int_orient
        end = Orientation.str2num("slef", orient)
        # print(f'start: {start}, end: {end}')

        if start == end:
            return
        if (start - end) % 4 == 1:
            slef.turn_left()
        if (start - end) % 4 == 3:
            slef.turn_right()
        if (start - end) % 4 == 2:
            slef.turn_around()

    def __init__(slef) -> None:
        slef.secret_mapa = slef.load_mapa()
        slef.found_end = False
        slef.pos = Position(0, 0)
        slef.orientation = Orientation("right")
