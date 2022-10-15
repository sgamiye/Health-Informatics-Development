from multiprocessing import Pool
import numpy as np

def para_alg2(data):
    if len(data) <= 1:
        return data
    else:
        split = len(data) // 2
        with Pool(processes=2) as pool:
            left, right = pool.map(alg2, [data[:split], data[split:]])
        return merge(iter(left), iter(right))


def alg2(data):
    if len(data) <= 1:
        return data
    else:
        split = len(data) // 2
        left = iter(alg2(data[:split]))
        right = iter(alg2(data[split:]))
        # note: this takes the top items off the left and right piles
        return merge(left, right)

def merge(left, right):
    left_top = next(left)
    right_top = next(right)
    result = []
    while True:
        if left_top < right_top:
            result.append(left_top)
            try:
                left_top = next(left)
            except StopIteration:
                # nothing remains on the left; add the right + return
                return result + [right_top] + list(right)
        else:
            result.append(right_top)
            try:
                right_top = next(right)
            except StopIteration:
                # nothing remains on the right; add the left + return
                return result + [left_top] + list(left)

def data1(n, sigma=10, rho=28, beta=8/3, dt=0.01, x=1, y=1, z=1):
    import numpy
    state = numpy.array([x, y, z], dtype=float)
    result = []
    for _ in range(n):
        x, y, z = state
        state += dt * numpy.array([
            sigma * (y - x),
            x * (rho - z) - y,
            x * y - beta * z
        ])
        result.append(float(state[0] + 30))
    return result

print(para_alg2([13, 566, 234, 36, 2, 8, 687]))

if __name__ == "__main__":
    ns = np.logspace(0,5, dtype=int)
    for n in ns:
        para_alg2(data1(n))