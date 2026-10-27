from parser import parse_function as parse
from ordinary import euler_solve as ode

f = parse()

t0 = float(input('Starting t value (t0): '))
y0 = float(input('Starting y value (y0): '))
t_end = float(input("Desired end value (t_end): "))
h = float(input('Step size h: '))

ts, ys = ode(f, t0, y0, t_end,h)

print(f'approximately, y({ts[-1]}) is {ys[-1]}')