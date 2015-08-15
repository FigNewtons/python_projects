import numpy as np

def edit_distance(s1, s2):
    '''Return the edit distance (Levenshtein) and list of changes made 
    between two strings, s1 and s2, using the Wagner-Fischer algorithm. 
    The changes are w.r.t the string s1. '''
    m, n = len(s1), len(s2)
    
    # Initialize the m+1 x n+1 distance array between s1 and s2
    distance = np.r_[ np.arange(n+1), np.zeros(m * (n+1))].reshape((m+1, n+1))
    distance[:, 0] = np.arange(m+1) 

    '''Operations:

        Diagonal - Substitution (either same or different letter)
        Left     - Insertion
        Right    - Deletion

    '''
    for j in range(1, n + 1):
        for i in range(1, m + 1):

            if s1[i - 1] == s2[j - 1]:
                distance[i, j] = distance[i - 1, j - 1] 
            else:
                distance[i, j] = min(distance[i-1 ,j  ] + 1, # Delete 
                                     distance[i  , j-1] + 1, # Insert
                                     distance[i-1 ,j-1] + 1  # Substitute
                                     )

    i, j = m , n
    changes = []
    while distance[i,j] != 0:

        delete = distance[ i - 1, j]
        insert = distance[ i, j - 1]
        sub = distance[i - 1, j - 1]

        back = min(delete, insert, sub)
        if back == delete:
            changes.append('Delete {0} from {1} at position {2}'.format(s1[i - 1], s1, i))
            i -= 1
        elif back == insert:
            changes.append('Insert {0} to {1} at position {2}'.format(s2[j - 1], s1, j))
            j -=1
        else:
            i -= 1
            j -= 1
            if s1[i] != s2[j]:
                changes.append('Substitute {0} with {1} at position {2}'.format(s1[i], s2[j], i+1))

    return (distance[m,n], changes[::-1])


if __name__ == '__main__':

    print('Comparing "basket" and "rockets"\n')
    d, changes = edit_distance('basket', 'rockets')
    print('Edit distance: {0:.0f}'.format(d))
    print('Changes: ')

    for n, change in enumerate(changes):
        print('\tStep {0}: {1}'.format(n + 1, change))








