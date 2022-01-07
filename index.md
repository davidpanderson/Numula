# Numula: a Python library for nuanced computer music

Numula* is a set of Python tools for making computer-rendered music with
[nuance](http://continuum-hypothesis.com/mnl.php):
variations in dynamics, timing, and articulation as are typical of human performance.
Numula can be used for algorithmic composition or to render human compositions
(what I call [prepared performance](http://continuum-hypothesis.com/prep_perf.php)).

Here's [an example](wasserklavier) of a piece ("wasserklavier" by Luciano Berio)
rendered with Numula.

Numula lets you:

* Vary tempo and dynamics piecewise linearly
* Insert delays
* Shift notes forward or backwards in time
* Emphasize or de-emphasize notes as a function
of their position in a chord or their time within a measure
* Change the articulation of notes
* Add random "jitter" to the timing or volume of notes.

... and so on. Each adjustment can affect all notes
or subsets of notes selected on the basis of time, pitch,
or "tags" that you can associate with notes - e.g. to mark a particular fugue voice.

These adjustments are specified:

* in Python code: the power of a programming language (functions, iteration, etc.) is available;
* separately from the score (analogous to CSS and HTML)

The output of a Numula program is a MIDI file that you can play
with a software synthesizer, e.g. [Pianoteq](https://www.modartt.com/).

Numula consists of three modules:

* [note.py](note.py): classes representing scores (notes and sets of notes).
* [notate.py](notate.py): a textual notation for entering scores.
* [nuance.py](Nuance.py): functions that apply nuance to a score.

Numula is oriented towards keyboard music:
it controls the timing and volume of notes,
but not (for example) the attack type or variation within a note.
It doesn't currently handle multiple instruments or MIDI channels.

Numula could be implemented on top of [Music21](https://web.mit.edu/music21/),
and this might be worth doing at some point,
since Music21 provides many ways of importing scores.
However, Music21 is gigantic, and for our purposes only a small part of it is needed.
Numula implements this part in a clean and simple way.

Numula uses the [MIDIUtil](https://github.com/MarkCWirt/MIDIUtil) module to write MIDI files.
For simplicity this file is included with Numula.

If you find a bug in Numula, or want a feature, please create an issue in this repo.

---
* NOOM-yoo-luh.  The name refers to FORMULA, a Forth-based music language
from which Numula borrows some ideas.
