#Imports
import cv2
from google.colab.patches import cv2_imshow   #workaround for showing images in google colab
import numpy as np

#Get and show image
watch = cv2.imread("watch.pgm", cv2.IMREAD_GRAYSCALE)
cv2_imshow(watch)


# Get and show image
# watch = cv2.imread("/content/drive/MyDrive/ComputerVision/watch.pgm", cv2.IMREAD_GRAYSCALE)
# cv2_imshow(watch)

'''
Perform horizontal shear on input image with given angle in degrees and interpolate
'''
def horizontal_shear(in_img, angle_degrees):
  theta = angle_degrees * (np.pi/180)                       #Convert degrees to radians

  M1, N1 = in_img.shape[0], in_img.shape[1]                 #Pixel dimensions of input image
  out_img = np.zeros((M1, N1))                              #Initialise 2d array of zeros (black image)
  out_img[:,:] = 255                                        #Set all pixel intensities to white

  for i in range(M1):
    for j in range(N1):
      x, y = round(i - (M1/2)), round(j - (N1/2))           #Centering x coordinate to origin of original image
      x_new = i                                             #x coord not recalculated due to horizontal shear
      y_new = y + np.sin(theta) * x                         #Calculates new y coordinate of pixel (M1[i],M2[j])
      k = x_new                                             
      l = round(y_new) - 1                                  
      v = y_new - (l+0.5)                                 
      out_img[i,y] = (1-v) * in_img[k,l] + v * in_img[k,l+1]  #1D interpolation along direction of the shear

  return out_img

'''
Perform vertical shear on input image with given angle in degrees and interpolate
'''
def vertical_shear(in_img, angle_degrees):
  theta = angle_degrees * (np.pi/180)                       #Convert degrees to radians

  M1, N1 = in_img.shape[0], in_img.shape[1]                 #Pixel dimensions of input image
  out_img = np.zeros((M1, N1))                              #Initialise 2d array of zeros (black image)
  out_img[:,:] = 255                                        #Set all pixel intensities to white

  for i in range(M1):
    for j in range(N1):
      x, y = round(i - (M1/2)), round(j - (N1/2))           #Centering x coordinate to origin of original image
      x_new = x - np.tan(theta/2)*y                         #Calculating new x coordinate of pixel (M1[i],N1[j])
      y_new = j
      k = round(x_new) - 1                                
      l = y_new
      u = x_new - (k+0.5)                                
      out_img[x,j] = (1-u) * in_img[k,l] + u * in_img[k+1,l]  #1D interpolation along direction of the shear

  return out_img

#Rotate image about center by a given angle
angle = 26

watch_sheared = vertical_shear(horizontal_shear(vertical_shear(watch, angle), angle), angle)           #Rotate image by 26 degrees by performing a combination of 3 shears
cv2_imshow(watch_sheared)

#Shearing back 
watch_sheared_back = vertical_shear(horizontal_shear(vertical_shear(watch_sheared, -angle), -angle), -angle)  #Rotate image back to original by performing a combination of 3 shears
cv2_imshow(watch_sheared_back)

#Comparing image of watch_shearead back to the original
cv2_imshow(abs(watch - watch_sheared_back))                                                              #Show difference between original and rotated and back images
print("\nThe average difference in intensity is: ",np.mean(np.abs(watch - watch_sheared_back)))          #Print average intensity difference between original and rotated and back images