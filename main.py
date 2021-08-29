#Main purpose of this program is to
#Embed a digital signature in images to
#prove ownership in case of piracy
import cv2
import os
class digital_signature:
	def __init__(self):
		self.source_image = ""
		# whenever something is embedded it will be embedded in the below file
		self.destination_img = "images\encoded.png"
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

	def embed(self, sign):         #this function takes signature
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
	src_img = input("Enter the source Image ")
	if os.path.exists(src_img) == False:
		print(src_img + "file does not exit , Wrong Path: ")
		return
	choice = int(input("1-> Embed Message \n2-> Extract Message \nYour Choice: "))
	if choice == 1:
		message = input(" Enter Your Message(Max len = 100): ")
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



