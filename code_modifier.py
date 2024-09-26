import os
import openai
import argparse
from pathlib import Path
from collections import defaultdict
import re
import subprocess

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # or set it directly

# Define code file extensions and their corresponding parsers
CODE_EXTENSIONS = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.java': 'java',
    '.cs': 'csharp',
    '.cpp': 'cpp',
    '.c': 'c',
    '.rb': 'ruby',
    '.php': 'php',
    '.swift': 'swift',
    '.go': 'go',
    '.kt': 'kotlin',
    '.rs': 'rust',
    '.dart': 'dart'
}

def is_code_file(file_path):
    return file_path.suffix.lower() in CODE_EXTENSIONS

def extract_symbols(file_path, language):
    # Placeholder function to extract symbols from code
    # For simplicity, we'll use regex for some languages
    symbols = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if language == 'python':
            # Simple regex to find class and function names
            symbols.update(re.findall(r'^class\s+(\w+)', content, re.MULTILINE))
            symbols.update(re.findall(r'^def\s+(\w+)', content, re.MULTILINE))
        elif language in ['javascript', 'typescript']:
            # Find function and class names
            symbols.update(re.findall(r'(?:function|class)\s+(\w+)', content))
        # Add more languages and parsing logic as needed
        # For unsupported languages, return an empty set
    except Exception as e:
        print(f"Error extracting symbols from {file_path}: {e}")
    return symbols

def process_files(file_paths, prompt, symbol_table):
    # Process files with OpenAI API, including context about symbol changes
    for file_path in file_paths:
        language = CODE_EXTENSIONS.get(file_path.suffix.lower())
        if not language:
            continue  # Unsupported language

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Include symbol table in the prompt to provide context
            symbol_changes = "\n".join([f"{old} -> {new}" for old, new in symbol_table.items()])
            extended_prompt = f"{prompt}\n\nHere are the symbol changes to apply throughout the codebase:\n{symbol_changes}\n\nModify the following {language} code accordingly:\n{content}"

            messages = [
                {"role": "system", "content": "You are an expert software developer."},
                {"role": "user", "content": extended_prompt}
            ]

            # Call the OpenAI API
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',  # or 'gpt-4' if you have access
                messages=messages,
                max_tokens=2048,
                temperature=0,
            )

            modified_content = response['choices'][0]['message']['content']

            # Write the modified content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)

            print(f"Processed: {file_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

def build_symbol_table(root_path):
    symbol_table = defaultdict(set)  # symbol -> set of file paths
    file_paths = []

    for root, dirs, files in os.walk(root_path):
        for file_name in files:
            file_path = Path(root) / file_name
            if is_code_file(file_path):
                language = CODE_EXTENSIONS.get(file_path.suffix.lower())
                symbols = extract_symbols(file_path, language)
                for symbol in symbols:
                    symbol_table[symbol].add(file_path)
                file_paths.append(file_path)
    return symbol_table, file_paths

def main():
    parser = argparse.ArgumentParser(description='Modify code files using OpenAI API.')
    parser.add_argument('path', type=str, help='Path to the project root directory')
    parser.add_argument('prompt', type=str, help='Prompt describing the changes to be made')
    args = parser.parse_args()

    root_path = args.path
    prompt = args.prompt

    if not os.path.isdir(root_path):
        print("The provided path is not a directory.")
        return

    # Step 1: Build the symbol table
    symbol_table, file_paths = build_symbol_table(root_path)

    # Step 2: Determine the changes to be made (this is a simplified example)
    # In a real scenario, you'd parse the prompt or use the OpenAI API to get the changes
    # For now, let's assume we have a mapping of old symbol names to new ones
    # For example, suppose the prompt is to rename 'OldClass' to 'NewClass'
    # We'll simulate that here:

    # This part would be dynamic based on the prompt and the AI's response
    symbol_changes = {
        'OldClass': 'NewClass',
        'old_function': 'new_function',
        # Add more symbol changes as needed
    }

    # Update the symbol table with the changes
    updated_symbol_table = {}
    for old_symbol, new_symbol in symbol_changes.items():
        updated_symbol_table[old_symbol] = new_symbol

    # Step 3: Process files with the updated symbol table
    process_files(file_paths, prompt, updated_symbol_table)

if __name__ == '__main__':
    main()
