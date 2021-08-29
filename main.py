#Main purpose of this program is to
#Embed a digital signature in images to
#prove ownership in case of piracy

import cv2
SIGNATURE_LENGTH = 100

#104---> [011,010,00]                #  this function takes the number say 104 and by using bitwise operator on that number we return list containing three elements of length 3,3,2(which contains only boolean values).
def getBits(n):
	return [n >> 5, (n & 28)>>2, n & 3]

#[011,010,00] ---> 104              #  this function takes list containing three elements, containing boolean values only, of length 3,3,2 and by using bitwise operator we return a number combination of all boolean values.
def getByte(bits):
	return (((bits[0]<<3) | bits[1])<<2) | bits[2]

def normalize_signature(x):         # this function takes the signature and normalize it to the length of SIGNATURE_LENGTH(100 in this case) by putting '*' at the end places if the length of the sign is less than SIGNATURE_LENGTH and return the same. 
	return  x[:SIGNATURE_LENGTH].ljust(SIGNATURE_LENGTH,'*')

def getEmbeddingPoints():           # this function return the lit of dimensions of points(x,y) where you want to embed the message
	return [(8, x*2) for x in range(SIGNATURE_LENGTH) ]

def embed(resultImage, srcImage, sign):         #this function the three arguments as -result image, source image and signature- respectively 
	image = cv2.imread(srcImage, cv2.IMREAD_COLOR)
	if image is None:
		print(srcImage, 'not found')
		return

	normalized = normalize_signature(sign)
	embedAt = getEmbeddingPoints()        # embedAt will store the pair of values of the points where message is being embedded. x and y will be taken from the first and second value of the pair resoectively. 
	cnt = 0
	for x, y in embedAt:             # since embedAt has pair of values so x will take first value from the pair and y will take the second value 
		data = ord(normalized[cnt])       #ord gives the ASCII of the character
		bits = getBits(data)
		image[x][y][2] = (image[x][y][2] & ~7) | bits[0] #red band
		image[x][y][1] = (image[x][y][1] & ~7) | bits[1]#green band
		image[x][y][0] = (image[x][y][0] & ~3) | bits[2]#blue band
		cnt+=1

	#save back
	cv2.imwrite(resultImage, image)

def extract(resultImage):
	image = cv2.imread(resultImage, cv2.IMREAD_COLOR)
	if image is None:
		print(resultImage, 'not found')
		return

	extractFrom = getEmbeddingPoints()

	cnt = 0
	sign = ''
	for x, y in extractFrom:
		bit1 = (image[x][y][2] & 7) #red band
		bit2 = (image[x][y][1] & 7)#green band
		bit3 = (image[x][y][0] & 3)#blue band
		data = getByte([bit1,bit2,bit3])
		sign = sign+ chr(data)     #chr converts ASCII to text
		cnt+=1
	#remove the padding
	return sign.strip('*')

def main():
	embed('images\encoded.png', 'images\decoded.png', "Name The only Crystal User From Naruto Series?")
	signature = extract('images\encoded.png')
	print(signature)
main()
# _____________________________________________________________________________________________________________________________________________________________________________________



# use of the functions used in the above program.

# cv2.imread() is used to load an image in memory (as a 3d array).
# It takes 2 parameters:
# 1) srcFile: image to load
# 2) flag: approach to build the memory image.
# In our case we used cv2.IMREAD_COLOR that instructs
# reading the image as color image.
# By this the image gets 3rd dimension that stores BGR bands per pixel.
#
#
# cv2.imwrite() is used to write an image on disk.
# It takes 2 parameters:
# 1) targetFile: file to save the image as. Keep it .png to avoid lossy compression (more on this ahead)
# 2) image : The data structure (3d or 2d array) of the image.
# ____________________________________________________________________________________________________________________________________________________________________________________




