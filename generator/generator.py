from collections import deque
from random import uniform
from time import time
import threading
import logging

CDF = [(1, 0.5), (2, 0.75), (3, 0.9), (4, 0.95), (5, 1)]
MAX = 100
logging.basicConfig(filename='numbergenerator.log',level=logging.WARNING)

class NumberGenerator(object):
	def __init__(self, cdfs=CDF, maxlen=MAX):
		self.set_cdf(cdfs)
		self.initialize_queue(maxlen)
		self.mutex = threading.Lock()
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
		self.mutex.acquire()
		l = len(self._queue)
		self.mutex.release()
		return l

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
			logging.error("{0}:{1}".format(self.message, cdf))
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
			logging.error("Maximum length is not valid: {0}".format(maxlen))
			return False
		else:
			if maxlen < 1:
				logging.error("Maximum length is not valid: {0}".format(maxlen))
				return False
			else:
				return True

	def _validate_filepath(self, path):
		if not isinstance(path, str):
			logging.error("Path is not valid: {0}".format(path))
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

	def generate_numbers_by_distribution(self, result_dict=None, identifier=0):
		'''
		If the operation ends successfully, it returns randomly generated number,
		otherwise None with a message.
		
		:cdf List of tuples. Restrictions are explained in _validate_cdf function.
		Returns tuple. Generated number and none if cdf is valid, otherwise None and error message
		'''
		if result_dict is None:
			result_dict = {}

		if self.isvalid:
			n = self._round_random_number(uniform(0,1))
			for gen, cdf_val in self._cdfs:
				if n == cdf_val:
					l = self.queue_length
					self.mutex.acquire()
					if l == self.queue_maxlength:
						self._frequencies[self._queue[0][0]] -= 1
					self._queue.append((gen, time()))
					self.mutex.release()
					self._frequencies[gen] += 1
					result_dict[identifier] = True
					return gen
		else:
			result_dict[identifier] = False

	def get_frequency_percentages(self):
		'''
		Calculates the percentage of frequencies for each number and returns as dictionary.
		'''
		if self.isvalid:
			queue_len = float(self.queue_length)
			try:
				for k,v in self._frequencies.iteritems():
					self._frequency_percentages[k] = (v / queue_len) * 100
				return self._frequency_percentages
			except ZeroDivisionError:
				logging.error("Zero division error: {0}".format(queue_len))
				return None
		else:
			return None

	def save_last_generated_number(self, result_dict, identifier, filepath="lastgeneratednumber.txt", mode="w"):
		'''
		Writes last generated number to a file.

		:result_dict Dictionary. A mutable object in order to keep the response from thread
		:identifier Integer. Indicates the index of the thread
		:filepath String. Path of the file.
		:mode String. File mode for writing, it can not be given as 'r'
		'''
		if not self._validate_filepath(filepath):
			result_dict[identifier] = False
			return

		with open(filepath, mode) as fout:
			self.mutex.acquire()
			value, time = self._queue[-1]
			self.mutex.release()
			fout.write("%d,%f\n" % (value, time))
			result_dict[identifier] = True

	@staticmethod
	def looper(itr, method, **wargs):
		if itr <= 0:
			while True:
				method(**wargs)
		else:
			for _ in xrange(0, itr):
				method(**wargs)
	def _run(self, iterations, result_dict, number_of_threads=1, method=None, is_deamon=False, **args):
		'''
		A generic method that calls relevant method from class. Stores the return values 
		inside a dictionary for debugging purpose.

		:result_dict Dictionary. A mutable object in order to keep the response from thread
		:number_of_threads Integer. Indicates number of threads to be created
		:method String. The method that is supposed to be called from the inside of the class
		:is_deamon Boolean. Determines whether created threads will be run as deamon
		:args Arguments for related method
		'''
		t_list = []
		try:
			method = getattr(self, method)
			if method and number_of_threads > 0:
				for i in xrange(0, number_of_threads):
					d = {"itr":iterations, "method":method, "result_dict":result_dict, "identifier":i}
					d = dict(d, **args)
					t = threading.Thread(target=self.looper, kwargs=d)
					t_list.append(t)
					t.deamon = is_deamon
					t.start()
				if not is_deamon:
					for t in t_list:
						t.join()
		except Exception, e:
			logging.error(str(e))
		return t_list

	def run_writer(self, iterations, filepath="lastgeneratednumber.txt", mode="w"):
		'''
		Runs save_last_generated_number method as a separated thread
		:filepath String. Path of the file.
		:mode String. File mode for writing, it can not be given as 'r'
		'''
		result = {}
		l = self._run(iterations, result, 1, "save_last_generated_number", True, **{"filepath":filepath, "mode":mode})
		return result

	def run_generator(self, iterations):
		'''
		Runs save_last_generated_number method as a separated thread
		:filepath String. Path of the file.
		:mode String. File mode for writing, it can not be given as 'r'
		'''
		result = {}
		l = self._run(iterations, result, 5, "generate_numbers_by_distribution", False)
		return result