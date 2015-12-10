import model
import random
import os



def my_get_offspring(x):
    '''
    Correlated correlation values
    Reproduce only if pass P_REPRODUCE
    Random number of offspring in range 0..N_OFFSPRING
    '''
    if model.get_random_boolean(model.P_REPRODUCE, x.fitness):
        return [model.Element(x.fitness, model.derive(x.correlation, x.correlation)) for i in range(random.randint(*model.N_OFFSPRING))]
    else:
        return []

model.P_REPRODUCE = 1.0 # All parents reproduce
model.P_SURVIVE = 0.0 # No parents survive
model.N_OFFSPRING = (0,5)
model.derive = model.gaussian_derive
model.get_offspring = my_get_offspring

def init_population(n):
    return [model.Element() for x in range(0,n)]

print("{}".format(os.path.basename(__file__)))

for repeat in range(0,30):
    model.run(init_population(1000), 20)
