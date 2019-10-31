#!/usr/bin/python3.7
# -*-coding:utf8 -*

import numpy as np
import unittest

from FDApy.basis import *

class TestBasis(unittest.TestCase):
	"""Test class for the functions in basis.py
	"""

	# Test basis_legendre function
	def test_basis_legendre(self):
		X = basis_legendre(M=2, argvals=np.array([0, 0.5, 1]), norm=True)
		self.assertTrue(np.allclose(X.values, 
			np.array([[1., 1., 1.], [0., 0.8660254, 1.73205081]])))

	# Test basis_wiener function
	def test_basis_wiener(self):
		X = basis_wiener(M=2, argvals=np.array([0, 0.5, 1]), norm=True)
		self.assertTrue(np.allclose(X.values,
			np.array([[0., 1., 1.41421356], [0., 1., -1.41421356]])))

	# Test simulate_basis_ function
	def test_simulate_basis_(self):
		X = simulate_basis_('legendre', M=2, 
				argvals=np.array([0, 0.5, 1]), norm=True)
		self.assertTrue(np.allclose(X.values, 
			np.array([[1., 1., 1.], [0., 0.8660254, 1.73205081]])))

	# Test eigenvalues_linear function
	def test_eigenvalues_linear(self):
		X = eigenvalues_linear(M=3)
		self.assertTrue(np.allclose(X, 
			[1.0, 0.6666666666666666, 0.3333333333333333]))

	# Test eigenvalues_exponential function
	def test_eigenvalues_exponential(self):
		X = eigenvalues_exponential(M=3)
		self.assertTrue(np.allclose(X, 
			[0.36787944117144233, 0.22313016014842982, 0.1353352832366127]))

	# Test eigenvalues_wiener function
	def test_eigenvalues_wiener(self):
		X = eigenvalues_wiener(M=3)
		self.assertTrue(np.allclose(X, 
			[0.4052847345693511, 0.04503163717437235, 0.016211389382774045]))

	# Test simulate_eigenvalues_ function
	def test_simulate_eigenvalues_(self):
		X = simulate_eigenvalues_('linear', M=3)
		self.assertTrue(np.allclose(X,
			[1.0, 0.6666666666666666, 0.3333333333333333]))
		

if __name__ == '__main__':
	unittest.main()