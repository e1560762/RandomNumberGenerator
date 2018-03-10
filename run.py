import argparse
from generator import generator

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Runs number generators and consumers concurrently")
	parser.add_argument("-g", dest="iterations_for_generator", default=0, type=int)
	parser.add_argument("-w", dest="iterations_for_writer", default=0, type=int)
	parser.add_argument("-f", dest="filepath", default="output.txt")
	parser.add_argument("-m", dest="writemode", default="w", choices=["w", "a"])
	ns = parser.parse_args()
	ng = generator.NumberGenerator()
	ng.run_generator(ns.iterations_for_generator)
	ng.run_writer(ns.iterations_for_writer, ns.filepath, ns.writemode)