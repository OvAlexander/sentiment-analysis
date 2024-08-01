import numpy as np

days_with_data = [True, True, False, True, False, False,
                  False, True, True, False, False, False, False, True]

data = [7.0, 5.0, None, 1.0, None, None, None,
        9.0, 6.0, None, None, None, None, 7.0]
interp_data = []

i = 0
while i < len(days_with_data):
    dd = days_with_data[i]
    if (i == 0 or i == len(days_with_data) - 1) and dd == 0:
        raise Exception('Cannot interpolate because of undefined bounds')

    if dd == False:
        # Find index bounds to lerp
        first = i - 1
        remaining = days_with_data[i:]
        last = remaining.index(True) + i
        n_steps = last - first - 1

        # Compute lerp
        # 2 to account for start and end, then cut off start and end
        pts = np.linspace(data[first], data[last], n_steps + 2)[1:n_steps + 1]
        print(pts)
        interp_data += list(pts)

        # Set i to last index
        i = last - 1

    else:
        interp_data += [data[i]]

    i += 1

print(interp_data)
