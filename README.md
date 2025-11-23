# Nirmaan AI – Communication Scoring Tool

## Project Overview

This project implements an AI-based tool to analyse and score students’ spoken communication skills from transcript text. The primary use case is evaluating short self-introductions.

The system computes rubric-based scores (0–100) and provides per-criterion feedback using a combination of:

1. Rule-based scoring: keyword presence and word-count checks.
2. NLP-based semantic scoring: semantic similarity between transcript and rubric descriptions using sentence embeddings.
3. Weighted aggregation: criterion weights from the provided rubric are applied to compute the final normalized score.

The tool outputs both overall scores and per-criterion feedback, including matched keywords, semantic similarity, and length suggestions.

## Features

- Input transcript via web UI (paste text).
- Compute overall score (0–100).
- Compute per-criterion score with detailed feedback:
  - Matched keywords
  - Semantic similarity (via embeddings)
  - Word count suggestions
- Simple and responsive frontend.
- Can be run locally or deployed publicly.

## Technology Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- NLP Tools:
  - Sentence Transformers (all-MiniLM-L6-v2)
- Data Handling: Pandas (for reading rubric CSV/Excel)
- Deployment: Local server, free-tier cloud hosting

## Project Structure
    nirmaan-ai-communication-scoring/
    │
    ├── app.py                # Flask backend
    ├── scoring.py            # Scoring logic (rule-based + NLP + weighting)
    ├── templates/
    │   └── index.html        # Frontend UI
    ├── static/
    │   ├── style.css         # Styling
    │   └── script.js         # JS for frontend interaction
    ├── rubric.csv            # Rubric file (criteria, keywords, weights)
    ├── requirements.txt      # Python dependencies
    └── README.md             # This file

## Installation & Setup

1. Clone the repository

2. Create a virtual environment (optional but recommended)
      python -m venv venv
      source venv/bin/activate   # Linux/Mac
      venv\Scripts\activate      # Windows

3. Install dependencies
      pip install -r requirements.txt

4. Run the application
      python app.py

5. Open in browser
      Navigate to: http://127.0.0.1:5000/
      Paste your transcript text and click Score to view results.

## Scoring Methodology

1. Keyword-based scoring
- Checks if rubric-specified keywords are present in the transcript.
- Partial score based on the fraction of keywords found.

2. Semantic similarity scoring
- Uses sentence-transformers to compute embeddings of transcript vs rubric descriptions.
- Cosine similarity is normalized to produce a score between 0–1.

3. Length/word count check
- Compares transcript length with rubric-specified min/max words.
- Adjusts score and provides feedback if too short or too long.

4. Combined score
- Weighted combination: 40% keywords, 40% semantic similarity, 20% length.
- Per-criterion scores are weighted by rubric-defined weight.
- Final overall score normalized to 0–100.

5. Feedback
- Provides per-criterion feedback including:
   - Word count suggestions
   - Keyword matches
   - Semantic similarity (internally used)

## Frontend

- Paste transcript text in the textarea.
- Click Score to see overall and per-criterion results.
- Results displayed in a clean table with score and feedback.

## Example Output
    {
      "overall_score": 82.5,
      "word_count": 52,
      "criteria": [
        {"criterion_name": "Introduction", "score": 85, "feedback": "Length OK"},
        {"criterion_name": "Age & Class", "score": 80, "feedback": "Too short"}
      ]
    }

