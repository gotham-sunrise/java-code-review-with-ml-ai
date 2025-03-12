import os
import argparse
import pandas as pd
import requests
import joblib
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans

class JavaCodeReviewer:
    def __init__(self, project_dir, api_key, model_file="code_review_model.pkl", style_model_file="style_detector.pkl"):
        self.project_dir = project_dir
        self.api_key = api_key
        self.model_file = model_file
        self.style_model_file = style_model_file
        self.model = self.load_model()
        self.style_model = self.load_style_model()
        self.reports = defaultdict(str)

    def traverse_project(self):
        """Recursively find all Java files in the src/main/java directory."""
        java_files = []
        src_path = os.path.join(self.project_dir, "src", "main", "java")
        
        for root, _, files in os.walk(src_path):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))
        
        return java_files

    def read_java_file(self, file_path):
        """Read and return the content of a Java file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def analyze_with_deepseek(self, java_code):
        """Use DeepSeek API to perform code review and suggest improvements."""
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {
            "model": "deepseek-code",
            "messages": [
                {"role": "system", "content": "You are a professional code reviewer. Suggest improvements and provide an updated version of the Java code."},
                {"role": "user", "content": f"Review the following Java code, suggest improvements, and return the modified code:\n{java_code}"}
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "DeepSeek API error: Unable to review code."

    def update_java_file(self, file_path, updated_code):
        """Overwrite the original Java file with the AI-suggested improvements."""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_code)
        print(f"Updated file: {file_path}")

    def generate_report(self, output_file):
        """Generate a report for the reviewed Java files and apply AI-suggested updates."""
        java_files = self.traverse_project()
        
        report_data = []
        for java_file in java_files:
            code_content = self.read_java_file(java_file)
            review_feedback = self.analyze_with_deepseek(code_content)
            
            if "Updated Code:" in review_feedback:
                updated_code = review_feedback.split("Updated Code:")[1].strip()
                self.update_java_file(java_file, updated_code)
            else:
                updated_code = "No update provided."
            
            self.reports[java_file] = review_feedback
            report_data.append({"File": java_file, "Review": review_feedback, "Updated": updated_code[:100]})
        
        df = pd.DataFrame(report_data)
        df.to_csv(output_file, index=False)
        print(f"Review report saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Java Code Review Tool using DeepSeek AI and Machine Learning")
    parser.add_argument("project_dir", help="Path to the Java project directory")
    parser.add_argument("apikey", help="DeepSeek API Key")
    parser.add_argument("--report", help="Output CSV file for review report", default="code_review_report.csv")
    args = parser.parse_args()
    
    reviewer = JavaCodeReviewer(args.project_dir, args.apikey)
    reviewer.generate_report(args.report)
