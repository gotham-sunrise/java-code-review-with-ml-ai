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
        """Use DeepSeek API to perform code review."""
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {
            "model": "deepseek-code",
            "messages": [
                {"role": "system", "content": "You are a professional code reviewer."},
                {"role": "user", "content": f"Review the following Java code and suggest improvements:\n{java_code}"}
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "DeepSeek API error: Unable to review code."

    def load_model(self):
        """Load or train a machine learning model for code classification."""
        if os.path.exists(self.model_file):
            return joblib.load(self.model_file)
        else:
            return self.train_model()

    def train_model(self):
        """Train a Naïve Bayes classifier for classifying Java code snippets."""
        sample_codes = [
            "public class Example { public static void main(String[] args) { System.out.println(\"Hello, World!\"); } }",
            "private void processData() { int x = 10; x += 5; }",
            "if (value > 10) { System.out.println(\"High value\"); } else { System.out.println(\"Low value\"); }"
        ]
        labels = ["class", "method", "conditional"]
        
        model = make_pipeline(CountVectorizer(), MultinomialNB())
        model.fit(sample_codes, labels)
        joblib.dump(model, self.model_file)
        return model

    def classify_code(self, java_code):
        """Classify Java code snippets using the trained model."""
        return self.model.predict([java_code])[0]

    def load_style_model(self):
        """Load or train a machine learning model for detecting code style discrepancies."""
        if os.path.exists(self.style_model_file):
            return joblib.load(self.style_model_file)
        else:
            return self.train_style_model()

    def train_style_model(self):
        """Train a KMeans clustering model for style detection."""
        sample_styles = [
            "public class Test { public void doSomething() {} }",
            "class Test{ void doSomething(){} }",
            "public class Test\n{\n  public void doSomething()\n  {\n  }\n}" 
        ]
        
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(sample_styles)
        
        model = KMeans(n_clusters=3, random_state=42)
        model.fit(X)
        joblib.dump((model, vectorizer), self.style_model_file)
        return model, vectorizer

    def detect_style_discrepancy(self, java_code):
        """Detects whether the given Java code follows the dominant style in the project."""
        model, vectorizer = self.style_model
        X = vectorizer.transform([java_code])
        cluster = model.predict(X)[0]
        return f"Style cluster {cluster}"

    def generate_report(self, output_file):
        """Generate a report for the reviewed Java files."""
        java_files = self.traverse_project()
        
        report_data = []
        for java_file in java_files:
            code_content = self.read_java_file(java_file)
            review_feedback = self.analyze_with_deepseek(code_content)
            classification = self.classify_code(code_content)
            style_feedback = self.detect_style_discrepancy(code_content)
            
            self.reports[java_file] = review_feedback
            report_data.append({"File": java_file, "Category": classification, "Review": review_feedback, "Style": style_feedback})
        
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
