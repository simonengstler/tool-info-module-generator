# Tool-Info Module Generator for BenchExec

This tool automates the generation of tool-info module files for [BenchExec](https://github.com/sosy-lab/benchexec) using GPT-4o mini.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Setting Environment Variables](#setting-environment-variables)
    - [Set OpenAI API Key](#set-openai-api-key)
    - [(OPTIONAL:) Set Execution Iterations](#set-execution-iterations)
    - [(OPTIONAL:) Set Refinement Iterations](#set-refinement-iterations)
  - [Running the Tool Info Module Process](#running-the-tool-info-module-process)

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.6 or higher
- `python-dotenv` package
- Add `template/mock_exes` to `PATH` (e.g. on Linux: `echo 'export PATH=$PWD/template/mock_exes:$PATH' >> ~/.bashrc`)
- Provide a (mock) executable (e.g. copy paste an existing one, rename it and make it executable) for the tool that you want to create the tool-info module file for.

## Installation

Clone the repository to your local machine:

git clone https://github.com/yourusername/benchexec-tool-info-generator.git  
cd benchexec-tool-info-generator

## Configuration

The script relies on several environment variables to function correctly. These variables are stored in a `.env` file. You can set these variables using the provided subcommands.

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key.
- `EXECUTION_ITERATIONS`: Number of execution iterations. Recommended: 2
- `REFINEMENT_ITERATIONS`: Number of refinement iterations. Recommended: 2

## Usage

The script provides several subcommands to set environment variables and run the tool info module process.
Make sure to first create a .env file with the following template:

```
OPENAI_API_KEY=YOUR_KEY
EXECUTION_ITERATIONS=2
REFINEMENT_ITERATIONS=2
```

### Setting Environment Variables

You can set various environment variables using the following subcommands:

#### Set OpenAI API Key

Sets the OpenAI API key in the `.env` file.

```python3 main.py set_openai_key your_openai_api_key_here```

#### (OPTIONAL:) Set Execution Iterations

Sets the number of execution iterations in the `.env` file.

```python3 main.py set_execution_iterations 2```

#### (OPTIONAL:) Set Refinement Iterations

Sets the number of refinement iterations in the `.env` file.

```python3 main.py set_refinement_iterations 2```

### Running the Tool Info Module Process

To run the tool info module process, use the following command:

```python3 main.py generator```

This command reads the necessary inputs and generates tool-info module files using the specified configuration.
