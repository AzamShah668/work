import os
import sys
# Import the correct class for Google's Gemini models
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import FakeListLLM


def run_langchain_demo():
    print("--- LangChain Demo: Gemini 2.5 Flash (Detailed Response) ---")

    # 1. Setup API Key Check
    # The Google SDK automatically looks for GEMINI_API_KEY
    if "GEMINI_API_KEY" not in os.environ:
        print("\n!!! ACTION REQUIRED !!!")
        print("Set the Gemini API key environment variable (AIza...)")
        print('Example (Linux/macOS): export GEMINI_API_KEY="AIza_your-secret-key"\n')
        USE_MOCK = True
    else:
        USE_MOCK = False

    # 2. Initialize the Model
    try:
        if USE_MOCK:
            print("NOTE: Using MOCK model (No API call made).")
            mock_response = "Mock detailed response: The Gemini 2.5 Flash model is chosen for this free demo because its high speed and generous free-tier quotas allow for fast, detailed, and reliable prototyping, minimizing the chance of hitting server timeouts or rate limits associated with older or larger models."
            model = FakeListLLM(responses=[mock_response])
        else:
            # Recommended Model: gemini-2.5-flash (Fast, powerful, and excellent free-tier performance)
            repo_id = "gemini-2.5-flash"
            print(f"NOTE: Using FREE Gemini API Model ({repo_id}).")

            # Initialize the model instance
            model = ChatGoogleGenerativeAI(
                model=repo_id,
                temperature=0.7, # Increased temperature slightly for more creative/detailed responses
                max_output_tokens=2048, # High limit to ensure a long, detailed answer is not truncated
            )

    except Exception as e:
        print(f"Error initializing model: {e}")
        return

    # 3. Create a Prompt Template
    # --- MODIFIED to ask for a DETAILED, multi-paragraph response ---
    prompt = ChatPromptTemplate.from_template(
        "Provide a detailed, multi-paragraph explanation of the following topic: {topic}"
    )

    # 4. Create an Output Parser
    parser = StrOutputParser()

    # 5. Build the Chain (LCEL Syntax)
    chain = prompt | model | parser

    # 6. Invoke the Chain
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = "why Gemini 2.5 Flash is the most stable choice for this free demo"
        print("No topic provided. Using default: 'why Gemini 2.5 Flash is the most stable choice for this free demo'")
        print("Usage: python your_script_name.py [topic]")

    print(f"Asking AI about: {topic}...\n")

    try:
        response = chain.invoke({"topic": topic})
        print("Response:")
        print(response)

    except Exception as e:
        print(f"\n!!! GEMINI API ERROR (Likely Quota, Key, or Server Issue) !!!")
        print(f"An unexpected error occurred: {e}")
        print("\n**If this fails, your API token or quota is the problem. Please check your key or wait for your quota to reset.**")
        print("Falling back to MOCK mode...")
        # Fallback to verify logic works
        mock_model = FakeListLLM(responses=["(Mock Response) The request failed due to an API error, but the program logic is sound. Please check your token or wait for your quota to reset."])
        mock_chain = prompt | mock_model | parser
        print("Response:", mock_chain.invoke({"topic": topic}))


if __name__ == "__main__":
    run_langchain_demo()
