""" Unit tests for stimulusmodel. """

###########
# Imports #
###########
# Testing
import pytest

# GUI packages
import tkinter as tk

# Misc
import random

# Custom Modules
from functions import general
from models.stimulusmodel import StimulusModel


############
# Fixtures #
############
# Arrange
@pytest.fixture
def create_root():
    return tk.Tk()

# Arrange
@pytest.fixture
def create_sessionpars():
    sessionpars = {
        # Session variables
        'subject': tk.StringVar(value='P1234'),
        'condition': 'unit_testing',
        'disp_plots': 0,
        # Stimulus option variables
        'num_stim_chans': tk.IntVar(value=1),
        'test_freqs': tk.StringVar(value="500, 1000, 2000, 4000"),
        'duration': 2,
        # Staircase option variables
        'starting_level': 30,
        'min_level': -50,
        'max_level': 90,
        'step_sizes': "10, 5, 2",
        'num_reversals': 5,
        'rapid_descend': 'Yes',
        'rapid_descend_bool': True,
        # Audio device variables
        'audio_device': 2,
        'channel_routing': '1',
        # Calibration variables
        'cal_file': 'cal_stim.wav',
        'cal_level_dB': -30.0,
        'slm_reading': 70.0,
        'slm_offset': 100.0,
        # Presentation level variables
        'adjusted_level_dB': -25.0,
        'desired_level_dB': 75,
        # Version control variables
        'config_file_status': 0,
        'check_for_updates': 'yes',
        'version_lib_path': r'\\starfile\Public\Temp\MooreT\Custom Software\version_library.csv',
    }
    return sessionpars


# Arrange
@pytest.fixture(autouse=True)
def stim_model(create_root, create_sessionpars):
    root = create_root
    return StimulusModel(create_sessionpars)


##############
# Unit Tests #
##############
def test_RETSPLs_exist(stim_model):
    # Assert
    assert len(stim_model.RETSPL) == 34


def test_RETSPL_at_1kHz(stim_model):
    # Assert
    assert stim_model.RETSPL[1000] == 0.8


def test_subject_from_sessionpars_exists(stim_model):
    # Assert
    assert stim_model.sessionpars['subject'].get() == "P1234"


def test_get_test_freqs(stim_model):
    # Assert
    assert stim_model.get_test_freqs() == ([500, 1000, 2000, 4000], 4)


def test_assign_stimulus_interval(monkeypatch, stim_model):
    # Mock function to replace random.sample
    def mock_random_sample(intervals, _):
        return [intervals[0]]
    # Apply monkeypatch
    monkeypatch.setattr(random, "sample", mock_random_sample)
    # Assert
    assert stim_model.assign_stimulus_interval([1,2]) == 1


def test_calc_presentation_lvl_invalid_freq(monkeypatch, stim_model):
    # Mock function to replace general.calc_RMS_based_on_sources
    def mock_level(desired_SPL, num_sources):
        return 45.4568165
    # Apply monkeypatch
    monkeypatch.setattr(general, "calc_RMS_based_on_sources", mock_level)
    # Act
    with pytest.raises(KeyError) as exc_info:
        level = stim_model.calc_presentation_lvl(stair_lvl=30, freq=1100)


def test_calc_presentation_lvl_valid_freq(monkeypatch, stim_model):
    # Mock function to replace general.calc_RMS_based_on_sources
    def mock_level(desired_SPL, num_sources):
        return 45.4568165
    # Apply monkeypatch
    monkeypatch.setattr(general, "calc_RMS_based_on_sources", mock_level)
    # Act
    level = stim_model.calc_presentation_lvl(stair_lvl=30, freq=1000)
    assert level == 45.46


def test__get_random_phis_one_chan(stim_model):
    assert stim_model._get_random_phis() == pytest.approx([2.443461])
    

def test__get_random_phis_three_chans(stim_model):
    stim_model.sessionpars['num_stim_chans'].set(3)
    assert stim_model._get_random_phis() == pytest.approx(
        [2.443461, 2.094395, 0.6981317]
    )


def test_create_stimulus_one_chan(monkeypatch, stim_model):
    # Mock function to replace _get_random_phis
    def mock_phis():
        return [2.443461]
    # Apply monkeypatch
    monkeypatch.setattr(stim_model, "_get_random_phis", mock_phis)
    # Act
    assert stim_model.create_stimulus(1,48000,1000,5,5).shape[1] == 1


def test_create_stimulus_three_chans(monkeypatch, stim_model):
    # Update number of stimulus channels to three
    stim_model.sessionpars['num_stim_chans'].set(3)
    # Mock function to replace _get_random_phis
    def mock_phis():
        return [2.443461, 2.094395, 0.6981317]
    # Apply monkeypatch
    monkeypatch.setattr(stim_model, "_get_random_phis", mock_phis)
    # Act
    sig = stim_model.create_stimulus(1,48000,1000,5,5)
    assert sig.shape[0] == 48000
    assert sig.shape[1] == 3
