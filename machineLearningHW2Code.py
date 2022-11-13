# -*- coding: utf-8 -*-
"""fall2022_hw2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gdAEW2wSOs4ygJSk_bxZvX_5lkiUYD8H

# CS171-EE142 - Fall 2022 - Homework 2

# Due: Thursday, October 28, 2022 @ 11:59pm

### Maximum points: 100 pts


## Submit your solution to Gradescope:
1. Submit a single PDF to **HW2**
2. Submit your jupyter notebook to **HW2-code**

Notice:
In Markdown, when you write in LaTeX math mode, do not leave any leading and trailing whitespaces inside the dollar signs ($). For example, write `(dollarSign)\mathbf(dollarSign)(dollarSign)` instead of `(dollarSign)(space)\mathbf{w}(dollarSign)`. Otherwise, nbconvert will throw an error and the generated pdf will be incomplete. [This is a bug of nbconvert.](https://tex.stackexchange.com/questions/367176/jupyter-notebook-latex-conversion-fails-escaped-and-other-symbols)

**See the additional submission instructions at the end of this notebook**

## Enter your information below:

### Your Name (submitter): Alexander Kaattari-Lim

### Your student ID (submitter): 862161616 
    
    
<b>By submitting this notebook, I assert that the work below is my own work, completed for this course.  Except where explicitly cited, none of the portions of this notebook are duplicated from anyone else's work or my own previous work.</b>


## Academic Integrity
Each assignment should be done  individually. You may discuss general approaches with other students in the class, and ask questions to the TAs, but  you must only submit work that is yours . If you receive help by any external sources (other than the TA and the instructor), you must properly credit those sources, and if the help is significant, the appropriate grade reduction will be applied. If you fail to do so, the instructor and the TAs are obligated to take the appropriate actions outlined at http://conduct.ucr.edu/policies/academicintegrity.html . Please read carefully the UCR academic integrity policies included in the link.
"""

# Standard library imports.
import random as rand

# Related third party imports.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split 

# Local application/library specific imports.
# import here if you write .py script

"""## Question 1: Linear Regression [70 pts]
We will implement linear regression using direct solution and gradient descent. 

We will first attempt to predict output using a single attribute/feature. Then we will perform linear regression using multiple attributes/features. 

### Getting data
In this assignment we will use the Boston housing dataset. 

The Boston housing data set was collected in the 1970s to study the relationship between house price and various factors such as the house size, crime rate, socio-economic status, etc.  Since the variables are easy to understand, the data set is ideal for learning basic concepts in machine learning.  The raw data and a complete description of the dataset can be found on the UCI website:

https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.names
https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.data

or 

http://www.ccs.neu.edu/home/vip/teach/MLcourse/data/housing_desc.txt

I have supplied a list `names` of the column headers.  You will have to set the options in the `read_csv` command to correctly delimit the data in the file and name the columns correctly.
"""

names = [
    'CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 
    'AGE',  'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'PRICE'
]

df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.data',
                 header=None,delim_whitespace=True,names=names,na_values='?')

df

"""### Basic Manipulations on the Data

What is the shape of the data?  How many attributes are there?  How many samples?
Print a statement of the form:

    num samples=xxx, num attributes=yy
"""

#number of samples is the amount of rows
print("num samples=", end='')
print(len(df.index), end='')
print(', ', end='')

print("num attributes=", end='')
print(len(df.columns), end='')
print(',', end ='')

numRows = len(df.index)
numFeatures = len(df.columns)

print(" data shape= ", end ='')
print(numRows, 'x', numFeatures )

"""In order to properly test linear regression, we first need to find a set of correlated variables, so that we use one to predict the other. Consider the following scatterplots:"""

# RM - average number of rooms per dwelling
# LSTAT - % lower status of the population

sns.pairplot(df[['RM','LSTAT','PRICE']])

"""Create a response vector `y` with the values in the column `PRICE`.  The vector `y` should be a 1D `numpy.array` structure."""

# TODO 
y = df['PRICE']
y = np.array(y)

#print(y)

"""Use the response vector `y` to find the mean house price in thousands and the fraction of homes that are above $40k. (You may realize this is very cheap.  Prices have gone up a lot since the 1970s!).   Create print statements of the form:

    The mean house price is xx.yy thousands of dollars.
    Only x.y percent are above $40k.
"""

# TODO 
house_price_mean = np.mean(y)
print('The mean house price is ', end = '')
house_price_mean = round(house_price_mean, 2) * 1000
print('$', end='')
print(house_price_mean ,'thousands of dollars.')

above_40k_cnt = 0

for i in y :
  if i > 40.0 :
    above_40k_cnt += 1

