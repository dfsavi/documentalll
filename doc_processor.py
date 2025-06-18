import os
import glob
import argparse
import requests

def process_file(file_path, model_name, prompt_prefix):
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Create full prompt
        full_prompt = f"{prompt_prefix}\n\n{content}"

        # Send to Ollama
        response = requests.post(
            'http://192.168.0.18:11434/api/generate',
            json={
                'model': model_name,
                'prompt': full_prompt,
                'stream': False
            },
            timeout=600
        )

        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code} - {response.text}")

        result = response.json()['response']

        # Create output path
        base = os.path.splitext(os.path.basename(file_path))[0]
        output_path = f"output/doc-{base}.md"

        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save result
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)

        return output_path

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Process files with Ollama')
    parser.add_argument('--input', default='input', help='Input folder path')
    parser.add_argument('--model', default='hf.co/unsloth/Qwen3-32B-GGUF:Q4_K_M', help='Ollama model name')
    parser.add_argument('--prompt', default='',
                      help='Prompt prefix to send to Ollama')
    args = parser.parse_args()
    model = args.model
    prompt = args.prompt

    # Process all files in input folder and subfolders
    files = glob.glob(f"{args.input}/**/*", recursive=True)
    files = [f for f in files if os.path.isfile(f)]
    print('files: ', files);

    if not files:
        print(f"No files found in {args.input}")
        return

    if prompt == "":
        prompt = "/not_think Create a technical document explaining the following code, including its purpose and how it works."
        prompt += "Use bullet points to explain each step of the code. Make sure to use proper grammar and punctuation."
        prompt += "Also, make sure that your document is easy to understand for someone who has no programming experience."
        prompt += "Make Sure the output is in Markdown format."

    for file_path in files:
        output_path = process_file(file_path, model, prompt)
        if output_path:
            print(f"Created: {output_path}")

if __name__ == '__main__':
    main()
