# Personal Calendar Research Engine — Source Reconciliation and Uncertainty

This research project explored how to turn a personal reflective-calendar concept into a deterministic data pipeline without confusing astronomical calculation with spiritual interpretation.

## Technical Work

- Calculated lunar sign ingresses and Moon phases with the Swiss Ephemeris through PySwissEph.
- Converted Universal Time events into Pacific civil time with explicit daylight-saving handling.
- Cross-checked calculated events against published ephemeris calendars and documented discrepancies.
- Replaced an incorrect full-moon anchor after independent computation and source comparison.
- Modeled exact, approximate, and unknown birth-time inputs as different states rather than silently inventing a midpoint.
- Designed release gates for ephemeris licensing, date-range support, versioned rules/data, reference vectors, place data, and historical time-zone resolution.

## Product Boundary

The astronomical layer can produce testable event times. The optional spiritual or reflective layer is a belief/content framework, not a scientific or medical claim. A public product must keep those layers visibly separate and suppress results when source, license, time-zone, or uncertainty requirements are not met.

## Privacy Boundary

This portfolio page intentionally excludes personal birth details, journal content, owner-specific fixtures, and the private interpretive calendar. It describes the engineering and validation method only.

## Tools and References

- Python and PySwissEph.
- IANA historical time-zone identifiers.
- Golden/reference-vector testing.
- [Swiss Ephemeris programming interface](https://www.astro.com/swisseph/swephprg.htm).
- External monthly ephemeris calendars used as secondary comparisons.

## Why It Matters

The same pattern applies beyond calendars: preserve uncertainty, bind outputs to versioned inputs and data, separate calculation from interpretation, and fail closed when provenance is missing.
