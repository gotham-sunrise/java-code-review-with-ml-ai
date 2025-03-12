# Java Unit Test Generator (DeepSeek AI)

## Overview
The **Java Unit Test Generator** is a Python tool that automatically generates **JUnit tests** for all Java classes in a project using **DeepSeek AI**. It:
- **Recursively scans** `src/main/java/` to find Java files.
- **Generates unit tests** for each class using **JUnit** and **Mockito** (if applicable).
- **Saves tests** in `src/test/java/`, maintaining the original project structure.

## Features
- **DeepSeek AI-powered test generation**.
- **Automatically detects Java classes** in a project.
- **Uses Mockito for dependency mocking**.
- **Generates structured test files** in `src/test/java/`.

## Installation
Ensure you have Python 3.8+ installed and run:

```sh
pip install -r requirements.txt
```

## Dependencies
```sh
requests
```
Install using:
```sh
pip install requests
```

## Usage
Run the tool with:
```sh
python generate_java_tests.py <project_dir> <deepseek_api_key>
```

### Arguments:
- `<project_dir>` - Path to the Java project directory.
- `<deepseek_api_key>` - Your DeepSeek AI API key.

### Example:
```sh
python generate_java_tests.py /path/to/java/project sk-123456
```

## Output
The tool generates:
1. **JUnit test classes** saved in `src/test/java/`.
2. **Mockito-based tests** for dependencies.
3. **Unit tests matching the structure** of your Java project.

## Notes
- Ensure your **DeepSeek API key** is valid.
- Large projects may take longer to process.
- The generated tests should be manually reviewed for correctness before use.

## License
MIT License

## Contributions
Feel free to fork and improve the tool!

## Author
Ming Li

