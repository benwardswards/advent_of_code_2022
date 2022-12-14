from rich import print, traceback

traceback.install()
from pathlib import Path
from dataclasses import dataclass, field, replace
import numpy as np
from collections import defaultdict

RAWTESTDATA = Path("day11test.yml").read_text()
RAWDATA = Path("day11.yml").read_text()

RAWMONKEY = """\
Monkey 1:
  Starting items: 99, 77, 79
  Operation: new = old + 8
  Test: divisible by 2
    If true: throw to monkey 6
    If false: throw to monkey 0"""


@dataclass
class Monkey:
    name: int
    op: str
    op_val: int
    divisible_by: int
    if_true: int
    if_false: int
    start_items: list[int] = field(default_factory=list)

    def __init__(self, rawdata):
        data_list = rawdata.splitlines()
        d0 = data_list[0]
        self.name = d0.strip(":").split(" ")[1]
        d1 = data_list[1]
        self.start_items = [int(d) for d in d1.split(":")[1].split(", ")]

        d2 = data_list[2]

        op, val = d2.split(" ")[6:]
        # print(">>>>>>>", d2, op, val)
        self.op = op
        self.op_val = val
        d3 = data_list[3]
        self.divisible_by = int(d3.strip("  Test: divisible by "))

        self.if_true = data_list[4].split(" ")[-1]
        self.if_false = data_list[5].split(" ")[-1]

    def apply(self, worry: int):
        if self.op_val == "old":
            second = worry
        else:
            second = int(self.op_val)

        if self.op == "*":
            return worry * second
        elif self.op == "+":
            return worry + second
        else:
            raise ValueError("invalid oparand")


my_mon = Monkey(RAWMONKEY)

print("test", my_mon.apply(79))


@dataclass
class MonkeyGame:
    monkeys: dict["str":"Monkey"]
    monkeys_names: list[str]
    inspected: dict["str":int]
    max_number: int = 1

    def __init__(self, rawdata):
        self.monkeys = {
            Monkey(rawmonkey).name: Monkey(rawmonkey)
            for rawmonkey in rawdata.split("\n\n")
        }
        self.monkeys_names = [str(a) for a in range(len(self.monkeys))]
        self.inspected = defaultdict(int)
        for monkey in self.monkeys.values():
            self.max_number *= monkey.divisible_by

    def startthrowing(self):
        monkey_out = defaultdict(lambda: list())
        for name in self.monkeys_names:
            for worry in self.monkeys[name].start_items:
                self.inspected[name] += 1

                out_worry = self.monkeys[name].apply(worry)
                if out_worry % self.monkeys[name].divisible_by == 0:
                    out_monkey = self.monkeys[name].if_true
                else:
                    out_monkey = self.monkeys[name].if_false
                self.monkeys[out_monkey].start_items.append(out_worry % self.max_number)
            self.monkeys[name].start_items = list()
        # print(monkey_out)

    def monkeybusiness(self, times=10000):
        for _ in range(times):
            self.startthrowing()
        print(self.inspected)
        # print(self.monkeys)
        thrown = list(self.inspected.values())
        thrown.sort()
        return thrown[-2] * thrown[-1]


test_monkeys = MonkeyGame(RAWTESTDATA)

print(test_monkeys)

print("monkey business test:", test_monkeys.monkeybusiness())

monkeys = MonkeyGame(RAWDATA)

print(monkeys)

print("monkey business:", monkeys.monkeybusiness())
