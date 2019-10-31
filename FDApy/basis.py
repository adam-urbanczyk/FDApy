#!/usr/bin/python3.7
# -*-coding:utf8 -*

import numpy as np
import scipy

import FDApy


#############################################################################
# Definition of the basis (eigenfunctions)

def basis_legendre(K=3, argvals=None, norm=True):
	"""Define Legendre basis of function.
	
	Build an orthogonal basis of `K` functions using Legendre polynomials 
	on the interval `argvals`.
	
	Parameters
	----------
	K : int, default = 3
		Maximum degree of the Legendre polynomials. 
	argvals : tuple or numpy.ndarray, default = None
		The values on which evaluated the Legendre polynomials. If `None`, 
		the polynomials are evaluated on the interval [-1, 1].
	norm : boolean, default = True
		Do we normalize the functions?

	Return
	------
	obj : FDApy.univariate_functional.UnivariateFunctionalData
		A UnivariateFunctionalData object containing the Legendre polynomial
		up to `K` functions evaluated on `argvals`.
	
	Example
	-------
	>>>basis_legendre(K=3, argvals=np.arange(-1, 1, 0.1), norm=True)
	"""

	if argvals is None:
		argvals = np.arange(-1, 1, 0.1)

	if isinstance(argvals, list):
		raise ValueError('argvals has to be a tuple or a numpy array!')

	if isinstance(argvals, tuple):
		argvals = np.array(argvals)

	values = np.empty((K, len(argvals)))

	for degree in range(K):
		legendre = scipy.special.eval_legendre(degree, argvals)

		if norm:
			legendre = legendre / np.sqrt(scipy.integrate.simps(
				legendre * legendre, argvals))
		values[degree, :] = legendre

	obj = FDApy.univariate_functional.UnivariateFunctionalData(
		tuple(argvals), values)
	return obj

def basis_wiener(K=3, argvals=None, norm=True):
	"""Define Wiener basis of function.

	Build a basis of functions of the Wiener process.

	Parameters
	----------
	K : int, default = 3
		Number of functions to compute.
	argvals : tuple or numpy.ndarray, default = None
		The values on which evaluated the Wiener basis functions. If `None`, 
		the functions are evaluated on the interval [0, 1].
	norm : boolean, default = True
		Do we normalize the functions?

	Return
	------
	obj : FDApy.univariate_functional.UnivariateFunctionalData
		A UnivariateFunctionalData object containing `M` Wiener basis functions
		evaluated on `argvals`.

	Example
	-------
	>>>basis_wiener(M=3, argvals=np.arange(0, 1, 0.05), norm=True)
	"""
	if argvals is None:
		argvals = np.arange(0, 1, 0.05)

	if isinstance(argvals, list):
		raise ValueError('argvals has to be a tuple or a numpy array!')

	if isinstance(argvals, tuple):
		argvals = np.array(argvals)

	values = np.empty((K, len(argvals)))

	for degree in np.linspace(1, K, K):
		wiener = np.sqrt(2) * np.sin((degree - 0.5) * np.pi * argvals)

		if norm:
			wiener = wiener / np.sqrt(scipy.integrate.simps(
				wiener * wiener, argvals))

		values[int(degree-1), :] = wiener

	obj = FDApy.univariate_functional.UnivariateFunctionalData(
		tuple(argvals), values)
	return obj 

def simulate_basis_(basis_name, K, argvals, norm):
	"""Function that redirects to the right simulation basis function.

	Parameters
	----------
	basis_name : str
		Name of the basis to use.
	K : int
		Number of functions to compute.
	argvals : tuple or numpy.ndarray
		The values on which evaluated the Wiener basis functions. If `None`, 
		the functions are evaluated on the interval [0, 1].
	norm : boolean
		Do we normalize the functions?

	Return
	------
	basis_ : FDApy.univariate_functional.UnivariateFunctionalData
		A UnivariateFunctionalData object containing `M` basis functions 
		evaluated on `argvals`.

	Example
	-------
	>>>simulate_basis_('legendre', M=3, 
		argvals=np.arange(-1, 1, 0.1), norm=True)
	"""
	if basis_name == 'legendre':
		basis_ = basis_legendre(K, argvals, norm)
	elif basis_name == 'wiener':
		basis_ = basis_wiener(K, argvals, norm)
	else:
		raise ValueError('Basis not implemented!')
	return basis_


#############################################################################
# Definition of the eigenvalues

def eigenvalues_linear(M=3):
	"""Function that generate linear decreasing eigenvalues.

	Parameters
	----------
	M : int, default = 3
		Number of eigenvalues to generates

	Return
	------
	val : list
		The generated eigenvalues 

	Example
	-------
	>>>eigenvalues_linear(M=3)
	[1.0, 0.6666666666666666, 0.3333333333333333]
	"""
	return [(M - m + 1) / M for m in np.linspace(1, M, M)]

def eigenvalues_exponential(M=3):
	"""Function that generate exponential decreasing eigenvalues.

	Parameters
	----------
	M : int, default = 3
		Number of eigenvalues to generates

	Return
	------
	val : list
		The generated eigenvalues 

	Example
	-------
	>>>eigenvalues_exponential(M=3)
	[0.36787944117144233, 0.22313016014842982, 0.1353352832366127]
	"""
	return [np.exp(-(m+1)/2) for m in np.linspace(1, M, M)]

def eigenvalues_wiener(M=3):
	"""Function that generate eigenvalues from a Wiener process.

	Parameters
	----------
	M : int, default = 3
		Number of eigenvalues to generates

	Return
	------
	val : list
		The generated eigenvalues 

	Example
	-------
	>>>eigenvalues_wiener(M=3)
	[0.4052847345693511, 0.04503163717437235, 0.016211389382774045]
	"""
	return [np.power((np.pi / 2) * (2 * m - 1), -2) 
			for m in np.linspace(1, M, M)]

