# Surfe's Inputs and Outputs

Definitions

*Interface*: a boundary surface separating two different regions. E.g. interface that separates two lithologies, a fault surface that separates two continuous domains/volumes

*CPD function*: Conditionally Positive Definite function. Conditional in the sense that the interpolation matrix is positive definite subject to the orthogonality constraints provided by the polynomial in the null space.

*SPD function*: Strictly Positive Definite function. A Gramm matrix (e.g. our interpolation matrices) generated by such a function/kernel will have all of items eigenvalues positive.

All input parameters and constraints as well as outputs to the Surfe interpolant are made through the Surfe_API class.

## Input Parameters

***Modelling method***
The modelling method parameter initializes the Surfe_API object.

Set by
```cpp
Surfe_API(const int &modelling_method)
```

Usage example:
```cpp
Surfe_API surfe(1); // Single Surface method
Surfe_API *surfe = new Surfe_API(2); // Lajaunie method
```

Acceptable integer values:
* **1** : Single_surface
  * Models a single interface surface. No increment points are used in this method and therefore is faster to obtain the interpolant and evaluate it at a list of points.
* **2** : Lajaunie_approach
  * Models multiple conformal interface surfaces. Increment points are used in this method.
* **3** : Vector_field
  * Models vectors fields from gradient and tangent constraints. Does not incorporate interface or increment constraints.
* **4**: Stratigraphic_horizons
  * Models multiple conformal interface surfaces with additional constraints on the order in which the layers/interfaces where deposited/created. E.g. Layer A is on top/younger of Layer B, Layer B is on top/younger of Layer C. This method is very useful in situations where the data does not sample the volume optimally. E.g. Interface data obtain from outcrops (horizon sampling bias) – Lajaunie method fails in these situation: The increment constraint only indicate that points on the same interface have the same scalar value – nothing about the order of these interfaces are imposed by such constraints. 
* **5**: Continuous_property
  * Models scalar data like assay data, points sampling a function like a fourier series. Does not incorporate gradient constraints.

***RBF Kernel***
The type of RBF/Kernel used in the interpolant.

Note: If CPD kernels are used special care must be taken when using inequality constraints. This is because a convex optimization problem must be solved in this case. As such, these methods require a SPD matrices. To make our matrices PD we use Lagrangian polynomial basis to ensure our functional space resides within a Reproducing Hilbert Kernel Space. Currently, the only CPD function that is supported is the cubic in these cases.

Acceptable strings:
* "r3" : <img src="https://latex.codecogs.com/svg.latex?\Large&space;\phi(r)=r^3" /> (CPD)
* "Gaussian" : <img src="https://latex.codecogs.com/svg.latex?\Large&space;\phi(r)=e^{-\epsilon^2r^2}" /> (SPD)
* "Multiquadrics":  <img src="https://latex.codecogs.com/svg.latex?\Large&space;\phi(r)=\sqrt{\epsilon-r^2}" /> (CPD)
* "Inverse Multiquadrics":  <img src="https://latex.codecogs.com/svg.latex?\Large&space;\phi(r)=\frac{1}{\sqrt{\epsilon-r^2}}" /> (SPD)
* "Thin Plate Spline": <img src="https://latex.codecogs.com/svg.latex?\Large&space;\phi(r)=r^4log(r)" /> (CPD)
* "r": <img src="https://latex.codecogs.com/svg.latex?\Large&space;\phi(r)=r" /> (CPD)
* "WendlandC2": <img src="https://latex.codecogs.com/svg.latex?\Large&space;\phi(r)=(1-r)^4(1+4r)\text{if}r<r_{cutoff}\text{otherwise}\phi(r)=0" /> (SPD)
* "MaternC4": <img src="https://latex.codecogs.com/svg.latex?\Large&space;\phi(r)=e^{-{\epsilon}r}(3+3{\epsilon}r+\epsilon^2r^2)" /> (SPD)

**Important**: For SPD kernels, a shape parameter is also needed. This is set by

```cpp
surfe.SetRBFShapeParameter(const double &shape_parameter);
```

***Polynomial order***
Polynomials of the correct minimum order are required for CPD kernels to ensure an unique minimum norm interpolant. For cubic kernels the minimum order is 1. These polynomials are the drift functions in co-kriging.

Acceptable integer values:
* **0** order: <img src="https://latex.codecogs.com/svg.latex?\Large&space;P=c(constant)" />
* **1** order: <img src="https://latex.codecogs.com/svg.latex?\Large&space;P=ax+by+cz+d" />
* **2** order: <img src="https://latex.codecogs.com/svg.latex?\Large&space;P=ax^2+by^2+cz^2+dxy+exz+fyz+gx+hy+iz+j" />

