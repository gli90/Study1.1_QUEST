# A QUEST for Perceptual Threshold Calibration

A PsychoPy-based psychophysical experiment designed to estimate individual blue-purple color discrimination thresholds using the QUEST adaptive staircase procedure.

## Overview

This experiment presents color stimuli along a blue-purple continuum and adaptively adjusts stimulus difficulty using QUEST.

The goal is to estimate the perceptual boundary and discrimination threshold between blue and purple hues.

## Features

- PsychoPy implementation
- QUEST adaptive staircase
- Trial-by-trial response recording
- Excel_CSV data export
- Participant information collection

## Requirements

- PsychoPy
- pandas
- numpy

## Run

```bash
/Applications/PsychoPy.app/Contents/MacOS/python blue_purple_quest.py

## Why were these three chromatic axes selected?

The present study aims to identify a chromatic axis that is most suitable for precise perceptual threshold estimation and subsequent metacognitive experiments. Rather than assuming a single optimal hue direction, three candidate axes were selected and evaluated empirically.

### Axis A — Blue ↔ Purple

This axis represents a relatively small hue transition within the cool-color region. It was chosen because blue–purple discrimination has been widely used in color perception studies and is expected to produce fine perceptual differences.

### Axis B — Blue ↔ Cyan

This axis explores another nearby hue direction within the blue region. Compared with Axis A, it allows us to examine whether a different local hue transition produces lower discrimination thresholds or more stable psychometric performance.

### Axis C — Blue ↔ Yellow

Unlike the first two axes, this direction spans a qualitatively different region of CIELAB space. It was included to test whether a larger perceptual hue separation yields more reliable discrimination and metacognitive performance.

### Why compare three axes?

The goal of Task A is **not** to compare color categories themselves, but to identify the chromatic axis that provides the most reliable perceptual measurements for the subsequent illusion experiment.

Each candidate axis is evaluated using identical QUEST procedures and compared according to:

1. QUEST threshold.
2. Threshold convergence (Last-10 stability).
3. Signal detection performance (d′ and false-alarm rate).
4. Behavioural consistency across repeated sessions.

The axis used in the formal experiment is therefore selected **empirically**, ensuring that subsequent experiments are based on the most stable and reliable perceptual dimension rather than subjective preference.
