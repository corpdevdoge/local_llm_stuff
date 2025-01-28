import asyncio
import time
from ollama import AsyncClient

async def query_ollama(model_name, prompt):
    """
    Queries the Ollama API asynchronously with the given model and prompt.

    Args:
        model_name (str): The model to use (e.g., 'phi3:mini', 'mistral:latest').
        prompt (str): The user input prompt.

    Returns:
        str: The response from the model.
    """
    message = {'role': 'user', 'content': prompt}
    response = ""
    start_time = time.time()  # Start timer
    async for part in await AsyncClient().chat(model=model_name, messages=[message], stream=True):
        response += part['message']['content']
        print(part['message']['content'], end='', flush=True)
    end_time = time.time()  # End timer
    
    elapsed_time = end_time - start_time
    print(f"\nTime taken (Python timing): {elapsed_time:.3f} seconds")
    
    # If the Ollama API provides a timing metric, extract and print it (assuming it's in part['metrics'])
    if 'metrics' in part:
        print(f"Time taken (Ollama-reported): {part['metrics']['total_time']:.3f} seconds")
    
    return response

async def chatbot():
    """Simple chatbot to interact with different LLM models via Ollama."""
    models = ["phi3:mini", "phi3:latest", "mistral:latest", "deepseek-r1:7b", "llama3.2:latest"]

    print("Welcome to the Ollama Chatbot!")
    print("Available models:")
    for idx, model in enumerate(models, start=1):
        print(f"{idx}. {model}")

    while True:
        try:
            model_choice = int(input("\nSelect a model by entering the corresponding number (or 0 to exit): "))
            if model_choice == 0:
                print("Goodbye!")
                break

            if 1 <= model_choice <= len(models):
                selected_model = models[model_choice - 1]
                prompt = input(f"\nEnter your prompt for '{selected_model}': ")

                print("\nQuerying the model- ",selected_model,"\n")
                await query_ollama(selected_model, prompt)
                print("\n")
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    asyncio.run(chatbot())