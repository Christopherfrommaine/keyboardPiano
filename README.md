This is a simple keyboard piano program I wrote.

I originally wrote it to explore microtonal tunings, but it serves quite well
as a basic keyboard piano, with a much bigger range than other programs or
websites like virtualpiano.net.

Each tuning system (12TET, 17TET, 19TET, 24TET) comes with a specific keyboard layout
based on the piano. Other equal tempered tunings can also be used, however the layout of the keys will
not be very intuitive.
There is also Pythagoran tuning (which uses the 12TET layout) and Extended tuning.

The tuning is set to extended by default, which lets you play more than two
octaves. Charachters zxcvbnm, represent C4-C5, and charachters qwertyui represent
C3-C4. You can use the shift key to move that up an octave, and the control key to
move it down by an octave, and the alt key to double the effect of the other modifyer keys.

I plan on implementing the ability to upload waveforms as .wav, but at the current moment,
I have included algorithmically generated waveforms like sine, square, saw, as well as
a pipe organ (based on doing a fourier anylsis of the pipe organ sample from musesounds,
then reconstructing that with pure tones.)

Hope you enjoy!
