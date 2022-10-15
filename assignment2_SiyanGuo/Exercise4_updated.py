import multiprocessing
import numpy as np
import time

from scipy.stats import nakagami

def alg2(data):
    if len(data) <= 1:
        return data
    else:
        split = len(data) // 2
        left = iter(alg2(data[:split]))
        right = iter(alg2(data[split:]))
        result = []
        # note: this takes the top items off the left and right piles
        left_top = next(left)
        right_top = next(right)
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

if __name__ == "__main__":
    ns = np.logspace(3,6, dtype = int)
    times = []
    time2s=[]
    for n in ns:
        data = data1(n)
        left = data[:len(data)//2]
        right = data[len(data)//2:]
        start_time = time.perf_counter()
        with multiprocessing.Pool(2) as worker:
            results = worker.map(alg2,[left,right])
        stop_time = time.perf_counter()
        times.append(stop_time-start_time)
        start2=time.perf_counter()
        alg2(data1(n))
        end2=time.perf_counter()
        time2=end2-start2
        time2s.append(time2)
        

    import plotnine as p9
    import pandas as pd
    plotdata = pd.DataFrame({'size':list(ns)*2,'time':times+time2s,'label':['parallel']*50+['unparallel']*50})
    plot=p9.ggplot(plotdata,p9.aes(x='size',y='time',color='label'))+p9.geom_line()
    p9.ggsave(plot,'runtime_amy.png')
