import copy

class Traktor_path():
    def __init__(self, matrix):
        self.matrix = matrix

        # Координаты входа [2,0], координаты выхода [7,0]. В которой 1 - это стена, 0 - это путь.
        # координаты входа
        pozIn, pozOut = (10, 1), (0, 9)
        # pozIn, pozOut = (3, 1), (0, 5)

        path = transform_lab(self.matrix)
        eval = evalution_lab(path)
        eval_final = eval * 2
        print(eval, eval_final)
        for i in path:
            for line in i:
                print("{:^3}".format(line), end=",")
            print("")
        print("-----")
        print("-----")
        path[pozIn[0]][pozIn[1]] = 1
        s_w = 1
        iter_num = 0
        while eval != eval_final and iter_num < 5:
            pozOuts = next_finish2(path, pozIn)
            iter_num += 1
            eval = evalution_lab(path)
            print(iter_num, " iteration")
            print(eval, eval_final, pozOuts, s_w)
            variants = []
            for pos in pozOuts:
                path2 = found(path, pos, s_w)
                for p in path2:
                    if evalution_lab(p) <= eval:
                        variants.append([evalution_lab(p), pos, p])

            variants = sorted(variants, key=lambda x: x[0])
            print("////////////////////")
            for v in variants:
                print(v[0], v[1])
                print("\n".join(",".join("{:^3}".format(line) for line in pp) for pp in v[2]))
            if variants:
                path = copy.deepcopy(variants[0][2])
                pos = variants[0][1]

                print("-----")
                print("-----")
                path, s_w = transform_lab2(path)
                print("Final, goto", pos)
                for i in path:
                    for line in i:
                        print("{:^3}".format(line), end=",")
                    print("")
                print("-----")
                print("-----")
            else:
                break
        turns, out = get_finish(path)
        result = printPath(path, out)
        print(result)


# общий массив всех вариантов
### сохраняем все варианты, рекурсивно от каждого вызываем следующий заход
###


def found(pathArr_0, finPoint, start_w=1):
    pathArr = copy.deepcopy(pathArr_0)
    weight = start_w
    paths = []
    # pathArr = [[0 if x == 1000 else x for x in y] for y in pathArr]
    xy = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    for i in range(len(pathArr) * len(pathArr[0])):
        weight += 1
        for y in range(len(pathArr)):
            for x in range(len(pathArr[y])):
                if pathArr[y][x] == (weight - 1):
                    for x1, y1 in xy:
                        try:
                            if pathArr[y + y1][x + x1] == -1:
                                pathArr[y + y1][x + x1] -= 1
                        except Exception:
                            pass
                    # добавить приоритеты направлений
                    move = []
                    try:
                        if x <= finPoint[1]:
                            move.append((x < (len(pathArr[y]) - 1)
                                         and pathArr[y][x + 1] == 0, y, x + 1))
                            move.append((x < (len(pathArr[y]) - 1)
                                         and y<(len(pathArr) - 1)
                                         and pathArr[y][x + 1] <= -1
                                         and pathArr[y + 1][x] == 0, y + 1, x))
                            move.append((x < (len(pathArr[y]) - 1)
                                         and y>0
                                         and pathArr[y][x + 1] <= -1
                                         and pathArr[y - 1][x] == 0, y - 1, x))
                        if x > finPoint[1]:
                            move.append((x > 0 and pathArr[y][x - 1] == 0, y, x - 1))
                            move.append((x > 0 and pathArr[y][x - 1] <= -1
                                         and y<(len(pathArr) - 1)
                                         and pathArr[y + 1][x] == 0, y + 1, x))
                            move.append((x > 0 and pathArr[y][x - 1] <= -1
                                         and y > 0
                                         and pathArr[y - 1][x] == 0, y - 1, x))
                        if y <= finPoint[0]:
                            move.append((y < (len(pathArr) - 1) and pathArr[y + 1][x] == 0, y + 1, x))
                            move.append((y < (len(pathArr) - 1)
                                         and pathArr[y + 1][x] <= -1
                                         and x>0
                                         and pathArr[y][x - 1] == 0, y, x - 1))
                            move.append((y < (len(pathArr) - 1)
                                         and pathArr[y + 1][x] <= -1
                                         and x<(len(pathArr[y]) - 1)
                                         and pathArr[y][x + 1] == 0, y, x + 1))
                        if y > finPoint[0]:
                            move.append((y > 0 and pathArr[y - 1][x] == 0, y - 1, x))
                            move.append((y > 0 and pathArr[y - 1][x] <= -1
                                         and pathArr[y][x - 1] == 0, y, x - 1))
                            move.append((y > 0 and pathArr[y - 1][x] <= -1
                                         and pathArr[y][x + 1] == 0, y, x + 1))
                    except Exception:
                        pass
                    if not move:
                        move = [(y > 0 and pathArr[y - 1][x] == 0, y - 1, x),
                                (y < (len(pathArr) - 1) and pathArr[y + 1][x] == 0, y + 1, x),
                                (x > 0 and pathArr[y][x - 1] == 0, y, x - 1),
                                (x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == 0, y, x + 1)]
                    v = 0
                    for m, yy, xx in set(move):
                        if m:
                            if v > 0:
                                pathArr2 = copy.deepcopy(pathArr)
                                pathArr2[yy][xx] = weight
                                paths.extend(found(pathArr2, finPoint, start_w=weight))
                            else:

                                pathArr[yy][xx] = weight
                                v += 1
                                break


    paths.append(copy.deepcopy(pathArr))

    return paths


