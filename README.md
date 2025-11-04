# Your-AI-Research-Assistant
This AI tool generates realistic research abstracts from just a title, offers customizable summaries, and ensures privacy with local execution using Streamlit and Hugging Face. Optimized with Apple MPS, it delivers fast, smooth, and secure performance for researchers.

Find YouTube Video Demo Here: https://www.youtube.com/watch?v=WXZOS3-3it4

📚 Generative Research Paper Summarizer

This project is a lightweight, two-stage AI application built with Streamlit and Hugging Face models designed to combat information overload by dynamically generating and then summarizing research paper abstracts based on a user-provided title.

It is ideal for researchers, students, and engineers looking to quickly grasp the core concepts of hypothetical papers or tailor explanations for different audiences.

✨ Features

Custom Content Generation: Generate a plausible abstract (Motivation, Method, Results, Conclusion) for any paper title, making the summarization task dynamic and context-agnostic.

Two-Stage Model Pipeline: Uses dedicated, optimized models for distinct tasks: one for stable text generation and one for abstractive summarization.

Customizable Output: Users can select the Style (e.g., Beginner-Friendly, Technical) and Length (Short, Medium, Long) of the final summary.

Local and Open Source: The application runs entirely on local machine resources using open-source Hugging Face models (t5-small and facebook/bart-base), ensuring data privacy and local execution stability.

Performance Optimized: Includes explicit configuration for performance on Apple MPS (Metal Performance Shaders) where available.

🧠 Architecture: The Two-Stage Pipeline

The application processes a user query in two sequential steps:

Stage

Model Used

Task

Primary Goal

Engineering Note

1. Content Generation

t5-small

text2text-generation

Create a coherent, multi-part mock research abstract (100-200 words).

Uses Beam Search (num_beams=4) to prevent repetitive output and ensure quality content.

2. Stylistic Summarization

facebook/bart-base

summarization

Take the generated abstract and synthesize it according to the user's selected style and length parameters.

BART is chosen for its superior abstractive capabilities compared to T5's more extractive nature.

The Streamlit interface ties these two pipelines together, providing input controls and displaying the final, styled summary.

🚀 Installation and Setup

Prerequisites

You need Python 3.8+ installed. All required dependencies are listed in the requirements file (assuming you create one) or can be installed directly.

# Assuming Python is installed
pip install streamlit transformers torch accelerate


Running the Application

Clone the Repository (Replace with your actual link):

git clone https://github.com/naveen151094/Your-AI-Research-Assistant
cd ai_research_summarizer


Save the Python Code:
Save the provided Python code as research_summarizer.py in the root directory.

Run the Streamlit App:

streamlit run ai_research_summarizer.py


The application will automatically open in your web browser (usually at http://localhost:8501).

💻 Usage

Enter a Title: In the main input box, type the title of the research paper you want to explore (e.g., "Attention Is All You Need").

Select Parameters: Use the sidebar controls to choose your desired Summary Style (e.g., Beginner-Friendly) and Length (e.g., Short).

Generate: Click the "Generate Summary" button.

The app will first generate the synthetic abstract (Stage 1), display it, and then feed it into the summarization model (Stage 2) to show the final, customized summary.

🤝 Contribution

Contributions, issues, and feature requests are welcome! Feel free to check the "https://github.com/naveen151094/Your-AI-Research-Assistant" and submit a pull request.
