# Yuricheck

Visually compare fingerprints using anime lesbians.

Build-Depends: `libjerasure-dev`
Depends: `python3-pil`, `libjerasure2`

Usage: `visual_digest.py outfile.jpg < data`


## Design

- Use an error-correcting code to reduce the accuracy of comparisons
  needed for correctness
- Deterministically shuffle so that the parity bytes aren't always at the end
  - This step doesn't do anything against an adversary, but is useful
    for accidental errors
- Convert each resulting byte into an anime girl
- Paste them together
