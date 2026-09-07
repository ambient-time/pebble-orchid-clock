# Orchid Clock

A moth orchid keeps time in its markings. Twelve freckles across the wings
fill for the hour. Sixty tiny spots settle along the lower petal for minutes,
while nectar fills the throat over each minute. Noon and midnight fill all
twelve hour freckles; the minute spots clear at the start of each hour.

Color watches show white petals, blush pink, and gold nectar. Monochrome
watches use a white flower with dark marks against black. The face updates
once a second, pauses drawing when another app takes focus, and needs no
phone connection, account, or settings.

## Watches

| Target | Display |
| --- | --- |
| basalt | 144 × 168, color |
| chalk | 180 × 180, color, round |
| diorite | 144 × 168, monochrome |
| emery | 200 × 228, color |
| flint | 144 × 168, monochrome |
| gabbro | 260 × 260, color, round |

## Build and verify

Install the Pebble command-line tool with SDK 4.33.1. Host checks require
a C compiler, Python 3, and Pillow. The checked-in artwork supports normal
native builds without regenerating assets.

```sh
make test
pebble build --sdk 4.33.1
```

The output is `build/orchid-clock.pbw` in a directory named `orchid-clock`.
Use `make assets` to regenerate the source-derived geometry and artwork.
The geometry fixtures capture coordinates and paths from the original canvas
functions. Regenerate those with `node tools/source-fixtures.mjs` only when
updating the supplied source; normal builds do not require Node.js.

The capture script requires the Python environment containing `pebble-tool`.
Run each target separately, followed by packaging and the independent build:

```sh
python test/emulator.py chalk --fresh
python test/package.py
python test/independent.py
```

Packaging requires reports for all six targets tied to the exact watchface
file. These checks cover installation, changing time, natural noon and
midnight rollovers, one-second updates, and package checksums. The source ZIP
contains project files at its root and builds outside the parent repository.

## Source and adaptation

Luke Steuber created [Orchid Clock](https://datapoems.io/clocks/orchid-clock/)
and this Pebble port. The supplied HTML and screenshot live in
[reference](reference/). [Provenance](reference/provenance.json) records the
original file hashes.

The specimen keeps the original Bézier wing and lower-petal shapes, twelve
hour positions, and five rows of twelve minute spots. The flower grows to
fit a small screen. All 72 mark centers remain distinct at each native
resolution. The minute markings are fine detail. Version 1.0.1 removes the
added digital caption so the flower alone shows the time, as in the source.

Host checks compare all mark positions with the source fixtures, verify the
compiled coordinate tables, and check the nectar mask pixel by pixel. The
mask keeps the center column clear, including the narrow split at its base.

This release uses the source’s cream orchid treatment. Pebble’s limited
palette reduces the soft gradients to white, gray, pink, and gold. Monochrome
uses filled and outlined hour freckles, with dark settled minute spots. A
clipped nectar fill preserves the source’s second fraction at one-second
resolution. The watch omits the browser’s grain, shadows, continuous motion,
and palette cycling. The static specimen streams from flash one row at a
time through a 260-byte buffer; the time markings draw on the watch.

The package UUID is `f7009e56-3676-4fec-b78a-4bef6019d2e8`. Keep it unchanged
for updates.

Copyright 2026 Luke Steuber. [MIT License](LICENSE).
