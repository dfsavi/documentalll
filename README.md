# documentalll

> **Status:** Work in progress

`documentalll` is a Python CLI for batch-generating Markdown documentation from source files by sending them to an Ollama server. It reads every file in the given input directory, prepends an instructional prompt, and writes the generated explanations to a mirrored folder structure under `output/`.

## Features
- Recursively walks an input folder and processes every file it finds
- Calls an Ollama-compatible API endpoint with a configurable model and prompt
- Persists responses as Markdown, mirroring the original directory layout

## Requirements
- Python 3.9+
- Access to an Ollama server reachable at `http://192.168.0.18:11434/api/generate` (adjust the code or network config if your server differs)

## Setup
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```
The editable install registers the `documentalll` console script.

## Usage
Process all files in the default `input/` directory:
```sh
documentalll
```
Customize the input directory, Ollama model, or prompt:
```sh
documentalll --input path/to/code --model my-model --prompt "Explain this code for internal docs."
```
Generated Markdown files appear in `output/`, keeping the same subfolder structure as the originals.

## Notes
- The default prompt emphasizes beginner-friendly explanations in Markdown. Supply your own prompt for other styles.
- Non-text or exceptionally large files may need filtering before running the tool.
- Expect interfaces and configuration options to change while the project is still in progress.
