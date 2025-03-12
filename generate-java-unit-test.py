import os
import argparse
import requests

def traverse_project(project_dir):
    """Recursively find all Java files in the src/main/java directory."""
    java_files = []
    src_path = os.path.join(project_dir, "src", "main", "java")
    
    for root, _, files in os.walk(src_path):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    
    return java_files


def read_java_file(file_path):
    """Read and return the content of a Java file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def generate_unit_test(api_key, java_code):
    """Use DeepSeek API to generate unit tests for the given Java code."""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-code",
        "messages": [
            {"role": "system", "content": "You are a professional software engineer specialized in Java unit testing. Generate a complete JUnit test class for the following Java code, using Mockito if necessary."},
            {"role": "user", "content": f"Generate JUnit test for this class:\n{java_code}"}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "DeepSeek API error: Unable to generate unit test."


def save_unit_test(file_path, unit_test_code):
    """Save the generated unit test to a corresponding test directory."""
    test_dir = file_path.replace("src/main/java", "src/test/java")
    test_dir = os.path.dirname(test_dir)
    os.makedirs(test_dir, exist_ok=True)
    
    test_file = os.path.join(test_dir, os.path.basename(file_path).replace(".java", "Test.java"))
    
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(unit_test_code)
    print(f"Generated unit test: {test_file}")


def generate_tests_for_project(project_dir, api_key):
    """Generate unit tests for all Java classes in a project."""
    java_files = traverse_project(project_dir)
    
    for java_file in java_files:
        java_code = read_java_file(java_file)
        unit_test_code = generate_unit_test(api_key, java_code)
        save_unit_test(java_file, unit_test_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Java Unit Test Generator using DeepSeek AI")
    parser.add_argument("project_dir", help="Path to the Java project directory")
    parser.add_argument("apikey", help="DeepSeek API Key")
    args = parser.parse_args()
    
    generate_tests_for_project(args.project_dir, args.apikey)
