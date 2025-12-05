import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

print("Fetching available models...\n")

# List all available models
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ Model: {model.name}")

print("\n" + "="*50)
print("Testing the first available model...\n")

# Get first available model and test it
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        model_name = model.name.replace('models/', '')
        print(f"Using model: {model_name}")
        
        try:
            test_model = genai.GenerativeModel(model_name)
            response = test_model.generate_content("Say hello in one word")
            print(f"\n✅ SUCCESS!")
            print(f"Response: {response.text}")
            print(f"\n🎯 USE THIS MODEL NAME: {model_name}")
            break
        except Exception as e:
            print(f"Error: {e}")
