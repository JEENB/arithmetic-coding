import os
import math
import tabulate


file = os.getcwd() + '/src/files/hello.txt'

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
	def __init__(self, file, distribution: dict = None, show_steps: bool = False) -> None:
		self.file = file
		self.show_steps = show_steps
		if distribution == None:
			self.__parse()
		else:
			self.prob_dist = distribution
			self.symbols = self.prob_dist.keys()
		self.__cumulativeDist()

		if self.show_steps:
			print(tabulate.tabulate(list(self.prob_dist.items()), headers=["Symbol", "Probability"], tablefmt='pretty', numalign='center'))
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
		f  =  open(self.file, 'r', encoding='ascii')
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

		self.__symbol_prob(symbols)  ## computes the truncation value 
		sym = ''
		for i, s in enumerate(symbols):
			sym += s
			if s not in self.symbols:
				raise ValueError("Value symbol not fround in prob distribuiton")

			interval  = self.cum_dist[s]

			low = low_old + range * interval[0]
			high = low_old + range * interval[1]
			while (high < 0.5 and low < 0.5) or (high > 0.5 and low > 0.5) and i != len(symbols)-1:
				if low > 0.5 and high > 0.5:
					if self.show_steps:
						output.append([sym, (low, high), "Right Scaling \nOutput = 1"])
					low = self.__right_scale(low)
					high = self.__right_scale(high)
					

				elif high < 0.5 and low < 0.5:
					if self.show_steps:
						output.append([sym, (low, high), "Left Scaling \nOutput = 0"])
					low = self.__left_scale(low)
					high = self.__left_scale(high)
					

			if self.show_steps:
				output.append([sym, (low, high), "Pick Next Symbol"])
				
			range = high - low

			low_old = low
			high_old = high


		self.tag = (high_old + low_old)/2  

		self.encoded_val = decToBinConversion(self.tag, self.lx)

		if self.show_steps:
			print(tabulate.tabulate(output, headers= ['Symbol', 'Interval', 'Remark'], tablefmt="pretty", numalign='center'))


		return self.encoded_val


	def decoding(self, tag:str, len:int):
		'''
		check interval, 
		update interval
		pick new 
		repeat
		'''

		
	

		
dist = {'a':0.8, 'b': 0.02, 'c': 0.18}


f = ArithmeticCoding(file, distribution= dist, show_steps= True)

print(f.encoding(value='acba'))
print(f.tag)
	
