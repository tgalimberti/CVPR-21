# CVPR-21

Computer Vision and Pattern Recognition assignments in collaboration with [@akbazuka](https://github.com/akbazuka)

Included are implementations of:

## Image rotation by shearing ##

With a composition of 3 successive shears we can rotate an image by an arbitrary angle in the interval [-\pi,\pi] radians due to the following laws of affine transformations: 
- previously parallel affine subspaces will remain parallel after an affine transformation,
- ratios of distances between points on a line will remain constant.

This implementation uses horizontal -> vertical -> horizontal shears

**Example: 26 degrees clockwise**

     Before     ->    Shear 1     ->    Shear 2    ->  Shear 3 (result)
     
<img src="https://user-images.githubusercontent.com/45520841/155027729-e842dbf8-3a81-4129-913e-99709cf259fc.png" alt="original" width="200"/> <img src="https://user-images.githubusercontent.com/45520841/155026937-86762809-c63f-458f-82ee-2b648d3f5741.png" alt="shear1" width="200"/>
<img src="https://user-images.githubusercontent.com/45520841/155026958-1421e5f6-0abd-4ee9-b396-abc8aff7424e.png" alt="shear2" width="200"/>
<img src="https://user-images.githubusercontent.com/45520841/155027012-d37c43bc-b977-4b06-b54a-704b493c43dd.png" alt="shear3" width="200"/>


There is the necessity of 1-D interpolation in the direction of each shear due to images existing in a discrete domain; this results in a loss of information that is evaluated in the code. For example, in the case of the above image the difference after rotating back to the original orientation results in the difference image below:

<img src="https://user-images.githubusercontent.com/45520841/155029333-2635e8b7-d8f8-495c-94cb-3871ed712820.png" alt="difference" width="220"/>

where pixel value scales from black (no difference) to white (maximal difference). This mostly occurs in regions where there is a large change in pixel values, i.e. edges.

## Histogram Equalisation ##

**Image and its pixel intensity distribution + CDF before equalisation**

<img src="https://user-images.githubusercontent.com/45520841/159370505-c612318b-799b-414d-9c7f-c4853adb6cc5.png" alt="original" width="324"> <img src="https://user-images.githubusercontent.com/45520841/159371431-94e46b00-c730-4c31-bf1c-8b2e63c58484.png" alt="originalhist" width="500">

For the above image, the bimodal peak in the pixel intensity graph shows us that the majority of the pixel values lie around the values of 25 and 200. This can also by seen by the comparitive steepness of the CDF in those regions. The aim of pixel equalisation is to achieve a more 'flat' distribution such that all the pixel values are evenly used. The result of this and the corresponding distribution are below:

**Image and its pixel intensity distribution + CDF after equalisation**

<img src="https://user-images.githubusercontent.com/45520841/159370528-6a25ccee-b984-4ad4-9c2e-4337a40e1f6d.png" alt="equalised" width = "324"> <img src="https://user-images.githubusercontent.com/45520841/159371438-3bcd6647-d28b-450a-adfc-69aebff19072.png" alt="equalhist" width="500">

The even distribution is achieved by stretching the 'overpopulated' pixel values out across a wider range vice-versa for the 'underpopulated' values.

## Edge Detection ##
More specifically, locating the edge of greatest gradient within an image using a 2 step process:
-   Apply the Sobel operator from the cv2 library to highlight the edges within the image.

           Before:                       After:

<img src="https://user-images.githubusercontent.com/45520841/159376880-70ec85d0-7dc9-4727-a275-63fea1b49097.png" alt="original" width = "400"> <img src="https://user-images.githubusercontent.com/45520841/159377508-55315534-0d7c-4ae8-aaf3-64d557b81e14.png" alt="operated" width = "400">

-   Populate a Hough space from the operated image parametrised by \rho and \theta to find the region with largest \theta then overlay the corresponding line on the original image.
<img src="https://user-images.githubusercontent.com/45520841/159376876-b8062588-b0ef-4bed-b877-22b4da3e9423.png" alt ="graddetect" width = "500">



