import math
import threading
import random
import itertools


class Factory():

	def __init__(self,input_dim=0,output_dim=0):
		self.input = self.rbl(input_dim)
		self.target = self.rbl(output_dim)
		self.output = []

		self.best = (0,1)
		self.error = 1.0
		self.pool = range(input_dim)

		self.mini_batch = []
		self.mini_batch_limit = int(math.sqrt(input_dim))
		self.counter = 0
		self.lock = False

		self.stopper = False
		self.thread = None
		self.start()

	def _start(self):
		while not self.stopper:
			self.output = self.NAND(self.best)
			# level1
			if self.mini_batch:
				combinations = list(itertools.combinations_with_replacement(self.pool,2))
				for combination in combinations:
					error = 0
					error_old = 0
					divisor = 0
					for data in self.mini_batch:
						self.input = data[0]
						self.target = data[1]
						error_old += abs(self.NAND(self.best) - self.target[0])
						error += abs(self.NAND(combination) - self.target[0])
						divisor += 1
					if divisor != 0:
						if error / divisor < error_old / divisor:
							self.best = combination
							self.error = error / divisor
							print self.best
							print self.error
				self.pool.extend(random.sample(combinations,len(self.input)))
				#print self.pool
				#print "\n"

	def start(self):
		self.stopper = False
		if not self.thread:
			self.thread = threading.Thread(target=self._start)
			self.thread.start()
		print "Factory has been started"

	def stop(self):
		self.stopper = True
		self.thread = None
		print "Factory is now stopped"

	def load(self,input_arr,output_arr=None):
		if len(self.input) != len(input_arr):
			print "Size of the input array: " + str(len(input_arr))
			print "Size of the input of the factory: " + str(len(self.input))
			print "These values are not matching! Please fix it and try it again."
		else:
			self.input = input_arr
		if output_arr is None:
			self.mini_batch = []
			#self.target = []
		else:
			if len(self.target) != len(output_arr):
				print "Size of the output/target array: " + str(len(output_arr))
				print "Number of the output/target of the factory: " + str(len(self.target))
				print "These values are not matching! Please fix it and try it again."
			else:
				self.target = output_arr
				self.mini_batch.append([input_arr,output_arr])
				if len(self.mini_batch) > self.mini_batch_limit:
					self.mini_batch.pop(0)

	def NAND(self,duo):
		if isinstance(duo[0], tuple):
			left = self.NAND(duo[0])
		else:
			left = self.input[duo[0]]
		if isinstance(duo[1], tuple):
			right = self.NAND(duo[1])
		else:
			right = self.input[duo[1]]
		if not (left and right):
			return 1
		else:
			return 0

	#random binary list
	def rbl(self,n):
		return [random.randint(0,1) for b in range(1,n+1)]
