import asyncio
import time
from ollama import AsyncClient
import shlex

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
    print(f"\nTime taken : {elapsed_time:.3f} seconds")

    # If the Ollama API provides a timing metric, extract and print it (assuming it's in part['metrics'])
    if 'metrics' in part:
        print(f"Time taken (Ollama-reported): {part['metrics']['total_time']:.3f} seconds")

    return response

async def chatbot():
    """Simple chatbot to interact with different LLM models via Ollama."""
    models = ["phi3:mini", "phi3:latest", "mistral:latest", "deepseek-r1:7b", "llama3.2:latest"]

    print("Welcome to the Ollama Chatbot!")

    # File path input
    file_path_input = input("Enter the file path within double quotes: ")
    try:
        file_path = shlex.split(file_path_input)[0]  # Extract path within quotes
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    query = input("\nEnter your query related to the file: \n")

    print("\n Available models:")
    for idx, model in enumerate(models, start=1):
        print(f"{idx}. {model}")

    while True:
        try:
            model_choice = int(input("\n\nSelect a model by entering the corresponding number (or 0 to exit): "))
            if model_choice == 0:
                print("Goodbye!")
                break

            if 1 <= model_choice <= len(models):
                selected_model = models[model_choice - 1]
                combined_prompt = f"File Content: {file_content}\n\nQuery: {query}"

                print("\nQuerying the model - ",selected_model,"\n")
                await query_ollama(selected_model, combined_prompt)
                print("\n")
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    asyncio.run(chatbot())
