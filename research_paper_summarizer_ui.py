import streamlit as st
import requests  # Required for making HTTP requests to the Gemini API
import json
import time

# --- Gemini API Configuration ---
# NOTE: The Canvas environment is set up to handle authentication if the key is empty.
# If running locally, you must install 'requests' and optionally provide a key.
API_KEY = "YOUR_GEMINI_API_KEY" 
# UPDATED: Changed the model endpoint to use gemini-2.0-flash as requested
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
MODEL_ID = "Gemini 2.0 Flash" # UPDATED: For display purposes

# List of well-known paper titles to be used as prompts
RESEARCH_PAPER_TITLES = [
    "Attention Is All You Need", 
    "BERT: Pre-training of Deep Bidirectional Transformers", 
    "GPT-3: Language Models are Few-Shot Learners", 
    "Diffusion Models Beat GANs on Image Synthesis",
    "Reinforcement Learning from Human Feedback (RLHF)",
    "ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)",
]

# --- Helper Function for API Calls with Retry ---

def gemini_api_call(user_prompt, system_instruction, max_tokens, retry_count=3):
    """
    Makes a request to the Gemini API with exponential backoff.
    """
    
    headers = {'Content-Type': 'application/json'}
    
    # Configure generation parameters
    generation_config = {
        "maxOutputTokens": max_tokens,
        # Use lower temp for summarization/higher for creation
        "temperature": 0.7 if "Summarize" in system_instruction else 0.9, 
    }
    
    payload = {
        "contents": [{"parts": [{"text": user_prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "generationConfig": generation_config,
    }

    url = f"{API_URL}?key={API_KEY}" if API_KEY else API_URL

    for i in range(retry_count):
        try:
            # st.info(f"Attempting API call {i + 1}...")
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            # --- Custom Error Check for API Key Issue (403 Forbidden) ---
            if response.status_code == 403:
                st.error("API Error (403 Forbidden): The API key is missing or invalid. If running locally, please ensure API_KEY is set in the script.")
                return ""
            # -----------------------------------------------------------
                
            response.raise_for_status() # Raises an HTTPError for other bad responses (4xx or 5xx)
            
            result = response.json()
            
            # Extract generated text
            candidate = result.get('candidates', [{}])[0]
            text = candidate.get('content', {}).get('parts', [{}])[0].get('text', '').strip()
            
            return text
            
        except requests.exceptions.RequestException as e:
            if i < retry_count - 1:
                wait_time = 2 ** i
                time.sleep(wait_time)
            else:
                st.error(f"Final API call failed after {retry_count} attempts: {e}")
                return ""
        except Exception as e:
            st.error(f"An unexpected error occurred during API processing: {e}")
            return ""
    return "" # Should be unreachable

# --- Generation Logic ---

def generate_paper_content(title):
    """Generates a detailed abstract for the given paper title using Gemini."""
    
    system_prompt = (
        "You are an academic writer and expert in AI. Your task is to generate a detailed, high-quality, "
        "and professionally structured abstract for a machine learning research paper. "
        "The abstract must include the motivation, method, results, and conclusion."
    )
    
    user_query = (
        f"Write a detailed, 250-word abstract for a research paper titled '{title}'. "
    )
    
    # Generous token limit for abstract generation
    max_tokens = 600 
    
    return gemini_api_call(user_query, system_prompt, max_tokens)

def summarize_content(content, title, style, length):
    """Summarizes the generated content using Gemini, based on style and length inputs."""
    
    # Map desired length to maximum output tokens
    max_tokens_map = {
        "Short (1-2 paragraphs)": 150,
        "Medium (3-5 paragraphs)": 300, 
        "Long (detailed explanation)": 450,
    }
    max_tokens = max_tokens_map[length]

    system_prompt = (
        "You are a skilled explainer. Your task is to summarize a complex research paper abstract. "
        "You must adhere strictly to the requested style and length. Do not add any introductory or concluding phrases outside of the summary content."
    )
    
    user_query = (
        f"Summarize the following research paper abstract for the paper titled '{title}'. "
        f"The explanation should be written in a **{style}** style, and the summary length "
        f"must be **{length}**, focusing on core findings and implications. "
        f"Abstract to summarize: \n\n{content}"
    )

    return gemini_api_call(user_query, system_prompt, max_tokens)

# --- Streamlit App Layout ---

st.set_page_config(page_title="Generative Research Summarizer", layout="wide")
st.title('🧠 Two-Stage Generative Research Summarizer')
st.markdown(f"**Stage 1:** Generate detailed Abstract with **`{MODEL_ID}`** (API)")
st.markdown(f"**Stage 2:** Summarize and style with **`{MODEL_ID}`** (API)")

with st.sidebar:
    st.header("1. Define Paper (Prompt)")
    
    paper_input_type = st.radio("Choose Input Type:", ("Select from List", "Enter Custom Title"))

    if paper_input_type == "Select from List":
        paper_input = st.selectbox(
            "Select Research Paper Title",
            RESEARCH_PAPER_TITLES,
            key="select_title"
        )
    else:
        paper_input = st.text_input(
            "Enter Custom Paper Title",
            "A New Framework for High-Fidelity Audio Generation",
            key="custom_title"
        )
        if not paper_input:
            st.warning("Please enter a paper title to generate content.")
            
    st.header("2. Define Summary Style")
    style_input = st.selectbox(
        "Select Explanation Style",
        ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical", "Historical Context"]
    )
    
    st.header("3. Define Summary Length")
    length_input = st.selectbox(
        "Select Explanation Length",
        ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"]
    )

if st.button('🚀 Generate & Summarize', type="primary"):
    if not paper_input:
        st.error("Please provide a paper title before continuing.")
    else:
        # --- Stage 1: Generate Mock Abstract ---
        with st.spinner(f"Stage 1: Generating detailed abstract for '{paper_input}' using {MODEL_ID}..."):
            try:
                generated_abstract = generate_paper_content(paper_input)
            except Exception as e:
                st.error(f"Error in Stage 1 (Abstract Generation): {e}. Please check the console for more details.")
                st.stop()
        
        # Explicit check for empty abstract
        if not generated_abstract:
            st.error(f"Stage 1 failed to generate content from the **{MODEL_ID}** API. This usually indicates an API key or connectivity issue.")
        else:
            # --- Stage 2: Summarize and Style ---
            st.subheader(f"Summary of '{paper_input}'")
            st.markdown(f"Style: **{style_input}** | Length: **{length_input}**")
            
            with st.spinner(f"Stage 2: Summarizing and styling using {MODEL_ID}..."):
                try:
                    final_summary = summarize_content(
                        generated_abstract, 
                        paper_input, 
                        style_input, 
                        length_input
                    )
                except Exception as e:
                    st.error(f"Error in Stage 2 (Summarization): {e}. Please check the console for more details.")
                    st.stop()
            
            # Explicit check for empty summary
            if not final_summary:
                 st.error(f"Stage 2 failed to generate content from the **{MODEL_ID}** API. This could be due to a connectivity issue.")
            
            # --- Display Results ---
            st.markdown("---")
            st.markdown(final_summary)
            st.markdown("---")

            with st.expander("View Model-Generated Abstract (Input for Summarization)"):
                st.code(generated_abstract, language='text')
