from random import uniform

CDF = [(1, 0.5), (2, 0.75), (3, 0.9), (4, 0.95), (5, 1)]
def generate_numbers_by_distribution(cdf=CDF):
	'''
	If the operation ends successfully, it returns randomly generated number, otherwise None with a message. 
	
	:cdf List of tuples. Each tuple should include two elements a number to be generated and
	its cumulative probability of distribution. Tuples should be sorted in ascending order by 
	cumulative distribution.
	'''
	if not cdf or not isinstance(cdf, list):
		return None, "Cdf must be non-empty list of tuples"

	'''
	Validates cdf. Restrictions are explained in generate_numbers_by_distribution function
	:cdf List of tuples that includes a number and its cumulative probabilty of distribution.
	'''
	def isvalid_cdf(cdf):
		s, curr = 0, 0
		for i in cdf:
			if not isinstance(i, tuple):
				return False 
			if len(i) != 2:
				return False 
			if i[1] < 0 or i[1] > 1:
				return False 
			if i[1] < curr:
				return False 
			s += abs(i[1] - curr)
			if s > 1:
				return False 
			curr = i[1]
		return False if s < 1 else True

	if not isvalid_cdf(cdf):
		return None, "Cdf is invalid. Should consist of list of \
		tuples of two (<GENERATED_NUMBER>, <CUMULATIVE DISTRIBUTION>).\
		List shoud be sorted by <CUMULATIVE DISTRIBUTION> in ascending order."

	def round_random_number(n):
		'''
		Rounds n to the corresponding probility
		:n Uniformly generated number. It is guaranteed to be between 0 and 1  
		'''
		if 0 <= n <= 0.5:
			return 0.5
		elif n <= 0.75:
			return 0.75
		elif n <= 0.9:
			return 0.9
		elif n <= 0.95:
			return 0.95
		else:
			return 1.0

	n = uniform(0,1)
	n = round_random_number(n)
	for gen, cdf_val in cdf:
		if n == cdf_val:
			return gen