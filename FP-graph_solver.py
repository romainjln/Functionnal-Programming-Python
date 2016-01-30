import unittest
from functools import reduce


# Iterates function f on x until the result verifies the condition p.
def loop(p, f, x):
    return x if p(x) else loop(p, f, f(x))


# Returns True if set s contains an element x such that p(x) = True.
def exists(p, l):
    return any(map(lambda x: x if p(x) else None, l))


# Returns x, first element of a set/list such as p(x)=True. Returns None if such x doesn't exist.
def find(p, l):
    return next((x for x in l if p(x)), None)


# Defines the relation "near". Returns a list of integers close to x: [x-2,x-1,x,x+1,x+2].
def near(integer):
    return [integer - 2, integer - 1, integer, integer + 1, integer + 2]


# Applies the relation rel to all the elements of list/set l via a reduction
# THE USE OF SETS HERE ALLOWS THE CODE TO RUN MUCH FASTER
def flat_map(rel, l):
    return set(reduce(lambda x, y: x + rel(y), l, []))


# Returns a function that apply relation rel applied N times
# If N <= 1 you have rel applied one time only.
def iterate(rel, n):
    return reduce(lambda f, g: lambda y: f(g(y)), [lambda l: flat_map(rel, l)] * max(1, (n - 1)) + [lambda x: rel(x)])


# Go through the graph by applying the relation rel from x until it finds y in the list
# such as p(y)=True. Returns this element y.
def solve(rel, p, x):
    return find(p, loop(lambda w: exists(p, w), lambda y: flat_map(rel, y), [x]))


# Go through the graph by applying the relation rel from x until it finds y in the list
# such as p(y)=True. Returns the path from x to y through the relation rel.
# For example, solve_path(near, lambda x: x == 12, 0) should return [0, 2, 4, 6, 8, 10, 12]
def solve_path(rel, p, x):
    a = solve(rel, p, x)
    return [a] if (a == x) else solve_path(rel, lambda y: True if a in rel(y) else False, x) + [a]


# Class that represents a state/node in the 3x3 jigsaw game.
# grid: ordered list of the numbers in the game (9 elements).
# pos0: index of the 0 (missing piece) in the array
# posV: vertical position of the 0 (in [0:2])
# posH: horizontal position of the 0 (in [0:2])
class JigsawState:
    # initiates an instance of jigsawState
    def __init__(self, grid):
        self.grid = grid
        self.pos0 = grid.index(0)
        self.posV = grid.index(0) // 3
        self.posH = grid.index(0) % 3

    def play(self, x, y):
        new_jigsaw = JigsawState([item for item in self.grid])
        previous_value = new_jigsaw.grid[x * 3 + y]
        new_jigsaw.grid[x * 3 + y] = 0
        new_jigsaw.grid[new_jigsaw.pos0] = previous_value
        new_jigsaw.pos0 = x * 3 + y
        return new_jigsaw

    def __getitem__(self, item):
        return [x for x in self.grid[3 * item: 3 * (item + 1)]]

    def __eq__(self, other):
        return self.grid == other.grid

    # Hash value, in order to use sets
    def __hash__(self):
        return hash(tuple(self.grid))

    # To print a jigsaw state in a readable way
    def __repr__(self):
        line1 = "[" + str(self.grid[0]) + "," + str(self.grid[1]) + "," + str(self.grid[2]) + "]"
        line2 = "[" + str(self.grid[3]) + "," + str(self.grid[4]) + "," + str(self.grid[5]) + "]"
        line3 = "[" + str(self.grid[6]) + "," + str(self.grid[7]) + "," + str(self.grid[8]) + "]"
        return line1 + "\n" + line2 + "\n" + line3


# Returns the neighbor states for the state "jigState", in the jigsaw game
def rel_jig(jig_state):
    neighbors = []
    if jig_state.posH < 2:
        neighbors.append(jig_state.play(jig_state.posV, jig_state.posH + 1))
    if jig_state.posH > 0:
        neighbors.append(jig_state.play(jig_state.posV, jig_state.posH - 1))
    if jig_state.posV < 2:
        neighbors.append(jig_state.play(jig_state.posV + 1, jig_state.posH))
    if jig_state.posV > 0:
        neighbors.append(jig_state.play(jig_state.posV - 1, jig_state.posH))
    return neighbors


# For a state jigState, in a jigsaw game, returns True if the game is won (numbers sorted and 0 at the end)
def jigsaw_won(jig_state):
    return jig_state.grid == [1, 2, 3, 4, 5, 6, 7, 8, 0]


# Unit tests for all previous methods and classes
class GraphSolverTests(unittest.TestCase):
    def test_print_the_step_of_solve_path_jigsaw(self):
        start = JigsawState([1, 0, 3, 4, 2, 5, 7, 8, 6])
        for step in solve_path(rel_jig, jigsaw_won, start):
            print step
            print "\n"

    def test_loop_should_loop_on_function_till_the_condition_is_verified(self):
        assert (loop(lambda x: True if x == 16 else False, lambda x: pow(x, 2), 2) == 16)

    def test_exists_should_check_if_an_element_verify_the_condition_in_an_iterable(self):
        def p(x): return True if x == 16 else False
        s1 = {1, 2, 3, 4}
        s2 = {1, 16, 20, 22}

        assert (exists(p, s1) == False)
        assert (exists(p, s2) == True)

    def test_find_should_return_the_first_element_verifying_the_condition_or_none(self):
        def p(x): return True if x > 16 else False
        s1 = {1, 2, 3, 4}
        s2 = {1, 16, 20, 22}

        assert (find(p, s1) is None)
        assert (find(p, s2) == 20)

    def test_near(self):
        assert (near(6) == [4, 5, 6, 7, 8])

    def test_flat_map_should_apply_a_relation_to_all_the_element_of_an_iterable(self):
        assert (flat_map(near, [2, 18, 25]) == {0, 1, 2, 3, 4, 16, 17, 18, 19, 20, 23, 24, 25, 26, 27})
        assert (flat_map(near, [2, 3, 4]) == {0, 1, 2, 3, 4, 5, 6})

    def test_iterate_should_return_a_function_which_represent_the_nth_iteration_of_a_relation(self):
        assert (iterate(near, 3)(6) == {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12})

    def test_solve_return_the_first_element_verifying_p_in_the_graph_build_from_x(self):
        assert (solve(near, lambda x: x == 12, 0) == 12)
        assert (solve(near, lambda x: x > 16, -10) == 17)
        assert (solve(near, lambda x: x < 12, -10) == -10)

    def test_solve_path_should_return_the_whole_path_of_the_graph_from_x_to_the_element_verifying_p(self):
        assert (solve_path(near, lambda x: x == 12, 0) == [0, 2, 4, 6, 8, 10, 12])
        assert (solve_path(near, lambda x: x == 12, -16) == [-16, -14, -12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12])

    def test_solve_path_can_scale(self):
        print(solve_path(near, lambda x: x == 200, -16))
