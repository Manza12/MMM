# MMM
## Mathematical Morphology & Music
### Gonzalo Romero-García
#### Spectrograms
The code of the PhD for spectrograms is in the folder `scripts/spectrograms`. Currently, there are the following scripts:
* `transient_generation.py`: it generates a transient by rotating in the TF plane a sinusoid. However, the code should be reviewed since it does not return the correct output. The figure is ok though, but not corresponding with the supposed spectrum.
The figures are stocked in the folder `phd/chapter_3`.
* `analysis_synthesis_pipeline.py`: it is the process of taking a sound, creating the spectrogram, analyzing it with MM and generating the synthesis version using the STN parameters.