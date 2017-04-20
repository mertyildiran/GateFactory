import math
import threading

class NAND():

	def __init__(self,factory):
		pass


class Factory():

	def __init__(self,input_dim=0,output_dim=0):
		self.input = []
		self.target = []
		self.output = []

		self.mini_batch = []
		self.mini_batch_limit = int(math.sqrt(input_dim))
		self.counter = 0
		self.lock = False

		self.stopper = False
		self.thread = None
		self.start()

	def _start(self):
		pass

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
			self.target = []
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
