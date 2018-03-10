from collections import deque
from random import uniform

CDF = [(1, 0.5), (2, 0.75), (3, 0.9), (4, 0.95), (5, 1)]
MAX = 100
class NumberGenerator(object):
	def __init__(self, cdfs=CDF, maxlen=MAX):
		self.set_cdf(cdfs)
		self.initialize_queue(maxlen)

		self._frequencies = {}
		self._frequency_percentages = {}
		for val, prob in self._cdfs:
			self._frequencies[val] = 0
			self._frequency_percentages[val] = 0

	@property
	def queue_maxlength(self):
		return self._queue.maxlen

	@property
	def queue_length(self):
		return len(self._queue)

	def _validate_cdf(self, cdf):
		'''
		Validates cdf.
		:cdf List of tuples that includes a number and its cumulative probabilty of distribution.
			Each tuple should include two elements a number to be generated and its cumulative 
			probability of distribution. Tuples should be sorted in ascending order by 
			cumulative distribution.
		Returns bool and error message. If cdf is valid, error message is set to None
		'''
		if not cdf:
			return False, "Cdf must be non-empty list of tuples"

		s, curr = 0, 0

		invalid_message = "Cdf is invalid. Should consist of list of \
		tuples of two (<GENERATED_NUMBER>, <CUMULATIVE DISTRIBUTION>).\
		List shoud be sorted by <CUMULATIVE DISTRIBUTION> in ascending order."

		for i in cdf:
			if not isinstance(i, tuple):
				return False, invalid_message 
			if len(i) != 2:
				return False, invalid_message
			if i[1] < 0 or i[1] > 1:
				return False, invalid_message
			if i[1] < curr:
				return False, invalid_message
			s += abs(i[1] - curr)
			if s > 1:
				return False, invalid_message
			curr = i[1]
		return (False, invalid_message) if s < 1 else (True, None)

	def set_cdf(self, cdf):
		'''
		Updates cumulative distribution list. Validates the list before assignment.
		:cdf : List of tuples. Restrictions are explained in _validate_cdf function
		'''
		self.isvalid, self.message = self._validate_cdf(cdf)

		if self.isvalid:
			self._cdfs = cdf
		else:
			self._cdfs = []

	def initialize_queue(self, maxlen):
		'''
		Creates new queue with maximum size of maxlen and assigns to _queue.
		If given length is neither an integer nor less than zero, size of queue becomes unlimited.

		:maxlen : Integer. It is used for setting maximum size of queue.
		'''
		if not self._validate_max_length(maxlen):
			self._queue = deque([])
		else:
			self._queue = deque([], maxlen)

	def _validate_max_length(self, maxlen):
		'''
		Validates given length. If it is neither an integer nor less than zero,
		size of queue becomes unlimited.

		:maxlen : Integer. Should be higher than 0.
		Returns boolean that indicates validness of parameter
		'''
		if not isinstance(maxlen, int):
			return False
		else:
			if maxlen < 1:
				return False
			else:
				return True

	def _round_random_number(self, n):
		'''
		Rounds n to the corresponding probility
		
		:n Uniformly generated number. It is guaranteed to be between 0 and 1.
		Returns nearest  
		'''
		cumulative_distributions = map(lambda x:x[1], self._cdfs)
		for i in cumulative_distributions:
			if n <= i:
				return i

	def generate_numbers_by_distribution(self):
		'''
		If the operation ends successfully, it returns randomly generated number,
		otherwise None with a message.
		
		:cdf List of tuples. Restrictions are explained in _validate_cdf function.
		Returns tuple. Generated number and none if cdf is valid, otherwise None and error message
		'''
		if self.isvalid:
			n = self._round_random_number(uniform(0,1))
			for gen, cdf_val in self._cdfs:
				if n == cdf_val:
					if self.queue_length == self.queue_maxlength:
						self._frequencies[self._queue[0]] -= 1
					self._queue.append(gen)
					self._frequencies[gen] += 1
					return gen, None
		else:
			return None, self.message

	def get_frequency_percentages(self):
		'''
		Calculates the percentage of frequencies for each number and returns as dictionary.
		'''
		if self.isvalid:
			queue_len = float(self.queue_length)
			try:
				for k,v in self._frequencies.iteritems():
					self._frequency_percentages[k] = (v / queue_len) * 100
				return self._frequency_percentages, None
			except ZeroDivisionError:
				return None, "Zero division error"
		else:
			return None, self.message
