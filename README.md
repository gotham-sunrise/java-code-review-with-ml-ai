# Java Code Review Tool (DeepSeek AI & Machine Learning)

## Overview
The **Java Code Review Tool** is a Python-based utility that analyzes Java projects by:
- **Recursively scanning** `src/main/java/` for Java files.
- **Using DeepSeek AI** to review code and suggest improvements.
- **Classifying Java code** (e.g., class, method, conditional) using **Naïve Bayes ML**.
- **Detecting style inconsistencies** using **KMeans clustering**.
- **Automatically updating Java files** based on AI-suggested improvements.
- **Generating reports** with code review feedback, classification, and applied updates.

## Features
- **DeepSeek AI-powered code review** with automated suggestions.
- **Machine learning model** for Java code classification.
- **Style analysis** to detect formatting discrepancies.
- **Automated Java file updates** using AI-reviewed improvements.
- **CSV report generation** for structured insights.

## Installation
Ensure you have Python 3.8+ installed and run:

```sh
pip install -r requirements.txt
```

## Dependencies
```sh
pandas
requests
scikit-learn
joblib
```
Install them using:
```sh
pip install pandas requests scikit-learn joblib
```

## Usage
Run the tool with:
```sh
python code_review_deepseek.py <project_dir> <deepseek_api_key> --report <output_file>
```

### Arguments:
- `<project_dir>` - Path to the Java project directory.
- `<deepseek_api_key>` - Your DeepSeek AI API key.
- `--report <output_file>` - (Optional) Path to save the review report (default: `code_review_report.csv`).

### Example:
```sh
python code_review_deepseek.py /path/to/java/project sk-123456 --report review.csv
```

## Output
The tool generates:
1. **CSV Report (`code_review_report.csv`)** - Summary of analyzed Java files.
2. **DeepSeek AI Analysis** - Automated suggestions and feedback for each file.
3. **Classified Java Code** - Identifies file type (class, method, etc.).
4. **Style Analysis** - Detects formatting discrepancies using clustering.
5. **Automatically Updated Java Files** - AI-generated improvements applied to source files.

## Training Machine Learning Models
- **To retrain the code classifier:**
  ```sh
  rm code_review_model.pkl
  python code_review_deepseek.py /path/to/java/project sk-123456
  ```
- **To retrain the style detector:**
  ```sh
  rm style_detector.pkl
  python code_review_deepseek.py /path/to/java/project sk-123456
  ```

## Notes
- Ensure your **DeepSeek API key** is valid.
- Large Java projects may take longer to process.
- The **machine learning models** can be improved with additional training data.
- AI-based modifications will be directly written to Java files, so ensure you have backups before running.

## License
MIT License

## Contributions
Feel free to fork and contribute to enhance the tool!

## Author
Ming Li
