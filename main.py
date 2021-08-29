#Main purpose of this program is to
#Embed a digital signature in images to
#prove ownership in case of piracy
import cv2
import os
class digital_signature:
	def __init__(self):
		self.source_image = ""
		self.destination_img = "images\decoded.png"
		self.SIGNATURE_LENGTH = 100

	# 104---> [011,010,00]                #  this function takes the number say 104 and by using bitwise operator on
	# that number we return list containing three elements of length 3,3,2(which contains only boolean values).
	def getBits(self, n):
		return [n >> 5, (n & 28) >> 2, n & 3]

	#[011,010,00] ---> 104              #  this function takes list containing three elements, containing boolean values
	# only, of length 3,3,2 and by using bitwise operator we return a number combination of all boolean values.
	def getByte(self, bits):
		return (((bits[0] << 3) | bits[1]) << 2) | bits[2]

	def normalize_signature(self, x):         # this function takes the signature and normalize it to the length of SIGNATURE_LENGTH(100 in this case) by putting '*' at the end places if the length of the sign is less than SIGNATURE_LENGTH and return the same.
		return  x[:self.SIGNATURE_LENGTH].ljust( self.SIGNATURE_LENGTH,'*')

	def getEmbeddingPoints(self):           # this function return the lit of dimensions of points(x,y) where you want to embed the message
		return [(8, x*2) for x in range(self.SIGNATURE_LENGTH) ]

# Concept of Inheritance
class Embed(digital_signature):
	def __init__(self, src_img):
		digital_signature.__init__(self )
		self.source_image = src_img

	def embed(self, sign):         #this function the three arguments as -result image, source image and signature- respectively
		image = cv2.imread(self.source_image, cv2.IMREAD_COLOR)
		if image is None:
			print(self.source_image, 'not found')
			return

		normalized = self.normalize_signature(sign)
		cnt = 0
		embedAt = self.getEmbeddingPoints()        # embedAt will store the pair of values of the points where
		# message is being embedded. x and y will be taken from the first and second value of the pair resoectively.
		for x, y in embedAt:             # since embedAt has pair of values so x and y will take first and second value respectively
			data = ord(normalized[cnt])       #ord gives the ASCII of the character
			bits = self.getBits(data)
			image[x][y][2] = (image[x][y][2] & ~7) | bits[0] #red band
			image[x][y][1] = (image[x][y][1] & ~7) | bits[1]#green band
			image[x][y][0] = (image[x][y][0] & ~3) | bits[2]#blue band
			cnt+= 1
		#save back
		cv2.imwrite(self.destination_img, image)

class Extract(digital_signature):
	def __init__(self, src_image):
		digital_signature.__init__(self)

		# extraction should take place at some source image
		self.source_image = src_image

	def extract(self):
		image = cv2.imread(self.source_image, cv2.IMREAD_COLOR)
		if image is None:
			print(self.source_image, 'not found ')
			return

		extractFrom = self.getEmbeddingPoints()

		sign = ''
		for x, y in extractFrom:
			bit1 = (image[x][y][2] & 7) #red band
			bit2 = (image[x][y][1] & 7)#green band
			bit3 = (image[x][y][0] & 3)#blue band
			data = self.getByte([bit1,bit2,bit3])
			sign = sign+ chr(data)     #chr converts ASCII to text
		#remove the padding
		return sign.strip('*')

def main():
	choice = int(input("1-> Embed Message: '\n'2-> Extract Message: "))
	try:
		src_img = input("Enter the source Image ")
	except:
		print(" File does not exit , Wrong Path: ")

	if choice == 1:
		message = input(" Enter Your Message(Max len = 100 ")
		if len(message) <= 100:
			Emb = Embed(src_img)
			Emb.embed(message)
		else:
			print("SIZE ERROR: ")
			return
	elif choice == 2:
		Ext = Extract(src_img)
		signature = Ext.extract()
		print(" The message is: " + signature)
	else:
		print("Wrong Choice !! ")
		return

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




