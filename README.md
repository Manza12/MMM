# MMM: Mathematical Morphology & Music
#### Gonzalo Romero-García
This is the repository that accompanies my PhD *Mathematical Morphology for Analysis and Generation of Time-Frequency Representations of Music*.
### Sounds from Chapter 3
They are stored in `results/chapter_3` organized by instrument. Each instrument has
- `input.wav`: the input file
- `sinusoids.wav`: the sinusoidal component
- `transient.wav`: the transient component
- `filtered_noise.wav`: the stochastic component
- `output.wav`: the output; the sum of the previous three
### Structure
The repository is organized as follows:
- `data`: the input data for the scripts, organized in:
  - `audio`: the `.wav` files
  - `midi`: the `.mid` files
  - `musicxml`: the `.musicxml` files
  - `objects`: the generic objects in pickle format
  - `scorexml`: the XSD for the ScoreTree object and the corresponding `.xml` files.
- `mmm`: the library itself, separated in piano rolls and spcetrograms
- `phd`: the folder where the images necessary for the PhD are saved, organized by chapter.
- `results`: some results of the PhD, in particular:
  - `chapter_3`: the audio files of each instrument. The audio files are the following:
    - `input.wav`: the input file
    - `sinusoids.wav`: the sinusoidal component
    - `transient.wav`: the transient component
    - `filtered_noise.wav`: the stochastic component
    - `output.wav`: the output; the sum of the previous three
  - `chapter_4`: some examples of the output of the compilation of a ScoreXML file into a `.mid` file
- `scripts`: all the scripts used. 
  - `graphs`: the scripts used for creating graph figures for the PhD
  - `introduction`: the scripts used for creating the images of the introduction
  - `pianorolls`: the scripts used for operating on piano rolls;
    - `analysis_harmonic_textures.py`: a script corresponding to the figures and computations from the chapter 5, section 1
    - `analysis_textures.py`: another script for the same purpose as the precedent
    - `compilation_score_tree.py`: the script for compiling a ScoreTree into a midi file. The name parameter in line 8 serves to refer the name of the file, i.e.m,  `data/scorexml/[name].xml`
    - `dilation_harmonic_textures.py`: a script for generating a figure of the PhD
    - `dilation_harmonic_textures_default.py`: another script for the same purpose as the precedent
    - `find_minimal_activations`: the script for finding finimal activations with the method proposed in the PhD (chspter 5, section 2)
    - `graph_covering_activations`: a script for generating some images from chapter 5, section 2
    - `tonal_graph.py`: the script for generating the tonal graph from chapter 5, section 3
  - `spectrograms`: the scripts for the chapter 3, namely:
    - `analysis_synthesis_pipeline.py`: the full pipeline (Mathematical Morphology and STN synthesis) of the chapter 3
    - `transient_generation.py`: the script for grnerating an image of chapter 3
- `tests`: a folder with tests