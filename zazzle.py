'''		This script analyzes trends within a csv file containing 
royalty sales from zazzle.com

'''
# Populates an empty dictionary (dic) mapping
# the values from the key_index to val_index
# If making a frequency dictionary, set the last parameter to true
def make_dict(dic, key_index, val_index, freq = False):
	for row in range(1, num_sales + 1):
		key = data[row][key_index].rstrip()
		value = data[row][val_index].rstrip()
		
		if key == '':
			pass
		elif key not in dic:
			if freq:
				dic[key] = 1
			else:
				dic[key] = value
		else:
			if freq:
				dic[key] += 1

# Given a column_index of a column having two
# possible values, this returns a tally of the
# positive compares with the search_item
def tally(col_index, search_item):
	count = 0
	for n in range(1, num_sales + 1):
		if data[n][col_index] == search_item:
			count += 1
	return count


# Display top n results of frequency pairings 
# Set name to true if you want the product name with its ID
def disp_freq(dic, n, name=False):
	dic_sort = sorted(dic, key=dic.get, reverse=True)
	for i in range(n):
		if name:
			fo.write(str(i + 1) + " " + str(prod_names[dic_sort[i]]) + " " + str(dic_sort[i]) + " " + str(dic[dic_sort[i]]) + "\n")
		else:
			fo.write(str(i + 1) + " " + str(dic_sort[i]) + " " + str(dic[dic_sort[i]]) + "\n")


# ------------------------------------------------------------------------
import time 

filename = 'royaltyHistory.csv'

# Load data
f = open(filename)
data = [line.split(',') for line in f]
f.close()

num_sales = len(data) - 1
# This will contain one extra column due to use of comma in ship address
columns = len(data[1]) 

# Map Product ID with Product title
prod_names = dict()
make_dict(prod_names, 1, 2)

# Percentage of orders that were not cancelled
sold_ratio = (tally(5, 'No') / num_sales) * 100
# Percentage of orders referred by a 3rd party
party_ratio = (1 - (tally(7, 'None') / num_sales)) * 100
# Percentage of orders that were customized
custom_ratio = (tally(4, 'Yes') / num_sales) * 100
# Percentage of orders cleared vs cancelled
clear_ratio = (tally(16, 'cleared\n') / num_sales) * 100

# Most popular product type
prod_type = dict()
make_dict(prod_type, 3, -1, True)

# Most popular item
pop_item = dict()
make_dict(pop_item, 1, -1, True)

# Stores
stores = dict()
make_dict(stores, 6, -1, True)

# Location
loc = dict()
make_dict(loc, 9, -1, True)


fo = open(time.strftime("%m-%d-%y") + ".txt", 'w')

# Output results to file
fo.write("Top ten most popular product types:\n")
disp_freq(prod_type, 10)
fo.write("\nTop ten most popular items:\n")
disp_freq(pop_item, 10, True)
fo.write("\nStores:\n")
disp_freq(stores, 5)
fo.write("\nLocation of customers:\n")
disp_freq(loc, 10)

fo.write("\nPercentage of non-cancelled orders: " + str(sold_ratio))
fo.write("\nPercentage of cleared orders: " + str(clear_ratio))
fo.write("\nPercentage of orders referred by a 3rd party: " + str(party_ratio))
fo.write("\nPercentage of orders that were customized: " + str(custom_ratio))

fo.close()



				






