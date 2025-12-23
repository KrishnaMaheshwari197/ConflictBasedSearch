import argparse
import glob
from pathlib import Path

from CBS_highlevel import CBSSolver
from Random_map import random_map
from Astar import get_sum_of_cost
from Animation import Animation

SOLVER = "CBS"


def print_mapf_instance(my_map, starts, goals):
    print('Start locations')
    print_locations(my_map, starts)
    print('Goal locations')
    print_locations(my_map, goals)


def print_locations(my_map, locations):
    starts_map = [[-1 for _ in range(len(my_map[0]))] for _ in range(len(my_map))]
    for i in range(len(locations)):
        starts_map[locations[i][0]][locations[i][1]] = i
    to_print = ''
    for x in range(len(my_map)):
        for y in range(len(my_map[0])):
            if starts_map[x][y] >= 0:
                to_print += str(starts_map[x][y]) + ' '
            elif my_map[x][y]:
                to_print += '@ '
            else:
                to_print += '. '
        to_print += '\n'
    print(to_print)


def import_mapf_instance(filename):
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    f = open(filename, 'r')
    line = f.readline()
    rows, columns = [int(x) for x in line.split(' ')]
    rows = int(rows)
    columns = int(columns)
    my_map = []
    for r in range(rows):
        line = f.readline()
        my_map.append([])
        for cell in line:
            if cell == '@':
                my_map[-1].append(True)
            elif cell == '.':
                my_map[-1].append(False)
    line = f.readline()
    num_agents = int(line)
    starts = []
    goals = []
    for a in range(num_agents):
        line = f.readline()
        sx, sy, gx, gy = [int(x) for x in line.split(' ')]
        starts.append((sx, sy))
        goals.append((gx, gy))
    f.close()
    return my_map, starts, goals


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs various MAPF algorithms')
    parser.add_argument('--instance', type=str, default=None,
                        help='The name of the instance file(s)')
    parser.add_argument('--random', action='store_true', default=False,
                        help='Use a random map with auto-genereted agents (see function random_map)')
    parser.add_argument('--batch', action='store_true', default=False,
                        help='Use batch output instead of animation')
    parser.add_argument('--disjoint', action='store_true', default=False,
                        help='Use the disjoint splitting')

    args = parser.parse_args()

    result_file = open("results.csv", "w", buffering=1)
    files = ["random.generated"] if args.random else glob.glob(args.instance)
    for file in files:
        print("***Import an instance***")
        my_map, starts, goals = random_map(8, 8, 6, .1) if args.random else import_mapf_instance(file)
        print_mapf_instance(my_map, starts, goals)
        print("Performing CBS")
        cbs = CBSSolver(my_map, starts, goals)
        paths = cbs.find_solution(args.disjoint)
        cost = get_sum_of_cost(paths)
        result_file.write("{},{}\n".format(file, cost))

        if not args.batch:
                animation = Animation(my_map, starts, goals, paths)
                animation.show()
    print("Execution Complete")
    result_file.close()
