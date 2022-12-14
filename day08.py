from rich import print, traceback

traceback.install()
from pathlib import Path
from dataclasses import dataclass, field
import numpy as np

RAWTESTDATA = """\
30373
25512
65332
33549
35390"""

print(RAWTESTDATA)


@dataclass
class MatrixTower:
    n_row: int
    n_col: int
    matrix: list[list[int]]
    visible: int = 0

    def __init__(self, rawdata) -> None:
        self.matrix = []
        for line in rawdata.splitlines():
            self.matrix.append([int(char) for char in line])
        self.n_row = len(self.matrix)
        self.n_col = len(self.matrix[0])

    def find_visible(self):
        self.visible = self.n_col * 2 + self.n_row * 2 - 4
        # right visible
        print(self.matrix)
        vis_set = set()
        for irow, row in enumerate(self.matrix[1 : (self.n_row - 1)]):
            for icol, (val, view) in enumerate(
                zip(row[1 : (self.n_row - 1)], self.cumlativemax(row))
            ):
                if view < val:
                    print(val, view)
                    vis_set.add((irow + 1, icol + 1, val))

        for irow, row in enumerate(self.matrix[1 : (self.n_row - 1)]):
            row = row[::-1]
            for icol, (val, view) in enumerate(
                zip(row[1 : (self.n_row - 1)], self.cumlativemax(row))
            ):
                if view < val:
                    print(val, view)
                    vis_set.add((irow + 1, self.n_col - icol - 2, val))

        mat_t = self.transpose(self.matrix)
        print(self.matrix)
        print(mat_t)
        for irow, row in enumerate(mat_t[1 : (self.n_row - 1)]):
            for icol, (val, view) in enumerate(
                zip(row[1 : (self.n_row - 1)], self.cumlativemax(row))
            ):
                if view < val:
                    print(val, view)
                    vis_set.add((icol + 1, irow + 1, val))

        for irow, row in enumerate(mat_t[1 : (self.n_row - 1)]):
            row = row[::-1]
            for icol, (val, view) in enumerate(
                zip(row[1 : (self.n_row - 1)], self.cumlativemax(row))
            ):
                if view < val:
                    print(val, view)
                    vis_set.add((self.n_col - icol - 2, irow + 1, val))

        print(vis_set)
        return self.visible + len(vis_set)

    def find_score(self):
        score = [[1 for _ in row] for row in self.matrix]
        S = self.find_h_score
        F = self.flip
        T = self.transpose

        score = S(self.matrix, score)
        score = F(S(F(self.matrix), F(score)))
        score = T(S(T(self.matrix), T(score)))
        score = T(F(S(F(T(self.matrix)), F(T(score)))))
        print(score)
        return max(max(line) for line in score)

    @staticmethod
    def flip(matrix):
        out = []
        for row in matrix:
            out.append(row[::-1])
        return out

    @staticmethod
    def find_h_score(mat, sco):
        # print(f"find score {mat=}{sco=}")
        for irow, row in enumerate(mat[1 : (len(mat) - 1)]):
            for j in range(1, len(row) - 1):
                # print("---")
                val = row[j]
                before = row[:j]
                # print("before", before, val)

                for ib, b in enumerate(before[::-1]):
                    if b >= val:
                        # print(f"{b=}, {val=}, {ib=}", "found a view")
                        sco[irow + 1][j] *= ib + 1
                        break
                    if ib == len(before) - 1:
                        # print("at end")
                        # print(f"{b=}, {val=}, {ib=}", "found a view")
                        sco[irow + 1][j] *= ib + 1

        # print(f"in_h{sco=}")
        return sco

    @staticmethod
    def transpose(mat):
        array = np.array(mat)
        transposed_array = array.T
        return transposed_array.tolist()

    @staticmethod
    def cumlativemax(row):
        out = []
        maxsofar = -99
        for num in row:
            if num >= maxsofar:
                maxsofar = num
            out.append(maxsofar)
        return out


my_test = MatrixTower(RAWTESTDATA)

# print(MatrixTower.cumlativemax([3, 6, 5, 4, 9]))

# print(f"{my_test.find_visible()}")

print("max_score:", my_test.find_score())
RAWDATA = Path("day08.txt").read_text()
matmat = MatrixTower(RAWDATA)
# print(f"{matmat.find_visible()}")
print(f"{matmat.find_score()}")


# print((my_test.flip([[1, 2, 3, 4], [2, 3, 4, 5]])))
