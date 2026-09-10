# ME Totalizer Dial-Verification Pipeline

**Program:** UC Riverside, Center for Environmental Research and Technology (CE-CERT)
**Role:** R&D Engineer II — built and led the verification methodology
**Status:** Complete (V8, final deliverable)

## The Problem

CE-CERT needed main-engine (ME) totalizer readings extracted from six timelapse video
recordings of an analog dial gauge — 4,889 individual dial reads in total. Read by hand,
that's not practical at scale; read by automated computer vision, the readings looked
plausible but were systematically wrong.

## What I Built

An extraction and verification pipeline (Python: `convert_me_totalizer.py`,
`verify_me_totalizer.py`) to process the video frames into structured data, plus a
verification methodology to catch and correct errors at scale rather than trust the
automation blindly.

## The Failure — and the Root Cause

Two different AI vision approaches were tried against this dial data and both failed.
The bug wasn't random noise — it was systematic: the extraction script was reading the
dial needle's **blunt tail** instead of its **white tip**, producing a consistent
~50-unit error in one direction. That's the kind of error that looks fine at a glance
and corrupts a dataset silently.

The fix was not "throw more AI at it." It was human verification against the actual
video frames, combined with rollover-aware interpolation for the totalizer's counter
behavior.

## Validation Standard

Rather than spot-check a handful of rows and call it done, I set a statistical bar and
met it:

- **977 of 4,889 rows (20%) human-verified** against source video, in seven review
  chunks
- **Statistically valid at 98% confidence, under 2% margin of error**
- Cross-checked against an independent manual-conversion reference set, with anchor
  points landing within +/-5 units, 1.85 average error

The verified rows are the program's ground truth for this dataset going forward — later
work builds on them rather than re-verifying what's already been checked.

## Why This Matters Beyond CE-CERT

This is a general pattern, not a one-off fix: automated data pipelines can produce
confident, wrong output, and the fix isn't always "better AI" — sometimes it's finding
the actual mechanical root cause of the error and building a human-verification step
with a real statistical standard around it. That's the same discipline this pipeline
applied to fleet/equipment data that a logistics, operations, or program-management
role would apply to freight, performance, or supply-chain data.
