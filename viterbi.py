


def viterbi(obs, states, start, transition, emission):
    ''' Dynamic programming implementation of the viterbi algorithm.

    We compute the values in the V table using Bayes' theorem 
    (omitting the denominator). So for example, on day one we observe
    that the patient is 'Normal'. Hence we compute

    P(H | N ) = P(H) * P(N | H) 
    P(F | N ) = P(F) * P(N | F)

    The values come from the start and emission dictionaries. We then 
    update the paths (since no transition occurred, 'Healthy' maps to 
    ['Healthy'] and likewise for 'Fever'.

    For subsequent days, we apply Bayes' theorem for each pair of 
    states. So for example:

    Probability that today the patient is healthy given that they are
    cold and were healthy yesterday
    P(H | C, H) = [P(H yesterday) * P(H -> H)] * P(C | H)

    We pick the highest probability for the state yesterday and update
    V and the path.

    Because the probabilities "cascade" due to the transitions, at the
    very end we choose the state with the highest end probability and 
    output its path. 

    '''
    V = [{}]
    path = {}

    # Base case (t = 0; s0)
    for s in states:
        V[0][s] = start[s] * emission[s][obs[0]]
        path[s] = [s]

    for time in range(1, len(obs)):
        V.append({})
        newpath = {}

        for s in states:
            (prob, state) = max((V[time - 1][s0] * transition[s0][s] * emission[s][obs[time]], s0) for s0 in states)
            V[time][s] = prob
            newpath[s] = path[state] + [s]

        path = newpath
    
    n = 0

    if len(obs) != 1:
        n = time
    
    print_table(V)
    (prob, state) = max((V[n][s], s) for s in states)
    return (prob, path[state])

def print_table(V):
    print(V)



if __name__ == '__main__':
    states = ('Healthy', 'Fever')
    observations = ('normal', 'cold', 'dizzy')
    
    start_probability = {'Healthy': 0.6, 'Fever': 0.4}

    transition_probability = {
        'Healthy': {'Healthy': 0.7, 'Fever': 0.3},
        'Fever': {'Healthy': 0.4, 'Fever': 0.6}
        }

    emission_probability = {
        'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
        'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
        }

    guess = viterbi(observations, states, start_probability, transition_probability, emission_probability)
    print(guess)
