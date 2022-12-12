from rich import print, traceback

traceback.install()
from pathlib import Path
from dataclasses import dataclass, field, replace
import numpy as np

RAWTESTDATA = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

print(RAWTESTDATA)


@dataclass
class Position:
    x: int
    z: int


assert Position(1, 2).z == 2


@dataclass
class Bridge:
    data: list[tuple[str, int]] = field(repr=False)
    tail_visited: set[(int, int)]
    head_visited: set[(int, int)]
    head: "Position"
    tail: "Position"

    def __init__(self, data) -> None:
        self.data = [
            (line.split()[0], int(line.split()[1])) for line in data.splitlines()
        ]
        self.head_visited = set()
        self.tail_visited = set()
        self.head = Position(0, 0)
        self.tail = Position(0, 0)

    def move_rope(self):
        for dir, length in self.data:
            for _ in range(length):
                # print(dir)
                match dir:
                    case "R":
                        self.head.x += 1
                    case "L":
                        self.head.x -= 1
                    case "U":
                        self.head.z += 1
                    case "D":
                        self.head.z -= 1
                    case _:
                        raise ValueError("invalid move")
                self.move_tail()
                self.head_visited.add((self.head.x, self.head.z))
                self.tail_visited.add((self.tail.x, self.tail.z))

    def move_tail(self):
        dx = self.head.x - self.tail.x
        dz = self.head.z - self.tail.z
        if dx == 2:
            self.tail.x += 1
            if abs(dz) == 1:
                self.tail.z += dz
        elif dx == -2:
            self.tail.x -= 1
            if abs(dz) == 1:
                self.tail.z += dz
        if dz == 2:
            self.tail.z += 1
            if abs(dx) == 1:
                self.tail.x += dx
        elif dz == -2:
            self.tail.z -= 1
            if abs(dx) == 1:
                self.tail.x += dx

    def number_visited(self):

        print(len(self.tail_visited))

    def print_tail_visited(self):
        mat = [["." for _ in range(6)] for _ in range(5)]
        for (x, z) in self.tail_visited:
            mat[z][x] = "*"
        for line in mat[::-1]:
            print("".join(line))


test_bridge = Bridge(RAWTESTDATA)
print(test_bridge)
test_bridge.move_rope()
# print(test_bridge)
test_bridge.print_tail_visited()
test_bridge.number_visited()

#
# RAWDATA = Path("day09.txt").read_text()
# test_bridge = Bridge(RAWDATA)
# print(test_bridge)
# test_bridge.move_rope()
## print(test_bridge)
## test_bridge.print_tail_visited()
# test_bridge.number_visited()


@dataclass
class Bridge_part2:
    data: list[tuple[str, int]] = field(repr=False)
    tail_visited: set[(int, int)]
    head: "Position"
    tails: list("Position")

    def __init__(self, data) -> None:
        self.data = [
            (line.split()[0], int(line.split()[1])) for line in data.splitlines()
        ]
        self.tail_visited = set()
        self.head = Position(0, 0)
        self.tails = [Position(0, 0) for _ in range(9)]

    def move_rope(self):
        for dir, length in self.data:
            for _ in range(length):
                # print(dir)
                match dir:
                    case "R":
                        self.head.x += 1
                    case "L":
                        self.head.x -= 1
                    case "U":
                        self.head.z += 1
                    case "D":
                        self.head.z -= 1
                    case _:
                        raise ValueError("invalid move")
                out_tail = []
                first = self.head
                for tail_next in self.tails:
                    second = tail_next

                    out = self.move_tail(first, second)
                    out_tail.append(out)
                    self.tail_visited.add((out.x, out.z))
                    first = out
                self.tails = out_tail

    def move_tail(self, first, second):
        dx = first.x - second.x
        dz = first.z - second.z
        x_out = second.x
        z_out = second.z
        if dx == 2:
            x_out += 1
            if abs(dz) == 1:
                z_out += dz
        elif dx == -2:
            x_out -= 1
            if abs(dz) == 1:
                z_out += dz
        if dz == 2:
            z_out += 1
            if abs(dx) == 1:
                x_out += dx
        elif dz == -2:
            z_out -= 1
            if abs(dx) == 1:
                x_out += dx
        return Position(x_out, z_out)

    def number_visited(self):

        print(len(self.tail_visited))

    def print_visited(self):
        mat = [["." for _ in range(6)] for _ in range(5)]
        for (x, z) in self.tail_visited:
            mat[z][x] = "*"
        for line in mat[::-1]:
            print("".join(line))

    def print_tail_visited(self):
        mat = [["." for _ in range(6)] for _ in range(5)]
        for (x, z) in self.tail_visited:
            mat[z][x] = "*"
        for line in mat[::-1]:
            print("".join(line))


RAWTESTDATA2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

test_bridge2 = Bridge_part2(RAWTESTDATA2)
print(test_bridge2)
test_bridge2.move_rope()
print(test_bridge2)
test_bridge.print_tail_visited()
test_bridge2.number_visited()
