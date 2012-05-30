#!/usr/bin/env python

def circle(x0, y0, radius):
    octants = [
                'x0 + y, y0 + x',  # Octant 1
                'x0 + x, y0 + y',  # Octant 2
                'x0 - x, y0 + y',  # Octant 3
                'x0 - y, y0 + x',  # Octant 4
                'x0 - y, y0 - x',  # Octant 5
                'x0 - x, y0 - y',  # Octant 6
                'x0 + x, y0 - y',  # Octant 7
                'x0 + y, y0 - x',  # Octant 8
              ]

    f = 1 - radius
    ddf_x = 1
    ddf_y = -2 * radius
    x = 0
    y = radius

    for eval_formula in octants:
        while x < y:
            if f >= 0: 
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x

        yield eval(eval_formula)
