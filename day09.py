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
test_bridge.move_rope()
print(test_bridge)
test_bridge.print_tail_visited()
print("The number of locations the tail visited, should be 13")
test_bridge.number_visited()

#
RAWDATA = Path("day09.txt").read_text()
test_bridge = Bridge(RAWDATA)
test_bridge.move_rope()
print("the number of locations the tail visited part a ")
test_bridge.number_visited()


@dataclass
class Bridge_part2:
    data: list[tuple[str, int]] = field(repr=False)
    tail_visited: set[(int, int)]
    head: "Position"
    tails: list("Position")
    matsize: int

    def __init__(self, data, matsize=6, startpos=(0, 0)) -> None:
        self.matsize = matsize
        self.data = [
            (line.split()[0], int(line.split()[1])) for line in data.splitlines()
        ]
        self.tail_visited = set()
        self.head = Position(*startpos)
        self.tails = [Position(*startpos) for _ in range(9)]

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
                    first = out

                self.tails = out_tail
                self.tail_visited.add((self.tails[-1].x, self.tails[-1].z))
            # self.print_snapshot()

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

    def print_snapshot(self):
        """after tail has been moved print tail."""
        mat = [["." for _ in range(self.matsize)] for _ in range(self.matsize)]
        mat[self.head.z][self.head.x] = "H"
        print("_________________")
        for itail, pos in enumerate(self.tails):
            mat[pos.z][pos.x] = str(1 + itail)
        for line in mat[::-1]:
            print("".join(line))

    def print_tail_visited(self):
        mat = [["." for _ in range(self.matsize)] for _ in range(self.matsize)]
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

test_bridge2 = Bridge_part2(RAWTESTDATA2, matsize=30, startpos=(13, 13))
print(test_bridge2)
test_bridge2.move_rope()
print(test_bridge2)
test_bridge2.print_tail_visited()
print(("The number locatinos the tail visited part 2 test set, should be 36"))

test_bridge2.number_visited()

RAWDATA = Path("day09.txt").read_text()
bridge = Bridge_part2(RAWDATA, matsize=30, startpos=(13, 13))
bridge.move_rope()
print(("The number locatinos the tail visited part 2"))
bridge.number_visited()
