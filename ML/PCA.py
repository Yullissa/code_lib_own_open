import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors

def cal_cov(X,Y=None):
    n = X.shape[0]
    X = X - np.mean(X)
    Y = X if Y== None else Y - np.mean(Y)
    res = 1/n * np.matmul(X.T,Y)
    print(res)
    return res

def transform(X,topN):
    cov_matrix = cal_cov(X)
    print(cov_matrix)
    eigenvalues,eigenvectors = np.linalg.eig(cov_matrix)
    print(eigenvalues)
    idx = eigenvalues.argsort()[::-1]
    print(idx)
    eigenvectors = eigenvectors[:,idx]
    eigenvectors = eigenvectors[:,:topN]
    return np.matmul(X,eigenvectors)

def main():

    # Demo of how to reduce the dimensionality of the data to two dimension
    # and plot the results.

    # Load the dataset
    data = datasets.load_digits()

    X = data.data
    y = data.target
    # X = np.array([[1,2,3],[7,8,9],[4,5,6]]).astype(float)
    # Project the data onto the 2 primary principal components
    X_trans = transform(X, 2)
    x1 = X_trans[:, 0]
    x2 = X_trans[:, 1]

    cmap = plt.get_cmap('viridis')
    colors = [cmap(i) for i in np.linspace(0, 1, len(np.unique(y)))]

    class_distr = []
    # Plot the different class distributions
    for i, l in enumerate(np.unique(y)):
        _x1 = x1[y == l]
        _x2 = x2[y == l]
        _y = y[y == l]
        class_distr.append(plt.scatter(_x1, _x2, color=colors[i]))

    # Add a legend
    plt.legend(class_distr, y, loc=1)

    # Axis labels
    plt.suptitle("PCA Dimensionality Reduction")
    plt.title("Digit Dataset")
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.show()


if __name__ == "__main__":
    main()