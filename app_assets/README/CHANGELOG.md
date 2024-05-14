<h1 style="text-align: center;">Change Log: P.E.A.T.</h1>
<h2 style="text-align: center;">(P.sychophysical E.stimation of A.uditory T.hresholds)</h2>
---

## Version 2.0.2

Date: May 14, 2024

### Patches
1. Replaced white noise calibration file with 1 kHz warble tone scaled to -30 dB.
<br>
<br>

---

## Version 2.0.1

Date: March 5, 2024

### Patches
1. Added several unit tests to test suite.
2. Added validation for several fields in the File>Settings window.
3. Updated README file with list of valid test frequencies.
<br>
<br>

---

## Version 2.0.0

Date: February 29, 2024

### Major Features
1. Added RETSPLs to levels to achieve perceptually-balanced presentations across frequencies.
2. Calculated appropriate "random" starting phases to avoid constructive/destructive interference as much as possible. 
3. Fixed random seed when choosing permissible starting phase values to ensure consistency in test results across trials, frequencies, and sessions. 
4. Moved stimulus generation to the start of each run, avoiding re-synthesizing on each trial to improve processing time. 

### Minor Features
1. Added new key binding/unbinding logic to avoid multiple responses during a single trial.
2. Levels are now rounded to two decimal places so Excel doesn't give conversion warning.

### Patches
1. Refactored stimulus code. 
<br>
<br>

---

## Version 1.0.0

Date: February 15, 2024

### Features
1. Exposed staircase parameters for minimum and maximum permissable presentation levels.
2. Added option to display or hide staircase plots after each threshold.
3. Added help documentation. 

### Bug Fixes
1. Fixed a bug where threshold calculations were averaged across subjects.
2. Fixed a bug where threshold calculations were averaged across conditions.

### Patches
1. Refactored threshold calculation code.
<br>
<br>

---

## Version 0.2.0

Date: February 12, 2024

### Features
1. Added multichannel stimulus capabilities, with random starting phases for each channel (for use in the sound field).
2. Added a 0.5-second pause at beginning of each trial (to offset the button click from the next trial onset).
3. Added interactive message boxes for participants after each threshold has been obtained (to delineate runs/frequencies).
4. Removed staircase plots from output (to blind participants to performance). 
<br>
<br>

---

## Version 0.1.0

Date: February 08, 2024

### Initial Release
1. Application for estimating auditory thresholds using a 2IAFC task.
<br>
<br>
