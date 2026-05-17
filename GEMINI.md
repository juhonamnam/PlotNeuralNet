# PlotNeuralNet

A LaTeX/TikZ-based tool for drawing neural network architectures for reports and presentations, featuring a Python interface for programmatic generation.

## Project Overview

*   **Purpose:** Programmatically generate high-quality 2D/3D neural network diagrams.
*   **Architecture:**
    *   **Python DSL (`pycore/`):** A set of Python functions (`tikzeng.py`, `blocks.py`) that generate TikZ LaTeX code.
    *   **LaTeX Styles (`layers/`):** Custom `.sty` files that define the visual appearance of layers (e.g., `Box`, `Ball`, `RightBandedBox`).
    *   **Orchestration (`tikzmake.sh`):** A shell script that runs the Python generator, compiles the resulting `.tex` file using `pdflatex`, and opens the PDF.

## Building and Running

### Prerequisites
*   LaTeX distribution (e.g., TeX Live, MiKTeX) with `standalone`, `import`, and `tikz` packages.
*   Python 3.

### Workflow
To generate a diagram from a Python script (e.g., `pyexamples/test_simple.py`):

1.  **Navigate to the script's directory:**
    ```bash
    cd pyexamples/
    ```
2.  **Run the build script:**
    ```bash
    bash ../tikzmake.sh test_simple
    ```
    *(Note: Omit the `.py` extension when passing the filename to `tikzmake.sh`)*

The script will:
1.  Run `python test_simple.py` to create `test_simple.tex`.
2.  Run `pdflatex test_simple.tex` to create `test_simple.pdf`.
3.  Clean up temporary LaTeX files (`.aux`, `.log`, etc.) and the generated `.tex` file.
4.  Open the resulting `test_simple.pdf`.

## Development Conventions

### Python DSL Usage
*   **Imports:** Scripts usually need to add the project root to `sys.path` to import `pycore`.
    ```python
    import sys
    sys.path.append('../')
    from pycore.tikzeng import *
    from pycore.blocks import *
    ```
*   **Architecture Definition:** Use a list of `to_*` and `block_*` function calls.
*   **Coordinates and Offsets:**
    *   Positions are defined as `(x, y, z)` strings.
    *   Use `offset="(dx, dy, dz)"` to position layers relative to others.
    *   Use `to="(layer_name-east)"` to snap a layer to the exit anchor of another.
*   **Connections:** Use `to_connection("source", "destination")` to draw arrows between layers.

### Adding New Layers
*   New primitive shapes should be defined in `layers/` as LaTeX `\tikzset` or `\pic` definitions.
*   Corresponding Python wrappers should be added to `pycore/tikzeng.py`.
*   Composite patterns (e.g., Conv+ReLU+Pool) should be added to `pycore/blocks.py`.

### File Structure
*   `pycore/`: Core Python library.
*   `layers/`: LaTeX style and initialization files.
*   `examples/`: Pure LaTeX examples (useful for debugging styles).
*   `pyexamples/`: Reference Python implementations.
*   `mymodels/`: Recommended location for user-defined models.