frac_above_40k = (above_40k_cnt / len(y)) * 100
frac_above_40k = round(frac_above_40k, 0)
print('Only', frac_above_40k, 'percent are above $40k.')

"""### Visualizing the Data

Python's `matplotlib` has very good routines for plotting and visualizing data that closely follows the format of MATLAB programs.  You can load the `matplotlib` package with the following commands.
"""

# Commented out IPython magic to ensure Python compatibility.
import matplotlib
import matplotlib.pyplot as plt
# %matplotlib inline

"""Similar to the `y` vector, create a predictor vector `x` containing the values in the `RM` column, which represents the average number of rooms in each region."""

# TODO
x = np.array(df['RM'])
#print(x)

"""Create a scatter plot of the price vs. the `RM` attribute.  Make sure your plot has grid lines and label the axes with reasonable labels so that someone else can understand the plot."""

# TODO
plt.title('The Effect of Room Numbers on Price')
plt.xlabel('Average Number of Rooms')
plt.ylabel('Price (in thousands of dollars)')
plt.grid()
plt.scatter(x, y)
plt.show()

"""The number of rooms and price seem to have a linear trend, so let us try to predict price using number of rooms first.

### Question 1a. Derivation of a simple linear model for a single feature [10 pts]
Suppose we have $N$ pairs of training samples $(x_1,y_1),\ldots, (x_N,y_N)$, where $x_i \in \mathbb{R}$ and $y_i \in \mathbb{R}$. 

We want to perform a linear fit for this 1D data as 
$$y = wx+b,$$
where $w\in \mathbb{R}$ and $b\in \mathbb{R}$. 

In the class, we looked at the derivation of optimal value of $w$ when $b=0$. The squared loss function can be written as  $$L(w) = \sum_{i=1}^N(w x_i -y_i)^2,$$ and the optimal value of $w*$ that minimizes $L(w)$ can be written as $$w^* = (\sum_{i=1}^N x_i^2)^{-1}(\sum_{i=1}^N x_i y_i)$$. 


Now let us include $b$ in our model. Show that the optimal values of $w^*,b^*$ that minimize the loss function 
$$L(w,b) = \sum_{i=1}^N(wx_i + b -y_i)^2$$ 
can be written as 
$$w^* = (\sum_i (x_i - \bar{x})^2)^{-1}(\sum_i (x_i-\bar{x})(y_i-\bar{y}))$$
and $$b^* = \bar{y} - w^*\bar{x},$$
where $\bar{x} = \frac{1}{N}\sum_i x_i, \bar{y} = \frac{1}{N}\sum_i y_i$ are mean values of $x_i,y_i$, respectively.

**TODO: Your derivation goes here.**




*   *Hint. Set the partial derivative of $L(w,b)$ with respect to $w$ and $b$ to zero.*
*   Type using latex commands and explain your steps

$$\frac{d}{dw} ( wx + b - y)^2 $$
$$\frac{d}{dw}(wx + b - y)^2 = 2(wx+b-y)(w) $$
$$w* = 2(wx+b-y)(w) = 0$$
$$b = y - wx$$

$$\frac{d}{db}(wx + b - y)^2$$
$$b* = 2(wx + b -y) $$

### Question 1b. Fitting a linear model using a single feature [10 pts] 

Next we will write a function to perform a linear fit. Use the formulae above to compute the parameters $w,b$ in the linear model $y = wx + b$.
"""

def fit_linear(x,y):
    """
    Given vectors of data points (x,y), performs a fit for the linear model:
       yhat = w*x + b, 
    The function returns w and b
    """
    # TODO complete the code below
    mean_y =np.mean(y)
    mean_x = np.mean(x)   

    xi_sub_xbar = 0
    for i in range (len(x)) :
      xi_sub_xbar = xi_sub_xbar + (x[i] - mean_x)**2

    xi_sub_xbar = xi_sub_xbar**-1 #first part of w*


    yi_sub_ybar = 0
    xi_sub_xbar_2nd_half = 0

    xi_mult_yi_sum = 0

    for i in range (len(x)) : #for second half of w*
      yi_sub_ybar = y[i] - mean_y
      xi_sub_xbar_2nd_half = x[i] - mean_x

      xi_mult_yi_sum = xi_mult_yi_sum + yi_sub_ybar * xi_sub_xbar_2nd_half

    w = xi_sub_xbar * xi_mult_yi_sum

    
    #b* depends on  w*
    b = mean_y - (w * mean_x)

    
    return w, b

"""Using the function `fit_linear` above, print the values `w`, `b` for the linear model of price vs. number of rooms."""

# TODO
w, b = fit_linear(x,y)
print('w = {0:5.1f}, b = {1:5.1f}'.format(w,b))

