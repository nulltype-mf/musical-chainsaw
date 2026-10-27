import math

#dy/dt = f(y,t). h = step size

def euler_solve(f, t0, y0, t_end, h):

    ts = [t0]
    ys = [y0]
    t = t0
    y = y0

    while t < float(t_end):
        if t + h > t_end:
            h = t_end - t
        y = y + h*(f(t, y))
        t = t + h

        ts.append(t)
        ys.append(y)

    return ts, ys