import sys

inp = sys.stdin.read()

grid = [[int(x) for x in y] for y in inp.split()]
nrow = len(grid)
ncol = len(grid[0])
hidden = [[True for _ in range(ncol)] for _ in range(nrow)]
scenic_score = [[1 for _ in range(ncol)] for _ in range(nrow)]


def vis_distance(height, in_front):
    view_distance = 0
    hidden = False
    for next_height in in_front:
        view_distance += 1
        if next_height >= height:
            hidden = True
            break
    return hidden, view_distance


for i in range(ncol):
    for j in range(nrow):
        for h, sc in [
            vis_distance(grid[j][i], [grid[jj][i] for jj in range(j + 1, nrow)]),
            vis_distance(grid[j][i], [grid[j][ii] for ii in range(i + 1, ncol)]),
            vis_distance(grid[j][i], [grid[jj][i] for jj in range(j - 1, -1, -1)]),
            vis_distance(grid[j][i], [grid[j][ii] for ii in range(i - 1, -1, -1)]),
        ]:
            hidden[j][i] &= h
            scenic_score[j][i] *= sc

print(sum(not v for hlist in hidden for v in hlist))
print(max(map(max, scenic_score)))
