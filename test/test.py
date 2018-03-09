import unittest
from generator import generator

class TestRandomNumberGenerator(unittest.TestCase):
	def test_null_cdf(self):
		res, message = generator.generate_numbers_by_distribution(None)
		self.assertEqual(res, None)
		self.assertEqual(message, "Cdf must be non-empty list of tuples")

	def test_invalid_cdf(self):
		res,message = generator.generate_numbers_by_distribution([(1,0.4), [2,0.6], (2, 0.6, "asd"), (2, 0.6)])
		self.assertEqual(res, None)
		self.assertIn("Cdf is invalid.",message)

		res,message = generator.generate_numbers_by_distribution([(1,0.4), (2, 0.6, "asd"), (2, 0.6)])
		self.assertEqual(res, None)
		self.assertIn("Cdf is invalid.",message)

		res,message = generator.generate_numbers_by_distribution([(1,0.4), (2, 1.6)])
		self.assertEqual(res, None)
		self.assertIn("Cdf is invalid.",message)

		res,message = generator.generate_numbers_by_distribution([(1,0.4), (2, 0.6)])
		self.assertEqual(res, None)
		self.assertIn("Cdf is invalid.",message)

		res,message = generator.generate_numbers_by_distribution([(1,0.4), (2, 0.3)])
		self.assertEqual(res, None)
		self.assertIn("Cdf is invalid.",message)

	def test_valid_numbers(self):
		for i in xrange(0,100):
			res = generator.generate_numbers_by_distribution()
			self.assertLess(res,6)
			self.assertGreater(res, 0)

def main():
	suite = unittest.TestLoader().loadTestsFromTestCase(TestRandomNumberGenerator)
	unittest.TextTestRunner(verbosity=2).run(suite)