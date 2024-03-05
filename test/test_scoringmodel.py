""" Unit tests for scoringmodel. """

###########
# Imports #
###########
# Testing
import pytest

# Data Science
import numpy as np
import pandas as pd

# System
import os

# Custom Modules
from models.scoringmodel import ScoringModel


############
# Fixtures #
############
@pytest.fixture
def temp_csv_dir(tmpdir):
    # Create mock CSV files in a temporary directory
    csv_files = ["file1.csv", "file2.csv"]

    # Data frame with 2 subjects, 4 responses, 1 condition
    # Take average of 2 reversals
    data_frames = [
        # Avg 2 reversals = 42.5
        pd.DataFrame({
            "subject": list(np.repeat(1234, 4)),
            "condition": np.repeat('A', 4),
            "test_freq": np.repeat(1000, 4),
            "desired_level_dB": [30, 35, 40, 45],
            "reversal": [True, False, True, True],
        }),
        # Avg 2 reversals = 60
        pd.DataFrame({
            "subject": list(np.repeat(5678, 4)),
            "condition": np.repeat('A', 4),
            "test_freq": np.repeat(1000, 4),
            "desired_level_dB": [50, 55, 60, 65],
            "reversal": [True, True, False, True],

        }),
    ]

    # Write data to CSV files
    for i, file_name in enumerate(csv_files):
        data_frames[i].to_csv(os.path.join(tmpdir, file_name), index=False)

    return tmpdir


@pytest.fixture
def scoring_model(temp_csv_dir, monkeypatch):
    # Patch the file dialog to return the temporary directory
    monkeypatch.setattr("models.scoringmodel.filedialog.askdirectory", 
                        lambda: temp_csv_dir
    )
    # Create ScoringModel instance
    return ScoringModel()


##############
# Unit Tests #
##############
def test__organize_data_output_type(scoring_model):
    # Assert that data attribute is of type DataFrame
    assert isinstance(scoring_model.data, pd.DataFrame)

def test__organize_data_output_shape(scoring_model):
    # Assert that data have expected shape and content
    assert scoring_model.data.shape == (8, 5)

def test__organize_data_output_columns(scoring_model):
    assert list(scoring_model.data.columns) ==\
    ["subject", "condition", "test_freq", "desired_level_dB", "reversal"]

def test__organize_data_output_subjects(scoring_model):
    assert list(scoring_model.data.iloc[:,0]) == list(np.repeat(1234, 4))\
          + list(np.repeat(5678, 4))

def test__organize_data_output_condition(scoring_model):
    assert list(scoring_model.data.iloc[:,1]) == list(np.repeat('A', 8))

def test__organize_data_output_levels(scoring_model):
    assert list(scoring_model.data.iloc[:,3]) == list(range(30, 70, 5))

def test__organize_data_output_reversals(scoring_model):
    assert list(scoring_model.data.iloc[:,4]) ==\
          [True, False, True, True, True, True, False, True]



def test__avg_revs(scoring_model):
    """ Have to make appropriate CSV files earlier
        (and update tests appropriately).
    """
    thresholds = scoring_model._avg_revs(scoring_model.data, 2)
    assert isinstance(thresholds, float)
    assert thresholds == 60



def test_score_error_raised_on_zero(scoring_model):
    with pytest.raises(ValueError) as exc_info:
        scoring_model.score(0)

        assert str(exc_info.value) ==\
              "Number of reversals cannot be 0 or negative!"

def test_score_error_raised_on_empty(scoring_model):
    with pytest.raises(TypeError) as exc_info:
        scoring_model.score()

def test_score_threshold_data_frame(scoring_model, monkeypatch):
    # Create monkeypatch
    def mock_to_csv(self, data_to_write):
        return None

    # Apply monkeypatch
    monkeypatch.setattr(ScoringModel, "write_to_csv", mock_to_csv)

    # Call function
    scoring_model.score(2)

    # Assert that the data attribute is of type DataFrame
    assert isinstance(scoring_model.thresholds_df, pd.DataFrame)

    # Assert that data have expected shape and content
    assert scoring_model.thresholds_df.shape == (2,4)
    assert list(scoring_model.thresholds_df.columns) ==\
          ['subject', 'condition', 'test_freq', 'threshold']