"""Does the price increase or decrease with the number of rooms? 

* The price increases with the number of rooms. Because y = wx + b, and in this situation w is equal to 9.1, there is a positive correlation between rooms and price. The 9.1 will continually make y increase for every increase in rooms x.

Replot the scatter plot above, but now with the regression line.  You can create the regression line by creating points `xp` from say min(x) to max(x), computing the linear predicted values `yp` on those points and plotting `yp` vs. `xp` on top of the above plot.
"""

# TODO
# Points on the regression line
plt.title('The Effect of Room Numbers on Price')
plt.xlabel('Average Number of Rooms')
plt.ylabel('Price (in thousands of dollars)')
plt.grid()
plt.scatter(x,y)
plt.plot(x, w*x+b)

"""### Question 1c. Linear regression with multiple features/attributes [20 pts]
One possible way to try to improve the fit is to use multiple variables at the same time.

In this exercise, the target variable will be the `PRICE`.  We will use multiple attributes of the house to predict the price.  

The names of all the data attributes are given in variable `names`. 
* We can get the list of names of the columns from `df.columns.tolist()`.  
* Remove the last items from the list using indexing.
"""

xnames = names[:-1]
print(names[:-1])

"""Let us use `CRIM`, `RM`, and `LSTAT` to predict `PRICE`. 

Get the data matrix `X` with three features (`CRIM`, `RM`, `LSTAT`) and target vector `y` from the dataframe `df`.  

Recall that to get the items from a dataframe, you can use syntax such as

    s = np.array(df['RM'])  
        
which gets the data in the column `RM` and puts it into an array `s`.  You can also get multiple columns with syntax like

    X12 = np.array(df['CRIM', 'ZN'])  

"""

# TODO
X = df[['CRIM', 'RM', 'LSTAT']].values
print(X)
print (X.shape)

y = df['PRICE'].values #the row number of X corresponds to the index of y
#print(y)

"""**Linear regression in scikit-learn**

To fit the linear model, we could create a regression object and then fit the training data with regression object.

```
from sklearn import linear_model
regr = linear_model.LinearRegression()
regr.fit(X_train,y_train)
```

You can see the coefficients as
```
regr.intercept_
regr.coef_
```

We can predict output for any data as 

    y_pred = regr.predict(X)

**Instead of taking this approach, we will implement the regression function directly.**

**Linear regression by solving least-squares problem (direct solution)**

Suppose we have $N$ pairs of training samples $(x_1,y_1),\ldots, (x_N,y_N)$, where $\mathbf{x}_i \in \mathbb{R}^d$ and $y_i \in \mathbb{R}$. 

We want to perform a linear fit over all the data features as 
$$y = \mathbf{\tilde w}^T\mathbf{x}+b,$$
where $\mathbf{\tilde w}\in \mathbb{R}^d$ and $b\in \mathbb{R}$. 

We saw in the class that we can write all the training data as a linear system 
$$ \begin{bmatrix} y_1 \\ \vdots \\ y_N \end{bmatrix} = \begin{bmatrix} - & \mathbf{x}_1^T & - \\ 
& \vdots & \\
- & \mathbf{x}_N^T& - \end{bmatrix} \mathbf{\tilde w} + b, $$
which can be written as 
$$ \begin{bmatrix} y_1 \\ \vdots \\ y_N \end{bmatrix} = \begin{bmatrix} 1 & \mathbf{x}_1^T \\ 
\vdots & \vdots \\
1 & \mathbf{x}_N^T\end{bmatrix} \begin{bmatrix} b \\ \mathbf{\tilde w} \end{bmatrix}.$$

Let us write this system of linear equations in a compact form as 
\begin{equation} 
\mathbf{y} = \mathbf{X}\mathbf{w}, 
\end{equation} 
where $\mathbf{X}$ is an $N \times d+1$ matrix whose first column is all ones and $\mathbf{w}$ is a vector of length $d+1$ whose first term is the constant and rest of them are the coefficients of the linear model. 

The least-squares problem for the system above can be written as 
$$\text{minimize}\; \frac{1}{2}\|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2$$
for which the closed form solution can be written as 
$$\mathbf{w} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}.$$

**Append ones to the data matrix**

To compute the coefficients $\mathbf{\tilde w}$, we first append a vector of ones to the data matrix.  This can be performed with the `ones` command and `hstack`.  Note that after we do this, `X` will have one more column than before.
"""

# TODO  
# your code here 
onesVector = np.ones((506, 1 ))
print('Shape of Ones vector:',onesVector.shape)
print('Shape of Data Vector:',X.shape)
#print(onesVector)

