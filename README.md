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

