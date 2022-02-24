#Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow

print('Original Image: ')
#Read img
A = cv2.imread("dog.pgm", cv2.IMREAD_GRAYSCALE)
cv2_imshow(A)

L = 256

# Get height and width of image
M = A.shape[0]
N = A.shape[1]

print('Histogram and Discrete CDf of Original Image: ')

# Normalized histogram and discrete cumulative distribution function; histogram of an original image
P, bins, ignored = plt.hist(A.ravel(), L, [0,L], density=True)
Pbar = np.zeros((L+1))
for i in range(1,L+1):
  Pbar[i] = Pbar[i-1] + P[i-1]
plt.plot(range(0,L+1), Pbar*max(P), color='r')
plt.show()

def relevant_neighbours(pixel, neighbours):
  good_neighbours = [pixel]
  for i in neighbours:
    if (abs(pixel-i) <= 2):
      good_neighbours.append(i)
  return good_neighbours

#Pre-processing A; (2) in Assignment
for i in range(0,M):
  for j in range(0,N):

    #Top row
    if i == 0:
      if j == 0: 
        A[i,j] = np.floor(np.mean(relevant_neighbours(A[i,j], [A[i+1,j], A[i+1,j+1], A[i,j+1]])))                           #Top-left corner
      elif j == N-1:
        A[i,j] = np.floor(np.mean(relevant_neighbours(A[i,j], [A[i+1,j], A[i,j-1], A[i+1,j-1]])))                           #Top-right corner
      else:
        A[i,j] = np.floor(np.mean(relevant_neighbours(A[i,j], [A[i,j-1], A[i+1,j-1], A[i+1,j], A[i+1,j+1], A[i,j+1]])))     #Top edge
    
    #Bottom row
    elif i == M-1:
      if j == 0:
        A[i,j] = np.floor(np.mean(relevant_neighbours(A[i,j], [A[i-1,j], A[i-1,j+1], A[i,j+1]])))                           #Bottom-left corner
      elif j == N-1:
        A[i,j] = np.floor(np.mean(relevant_neighbours(A[i,j], [A[i,j-1], A[i-1,j-1], A[i-1,j]])))                           #Bottom-right corner
      else:
        A[i,j] = np.floor(np.mean(relevant_neighbours(A[i,j], [A[i,j-1], A[i-1,j-1], A[i-1,j], A[i-1,j+1], A[i,j+1]])))     #Bottom edge

    #Left side column excluding the corners
    elif (j == 0 and i != 0) or (j==0 and i!= M-1):
      A[i,j] = np.floor(np.mean(relevant_neighbours(A[i,j], [A[i-1,j], A[i-1,j+1], A[i,j+1], A[i+1,j+1], A[i+1,j]])))

    #Right side column excluding the corners
    elif (j == N-1 and i != 0) or (j==N-1 and i!= M-1):
      A[i,j] = np.floor(np.mean(relevant_neighbours(A[i,j], [A[i-1,j], A[i-1,j-1], A[i,j-1], A[i+1,j-1], A[i+1,j]])))

    #All other cases
    else:
      A[i,j] = np.floor(np.mean(relevant_neighbours(A[i,j],[A[i+1,j], A[i+1,j+1], A[i,j+1], A[i-1,j], A[i,j-1], A[i-1,j-1], A[i+1,j-1], A[i-1,j+1]])))

#Equalize image by creating linear histogram
F = []
pixels_per_intensity = int(np.floor(len(A.ravel())/L))
for i in range(1, L):
  for j in range(0, pixels_per_intensity-1):
    F.append(i)

Q, bins, ignored = plt.hist(F, L, [0,L], density=True) #Bins are the number of intensity values
Qbar = np.zeros((L+1))
for i in range(1,L+1):
  Qbar[i] = Qbar[i-1] + Q[i-1]
plt.plot(range(0,L+1),Qbar*max(Q),color='r')
plt.show()

print('Pre-processed image matched to equalised histogram: ')

# Histogram matching
C = np.zeros((M,N))
for i in range(0,M):
  for j in range(0,N):
    k = A[i,j]
    z = 0.5 * (Pbar[k]+Pbar[k+1])
    m = 0
    while Qbar[m+1] < z:
      m = m + 1
    Ls = m + (z-Qbar[m]) / Q[m]
    C[i,j] = np.round(Ls - 0.5)
cv2_imshow(C)

# Histogram and Discrete CDF of equalised result
R, bins, ignored = plt.hist(C.ravel(), L, [0,L], density=True)
Rbar = np.zeros((L+1))
for i in range(1,L+1):
  Rbar[i] = Rbar[i-1] + R[i-1]
plt.plot(range(0,L+1),Rbar*max(R),color='r')
plt.show()

cv2_imshow(abs(A - C)) #Difference between pre-processes + equalized image, and the original image
