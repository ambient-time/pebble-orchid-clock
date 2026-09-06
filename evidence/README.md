# Orchid Clock checks

The host test covers all 86,400 seconds of a day, including noon and midnight.
At each native flower scale, the integer nectar endpoint agrees with the
source equation within half a pixel. Geometry checks compare all 72 marks
with coordinates captured from the supplied canvas functions. They verify
distinct centers inside every display, compiled tables, and reproducible
artwork. An independent path evaluation checks the nectar mask pixel by pixel,
including the split where the center column covers part of the throat.

All six native emulators installed and rendered the same final watchface.
The captures show changing seconds and natural noon and midnight rollovers.
Each target logged four frames over approximately 4.2 seconds. Capture checks
compare each requested pose with the latest native frame log.

Logged render times ranged from 2 to 31 milliseconds, with at least 61,148
bytes of free heap. The visual review covers the hero and a second pose from
each target at native size. The source silhouette, hour marks, nectar, and direct time
readout remain visible on round, rectangular, color, and monochrome screens.

The release archive includes the source, artwork, tests, and this evidence.
The separate independent-build report records a build from the extracted
archive, with six native code and resource payload comparisons.

Emulator captures show the native renderer. They do not measure battery use
or establish whether the minute spots are readable on a physical watch.