def printPath(pathArr, finPoint):
    y = finPoint[0]
    x = finPoint[1]
    weight = pathArr[y][x]
    result = list(range(weight))
    while (weight):
        weight -= 1
        if y > 0 and pathArr[y - 1][x] == weight:
            y -= 1
            result[weight] = 'down'
        elif y < (len(pathArr) - 1) and pathArr[y + 1][x] == weight:
            result[weight] = 'up'
            y += 1
        elif x > 0 and pathArr[y][x - 1] == weight:
            result[weight] = 'right'
            x -= 1
        elif x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == weight:
            result[weight] = 'left'
            x += 1

    return result[1:]


def transform_lab(labirint):
    for i in range(len(labirint)):
        for j in range(len(labirint[i])):

            if labirint[i][j] != 0:
                labirint[i][j] = -1
    return labirint


def transform_lab2(labirint):
    for i in range(len(labirint)):
        for j in range(len(labirint[i])):

            if labirint[i][j] > 0:
                # labirint[i][j] += 1
                pass
    return labirint, max(max(i for i in j) for j in labirint)


def evalution_lab(labirint):
    eval = sum([sum([i for i in j if i < 0]) for j in labirint])
    return eval


def next_finish(labirint, start_pos):
    y, x = start_pos
    min_x, min_y = len(labirint), len(labirint[0])
    f_x, f_y = len(labirint), len(labirint[0])
    for i in range(len(labirint)):
        for j in range(len(labirint[i])):
            if labirint[i][j] == -1:
                min_x_, min_y_ = abs(y - i), abs(x - j)
                if min_x_ + min_y_ <= min_x + min_y:
                    min_x, min_y = min_x_, min_y_
                    f_x, f_y = j, i
    s_f = + x
    if (y < len(labirint) / 2 or x < len(labirint) / 2):
        xy = [(1, 0), (0, 1)]
    else:

        xy = [(-1, 0), (0, -1)]

    for dx, dy in xy:
        try:
            while (labirint[f_y + dy][f_x + dx] == -1) and f_y + dy >= 0 and f_x + dx >= 0:
                f_y = f_y + dy
                f_x = f_x + dx
                f_x = f_x + dx
                print(f_y, f_x)
        except Exception:
            print(f_y, f_x)
    return f_y, f_x


def check_edge(point, lab):
    y, x = point
    r = 0
    mass = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    for mx, my in mass:
        if y + my >= 0 and y + my < len(lab) and x + mx >= 0 and x + mx < len(lab[0]):
            if lab[y + my][x + mx] == -1:
                r += 1
    if r <= 1:
        return True
    return False


def next_finish2(labirint, start_pos):
    y0, x0 = start_pos

    mass_edge = []
    delta = 3
    for i in range(max(y0 - delta, 0), min(y0 + delta, len(labirint))):
        for j in range(0, len(labirint[i])):
            if labirint[i][j] == -1:
                if check_edge((i, j), labirint):
                    mass_edge.append([i, j])

    for i in range(0, len(labirint)):
        for j in range(max(x0 - delta, 0), min(x0 + delta, len(labirint[i]))):
            if labirint[i][j] == -1:
                if check_edge((i, j), labirint) and [i, j] not in mass_edge:
                    mass_edge.append([i, j])
    mass_edge = sorted(mass_edge, key=lambda x: (abs(x[1] - x0), abs(x[0] - y0)))

    return mass_edge

def get_finish(labirint):
    y,x = 0,0
    value = 0
    for i in range(len(labirint)):
        for j in range(len(labirint[i])):
            if labirint[i][j]>value:
                value = labirint[i][j]
                y,x = i,j
    return value, (y,x)

def main():
    # Выход из лабиринта .Волновой алгоритм
    labirint = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    #labirint = [
     #   [1, 0, 0, 0, 1, 0],
    #    [1, 0, 1, 0, 1, 0],
    #    [1, 0, 1, 0, 1, 0],
   #     [1, 0, 1, 0, 0, 0],
   # ]
    # Координаты входа [2,0], координаты выхода [7,0]. В которой 1 - это стена, 0 - это путь.
    # координаты входа
    pozIn, pozOut = (10, 1), (0, 9)
   # pozIn, pozOut = (3, 1), (0, 5)

    path = transform_lab(labirint)
    eval = evalution_lab(path)
    eval_final = eval * 2
    print(eval, eval_final)
    for i in path:
        for line in i:
            print("{:^3}".format(line), end=",")
        print("")
    print("-----")
    print("-----")
    path[pozIn[0]][pozIn[1]] = 1
    s_w = 1
    iter_num = 0
    while eval!=eval_final and iter_num < 5:
        pozOuts = next_finish2(path, pozIn)
        iter_num += 1
        eval = evalution_lab(path)
        print(iter_num, " iteration")
        print(eval, eval_final, pozOuts, s_w)
        variants = []
        for pos in pozOuts:
            path2 = found(path, pos, s_w)
            for p in path2:
                if evalution_lab(p)<= eval:
                    variants.append([evalution_lab(p), pos, p])

        variants = sorted(variants, key=lambda x: x[0])
        print("////////////////////")
        for v in variants:
            print(v[0],v[1])
            print("\n".join(",".join("{:^3}".format(line) for line in pp) for pp in v[2]))
        if variants:
            path = copy.deepcopy(variants[0][2])
            pos = variants[0][1]

            print("-----")
            print("-----")
            path, s_w = transform_lab2(path)
            print("Final, goto", pos)
            for i in path:
                for line in i:
                    print("{:^3}".format(line), end=",")
                print("")
            print("-----")
            print("-----")
        else:
            break
    turns, out = get_finish(path)
    result = printPath(path, out)
    print(result)


if __name__ == '__main__':
    main()
