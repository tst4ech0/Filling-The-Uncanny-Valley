# Essay Style Checker

An AI-powered essay authenticity verification tool using stylometric analysis to detect potential AI-generated or plagiarized content.

## A Note From The "Creator"
This tool was built starting around Feb 2026. I am an idiot who knows just enough about code to get myself in trouble. The majority of this system is build by Claude Sonnet 4.5. I have done my best to robustly test everything to double check it works as intended. Please only trust this software as far as you can throw it. Before deploying in any meaningful way, please perform a full audit of the code and test things out with sample data to make sure it is performing reliably before implementation into a real learning environment. 

## Overview

This tool creates a personalized writing profile for each student based on baseline essays, then compares new submissions against that profile to detect stylistic inconsistencies. Unlike generic AI detectors, this approach identifies deviations from a specific writer's patterns, making it more reliable and defensible.

## Features

- **Multi-format support**: Accepts .txt, .docx, and .pdf files
- **Stylometric analysis**: Extracts 9+ writing features including:
  - Sentence length patterns
  - Lexical diversity
  - Part-of-speech distributions
  - Punctuation usage
  - Average word length
- **Statistical scoring**: Uses z-scores to measure deviation from baseline
- **Visual feedback**: Color-coded feature comparison table
- **User-friendly interface**: Clean web UI requiring no technical knowledge

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Setup

1. **Clone this repository**
```bash
   git clone https://github.com/tst4ech0/Filling-The-Uncanny-Valley.git
   cd Filling-The-Uncanny-Valley
```

2. **Create a virtual environment**
```bash
   python -m venv venv
```

3. **Activate the virtual environment**
   
   Windows:
```bash
   venv\Scripts\activate.bat
```
   
   Mac/Linux:
```bash
   source venv/bin/activate
```

4. **Install dependencies**
```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
```

## Usage

1. **Start the application**
```bash
   python app.py
```

2. **Open your browser**
   
   Navigate to: `http://127.0.0.1:5000`

3. **Upload baseline essays**
   - Upload 2-5 essays known to be authentic student work
   - Supports .txt, .docx, and .pdf formats
   - More baselines = better statistical accuracy

4. **Test a new essay**
   - Upload the essay you want to verify
   - Click "Analyze Essay"

5. **Review results**
   - **Similarity score**: 0-100% (higher = more similar to baseline)
   - **Feature analysis**: Shows which writing patterns differ most
   - **Z-scores**: Statistical measure of deviation
     - < 1.5: Normal variation (green)
     - 1.5-3.0: Moderate difference (orange)
     - > 3.0: Significant difference (red)

## How It Works

### Baseline Profile Creation
1. Each baseline essay is analyzed to extract stylometric features
2. Statistical profile is created (mean and standard deviation for each feature)
3. This profile represents the student's typical writing style

### Essay Comparison
1. New essay is analyzed using the same feature extraction
2. Each feature is compared to the baseline using z-scores
3. Z-score = (new_value - baseline_mean) / baseline_stdev
4. Similarity score = 100 - (average_z_score × 20)

### Interpretation
- **85-100%**: Highly consistent with baseline style
- **70-84%**: Generally consistent, minor variations
- **50-69%**: Moderate differences, worth reviewing
- **30-49%**: Significant stylistic differences, likely flag
- **0-29%**: Major inconsistencies, strong indication of different authorship

## Use Cases

- **Academic integrity**: Flag potentially AI-generated or plagiarized essays
- **Student support**: Identify students who may need writing assistance
- **Progress tracking**: Detect genuine improvement in writing skills
- **Verification**: Confirm authorship of high-stakes assignments

## Limitations

- Requires baseline essays to be available
- Writing style can legitimately change over time (especially in writing courses)
- Different essay topics/formats may affect some features
- Should be used as a screening tool, not definitive proof
- Best used in combination with other academic integrity measures

## Considerations for baseline selections
Use essays with similar prompts types and expectations. Using a diverse writing sample leads to higher variance in the baseline, and thus a much higher chance for false positives. 
- Example of a bad set of samples for a baseline dataset
  - A discussion post reply from canvas discussing class expectations
  - A chemistry lab report detailing experimental work
  - An English essay about Shakespear
- Example of what would make a good baseline dataset
  - An essay from the student’s poetry class last semester
  - An English essay about Shakespear turned in earlier this semester
  - Multiple discussion posts focused around class topics and material

Keep in mind that how effective this program is at telling students from AI relies heavily on being able to effectively analyze patterns in the student, not patterns in AI. Ergo, the baseline essays are critically important to getting good results

## Technical Details

### Features Extracted
- Average sentence length
- Lexical diversity (unique words / total words)
- Average word length
- Part-of-speech ratios (nouns, verbs, adjectives, adverbs)
- Punctuation ratios (commas, semicolons)

### Tech Stack
- **Backend**: Python 3.11, Flask
- **NLP**: spaCy with en_core_web_sm model
- **Document parsing**: python-docx, pdfplumber
- **Statistics**: Python statistics module
- **Frontend**: Vanilla HTML/CSS/JavaScript

## Project Structure
```
essay-checker/
├── app.py                  # Flask web application
├── feature_extractor.py    # Stylometric feature extraction
├── compare_essay.py        # Similarity scoring logic
├── student_profile.py      # Profile creation and management
├── file_reader.py          # Multi-format file parsing
├── templates/
│   └── index.html         # Web interface
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Future Enhancements

- Feature weighting based on empirical data
- Support for additional file formats
- Batch processing for multiple essays
- Persistent student profile storage
- API endpoint for programmatic access
- Enhanced visualizations (graphs, heatmaps)
- Multi-language support

## Contributing

This project was developed as a proof of concept for educational technology. Contributions, suggestions, and feedback are welcome!

## License

MIT

## Acknowledgments

Developed as part of [competition/course name] to address the growing challenge of AI-generated academic content while respecting student privacy and emphasizing educational support over punitive measures.

## Contact

trnm@durhamtech.edu

---

**Note**: This tool is designed as a screening mechanism to flag essays for human review, not as definitive proof of academic dishonesty. Always follow your institution's academic integrity policies and provide students with due process.
