import cv2, math
import numpy as np
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow
import numpy as np
from sympy import *
import math

p_vals = np.array([[244, 263, 1], [238, 353, 1], [199, 350, 1], [201, 262,1 ]]) # pixel coords to map FROM image A (from assignment sheet)
q_vals = np.array([[232, 216, 1], [232, 311, 1], [197, 311, 1], [197, 216, 1]]) # pixels to map TO for image B (from assignment sheet)

h1, h2, h3, h4, h5, h6, h7, h8 = symbols(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'])  # create symbols

H_ = np.array([[h1, h2, h3], [h4, h5, h6], [h7, h8, 1]])  # H matrix with symbols, to be calculated as a linear system

#calculate the values of the h matrix
equations = []

#create equations for h1-h3
for i in range(len(p_vals)):
  mult = H_ @ p_vals[i]
  lhs = mult[0] / mult[2]
  rhs = q_vals[i][0] / q_vals[i][2]
  equations.append(lhs-rhs)

#create equations for h4-h9
for i in range(len(p_vals)):
  mult = H_ @ p_vals[i]
  lhs = mult[1] / mult[2]
  rhs = q_vals[i][1] / q_vals[i][2]
  equations.append(lhs - rhs)

sol = solve(equations, [h1, h2, h3, h4, h5, h6, h7, h8])  # Calculate the values of the matrix from the created equations, as a system
sol['h9'] = 1

h = np.array([x for x in sol.values()], dtype='float').reshape(3,3) # Re-create h matrix after value calculation
print(h)

# Load in the image here
A = cv2.imread("homework4.pbm", cv2.IMREAD_GRAYSCALE)
cv2_imshow(A)

inv_h = np.linalg.inv(np.array(h))
old_dim = A.shape
new_dim = (300, 370)

# Generate empty image (array) of zeros with the correct dimensions
B = np.zeros(new_dim)

# Calcualte pixels of new image by using the inverse of the transofrmation h
for i in range(new_dim[0]): 
  for j in range(new_dim[1]):

    r = inv_h @ np.array([i, j, 1])
    r = np.floor(r/r[2])

    # Make sure that the dimensions are within bounds
    if (r[0] > 0 and r[1] > 0 and r[0] < new_dim[0] and r[1] < old_dim[1]):
      B[i, j] = A[int(r[0]),int(r[1])]

cv2_imshow(B)

# Function to create bilinear interpolation on the input image_pixels with the input dimensions
def bi_interpol(pic, dim):

  # Dimenstions of image after interpolation
  new_height = dim[0]
  new_width = dim[1]

  # Dimenstions of pre-interpolated image
  old_height = pic.shape[0]
  old_width = pic.shape[1]

  new_pic = np.zeros([new_height, new_width])

  width_prop = float(old_width - 1)/(new_width-1)
  height_prop = float(old_height-1)/(new_height-1)

  # Interpolate image by calculating new pixels
  for i in range(new_height):
    for j in range(new_width):

      x = int(np.floor(width_prop*j))
      y = int(np.floor(height_prop*i))
      x_ = int(np.ceil(width_prop*j))
      y_ = int(np.ceil(height_prop*i))

      x_inten = (width_prop*j)-x
      y_inten = (height_prop*i)-y
      a_1, a_2, a_3, a_4 = pic[y, x], pic[y, x_], pic[y_, x], pic[y_, x_]

      new_pic[i, j] = a_1*(1-x_inten)*(1-y_inten) + a_2*x_inten*(1 - y_inten) + a_3*x_inten*(1-x_inten) + a_4*x_inten*y_inten

  return new_pic

B_inter = bi_interpol(B, new_dim) # Calculate output image after bilinear interpolation

cv2_imshow(B_inter)