X = np.hstack((X, onesVector))
#print(np.hstack((X, onesVector)))
print(X)
print('Shape of X with Ones Vector Appended:', X.shape)

"""**Split the Data into Training and Test**

Split the data into training and test.  Use 30% for test and 70% for training.  You can do the splitting manually or use the `sklearn` package `train_test_split`.   Store the training data in `Xtr,ytr` and test data in `Xts,yts`.

"""

from sklearn.model_selection import train_test_split

(Xtr, Xts, ytr, yts) = train_test_split(X,y, test_size = 0.3)

"""Now let us compute the coefficients $\mathbf{w}$ using `Xtr,ytr` via the direct matrix inverse: $$\mathbf{w} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}.$$

You may use `np.linalg.inv` to compute the inverse. For a small problem like this, it makes no difference.  But, in general, using a matrix inverse like this is *much* slower computationally than using functions such as `lstsq` method or the `LinearRegression` class.  In real world, you will never solve a least squares problem like this. 
"""

# TODO
# compute w using the direct solution equation 
#Xtr = training data
#ytr = training labels
#Xts = test data
#yts = test labels

Xtr_transpose = Xtr.transpose()
#print(np.dot(Xtr_transpose, Xtr))
#print(np.shape(np.dot(Xtr_transpose, Xtr)))
Xtr_transpose_Xtr = np.dot(Xtr_transpose, Xtr) #inner product of X'X
Xtr_transpose_Xtr_in = np.linalg.inv(Xtr_transpose_Xtr) #inverse of X'X


second_half = np.dot(Xtr_transpose, ytr)
#print(np.shape(ytr))
#print(np.shape)

coeff_w = np.dot(Xtr_transpose_Xtr_in, second_half)

print(coeff_w)

"""Compute the predicted values `yhat_tr` on the training data and print the average square loss value on the training data."""

# TODO 
# your code here 
#y = Xw
yhat_tr = np.dot(Xtr, coeff_w) # calculates predicted labels 
print(yhat_tr) 

#to find the average square loss we need to iterate through the real labels 

avg_sqr_loss = 0
for i in range(len(yhat_tr)) :
  avg_sqr_loss = avg_sqr_loss + (yhat_tr[i] - ytr[i])**2

avg_sqr_loss = round(avg_sqr_loss / len(yhat_tr), 1)
print('\n')
print('The average squared loss is:', avg_sqr_loss)

"""Create a scatter plot of the actual vs. predicted values of `y` on the training data."""

# TODO 
# your code here 
plt.title('Actual Vs Predicted Values')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.grid()
plt.scatter(ytr, yhat_tr)

"""Compute the predicted values `yhat_ts` on the test data and print the average square loss value on the test data."""

# TODO 
# your code here 
#yhat_tr = np.dot(Xtr, coeff_w) # calculates predicted labels 
#print(yhat_tr) 

# avg_sqr_loss = 0
# for i in range(len(yhat_tr)) :
#   avg_sqr_loss = avg_sqr_loss + (yhat_tr[i] - ytr[i])**2

# avg_sqr_loss = round(avg_sqr_loss / len(yhat_tr), 1)
# print('\n')
# print('The average squared loss is:', avg_sqr_loss)

yhat_ts = np.dot(Xts, coeff_w) #calculates predicted labels for test data 
print(yhat_ts)

avg_sqr_loss = 0
for i in range(len(yhat_ts)):
  avg_sqr_loss = avg_sqr_loss + (yhat_ts[i] - yts[i])**2

avg_sqr_loss = round(avg_sqr_loss / len(yhat_ts),1)
print('\n')
print('The average squared loss is:', avg_sqr_loss)
print('size of test labels:', len(yts))
print('number of predicted labels:', len(yhat_ts))

"""Create a scatter plot of the actual vs. predicted values of `y` on the test data."""

# TODO 
# your code here 
plt.title('Actual Vs Predicted Values')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.grid()
plt.scatter(yts, yhat_ts)