***Regression Smoothing***
Regression smoothing creates an approximate interpolant instead of exact fitting. Exact fitting with real (non-synthetic data) will likely produce topological errors especially with noisy or highly varying data. If a threshold for fitting data constraints is given effectively a least squares minimization is applied to residuals. In the co-kriging world this is the nugget effect.

Set by
```cpp
surfe.SetRegressionSmoothing(const bool &use_regression_smoothing, const double &amount);
```
Note: Depending on the kernel used and the structural complexity sampled by the data, the value specified does not necessarily correspond to physical interpretable meaning: e.g. distance

***Greedy Algorithm***
Reduces the number of data constraints (a.k.a centers in approximation theory) used by the interpolant while also accurately approximating the interpolant. Effectively this is a massive speed boost in evaluation of the interpolant. This algorithm will start with the minimum number of constraints needed to obtain an interpolant, then the interpolant will be evaluated at every data constraint which was not included into the interpolant to measure residuals (how much discrepancy there is). A small number of residuals beyond the user specified residual threshold will then be added to the interpolant until all residuals are below this threshold. A threshold for interface data and orientation data are required.

Set by
```cpp
surfe.SetRegressionSmoothing(const bool &use_greedy, const double &interface_uncertainty, const double &angular_uncertainty);
```
Note: The disadvantage of this method is that a bias is placed on outliers. Also note, that support for this method is very limited. I believe only single surface method is support.

Interface residual at point <img src="https://latex.codecogs.com/svg.latex?\Large&space;x_i" /> not included in interpolant: <img src="https://latex.codecogs.com/svg.latex?\Large&space;|s(x_i)-f(x_i)|<f_{threshold}" /> where f is the scalar field constraint for the interface point. For single surface methods, this is set to 0. 

Orientation residual at point <img src="https://latex.codecogs.com/svg.latex?\Large&space;x_i" /> not included in interpolant: <img src="https://latex.codecogs.com/svg.latex?\Large&space;\theta=arccos(\frac{{\nabla}s(x_i){\cdot}{\nabla}f(x_i)}{\|{\nabla}s(x_i)\|{\cdot}\|{\nabla}f(x_i)\|})<\theta_{threshold}" />

***Restricted Range***
This option is somewhat like the greedy algorithm but does not suffer from the bias of outliers. All data constraints are included into the interpolant, and every data constraint has a bound on it where the smoothest interpolant is to be constrained within. To obtain such an interpolant a quadratic optimization problem is solved, which introduces computational overhead. But only finding the interpolant compute time is affected, the evaluation of the interpolant at user specified points is not affected.

For interface points:  <img src="https://latex.codecogs.com/svg.latex?\Large&space;s(x_i)-interface_{uncertainty}<s(x_i)<s(x_i)+interface_{uncertainty}" />
For orientation onts:  <img src="https://latex.codecogs.com/svg.latex?\Large&space;0<\theta=arccos(\frac{{\nabla}s(x_i){\cdot}{\nabla}f(x_i)}{\|{\nabla}s(x_i)\|{\cdot}\|{\nabla}f(x_i)\|})<\theta_{uncertainty}" />

Set by
```cpp
surfe.SetRestrictedRange(const bool &use_restricted_range, const double &interface_uncertainty, const double &angular_uncertainty);
```

***Global Anisotropy***
This option derives principle directions of anisotropy using all supplied planar/gradient constraints. These directions are used to modified how distances are computed. Works well if modelled structures are very global. However, works very poorly when plunge of structures largely vary.

Set by
```cpp
surfe.SetGlobalAnisotropy(const bool &g_anisotropy);
```

## Input Constraints

There are 4 types on data constraints that can be supplied into surfe: 

1. ***Interface constraints***
  * 3D points sampling an interface that separates two volumetric domains (e.g. lithologies, fault domains)
  * (x, y, z, level)
    * Level is a float value that organizes the stratigraphic order of the interfaces and lithologies (via inequalities). **Important**: Larger level values are younger (on top) than smaller level values (on bottom). Points sampling the same interface must have the same level value.
    * Note: If only one interface is being model, any level value can be chosen. Normally 0 is specified in this case.
  * Added by
  ```cpp
surfe.AddInterfaceConstraint(const double &x,const double &y,const double &z,const double &level);
```
  * Added by
 ```cpp
surfe.SetInterfaceConstraints(const MatrixXd &interface_constraints);
```
Accepted structure for MatrixXd:

Nx4 matrix, N = number of interface points

Columns: x, y, z, level

**Note**: In python, MatrixXd is a numpy array

2. ***Planar constraints***
  * 3D points that have normal (Younging) information attributed to them. The normal indicates the direction in which younger stratigraphy is found. If fault surfaces are being modelled, the polarity of the normal does not matter.
  * There are four ways planar constraints can be added:
