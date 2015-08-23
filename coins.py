import numpy as np
import pandas as pd
from functools import reduce


def gcd(a,b):
    while b:
        a, b = b, a % b
    return a


def build_table(coins, limit):
    '''Build a data frame showing the number of ways to represent a monetary
    value using the given coins. 

    Args:
        - coins : dictionary containing coin name and respective value
        - limit : highest monetary value calculated in the table (in cents)
    '''

    sorted_coins = sorted(coins.items(), key = lambda c: c[1])

    # Table variables
    over_one = list(filter(lambda a: a > 1, coins.values()))
    interval = reduce(gcd, over_one)
    names = [c[0] for c in sorted_coins]

    seq = np.arange(0, limit + 1, interval)

    table = pd.DataFrame(np.zeros((len(coins) + 1, len(seq))), 
                        index = list(names) + ['Total'],
                        columns = seq)
   
    ''' Dynamic programming

    This is a lookup table ordered by coin value (cheaper coins on top).

    This is how the algorithm works:
    
        Base case: We initialize the table by assigning the cheapest coin
        count 1 for 0.00 amount. (Clearly, there's only one way to have no 
        money!)

        - If the coin is worth more than the present amount, we skip.

        - Else if the coin is a penny (or some equivalent), we assign count 1 
          since there are no smaller integer values.

        - Else, we iterate in increments of the coin value up until the 
          present amount. For example, say n = 35 and we have a dime,
          then we iterate through [10, 20, 30]. This represents using one,
          two, and three dimes, respectively. Then, we subtract from n
          to give us a remainder...say 35 - 20 = 15. We round this 
          number down to nearest table value (in this case, no rounding
          is needed). Finally we look up the number of ways to represent
          this remainder using coins smaller than the current coin.
          So in this case, we represnt 15 cents in pennies and nickels.
          This simply means taking a sum of the precomputed values and
          adding it to our running total.

    '''

    # Base case: There's only one way to have no money!
    table.iloc[0, 0] = 1
    table.at['Total', 0] = 1

    for n in seq[1:]:

        # Column index
        c = table.columns.get_loc(n)

        for co, amt in sorted_coins:
            
            if amt > n:
                pass
            elif amt == 1:
                table.loc[co, n] = 1
            else:
                r = table.index.get_loc(co)
                total = 0
                # We added a small amount to include n within range
                for i in np.arange(amt, n + 0.00001, amt):                    
                    remain = int(n - i)
                    c_amt = table.columns.get_loc(remain - (remain % interval))
                    total += sum(table.iloc[ : r, c_amt])

                table.loc[co, n] = total

        table.loc['Total', n] = sum(table.iloc[:-1, c])

    return table


if __name__ == '__main__':
    coins = {'penny':1, 'nickel':5, 'dime':10, 'quarter':25, 'half':50}

    table = build_table(coins, 100)
    
