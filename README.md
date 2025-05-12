# 🎮 Movie Recommendation System using LLMs

This project demonstrates a novel approach to movie recommendation by combining **LLM-based genre prediction**, **script summarization**, and **user interaction data**. It uses **YouTube trailer transcriptions**, **Whisper**, and **LLAMA 3.1 8B via Langchain’s ChatGroq** to build a personalized ranking system for users.

---

## 🔍 Project Overview

Traditional recommendation systems rely heavily on numerical ratings and metadata. This project augments such systems by leveraging **natural language understanding of movie scripts** and **LLM reasoning** to generate more intuitive and context-aware recommendations.

---

## 🚀 Key Features

* **Script Extraction**:
  Transcribed audio from YouTube trailers using:

  * YouTube Transcript API
  * Whisper ASR (for trailers without transcripts)

* **Summary Generation**:
  Movie summaries generated from transcribed scripts using **LLAMA 3.1 8B**, enabling content-aware recommendation logic.

* **Genre Prediction**:
  LLAMA was also prompted to predict movie genres based on the generated summaries, adding semantic metadata for better personalization.

* **User Interaction-Based Prompting**:

  * Each user is associated with 20 watched movies (from most to least liked).
  * The first 15 movies (with summaries + genres) are provided as examples.
  * The model is prompted to predict rankings of the remaining 5 as a Python list (most to least liked).

* **Ranking Task**:
  Model's predicted rankings are compared to the actual user preferences to evaluate performance.

---

## 🧠 LLM Usage

* **Model**: LLaMA 3.1 8B
* **Platform**: Langchain + ChatGroq
* Prompts are structured to simulate human-like reasoning for genre prediction and movie preference understanding.

---

## 📊 Evaluation

* **Summary Quality**:

  * Evaluated using **ROUGE** metrics (ROUGE-1, ROUGE-2, ROUGE-L) to measure the overlap between generated and reference summaries.

* **Genre Classification**:

  * Assessed using **Precision**, **Recall**, and **F1 Score**, computed **per genre** to understand classification performance across categories.

* **Recommendation Performance**:

  * Measured using **Precision\@k** and **NDCG (Normalized Discounted Cumulative Gain)** to evaluate how well the predicted rankings align with actual user preferences.

---

## 📁 Datasets

* **User Interaction Data**:
  Movie Lens(100k) dataset - 943 users × 1600 movies, with ratings from 1 to 5.
  
* **Fallback Handling**:
  If a trailer summary was not available, LLAMA generated summaries from model knowledge.

---

## ✅ Applications

* Personalized recommendation engines
* Content-aware streaming suggestions
* LLM-driven multimedia understanding

---

## 📌 Future Enhancements

* Add fine-tuned LLMs trained specifically on movie plots
* Incorporate user demographic/contextual data
* Add feedback loop to refine recommendations with real-time data
