# Personalized Learning Path Generator

## Overview
The Personalized Learning Path Generator is a tool designed to help users achieve their career and personal development goals. It uses a combination of goal-oriented quizzes, analysis, and roadmap generation to create a customized path for the user.

## Installation
To set up the environment, install the required dependencies listed in `requirments.txt`:
```
langchain-groq
langchain-core
asyncio
```

## Components

### 1. `LLama_config.py`
This file contains the core configuration and classes for the project.

- **Classes:**
  - **LLM_Config**: Initializes the LLM model using the `ChatGroq` API.
  - **GoalQuiz**: Inherits from `LLM_Config` and handles quiz interactions.
  - **Analyzer**: Inherits from `LLM_Config` and analyzes quiz results.
  - **RoadmapGenerator**: Inherits from `LLM_Config` and generates a personalized roadmap based on quiz analysis.

### 2. `main_v4.py`
This file contains the main Streamlit application code.

- **Functions:**
  - **run_quiz(quiz_type)**: Runs the goal-oriented quiz.
  - **main()**: Initializes the Streamlit app and handles the quiz workflow.

### 3. `setup.py`
This file contains the setup for chat history and processing interactions.

- **Classes:**
  - **ChatSetup**: Manages chat history and parses responses from the LLM.

### 4. `textprocessor.py`
This file contains the text preprocessing functions.

- **Classes:**
  - **TextPreprocessor**: Cleans and preprocesses text, extracts key phrases.

## Usage

1. **Run the Streamlit App:**
   ```bash
   streamlit run main_v4.py
   ```
2. **Follow the prompts to complete the goal-oriented quiz.**
3. **View the analysis and personalized roadmap generated based on your responses.**

## Example
```python
# Sample usage of TextPreprocessor
from textprocessor import TextPreprocessor

input_text = "Welcome to the complete HTML and CSS course. In this course, we're going to learn how to build websites from a beginner to a professional level."
preprocessor = TextPreprocessor()
result = preprocessor.preprocess_for_llm(input_text)
print("Key Phrases: ", result['key_phrases'])
```

This README provides an overview of the main components and usage instructions for the Personalized Learning Path Generator.
