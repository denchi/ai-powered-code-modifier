# AI-Powered Code Modifier

This project is a Python application that leverages OpenAI's GPT models to analyze a codebase, generate a change plan, and apply consistent modifications across the codebase based on user input.

## Features

- Analyzes a codebase for classes, functions, and dependencies.
- Automatically suggests changes based on the user prompt (e.g., refactoring, upgrading frameworks, renaming symbols).
- Consistently applies changes across all files in the project.
- Works with multiple programming languages including Python, JavaScript, TypeScript, Java, and more.

## Requirements

- Python 3.x
- An OpenAI API Key

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/denchi/ai-powered-code-modifier.git
    cd ai-powered-code-modifier
    ```

2. **Install Dependencies:**

    Make sure you have `pip` installed, then run:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set the OpenAI API Key:**

    You need to set your OpenAI API key as an environment variable.

    ```bash
    export OPENAI_API_KEY='your-api-key'
    ```

## Usage

To use the AI-powered code modifier, run the `code_modifier.py` script, specifying the path to your project and the prompt for the changes you want:

```bash
python code_modifier.py /path/to/your/project "Please upgrade the project to be compatible with Python 3.10."
