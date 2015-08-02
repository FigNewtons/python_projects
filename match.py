import numpy as np

def next_choice(ranks, proposed):
    """Given a numpy row vector of ranks (e.g. [2, 4, 3, 1, 5]),
    and a logical vector of proposals (e.g. proposed[0] = True means
    the man proposed to the woman with index 0), return the index
    corresponding to the person's highest, available choice. """
    choice = min(ranks[~proposed])
    return list(ranks == choice).index(True)


def is_free(index, engaged, gender = 0):
    """Return true if the given person is not engaged. Each person
    is uniquely represented by their gender (0 - male; 1 - female)
    and index. """
    return index not in [couple[gender] for couple in engaged]


def partner(index, engaged, gender = 0):
    """Return the index of a person's partner that is already 
    engaged. """
    c = [couple[gender] for couple in engaged].index(index)
    return engaged[c][(gender + 1) % 2]


def broke(index, engaged, gender = 0):
    "Cancel a person's current engagement. "
    c = [couple[gender] for couple in engaged].index(index)
    del engaged[c]

def free_men(engaged, num_pairs):
    "Return a logical list of the men that are not engaged. "
    return list(map(lambda m: is_free(m, engaged, 0), range(num_pairs)))


def match(men, women):
    """Return a list of tuples representing the stable pairing of men
    and women using the Gale-Shapely algorithm. The arguments are 
    n by n numpy arrays. """
    
    num_pairs = men.shape[0]
    engaged = []
    
    proposed = np.array([False] * (num_pairs**2)).reshape(num_pairs, num_pairs)
    bachelors = free_men(engaged, num_pairs)
    
    while any(bachelors):
        m_indices = [m for m, free in enumerate(bachelors) if free == True]
        
        for m in m_indices:
            w = next_choice(men[m], proposed[m])
            proposed[m][w] = True
            if is_free(w, engaged, 1):
                engaged.append((m, w))
            else:
                fiance = partner(w, engaged, 1)
                # Fiance has lower preference than current man
                if women[w][fiance] > women[w][m]:
                    broke(w, engaged, 1)
                    engaged.append((m, w))
        bachelors = free_men(engaged, num_pairs)
    return engaged


if __name__ == '__main__':
    men = np.array([(2, 1, 4, 3, 5),
                    (2, 1, 3, 5, 4),
                    (1, 2, 3, 4, 5),
                    (3, 2, 4, 1, 5),
                    (1, 4, 2, 5, 3)])
    
    women = np.array([(5, 3, 2, 1, 4),
                      (4, 3, 1, 2, 5),
                      (4, 2, 1, 3, 5),
                      (3, 1, 2, 5, 4),
                      (5, 2, 3, 1, 4)])
    print(sorted(match(men, women)))
