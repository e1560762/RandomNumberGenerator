import unittest
from generator import generator
from time import time, sleep

class TestRandomNumberGenerator(unittest.TestCase):
	def setUp(self):
		self.number_generator = generator.NumberGenerator()
		self.invalid_number_generator = generator.NumberGenerator(None, "100")

	def test_invalid_cdf(self):
		self.invalid_number_generator.set_cdf(None)
		res = {}
		self.invalid_number_generator.generate_numbers_by_distribution(res, 0)
		self.assertEqual(res[0], False)
		#self.assertEqual(message, "Cdf must be non-empty list of tuples")

		self.invalid_number_generator.set_cdf([(1,0.4), [2,0.6], (2, 0.6, "asd"), (2, 0.6)])
		self.invalid_number_generator.generate_numbers_by_distribution(res, 0)
		self.assertEqual(res[0], False)
		#self.assertIn("Cdf is invalid.",message)

		self.invalid_number_generator.set_cdf([(1,0.4), (2, 0.6, "asd"), (2, 0.6)])
		self.invalid_number_generator.generate_numbers_by_distribution(res, 0)
		self.assertEqual(res[0], False)
		#self.assertIn("Cdf is invalid.",message)

		self.invalid_number_generator.set_cdf([(1,0.4), (2, 1.6)])
		self.invalid_number_generator.generate_numbers_by_distribution(res, 0)
		self.assertEqual(res[0], False)
		#self.assertIn("Cdf is invalid.",message)

		self.invalid_number_generator.set_cdf([(1,0.4), (2, 0.6)])
		self.invalid_number_generator.generate_numbers_by_distribution(res, 0)
		self.assertEqual(res[0], False)
		#self.assertIn("Cdf is invalid.",message)

		self.invalid_number_generator.set_cdf([(1,0.4), (2, 0.3)])
		self.invalid_number_generator.generate_numbers_by_distribution(res, 0)
		self.assertEqual(res[0], False)
		#self.assertIn("Cdf is invalid.",message)

	def test_invalid_maxlength(self):
		self.assertEqual(self.invalid_number_generator.queue_maxlength, None)

	def test_valid_numbers(self):
		occurrence_dict = {1:0, 2:0, 3:0, 4:0, 5:0}
		for i in xrange(0,generator.MAX):
			res = self.number_generator.generate_numbers_by_distribution()
			occurrence_dict[res] += 1
			self.assertLess(res,6)
			self.assertGreater(res, 0)

		res = self.number_generator.get_frequency_percentages()
		self.assertEqual(sorted(res.keys()), sorted(occurrence_dict.keys()))

		f = float(generator.MAX)
		for k in occurrence_dict.keys():
			self.assertEqual((occurrence_dict[k] / f)*100, res[k])

	def test_queue_length(self):
		from collections import deque

		queue = deque([], generator.MAX)
		for i in xrange(0,generator.MAX * 2):
			res = self.number_generator.generate_numbers_by_distribution()
			queue.append(res)

		self.assertEqual(self.number_generator.queue_length, generator.MAX)
		
		occurrence_dict = {1:0, 2:0, 3:0, 4:0, 5:0}
		for e in queue:
			occurrence_dict[e] += 1

		res = self.number_generator.get_frequency_percentages()
		f = float(generator.MAX)
		for k in occurrence_dict.keys():
			self.assertEqual((occurrence_dict[k] / f)*100, res[k])

	def test_round_number(self):
		from random import uniform
		d = map(lambda x: x[1], generator.CDF)
		length = len(d)
		for i in xrange(0, generator.MAX):
			n = uniform(0,1)
			m = self.number_generator._round_random_number(n)
			i = d.index(m)
			if i>0:
				self.assertGreater(n, d[i-1])
				self.assertLessEqual(n, m)

	def test_invalid_write_to_file(self):
		for i in xrange(0,generator.MAX):
			self.number_generator.generate_numbers_by_distribution()
		
		result = self.number_generator.run_writer(1, 3453)
		print result
		sleep(1)
		self.assertEqual(result[0], False)

	def test_valid_write_to_file(self):
		for i in xrange(0,generator.MAX * 2):
			self.number_generator.generate_numbers_by_distribution()
		filepath = "testfile.txt"
		start = time()
		result = self.number_generator.run_writer(1,filepath,"w")
		print result
		sleep(1)
		self.assertEqual(result[0], True)

		fp = open(filepath, 'r')
		line = fp.readline().strip()
		number, written_time = line.split(',')
		fp.close()
		self.assertEqual(int(number), self.number_generator._queue[-1][0])
		self.assertEqual(float(written_time), self.number_generator._queue[-1][1])
		self.assertGreaterEqual(written_time, start)

def main():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestRandomNumberGenerator)
	unittest.TextTestRunner(verbosity=2).run(suite)