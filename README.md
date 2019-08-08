LGenerator
This is my Master's thesis code for creating artificial point clouds from simple defined geometry or STL files.
The code works as a pipeline where the end product is an HDF5-file.

The goal is to create a so called scene where different element geometries are placed and scaled randomly without overlaps.
The scene is then cut into rectangular equally sized slices and put together into batches where the corresponding PointNet
is trained on. Every point has an additional fourth coordinate which indicates the class of the object it represents.

The PointNet can be views as a Convolutional Neuronal Network but for 3D points rather than pixels. These minor detail causes
a lot of difficulty for the NN because there is no uniform way to define a neighborhood and the point set's order must not influence
the net's final decision.

This approach was chosen, because of the lack of labeled training data (as so often) of construction site related point clouds.
PointNet and PointNet2 were trained on the DGX/P100-cluster from the LRZ in Garching. Due to this approach I had sufficient training,
test and validation data at hand to properly train the NN. The results on the test data were reasonable.

![Green: correctly classified points](https://github.com/CheesyB/PCLGenerator/blob/master/pics/11Classes.png)
![test case on realworld data](https://github.com/CheesyB/PCLGenerator/blob/master/pics/result_inference_with_origin.png-1.png)
![problem on too big items](https://github.com/CheesyB/PCLGenerator/blob/master/pics/Results_twoPartsNotRecognizingpdf.pdf-1.png)
