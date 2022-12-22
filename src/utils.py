
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

def check(t1:str, t2:str) -> float:
	'''
	Computes the error rate and calculates the places where error occured
	'''
	min_str = min(len(t1), len(t2))
	max_str = max(len(t1), len(t2))
	err = 0
	for i in range(min_str):
		if t1[i] != t2[i]:
			err += 1
		else:
			err += 0
	print(f"Error = {err*100/max_str}%")