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
            'http://localhost:11434/api/generate',
            json={
                'model': model_name,
                'prompt': full_prompt,
                'stream': False
            },
            timeout=300
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
    parser.add_argument('--model', default='llama3', help='Ollama model name')
    parser.add_argument('--prompt', default='Summarize the following text:', 
                      help='Prompt prefix to send to Ollama')
    args = parser.parse_args()

    # Process all files in input folder
    files = glob.glob(f"{args.input}/*")
    
    if not files:
        print(f"No files found in {args.input}")
        return

    for file_path in files:
        output_path = process_file(file_path, args.model, args.prompt)
        if output_path:
            print(f"Created: {output_path}")

if __name__ == '__main__':
    main()