def simulate_eigenvalues_(eigenvalues_name, M):
	"""Function that redirects to the right simulation eigenvalues function.

	Parameters
	----------
	eigenvalues_name : str
		Name of the eigenvalues generation process to use.
	M : int
		Number of eigenvalues to generates

	Return
	------
	eigenvalues_: list
		The generated eigenvalues

	Example
	-------
	>>>simulate_eigenvalues_('linear', M=3)
	[1.0, 0.6666666666666666, 0.3333333333333333]
	"""
	if eigenvalues_name == 'linear':
		eigenvalues_ = eigenvalues_linear(M)
	elif eigenvalues_name == 'exponential':
		eigenvalues_ = eigenvalues_exponential(M)
	elif eigenvalues_name == 'wiener':
		eigenvalues_ = eigenvalues_wiener(M)
	else:
		raise ValueError('Eigenvalues not implemented!')
	return eigenvalues_


#############################################################################
# Class Simulation

class Simulation(object):
	"""An object to simulate functional data.

	Parameters
	----------
	N: int
		Number of curves to simulate.
	M: int or numpy.ndarray
		Sampling points.
		If M is int, we use np.linspace(0, 1, M) as sampling points.
		Otherwise, we use the numpy.ndarray.
	"""

	def __init__(self, N, M):
		self.N_ = N
		if isinstance(M, int):
			M = np.linspace(0, 1, M)
		self.M_ = M

	def new():
		"""Function to simulate observations.
		To redefine.
		"""
		pass

	def add_noise(self, noise_var=1, sd_function=None):
		"""Add noise to the data.
		
		Model: Z(t) = f(t) + sigma(f(t))epsilon
		
		If sd_function is None, sigma(f(t)) = 1 and epsilon ~ N(0, noise_var)
		Else, we consider heteroscedastic noise with:
			- sigma(f(t)) = sd_function(self.obs.values)
			- epsilon ~ N(0,1)
			
		Parameters
		----------
		noise_var : float
			Variance of the noise to add.
		sd_function : callable
			Standard deviation function for heteroscedatic noise.

		"""

		noisy_data = []
		for i in self.obs:
			if sd_function is None:
				noise = np.random.normal(0, np.sqrt(noise_var), 
					size=len(self.M))
			else:
				noise = sd_function(i.values) *\
					np.random.normal(0, 1, size=len(self.obs.argvals[0]))
			noise_func = FDApy.univariate_functional.UnivariateFunctionalData(
				self.obs.argvals, np.array(noise, ndmin=2))
			noisy_data.append(i + noise_func)

		data = FDApy.multivariate_functional.MultivariateFunctionalData(
			noisy_data)

		self.noisy_obs = data.asUnivariateFunctionalData()


class Basis(Simulation):
	"""A functional data object representing an orthogonal (or orthonormal)
	basis of functions.

	The function are simulated using the Karhunen-Loève decomposition :
		X_i(t) = mu(t) + sum_{j = 1}^M c_{i,j}phi_{i,j}(t), i = 1, ..., N

	Parameters:
	-----------
	basis_name: str
		String which denotes the basis of functions to use.
	K: int
		Number of basis functions to use to simulate the data.
	eigenvalues: str or numpy.ndarray
		Define the decreasing of the eigenvalues of the process.
		If `eigenvalues` is str, we define the eigenvalues as using the
		corresponding function. Otherwise, we keep it like that. 
	norm: bool
		Should we normalize the basis function?
	Attributes
	----------
	coef_: numpy.ndarray
		Array of coefficients c_{i,j}
	obs: FDApy.univariate_functional.UnivariateFunctionalData
		Simulation of univariate functional data

	Notes
	-----

	References
	---------

	"""
	def __init__(self, N, M, basis_name, K, eigenvalues, norm):
		Simulation.__init__(self, N, M)
		self.basis_name_ = basis_name
		self.K_ = K
		self.norm_ = norm_

		# Define the basis
		self.basis_ = simulate_basis_(self.basis_name_, 
			self.K_, self.M_, self.norm_)

		# Define the decreasing of the eigenvalues
		if isinstance(eigenvalues) is str:
			eigenvalues = simulate_eigenvalues_(eigenvalues, self.K_)
		self.eigenvalues_ = eigenvalues

	def new(self, argvals, N):
		"""Function that simulates `N` observations
		
		Parameters
		----------
		argvals : tuple or numpy.ndarray
			A single numeric vector giving the sampling points 
			in the domain.
		N : int
			Number of observations to generate.

		"""

		#if isinstance(argvals, np.ndarray):
		#	argvals = tuple(argvals)
		
		# Simulate the N observations
		#obs = np.empty(shape=(N, len(argvals)))
		#coef = np.empty(shape=(N, len(eigenvalues_)))
		#for i in range(N):
		#	coef_ = list(np.random.normal(0, eigenvalues_))
		#	prod_ = coef_ * basis_
			
		#	obs[i, :] = prod_.values.sum(axis=0)
		#	coef[i, :] = coef_

		#self.coef_ = coef
		#self.obs = FDApy.univariate_functional.UnivariateFunctionalData(
		#	argvals, obs)


class Brownian(Simulation):
	"""A functional data object representing a brownian motion.
	
	Parameters
	----------
	N: int, default=100
		Number of curves to simulate.
	brownian_type: str, default='regular'
		Type of brownian motion to simulate.
		One of 'regular', 'geometric' or 'fractional'.
	"""

	def __init__(self, N, M, brownian_type='regular'):
		Simulation.__init__(N)
		self.brownian_type = brownian_type