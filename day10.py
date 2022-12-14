from rich import print, traceback

traceback.install()
from pathlib import Path
from dataclasses import dataclass, field, replace
import numpy as np

RAWTEST1 = """\
noop
addx 3
addx -5"""

RAWTEST2 = Path("day10test.txt").read_text()
RAWDATA = Path("day10.txt").read_text()


@dataclass
class Adder:
    instructions: list[int] = field(repr=False)
    out: list[int] = field(default_factory=list, repr=False)
    x: int = 1
    cycle: int = 1

    def run(self):
        print(self)
        for line in self.instructions.splitlines():
            self.run_instruc(line)

    def run_instruc(self, line):
        line_list = line.split(" ")
        match line_list:
            case ["noop"]:
                self.cycle += 1
                self.out.append(self.x)
            case ["addx", _]:
                self.out.append(self.x)
                self.out.append(self.x)

                self.cycle += 2
                num = int(line_list[1])
                self.x += num
            case _:
                raise ValueError("invalid parse")
        print(line, self)

    def signal_stregth(self):
        total = 0
        for i, val in enumerate(self.out):
            print(i, val, "strength", end="")

            if (i + 1 - 20) % 40 == 0:
                print(i * val)
                total += (i + 1) * val
            else:
                print("")
        print("total signal strength", total)


test_adder = Adder(RAWTEST1)
test_adder.run()

print("done!!")

test_adder = Adder(RAWTEST2)
test_adder.run()

print("checking stregth!!")
test_adder.signal_stregth()

adder = Adder(RAWDATA)
adder.run()

print("checking stregth!!")
adder.signal_stregth()
