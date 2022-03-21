#AK_GT_ComputerVision_Hw3

import cv2, math
import numpy as np
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow # remove this if not using Colab import matplotlib.pyplot as plt

# Read image
A = cv2.imread("building.tif", cv2.IMREAD_GRAYSCALE)
cv2_imshow(A)

# Compute gradient magnitude
G_x = cv2.Sobel(A,cv2.CV_64F,0,1)
G_y = cv2.Sobel(A,cv2.CV_64F,1,0)
G = np.abs(G_x) + np.abs(G_y)
# G = np.sqrt(np.power(G_x,2)+np.power(G_y,2)) 
G = G/np.max(G)*255
cv2_imshow(G)

n = A.shape[0]
m = A.shape[1]

#Define bin ranges for rho and theta values
theta_max = 90
theta_min = -89
n_squared = math.pow(n, 2)
m_squared = math.pow(m, 2)
rho_max = int(math.sqrt(n_squared + m_squared))
rho_min = -int(math.sqrt(n_squared + m_squared))

#Calculate the bins of the Hough Space for the Rho and Theta values
thetas = [np.deg2rad(x) for x in range(theta_min, theta_max+1)]
rhos = [x for x in range(rho_min, rho_max+1)]

H = [[0 for x in range(len(thetas))] for y in range(len(rhos))]         #Initialise Hough Space

'''
Populate the Hough Space (takes about 5 minutes)
'''
# Iterate through all pixels in input image
for i in range(n):
  for j in range(m):
    # Iterate through all theta values to fill matrix
    for theta_idx, theta_val in enumerate(thetas):
      rho_val = int(i*np.cos(theta_val) + j*np.sin(theta_val))          # Calculate the rho value for the corresponding theta value
      H[rho_val+rho_min][theta_idx] += G[i,j]                           # Add magnitude to index in Hough Space

peak_index = np.argmax(H)                                               # Calculate the peak of the Hough Space
hough_space_dim = (len(H), len(H[0]))                                   # Dimensions of the Hough Space
peak_indeces = np.unravel_index(peak_index, hough_space_dim)            # Retrieve the 2d indexes of the peak

# Retrieve the final theta and rho values from the peak to get the steepest angle
theta_index = peak_indeces[1]
rho_index = peak_indeces[0]
final_theta = thetas[theta_index]
final_rho = rhos[rho_index]

#Function to draw a line on an image based on input rho and theta values
def draw_line(A,rho,theta):
  # A - MxN original input image
  # rho - 1x1 $\rho$ of peak
  # theta - 1x1 $\theta$ of peak
  x = np.arange(0,A.shape[0])
  y = (rho - x * math.cos(theta)) / math.sin(theta)
  fig, ax = plt.subplots()
  ax.imshow(A, cmap='gray', vmin=0, vmax=255)
  ax.plot(y, x, '-', linewidth=2, color='red')
  plt.xlim(0,A.shape[1]-1)

draw_line(A,final_rho,final_theta)                                      #Draw steepest angle line along the input image