"""### Question 1d: Gradient descent for linear regression [20 pts]
Finally, we will implement the gradient descent version of linear regression.

In particular, the function implemented should follow the following format:
```python
def linear_regression_gd(X,y,learning_rate = 0.00001,max_iter=10000,tol=pow(10,-5)):
```
Where `X` is the same data matrix used above (with ones column appended), `y` is the variable to be predicted, `learning_rate` is the learning rate used ($\alpha$ in the slides), `max_iter` defines the maximum number of iterations that gradient descent is allowed to run, and `tol` is defining the tolerance for convergence (which we'll discuss next).

The return values for the above function should be (at the least) 1) `w` which are the regression parameters, 2) `all_cost` which is an array where each position contains the value of the objective function $L(\mathbf{w})$ for a given iteration, 3) `iters` which counts how many iterations did the algorithm need in order to converge to a solution.

Gradient descent is an iterative algorithm; it keeps updating the variables until a convergence criterion is met. In our case, our convergence criterion is whichever of the following two criteria happens first:

- The maximum number of iterations is met
- The relative improvement in the cost is not greater than the tolerance we have specified. For this criterion, you may use the following snippet into your code:
```python
np.absolute(all_cost[it] - all_cost[it-1])/all_cost[it-1] <= tol
```

Gradient can be computed as $$\nabla_\mathbf{w}L = \mathbf{X}^T(\mathbf{X}\mathbf{w} - \mathbf{y}).$$

Estimate will be updated as $\mathbf{w} \gets \mathbf{w} - \alpha \nabla_\mathbf{w}L$ at every iteration. 

**Note that the $\mathbf{w}$ in this derivation includes the constant term and $\mathbf{X}$ is a matrix that has ones column appended to it.**
"""

# TODO 
# Implement gradient descent for linear regression 

def compute_cost(X,w,y):
    # your code for the loss function goes here 
    #L = 0.5*(y - np.dot(X,w))**2
    L = np.sum((y - np.dot(X,w))**2)
#    L = np.sum(np.dot(X,w) - y)**2
    L = L / len(X) 

    return L

def linear_regression_gd(X,y,learning_rate = 0.00001,max_iter=10000,tol=pow(10,-5)):
    # your code goes here 
    iters = 0
    gradient = 0
    all_cost = []
    w = np.zeros(4) #not zero so we dont zero out
    X_transpose = X.transpose()
    for i in range(max_iter) :
      iters += 1
      inside_parenthesis = np.dot(X,w) - y
      gradient = np.dot(X_transpose, inside_parenthesis)
     # gradient = np.dot(X.transpose(), ((np.dot(X, w) - y)))
      w = w - learning_rate * gradient
      all_cost.append(compute_cost(X,w,y))
      #print(w)


      #np.append(all_cost, compute_cost(X,w,y)) 
    #   print('iteration',i,'costsize', len(all_cost))
      # if len(all_cost) >= 2 :
      #   if abs(all_cost[i] - all_cost[iters-1])/all_cost[i-1] <= tol :
      #     break
   # print(w)
    #print(w, all_cost, iters+1)
    return w, all_cost, iters

"""### Question 1e: Convergence plots [10 pts]
After implementing gradient descent for linear regression, we would like to test that indeed our algorithm converges to a solution. In order see this, we are going to look at the value of the objective/loss function $L(\mathbf{w})$ as a function of the number of iterations, and ideally, what we would like to see is $L(\mathbf{w})$ drops as we run more iterations, and eventually it stabilizes. 

The learning rate plays a big role in how fast our algorithm converges: a larger learning rate means that the algorithm is making faster strides to the solution, whereas a smaller learning rate implies slower steps. In this question we are going to test two different values for the learning rate:
- 0.00001
- 0.000001

while keeping the default values for the max number of iterations and the tolerance.


- Plot the two convergence plots (cost vs. iterations) [5]

- What do you observe? [5]

<b>Important</b>: In reality, when we are running gradient descent, we should be checking convergence based on the <i>validation</i> error (i.e., we would have to split our training set into e.g., 70/30 training'/validation subsets, use the new training set to calculate the gradient descent updates and evaluate the error both on the training set and the validation set, and as soon as the validation loss stops improving, we stop training. <b>In order to keep things simple, in this assignment we are only looking at the training loss</b>, but as long as you have a function 
```python
def compute_cost(X,w,y):
```
that calculates the loss for a given X, y, and set of parameters you have, you can always compute it on the validation portion of X and y (that are <b>not</b> used for the updates).  
"""

# TODO 
# test gradient descent with step size 0.00001
# test gradient descent with step size 0.000001

(w, all_cost,iters) = linear_regression_gd(Xtr,ytr,learning_rate = 0.00001,max_iter = 1000, tol=pow(10,-6))  
plt.figure(0)
plt.semilogy(all_cost[0:iters])    
plt.grid()
plt.title('Training loss vs iteration with Rate = 0.00001')
plt.xlabel('Iteration')
plt.ylabel('Training loss')  

(w, all_cost,iters) = linear_regression_gd(Xtr,ytr,learning_rate = 0.000001,max_iter = 1000, tol=pow(10,-6))  
plt.figure(1)
plt.semilogy(all_cost[0:iters])    
plt.grid()
plt.title('Training loss vs iteration with Rate = 0.000001')
plt.xlabel('Iteration')
plt.ylabel('Training loss') 


