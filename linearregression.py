import numpy as np
from numpy import linalg
class LinearRegression():
    def center_data(X, y, fit_intercept, normalize=False, copy=True,
                    sample_weight=None):
        """
        Centers data to have mean zero along axis 0. This is here because
        nearly all linear models will want their data to be centered.

        If sample_weight is not None, then the weighted mean of X and y
        is zero, and not the mean itself
        """
        X = X.copy()
        if fit_intercept:
            if isinstance(sample_weight, numbers.Number):
                sample_weight = None
            if sp.issparse(X):
                X_mean = np.zeros(X.shape[1])
                X_std = np.ones(X.shape[1])
            else:
                X_mean = np.average(X, axis=0, weights=sample_weight)
                X -= X_mean
                if normalize:
                    # XXX: currently scaled to variance=n_samples
                    X_std = np.sqrt(np.sum(X ** 2, axis=0))
                    X_std[X_std == 0] = 1
                    X /= X_std
                else:
                    X_std = np.ones(X.shape[1])
            y_mean = np.average(y, axis=0, weights=sample_weight)
            y = y - y_mean
        else:
            X_mean = np.zeros(X.shape[1])
            X_std = np.ones(X.shape[1])
            y_mean = 0. if y.ndim == 1 else np.zeros(y.shape[1], dtype=X.dtype)
        return X, y, X_mean, y_mean, X_std
    def __init__(self, fit_intercept=True, normalize=False, copy_X=True,
                 n_jobs=1):
        self.fit_intercept = fit_intercept
        self.normalize = normalize
        self.copy_X = copy_X
        self.n_jobs = n_jobs
    def _set_intercept(self, X_mean, y_mean, X_std):
        """Set the intercept_
        """
        if self.fit_intercept:
            self.coef_ = self.coef_ / X_std
            self.intercept_ = y_mean - np.dot(X_mean, self.coef_.T)
        else:
            self.intercept_ = 0.
    def fit(self, X, y, sample_weight=None):
        """
        Fit linear model.

        Parameters
        ----------
        X : numpy array or sparse matrix of shape [n_samples,n_features]
            Training data

        y : numpy array of shape [n_samples, n_targets]
            Target values

        sample_weight : numpy array of shape [n_samples]
            Individual weights for each sample

            .. versionadded:: 0.17
               parameter *sample_weight* support to LinearRegression.

        Returns
        -------
        self : returns an instance of self.
        """

        n_jobs_ = self.n_jobs
        X=X.copy()
        y=y.copy()

        X, y, X_mean, y_mean, X_std = self._center_data(
            X, y, self.fit_intercept, self.normalize, self.copy_X,
            sample_weight=sample_weight)

        self.coef_, self._residues, self.rank_, self.singular_ = \
            linalg.lstsq(X, y)
        self.coef_ = self.coef_.T

        if y.ndim == 1:
            self.coef_ = np.ravel(self.coef_)
        self._set_intercept(X_mean, y_mean, X_std)
        return self

