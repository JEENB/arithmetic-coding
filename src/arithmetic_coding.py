import os
import math
import tabulate
import json
from utils import *
class ArithmeticCoding:
	'''
	Parameters:
	------------
	file: file you want to encode
	distribution: default None/ dict
			accepts arbitrary distribution, {symbol, probability}
			dist = {'a':0.8, 'b': 0.02, 'c': 0.18}
	show_steps: bool: default False 
			show encoding and decoding process in the terminal
			use for small inputs only. 
	
	'''
	def __init__(self, file: str = None, distribution: dict = None, show_steps: bool = False) -> None:
		if file != None and distribution != None:
			raise ReferenceError("Expected either a file or a distribution")
		self.show_steps = show_steps
		if distribution == None:
			self.file = file  #file = 'path to file'
			self.__parse()
		else:
			self.file = file  # file = None
			self.prob_dist = distribution
			total = sum(values for values in self.prob_dist.values())
			if total != 1:
				raise ValueError(f"Excepted total probability,1 got {total}")
			self.symbols = list(self.prob_dist.keys())
			
		self.__cumulativeDist()

		if self.show_steps:
			print("Probability Distribution")
			print("-------------------------")
			print(tabulate.tabulate(list(self.prob_dist.items()), headers=["Symbol", "Probability"], tablefmt='pretty', numalign='center'))
			print("\nCumulative Distribution")
			print("------------------------")
			print(tabulate.tabulate(list(self.cum_dist.items()), headers=["Symbols", 'Range'],tablefmt="pretty", numalign='center'))
		

	def __parse(self):
		'''
		Key value pair
		+-----------------------+-----------------------+
		|		Symbol			|			Freq		|
		+-----------------------+-----------------------+
		|			a			|			0.25		|									
		|			b			|			0.25		|				
		|			c			|			0.50		|	
		+-----------------------+-----------------------+
		'''
		self.prob_dist = {}
		self.num_elements = 0
		self.symbols = []
		f  =  open(self.file, 'r', encoding='utf-8')
		for line in f:
			for i in line:
				self.symbols.append(i)
				try:
					self.prob_dist[i] += 1
				except:
					self.prob_dist[i] = 1
				self.num_elements += 1
		
		for key in self.prob_dist.keys():
			self.prob_dist[key] = self.prob_dist[key]/self.num_elements



	def __cumulativeDist(self):

		'''
		+-----------------------+-------------------+
		|		Symbol			|		Range		|
		+-----------------------+-------------------+
		|			a			|	[0,0.25]		|												
		|			b			|	[0.25,0.50]		|					
		|			c			|	[0.50, 1]		|			
		+-----------------------+-------------------+
		'''
		self.cum_dist = {}
		temp_freq = 0
		for symbol, freq in self.prob_dist.items():
			self.cum_dist[symbol] = [temp_freq, (temp_freq + freq)]  ## storing high and low
			temp_freq += freq
		
		

	def __symbol_prob(self, symbols):
		'''
		P(x_1, x_2, ...) = p(x_1).p(x_2). ...
		-log2(P(x_1, x_2, ...)) + 1
		returns binary truncation value
		'''
		self.prob = 1
		for s in symbols:
			self.prob *= self.prob_dist[s]
		self.lx =  abs(math.ceil(math.log2(self.prob))) + 1

	def __left_scale(self, x:float):
		return 2 * x
	
	def __right_scale(self, x:float):
		return 2 * x - 1

	def encoding(self, value:str = None) -> float:
		'''
		encodes for a subset of strings as well as the entire file. 
		'''

		if self.show_steps: 
			output = []

		low_old = 0
		high_old = 1
		range = 1
		symbols= self.symbols if value == None else value

		# self.__symbol_prob(symbols)  ## computes the truncation value  
		sym = ''
		output_sym = ''  ## output from encoding process
		for i, s in enumerate(symbols):
			sym += s
			if s not in self.symbols:
				raise ValueError("Value symbol not fround in prob distribuiton")

			interval  = self.cum_dist[s]

			low = low_old + range * interval[0]
			high = low_old + range * interval[1]
			while (high < 0.5 and low < 0.5) or (high > 0.5 and low > 0.5):
				if low > 0.5 and high > 0.5:
					output_sym += '1'
					if self.show_steps:
						output.append([sym, (low, high), "Right Scaling \nOutput = 1"])
					low = self.__right_scale(low)
					high = self.__right_scale(high)
					

				elif high < 0.5 and low < 0.5:
					output_sym += '0'
					if self.show_steps:
						output.append([sym, (low, high), "Left Scaling \nOutput = 0"])
					low = self.__left_scale(low)
					high = self.__left_scale(high)
					

			if self.show_steps:
				output.append([sym, (low, high), "Pick Next Symbol"])
				
			range = high - low

			low_old = low
			high_old = high

		# print(low_old, high_old)
		self.tag = 0.5 ## since 0.5 always lies between high and low because we rescale even after the last symbol encoding. 

		# tag_to_bin = decToBinConversion(self.tag, self.lx - len(output_sym))
		tag_to_bin = '0.1'   ## binary conversion of 0.5

		self.encoded_value = '0.' + output_sym + tag_to_bin.split('.')[1]

		if self.show_steps:
			output.append([' ', f"Symbols Encoded = {i+1}\nRescaling Output = {output_sym}\nTag = {self.tag}\nCompressed Value = {self.encoded_value}"])
			print("\nEncoding Process")
			print("------------------")
			print(tabulate.tabulate(output, headers= ['Symbol', 'Interval', 'Remark'], tablefmt="pretty", numalign='center'))
		else: 
			print("Encoded value \n-------------\n", self.encoded_value)
		
		return self.encoded_value, len(symbols)

	def __return_symbol(self, tag):
		''' 
		Given a tag returns the corresponding symbol
		'''
		for key, value in self.cum_dist.items():

			if tag < value[1]:
				'''
				intervals are disjoints
				'''
				return (key, value)


	def decoding(self, encoded_value:str, length:int):
		'''
		check interval, 
		update interval
		pick new 
		repeat
		'''
		if self.show_steps:
			output = []

		t = getBinaryFractionValue(encoded_value)
		decoded_symbols = ''
		low_old = 0
		high_old = 1
		ran = 1
		for i in range(length):
			t_prime = (t - low_old)/(ran)

			symb, interval = self.__return_symbol(t_prime)
			decoded_symbols += symb

			low = low_old + ran * interval[0]
			high = low_old + ran * interval[1]


			
			while (high < 0.5 and low <= 0.5) or (high > 0.5 and low >= 0.5):
		
				if low >= 0.5 and high > 0.5:
					
					if self.show_steps:
						output.append([decoded_symbols, encoded_value, t, (low, high), "Right Scaling\nRemove 1\n"])

					encoded_value = "0." + encoded_value[3:]
					t = getBinaryFractionValue(encoded_value)

					
					low = self.__right_scale(low)
					high = self.__right_scale(high)
		
					

				elif high < 0.5 and low <= 0.5:
					if self.show_steps:
						output.append([decoded_symbols, encoded_value, t, (low, high), "Left Scaling\nRemove 0"])

					encoded_value = "0." + encoded_value[3:]
					t = getBinaryFractionValue(encoded_value)

					low = self.__left_scale(low)
					high = self.__left_scale(high)
					
			ran = high - low

			low_old = low
			high_old = high
			if self.show_steps:
				output.append([decoded_symbols, encoded_value, t, (low, high), "Pick next\n"])	
		# print(low_old, high_old)

		if self.show_steps:
			print("\nDecoding Process")
			print("------------------")
			print(tabulate.tabulate(output, headers=['Decoded Symb', 'Encoded Value', 'Tag', 'Range', 'Remark'], tablefmt="pretty", numalign='center'))
			print(f"Decoded Value = {decoded_symbols}\n")
		else: 
			print(f"\nDecoded Value\n-------------\n{decoded_symbols}")
		
		return decoded_symbols

#=================================================================================================
		
dist = {'a':0.8, 'b': 0.02, 'c': 0.18}

file = os.getcwd() + '/src/files/hello.txt'
f = ArithmeticCoding(file=file, distribution= None, show_steps= True)
encoded_value, number = f.encoding()
decoded_symbols = f.decoding(encoded_value, length = number)
check(f.symbols, decoded_symbols)
