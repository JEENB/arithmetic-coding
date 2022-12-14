import os
import math


file = os.getcwd() + '/files/hello.txt'

def decToBinConversion(no:int, precision:int)->str: 
    binary = ""  
    IntegralPart = int(no)  
    fractionalPart = no- IntegralPart
    #to convert an integral part to binary equivalent
    while (IntegralPart):
        re = IntegralPart % 2 
        binary += str(re)  
        IntegralPart //= 2
    binary = binary[ : : -1]    
    binary += '.'
    #to convert an fractional part to binary equivalent
    while (precision):
        fractionalPart *= 2
        bit = int(fractionalPart)
        if (bit == 1) :   
            fractionalPart -= bit  
            binary += '1'
        else : 
            binary += '0'
        precision -= 1
    return binary  

def getBinaryFractionValue(binaryFraction):
	"""
		Compute the binary fraction value using the formula
		of:
			(2^-1) * 1st bit + (2^-2) * 2nd bit + ...
	"""
	value = 0
	power = 1

	# Git the fraction bits after "."
	fraction = binaryFraction.split('.')[1]

	# Compute the formula value
	for i in fraction:
		value += ((2 ** (-power)) * int(i))
		power += 1

	return value

class ArithmeticCoding:
	def __init__(self, file) -> None:
		self.file = file
		self.__parse()
		self.__cumulativeDist()
		

	def __parse(self):
		'''
		+-----------------------+-------------------+
		|       Symbol			|		Freq		|
		+-----------------------+-------------------+
		|			a			|      	  3			|												
		|			b			|	      3			|					
		|			c			|	   	  6			|			
		+-----------------------+-------------------+
		'''
		self.prob_dist = {}
		self.num_elements = 0
		self.symbols = []
		f  =  open(self.file, 'r', encoding='ascii')
		for line in f:
			for i in line:
				self.symbols.append(i)
				try:
					self.prob_dist[i] += 1
				except:
					self.prob_dist[i] = 1
				self.num_elements += 1

	def __cumulativeDist(self):

		'''
		+-----------------------+-------------------+
		|       Symbol			|		Range		|
		+-----------------------+-------------------+
		|			a			|      [0,0.25]		|												
		|			b			|	  [0.25,0.50]	|					
		|			c			|	   [0.50, 1]	|			
		+-----------------------+-------------------+
		'''
		self.cum_dist = {}
		temp_freq = 0
		for symbol, freq in self.prob_dist.items():
			self.cum_dist[symbol] = [temp_freq/self.num_elements, (temp_freq + freq)/self.num_elements]  ## storing high and low
			temp_freq += freq

	def __symbol_prob(self, symbols):
		'''
		P(x_1, x_2, ...) = p(x_1).p(x_2). ...
		-log2(P(x_1, x_2, ...)) + 1
		returns binary truncation value
		'''
		self.prob = 1
		for s in symbols:
			self.prob *= self.prob_dist[s]/self.num_elements
		self.lx =  abs(math.ceil(math.log2(self.prob))) + 1



	def encoding(self, value:str = None) -> float:
		'''
		encodes for a subset of strings as well as the entire file. 
		'''

		low_old = 0
		high_old = 1
		range = 1
		symbols= self.symbols if value == None else value

		self.__symbol_prob(symbols)  ## computes the truncation value 

		for s in symbols:
			if s not in self.symbols:
				raise ValueError("Value symbol not fround in prob distribuiton")

			interval  = self.cum_dist[s]
			
			low = low_old + range * interval[0]
			high = low_old + range * interval[1]
			range = high - low

			low_old = low
			high_old = high


		self.tag = (high_old + low_old)/2  

		self.encoded_val = decToBinConversion(self.tag, self.lx)
		return self.encoded_val


	def decoding(self, tag:str, len:int):
		'''
		check interval, 
		update interval
		pick new 
		repeat
		'''


		self.t = getBinaryFractionValue(tag)
		n = 0
		decode_value = ''
		low_old = 0
		high_old = 1
		range = 1
		while n != len:
			
			for key, values in self.cum_dist.items():
				low_old = values[0]
				high_old = values[1]
				if self.t > low and self.t < high:
					decode_value += key
					low = low_old + range * values[0]
					high = low_old + range * values[1]
					range = high - low
					low_old = low
					high_old = high

		
	

		



f = ArithmeticCoding(file)
print("Prob distn", f.prob_dist)
print("Cum distn", f.cum_dist)
print(f.encoding("l"))
print(f.tag)
	