# complete the rest

"""Observations: 

1. With a higher training rate, gradient descent converged faster
1.  With a lower training rate, gradient descent took many many more iterations to converge but yielded a much more charcteristic half parabolic shape.

### Question 2. Logistic regression [30 pts]

In this question, we will plot the logistic function and perform logistic regression. We will use the breast cancer data set.  This data set is described here:

https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin

Each sample is a collection of features that were manually recorded by a physician upon inspecting a sample of cells from fine needle aspiration.  The goal is to detect if the cells are benign or malignant.  

We could use the `sklearn` built-in `LogisticRegression` class to find the weights for the logistic regression problem.  The `fit` routine in that class has an *optimizer* to select the weights to best match the data.  To understand how that optimizer works, in this problem, we will build a very simple gradient descent optimizer from scratch.

### Loading and visualizing the Breast Cancer Data

We load the data from the UCI site and remove the missing values.
"""

names = ['id','thick','size_unif','shape_unif','marg','cell_size','bare',
         'chrom','normal','mit','class']
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/' +
                 'breast-cancer-wisconsin/breast-cancer-wisconsin.data',
                names=names,na_values='?',header=None)
df = df.dropna()
df.head(6)

"""After loading the data, we can create a scatter plot of the data labeling the class values with different colors.  We will pick two of the features.  """

# Get the response.  Convert to a zero-one indicator 
yraw = np.array(df['class'])
BEN_VAL = 2   # value in the 'class' label for benign samples
MAL_VAL = 4   # value in the 'class' label for malignant samples
y = (yraw == MAL_VAL).astype(int)
Iben = (y==0)
Imal = (y==1)

# Get two predictors
xnames =['size_unif','marg'] 
X = np.array(df[xnames])

# Create the scatter plot
plt.plot(X[Imal,0],X[Imal,1],'r.')
plt.plot(X[Iben,0],X[Iben,1],'g.')
plt.xlabel(xnames[0], fontsize=16)
plt.ylabel(xnames[1], fontsize=16)
plt.ylim(0,14)
plt.legend(['malign','benign'],loc='upper right')

"""The above plot is not informative, since many of the points are on top of one another.  Thus, we cannot see the relative frequency of points.

### Logistic function

We will build a binary classifier using *logistic regression*.  In logistic regression, we do not just output an estimate of the class label.  Instead, we ouput a *probability*, an estimate of how likely the sample is one class or the other.  That is our output is a number from 0 to 1 representing the likelihood:
$$
    P(y = 1|x)
$$
which is our estimate of the probability that the sample is one class (in this case, a malignant sample) based on the features in `x`.  This is sometimes called a *soft classifier*.  

In logistic regression, we assume that likelihood is of the form
$$
    P(y=1|x) = \sigma(z),  \quad z = w(1)x(1) + \cdots + w(d)x(d) + b = \mathbf{w}^T\mathbf{x}+b,  
$$
where $w(1),\ldots,w(d),b$ are the classifier weights and $\sigma(z)$ is the so-called *logistic* function:
$$
    \sigma(z) = \frac{1}{1+e^{-z}}.
$$

To understand the logistic function, suppose $x$ is a scalar and samples $y$ are drawn with $P(y=1|x) = f(w x+b)$ for some $w$ and $b$.  We plot these samples for different $w,b$.
"""

N = 100
xm = 20
ws = np.array([0.5,1,2,10])
bs = np.array([0, 5, -5])
wplot = ws.size
bplot = bs.size
iplot = 0
for b in bs: 
  for w in ws:
    iplot += 1
    x  = np.random.uniform(-xm,xm,N)
  
    py = 1/(1+np.exp(-w*x-b))
 
    yp = np.array(np.random.rand(N) < py) # hard label for random points
    xp = np.linspace(-xm,xm,100) 
    pyp = 1/(1+np.exp(-w*xp-b)) # soft label (probability) for the points

    plt.subplot(bplot,wplot,iplot)

    plt.scatter(x,yp,c=yp,edgecolors='none',marker='+')
    plt.plot(xp,pyp,'b-')
    plt.axis([-xm,xm,-0.1,1.1])
    plt.grid() 
    if ((iplot%4)!=1):
        plt.yticks([])
    plt.xticks([-20,-10,0,10,20])
    plt.title('w={0:.1f}, b={1:.1f}'.format(w,b))

    plt.subplots_adjust(top=1.5, bottom=0.2, hspace=0.5, wspace=0.2)

