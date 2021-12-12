from matplotlib import markers
import numpy as np

class AdalineGB(object):
    """
    Adaptive linear Neuron classifier

    Parameters
    -----------
    eta : float
        Learning rate (between 0.0 and 1.0)
    n_iter: int
        Passes over the training dataset

    Attributes
    ----------
    w_: 1d-array
        Weights after fitting
    errors_ : list
        Number of misclassifications in every epoch

    """

    def __init__(self, eta=0.01, n_iter=50):
        self.eta = eta
        self.n_iter = n_iter
    
    def fit(self, X, y):
        """
        Fit training data

        Parameters
        ----------
        X : {array-like}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of
            samples and n_features is the number of features-
        y : {array-like}, shape = [n_samples]
            Target values

        Returns
        -------
        self : object
        """

        self.w_ = np.zeros(1 + X.shape[1])
        self.cost_ = []

        for _ in range(self.n_iter):
            output = self.net_input(X)
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = (errors**2).sum()/2.0
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        """Calculate net input"""
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def activation(self, X):
        """Compute linear activation"""
        return self.net_input(X)

    def predict(self, X):
        """Returns class label after unit step"""
        return np.where(self.net_input(X) >= 0.0, 1, -1)


# Grab training data from internet
import pandas as pd
import numpy as np
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)
print(df.head())

y = df.iloc[:100, 4].values
y = np.where(y== 'Iris-setosa', -1, 1)
X = df.iloc[:100, [0,2]].values

# traint and plot
import matplotlib.pyplot as plt
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
ada1 = AdalineGB(eta=0.1, n_iter=30).fit(X, y)
ax[0].plot(range(1, len(ada1.cost_) + 1), np.log10(ada1.cost_), marker='o')
ax[0].set_xlabel("Epochs")
ax[0].set_ylabel("log(Sum-squared-error")
ax[0].set_title("Adaline learning rate 0.01")

ada2 = AdalineGB(n_iter=30, eta=0.0001).fit(X, y)
ax[1].plot(range(1, len(ada2.cost_) + 1), np.log10(ada2.cost_), marker='o')
ax[1].set_xlabel("Epochs")
ax[1].set_ylabel("log(Sum-squared-error")
ax[1].set_title("Adaline learning rate 0.0001")
plt.show()




