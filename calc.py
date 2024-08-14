from common import LOGGING, DATES, NUM_DATES, NUM_TEAMS, CHAT_PATH, GRAPH_PATH
import numpy as np


def scale(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def interp(data: list, days: list) -> list:
    days_with_data = []

    # data = [7.0, 5.0, None, 1.0, None, None, None,
    #         9.0, 6.0, None, None, None, None, 7.0]
    interp_data = []
    for date in DATES:
        if date in days:
            days_with_data.append(True)
        else:
            days_with_data.append(False)
            pos = DATES.index(date)
            data.insert(pos, None)

    i = 0
    while i < len(days_with_data):
        dd = days_with_data[i]
        if (i == 0 or i == len(days_with_data) - 1) and dd == 0:
            raise ValueError('Cannot interpolate because of undefined bounds')

        if dd == False:
            # Find index bounds to lerp
            first = i - 1
            remaining = days_with_data[i:]
            last = remaining.index(True) + i
            n_steps = last - first - 1

            # Compute lerp
            # 2 to account for start and end, then cut off start and end
            pts = np.linspace(data[first], data[last],
                              n_steps + 2)[1:n_steps + 1]
            interp_data += list(pts)

            # Set i to last index
            i = last - 1

        else:
            interp_data += [data[i]]
        i += 1
    return interp_data
