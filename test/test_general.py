""" Unit tests for general functions. """

###########
# Imports #
###########
# Testing
import pytest

# Data Science
import numpy as np

# Custom Modules
from functions import general


##############
# Unit Tests #
##############
@pytest.mark.parametrize("desired_SPL, num_sources, expected", 
                         [(50,1,50), (50,2,46.9897), (50,3,45.2288)]
)
def test_calc_RMS_based_on_sources(desired_SPL, num_sources, expected):
    result = general.calc_RMS_based_on_sources(desired_SPL, num_sources)
    assert np.isclose(result, expected)