"""We see that $\sigma(wx+b)$ represents the probability that $y=1$.  The function $\sigma(wx) > 0.5$ for $x>0$ meaning the samples are more likely to be $y=1$.  Similarly, for $x<0$, the samples are more likely to be $y=0$.  The scaling $w$ determines how fast that transition is and $b$ influences the transition point.

### Fitting the Logistic Model on Two  Variables

We will fit the logistic model on the two variables `size_unif` and `marg` that we were looking at earlier.
"""

# load data 
xnames =['size_unif','marg'] 
X = np.array(df[xnames])
print(X.shape)

"""Next we split the data into training and test"""

# Split into training and test
from sklearn.model_selection import train_test_split
Xtr, Xts, ytr, yts = train_test_split(X,y, test_size=0.30)

"""**Logistic regression in scikit-learn**

The actual fitting is easy with the `sklearn` package.  The parameter `C` 
states the level of inverse regularization strength with higher values meaning less regularization. Right now, we will select a high value to minimally regularize the estimate.

We can also measure the accuracy on the test data. You should get an accuracy around 90%. 
"""

from sklearn import datasets, linear_model, preprocessing
reg = linear_model.LogisticRegression(C=1e5)
reg.fit(Xtr, ytr)

print(reg.coef_)
print(reg.intercept_)

yhat = reg.predict(Xts)
acc = np.mean(yhat == yts)
print("Accuracy on test data = %f" % acc)

"""**Instead of taking this approach, we will implement the regression function using gradient descent.**

### Question 2a. Gradient descent for logistic regression [20 pts]
In the class we saw that the weight vector can be found by minimizing the negative log likelihood over $N$ training samples.  The negative log likelihood is called the *loss* function.  For the logistic regression problem, the loss function simplifies to

$$L(\mathbf{w}) = - \sum_{i=1}^N y_i \log \sigma(\mathbf{w}^T\mathbf{x}_i+b) + (1-y_i)\log [1-\sigma(\mathbf{w}^T\mathbf{x}_i+b)].$$

Gradient can be computed as $$\nabla_\mathbf{w}L = \sum_{i=1}^N(\sigma(\mathbf{w}^T\mathbf{x}_i)-y_i)\mathbf{x}_i ,~~~ \nabla_b L = \sum_{i=1}^N(\sigma(\mathbf{w}^T\mathbf{x}_i)-y_i).$$


We can update $\mathbf{w},b$ at every iteration as  
$$ \mathbf{w} \gets \mathbf{w} - \alpha \nabla_\mathbf{w}L, \\ b \gets b - \alpha \nabla_b L.$$ 

**Note that we could also append the constant term in $\mathbf{w}$ and append 1 to every $\mathbf{x}_i$ accordingly, but we kept them separate in the expressions above.**

**Gradient descent function implementation** 

We will use this loss function and gradient to implement a gradient descent-based method for logistic regression.

Recall that training a logistic function means finding a weight vector `w` for the classification rule:

    P(y=1|x,w) = 1/(1+\exp(-z)), z = w[0]+w[1]*x[1] + ... + w[d]x[d]
    
The function implemented should follow the following format:
```python
def logistic_regression_gd(X,y,learning_rate = 0.001,max_iter=1000,tol=pow(10,-5)):
```
Where `X` is the training data feature(s), `y` is the variable to be predicted, `learning_rate` is the learning rate used ($\alpha$ in the slides), `max_iter` defines the maximum number of iterations that gradient descent is allowed to run, and `tol` is defining the tolerance for convergence (which we'll discuss next).

The return values for the above function should be (at the least) 1) `w` which are the regression parameters, 2) `all_cost` which is an array where each position contains the value of the objective function $L(\mathbf{w})$ for a given iteration, 3) `iters` which counts how many iterations did the algorithm need in order to converge to a solution.

Gradient descent is an iterative algorithm; it keeps updating the variables until a convergence criterion is met. In our case, our convergence criterion is whichever of the following two criteria happens first:

- The maximum number of iterations is met
- The relative improvement in the cost is not greater than the tolerance we have specified. For this criterion, you may use the following snippet into your code:
```python
np.absolute(all_cost[it] - all_cost[it-1])/all_cost[it-1] <= tol
```
"""

# TODO 
# Your code for logistic regression via gradient descent goes here 
#b is a scalar value
#w is not a scalar value
import math
def sigmoid_loss(this_X,w,b):
  z = np.dot(this_X, w) + b

  return 1 / (1 + math.e**-z)


def sigmoid_gd(w,this_X):
  z = np.dot(this_X, w)

  return 1 / (1 + math.e**-z)


def compute_cost(X,w,y,b):
    # your code for the loss function goes here 
    loss_sigmoid = sigmoid_loss(X,w,b)

    L = -np.sum(y * np.log(loss_sigmoid) + (1 - y) * np.log(1 - loss_sigmoid))


    return L

