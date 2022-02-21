# CVPR-21

Computer Vision and Pattern Recognition assignments in collaboration with [@akbazuka](https://github.com/akbazuka)

Included are implementations of:

## Image rotation by shearing ##

With a composition of 3 successive shears we can rotate an image by an arbitrary angle in the interval [-\pi,\pi] radians due to the following laws of affine transformations: 
- previously parallel affine subspaces will remain parallel after an affine transformation
- ratios of distances between points on a line will remain constant

This implementation uses horizontal -> vertical -> horizontal shears

**Example: 26 degrees clockwise**

     Before           Shear 1           Shear 2         Shear 3 (result)

<img src="https://user-images.githubusercontent.com/45520841/155027729-e842dbf8-3a81-4129-913e-99709cf259fc.png" alt="original" width="220"/> <img src="https://user-images.githubusercontent.com/45520841/155026937-86762809-c63f-458f-82ee-2b648d3f5741.png" alt="shear1" width="220"/>
<img src="https://user-images.githubusercontent.com/45520841/155026958-1421e5f6-0abd-4ee9-b396-abc8aff7424e.png" alt="shear2" width="220"/>
<img src="https://user-images.githubusercontent.com/45520841/155027012-d37c43bc-b977-4b06-b54a-704b493c43dd.png" alt="shear3" width="220"/>


There is the necessity of 1-D interpolation in the direction of each shear due to images existing in a discrete domain; this results in a loss of information that is evaluated in the code. For example, in the case of the above image the difference after rotating back to the original orientation results in the difference image below. 

<img src="https://user-images.githubusercontent.com/45520841/155029333-2635e8b7-d8f8-495c-94cb-3871ed712820.png" alt="difference" width="220"/>

Where pixel value scales from black (no difference) to white (maximal difference). This mostly occurs in regions where there is a large change in pixel values, i.e edges.

## Histogram Equalisation ##

