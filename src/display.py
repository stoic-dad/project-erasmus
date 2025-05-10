import subprocess

def call_ollama(prompt, model='llama3.2'):
    try:
        result = subprocess.run(
            ['ollama', 'run', model, prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.stdout.strip()
    except Exception as e:
        return f"❌ Ollama error: {e}"