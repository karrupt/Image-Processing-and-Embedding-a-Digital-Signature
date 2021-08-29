# Image-Processing-and-Embedding-a-Digital-Signature
___
To run program in open cv you must download first python open-cv. If you don't already have it the do the following step:
```python
pip install opencv-python
```

## Improtant points to remember
1. Whenever a file is encoded the result will be available in images\encoded.png
2. When you want to extract a file you need the give the source file from where we need to extract the information.

___


Use of the functions used in the above program.

***cv2.imread()*** is used to load an image in memory (as a 3d array).
It takes 2 parameters:
1) Source File: image to load
2) flag: approach to build the memory image.
In our case we used ***cv2.IMREAD_COLOR*** that instructs
reading the image as color image.
By this the image gets 3rd dimension that stores ***BGR*** bands per pixel (and not RGB).


***cv2.imwrite()*** is used to write an image on disk.
It takes 2 parameters:
1) target File: file to save the image as. Keep it .png to avoid lossy compression (more on this ahead)
2) image : The data structure (3d or 2d array) of the image.
___
There are other functions like converting **Bits list** to a **Byte** and **vice-versa**.
Those are best explained with the following diagram.

![bitwise operator](https://github.com/proacher/Image-Processing-and-Embedding-a-Digital-Signature/blob/main/images/bitwise_operators.jpeg "how bitwise operators works")
___

### How data is changing:

![Data Changing](https://github.com/proacher/Image-Processing-and-Embedding-a-Digital-Signature/blob/main/images/data_changing.jpeg "visually no change but we have embedded what we wanted") 
