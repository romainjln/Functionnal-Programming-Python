from functools import reduce


def loop(p, f, x):
    return x if p(x) else loop(p, f, f(x))


def exists(p, l):
    return any(map(lambda x: x if p(x) else None, l))


def find(p, l):
    return next((x for x in l if p(x)), None)


def near(integer):
    return [integer - 2, integer - 1, integer, integer + 1, integer + 2]


def flat_map(rel, l):
    return set(reduce(lambda x, y: x + rel(y), l, []))


def iterate(rel, n):
    return reduce(lambda f, g: lambda y: f(g(y)), [lambda l: flat_map(rel, l)] * (n - 1) + [lambda x: rel(x)])


def solve(rel, p, x):
    return find(p, loop(lambda w: exists(p, w), lambda y: flat_map(rel, y), [x]))


def solve_path(rel, p, x):
    a = solve(rel, p, x)
    return [a] if (a == x) else [a] + solve_path(rel, lambda y: True if a in rel(y) else False, x)
