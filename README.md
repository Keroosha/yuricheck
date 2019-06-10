# Yuricheck

Visually compare fingerprints using anime lesbians.

Build-Depends: `libjerasure-dev`
Depends: `python3-pil`, `libjerasure2`

Usage: `visual_digest.py outfile.jpg < data`


## Example

    $ gpg --fingerprint Kureha
    pub   rsa3072 2019-06-10 [SC] [expires: 2021-06-09]
          755D 01F6 B701 5045 7BE1  6593 3826 8AF2 9CD9 153F
          uid           [ultimate] Tsubaki Kureha <kureha@arashigaoka.jp>
          sub   rsa3072 2019-06-10 [E] [expires: 2021-06-09]
    $ echo 755D 01F6 B701 5045 7BE1  6593 3826 8AF2 9CD9 153F | tr -d ' ' | ./visual_digest.py -t hex kureha.jpg
    $ echo 755D 01F6 B701 5045 7BE1  6593 3826 BAF2 9CD9 153F | tr -d ' ' | ./visual_digest.py -t hex kureha-wrong.jpg

![kureha.jpg](http://web.mit.edu/~ikdc/Public/kureha.jpg "See, they're totally different!")

![kureha-wrong.jpg](http://web.mit.edu/~ikdc/Public/kureha-wrong.jpg "See, they're totally different!")

## Design

- Use an error-correcting code to reduce the accuracy of comparisons
  needed for correctness
- Deterministically shuffle so that the parity bytes aren't always at the end
  - This step doesn't do anything against an adversary, but is useful
    for accidental errors
- Convert each resulting byte into an anime girl
- Paste them together