1. Supply normal vector
```cpp
surfe.AddPlanarConstraintwNormal(const double &x,const double &y,const double &z,
const double &nx,const double &ny,const double &nz);
```
2. Supply strike, dip, polarity
  * Note polarity has two acceptable values: 0 == upright, 1 == overturned (points down)  
```cpp
surfe.AddPlanarConstraintwStrikeDipPolarity(const double &x,const double &y,const double &z,
const double &strike, const double &dip, const int &polarity);
```
3. Supply azimuth, dip, polarity
  * Note polarity has two acceptable values: 0 == upright, 1 == overturned (points down)
  * Note that azimuth is the same as dip direction     
 ```cpp
surfe.AddPlanarConstraintwAzimuthDipPolarity(const double &x,const double &y,const double &z,
const double &azimuth,const double &dip,const int &polarity);
```
4. Supply a matrix or array
```cpp
surfe.SetPlanarConstraints(const MatrixXd &planar_constraints);
```

Accepted structure for MatrixXd:

Nx6 matrix, N = number of planar points

Columns: x, y, z, nx, ny, nz

3. ***Tangent constraints***
  * 3D points that have vector <img src="https://latex.codecogs.com/svg.latex?\Large&space;\vec{t}" /> attributed to them. The relationship between this vector and the scalar field is <img src="https://latex.codecogs.com/svg.latex?\Large&space; {\nabla}s(x_i){\cdot}{\vec{t}=0" />. In other words, the vector <img src="https://latex.codecogs.com/svg.latex?\Large&space;\vec{t}" /> is orthogonal (90°) with respect to the gradient of the scalar field  <img src="https://latex.codecogs.com/svg.latex?\Large&space; {\nabla}s(x_i)" />. This constraint does not have a lot of effect on changing the modeled geometry since there is a large amount of freedom with fitting this constraint. However, if a lot of these are specified in addition to supplying two tangent constraints at the same point (different vectors!) then this constraint can be useful especially for foliation orientations (there is no polarity).
  * Added by
```cpp
surfe.AddTangentConstraint(const double &x,const double &y,const double &z,
const double &tx,const double &ty,const double &tz);
```
  * Added by
```cpp
surfe.SetTangentConstraints(const MatrixXd &tangent_constraints);
```

Accepted structure for MatrixXd:

Nx6 matrix, N = number of tangent points

Columns: x, y, z, tx, ty, tz

4. ***Inequality constraints***
  * 3D points sampling lithologies or inside/outside points relative to an interface/s. E.g. Does not belong to an interface. Very useful constraint since observing interface between lithologies is extremely rare and this is the most abundant type of data especially for Geological surveys.
  * (x, y, z, level)
    * Note: the level property has to be compatible and make sense with respect to the level property of the interface level property. For example, you can’t have an inequality point having the same level value as an interface point.
  * Added by
```cpp
surfe.AddInequalityConstraint(const double &x,const double &y,const double &z,const double &level);
```
  * Added by
```cpp
surfe.SetInequalityConstraints(const MatrixXd &inequality_constraints);
```

Accepted structure for MatrixXd:

Nx4 matrix, N = number of inequality points

Columns: x, y, z, level

## Outputs

***Scalar field***
Obtain the value of the scalar field at a 3D point

Get by
```cpp
surfe.EvaluateInterpolantAtPoint(const double &x,const double &y,const double &z);
```
**Returns** a double

***Gradient field***
Obtain the gradient of the scalar fied at a 3D point

Get by
```cpp
surfe.EvaluateVectorInterpolantAtPoint(const double &x,const double &y,const double &z);
```
**Returns** a 3D vector

***Spatial Parameters***
Obtain spatial metrics of the inputted data constraints

Get by
```cpp
surfe.GetDataBoundsAndResolution();
```
**Returns** a data structure called SpatialParameters

SpatialParameters data members: xmin, xmax, ymin, ymax, zmin, zmax, resolution

Note: *resolution* is the spatial resolution required to model the structural variability.

***Interface Reference Points***
For every interface being model there is a reference point for that interface (used for increments). Getting these reference points is critical when increments are used to model multiple conformal surfaces. This is because we don’t know what the scalar field values are associated to the interfaces. These values are need when applying marching cubes/tetrahedral algorithms to extract the iso surface from the modelled scalar field. The get these values you need to evaluate the interpolant at these reference points.

Get by
```cpp
surfe.GetInterfaceReferencePoints(); 
```
**Returns** an array/matrix
* Nx3 matrix, N = number of intefaces

***Number of Interfaces***
Gets the number of modeled interfaces by the interpolant.

Get by
```cpp
surfe.GetNumberOfInterfaces();
```
**Returns** an integer

***Has Interpolant been computed***
This is a convenience method to determine whether or not the interpolant has been computed yet.

Get by
```cpp
surfe.InterpolantComputed(); 
```
**Returns** a Boolean