def logistic_regression_gd(X,y,learning_rate = 0.00001,max_iter=1000,tol=pow(10,-5)):
    # your code goes here 
    iters = 0
    w=np.ones(2)
    b = 0
    all_cost = []

    for i in range(len(X)) :
      iters+=1
      gradient_sigmoid = sigmoid_gd(w,X[i])

      gradient_w = np.sum(np.dot((gradient_sigmoid - y), X))
      gradient_b = np.sum(gradient_sigmoid - y)

      w = w - learning_rate * gradient_w
      b = b - learning_rate * gradient_b

      all_cost.append(compute_cost(X,w,y,b))
      #print(w)

    return w, all_cost, iters


#(w, all_cost,iters) = logistic_regression_gd(Xtr,ytr,learning_rate = 0.001,max_iter = 1000, tol=pow(10,-6))  
#print(w)

"""### Question 2b: Convergence plots and test accuracy [10 pts]

After implementing gradient descent for logistic regression, we would like to test that indeed our algorithm converges to a solution. In order see this, we are going to look at the value of the objective/loss function $L(\mathbf{w})$ as a function of the number of iterations, and ideally, what we would like to see is $L(\mathbf{w})$ drops as we run more iterations, and eventually it stabilizes. 

The learning rate plays a big role in how fast our algorithm converges: a larger learning rate means that the algorithm is making faster strides to the solution, whereas a smaller learning rate implies slower steps. In this question we are going to test two different values for the learning rate:
- 0.001
- 0.00001

while keeping the default values for the max number of iterations and the tolerance.


- Plot the two convergence plots (cost vs. iterations)
- Calculate the accuracy of classifier on the test data `Xts` 
- What do you observe?

**Calculate accuracy of your classifier on test data**

To calculate the accuracy of our classifier on the test data, we can create a predict method. 

Implement a function `predict(X,w)` that provides you label 1 if $\mathbf{w}^T\mathbf{x} + b > 0$ and 0 otherwise.
"""

# TODO 
# Predict on test samples and measure accuracy
def predict(X,w):
  # your code goes here
  yhat = [] 
  for i in range(len(X)) :
    if np.dot(w.transpose(), X[i]) > 0 :
      yhat.append(1)

    else :
      yhat.append(0)

  return yhat

# TODO 
# test gradient descent with step size 0.001
# test gradient descent with step size 0.00001
 
(w, all_cost,iters) = logistic_regression_gd(Xtr,ytr,learning_rate = 0.001,max_iter = 1000, tol=pow(10,-6))  
plt.figure(0)
plt.semilogy(all_cost[0:iters])    
plt.grid()
plt.xlabel('Iteration')
plt.ylabel('Training loss')
plt.title('Learning rate of 0.001')

yhat = predict(Xts,w)
acc = np.mean(yhat == yts)
print("Test accuracy = %f" % acc)

plt.figure(1)
(w, all_cost,iters) = logistic_regression_gd(Xtr,ytr,learning_rate = 0.00001,max_iter = 1000, tol=pow(10,-6))  
plt.semilogy(all_cost[0:iters])    
plt.grid()
plt.xlabel('Iteration')
plt.ylabel('Training loss')
plt.title('Learning rate of 0.00001')

yhat = predict(Xts,w)
acc = np.mean(yhat == yts)
print("Test accuracy = %f" % acc)


# complete the rest

"""Observations: 

1. A smaller learning rate results in a much more logical looking training loss graph
1.  The larger learning rate is completely wrong

---
## Submission instructions
1. Download this Colab to ipynb, and convert it to PDF. Follow similar steps as [here](https://stackoverflow.com/questions/53460051/convert-ipynb-notebook-to-html-in-google-colab) but convert to PDF.
 - Download your .ipynb file. You can do it using only Google Colab. `File` -> `Download` -> `Download .ipynb`
 - Reupload it so Colab can see it. Click on the `Files` icon on the far left to expand the side bar. You can directly drag the downloaded .ipynb file to the area. Or click `Upload to session storage` icon and then select & upload your .ipynb file.
 - Conversion using %%shell. 
 ```
!sudo apt-get update
!sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-generic-recommended
!jupyter nbconvert --log-level CRITICAL --to pdf name_of_hw.ipynb
  ```
 - Your PDF file is ready. Click 3 dots and `Download`.


  

2. Upload the PDF to Gradescope, select the correct pdf pages for each question. **Important!**

3. Upload the ipynb file to Gradescope
"""

!sudo apt-get update
!sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-generic-recommended

!jupyter nbconvert --log-level CRITICAL --to pdf fall2022_hw2.ipynb # make sure the ipynb name is correct

