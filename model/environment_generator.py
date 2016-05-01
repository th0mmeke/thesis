import random

GENERATIONS = 500


def get_ar_timeseries(theta, sd):
    value = 0
    t = random.randint(-100, 0)  # initial burn-in period
    for i in range(t, GENERATIONS):
        value = theta * value + random.gauss(0, sd)  # error term with mean = 0 and sd = sd
        if i >= 0:
            yield value

MAX_SD = 0.2
with open("environments.csv", "w") as f:
    for i in range(500):
        theta, sd = random.uniform(-MAX_SD, MAX_SD), random.uniform(0, MAX_SD)
        print(theta)
        # ts = [x for x in get_ar_timeseries(theta, sd)]
        # f.write(str(theta) + "," + str(sd) + "," + ",".join([str(x) for x in ts]) + "\n")





