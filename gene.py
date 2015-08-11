from random import randint, sample as rsample
from numpy.random import geometric
from math import floor
from copy import deepcopy

# TODO: Include variable string lengths


class Population:

    def __init__(self, size = 10, correct = ' '):
        self.corr = [ord(c) for c in correct]
        self.pop = self.populate(size)
        self.rate = {'kill': 0.3, 'cross': 0.35, 'mutate': 0.4, 'mate': 0.7, 'maxpos': 3}

    def populate(self, size):
        "Return a randomly generated initial population. "
        return [self.sample(len(self.corr)) for j in range(size)]

    def sample(self, n = 1):
        '''Return a list of size n (sampled with replacement from ASCII 
        range 32-126). '''
        return [randint(97, 122) for i in range(n)] 
    
    def fitness(self, individual):
        '''Return a metric representing the fitness of the given individual
        based on its similarity to the correct string.
        '''
        # Fuck yes this shit scales!
        return sum([ i == j for i,j in zip(individual, self.corr)])

    def kill(self, indices):
       '''Kill the weakest in the population. Indices are sorted in 
       descending order. '''
       for i in indices:
           del self.pop[i]
           #print("Individual {0} killed.".format(i))

    def convert(self, nums):
        "Convert list of nums back into a string via ASCII. "
        return ''.join([chr(n) for n in nums])

    def display(self):
        '''Print the current members of the population. '''
        print('Correct output'.ljust(17) + ': ' + self.convert(self.corr))
        for c, i in enumerate(self.pop):
            label = 'Individual {0:06d}'.format(c)
            print(label + ': ' + self.convert(i))

    def crossover(self, parents):
        '''Create a new baby! The argument parents is a two-element
        list containing the index of the respective parent in the 
        population. '''
        #print('Individual {0:06d} and {1:06d} had a baby'.format(parents[0], parents[1]))
        return [ self.pop[parents[randint(0,1)]][i] for i in range(len(self.corr))]

    def mutate(self, index):
        'Mutate position(s) for an individual given their index. '
        num_pos = randint(1, self.rate['maxpos'])
        
        pos = rsample([i for i in range(len(self.corr))], num_pos)
        
        for p in pos:
            self.pop[index][p] = self.sample()[0]

        #print('Individual {0:06d} had a mutation at pos {1}'.format(index, pos))


    def run(self, gen = 100):
        '''Run the natural selection simulation for up to "gen" generations,
        or until an individual exactly matches the correct output. 
        
        The generation loop works as follows:

                1. Evaluate every individual's fitness
                2. Rank them
                3. Check if top individual matches correct output.
                        If so, stop
                        Else, continue
                4. Determine number of individuals to kill
                5. Using 2 + 3, kill off the weakest indivduals
                6. Crossover: Replenish the dead + add more
                7. Mutation
                8. Repeat
        '''
        corr = deepcopy(self.corr)
        pop = deepcopy(self.pop)

        for i in range(1, gen + 1):
           
            evaluate = [ self.fitness(i) for i in self.pop]

            ranked = sorted([(score, i) for i, score in enumerate(evaluate)], reverse = True)
        
            top, success = ranked[0][0], len(self.corr)

            if i % 10 == 0:
                print('----------- Generation {0} -----------'.format(i))
                print('Correct   : {0}'.format(self.convert(self.corr)))
                print('Top ranked: {0}'.format(self.convert(self.pop[ranked[0][1]])))
                print('Score: {0}'.format(top))
                print('Population count: {0}'.format(len(self.pop)))

            if top == success:
                print('Perfect match found: success!')
                print('Individual {0:06d}'.format(ranked[0][1]))
                return

            # Kill
            amount_to_kill = floor(self.rate['kill'] * len(self.pop))
            weakest = [r[0] for r in ranked[-amount_to_kill:] ]
            self.kill(weakest)

            # Crossover
            size = len(self.pop)
            for i in range(size):
                if randint(0, 100) < self.rate['cross'] * 100:
                    score = evaluate[i]
                    number_offspring = randint(1, score + 1) 
                    for j in range(number_offspring):
                        index = geometric(self.rate['mate']) - 1
                        mate = ranked[index][1]
                        if mate >= size:
                            mate = size - 1 
                        self.pop.append(self.crossover([i, mate]))

            #Mutation
            for i in range(size):
                if randint(0, 100) < self.rate['mutate'] * 100:
                    self.mutate(i)

        print('Reached total number of generations. No success.')
        print('Reverting to original population data.')
        self.corr = corr
        self.pop = pop
        
                    
if __name__ == '__main__':

    c = "success"
    pop = Population(size = 500, correct = c)
    pop.run(gen = 10000)
