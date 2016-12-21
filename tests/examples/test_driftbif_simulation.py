# -*- coding: utf-8 -*-
# This file as well as the whole tsfresh package are licenced under the MIT licence (see the LICENCE.txt)
# Maximilian Christ (maximilianchrist.com), Blue Yonder Gmbh, 2016

import numpy as np
import unittest
import pandas as pd

from tsfresh.examples.driftbif_simulation import velocity, load_driftbif


class DriftBifSimlationTestCase(unittest.TestCase):
    def test_intrinsic_velocity_at_default_bifurcation_point(self):
        """
        The intrinsic velocity of a dissipative soliton at the Drift bifurcation point is zero.
        """
        ds = velocity(tau=1.0/0.3)
        self.assertEqual(ds.deterministic, 0.0)

    def test_relaxation_dynamics(self):
        """
        Test accuracy of integrating the deterministic dynamics [6, p. 116]
        """
        v0 = velocity(tau=1.1/0.3).deterministic

        ds = velocity(tau=1.01/0.3, R=0)
        Nt = 100 # Number of time steps
        v = ds.simulate(Nt, v0=np.array([v0, 0.]))

        k3t = ds.kappa_3 * ds.tau
        k3st = ds.kappa_3**2 * ds.tau
        a0 = v0 / ds.kappa_3
        acceleration = lambda t: ds.kappa_3 * (a0 * np.sqrt(k3t - 1) * np.exp(k3st * t) /
                                               np.sqrt(np.exp(2.0 * k3st * t) * ds.Q * a0**2 +
                                                       np.exp(2.0 * ds.kappa_3 * t) * (k3t - 1 - ds.Q * a0**2)))
        t = ds.delta_t * np.arange(Nt)
        return np.testing.assert_array_almost_equal(v[:,0], np.vectorize(acceleration)(t),
                                                    decimal=8)

class LoadDriftBifTestCase(unittest.TestCase):
    def test_classification_labels(self):
        X, y = load_driftbif(10, 100)
        self.assertEqual(set(y), set([0,1]))

    def test_regression_labels(self):
        Nsamples = 10
        X, y = load_driftbif(Nsamples, 100, classification=False)
        self.assertEqual(y.size, np.unique(y).size,
                         'For regression the target vector is expected to not contain any dublicated labels.')
        
if __name__ == '__main__':
    unittest.main()
