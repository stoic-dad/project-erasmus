from rich.console import Console
from rich.table import Table
import subprocess

def display_table(df):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    for col in df.columns:
        table.add_column(col)
    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row])
    console.print(table)

def call_ollama(prompt, model='codellama'):
    try:
        result = subprocess.run(
            ['ollama', 'run', model, prompt],
            capture_output=True, text=True, timeout=300  # increased timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "❌ Ollama timed out. Try using a shorter prompt or a faster model."
    except KeyboardInterrupt:
        return "❌ User canceled the request (Ctrl+C). Exiting gracefully."
    except Exception as e:
        return f"❌ Ollama error: {e}"