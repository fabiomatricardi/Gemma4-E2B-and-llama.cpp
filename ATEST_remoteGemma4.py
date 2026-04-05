import sys
import time
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

# Initialize Rich Console
console = Console()

client = OpenAI(
    base_url="http://192.168.1.75:8888/v1",
    api_key="sk-no-key-required"
)

def get_multiline_input():
    console.print("\n[bold cyan]User[/bold cyan] [dim](Ctrl+D/Z to send, 'exit' to quit):[/dim]")
    contents = []
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            contents.append(line)
    except EOFError:
        pass
    
    return "".join(contents).strip()

def chat():
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use Markdown for formatting."}
    ]

    console.print(Panel.fit("[bold reverse] Local LLM Chat [/bold reverse]\nConnected to 192.168.1.75:8888", border_style="green"))

    while True:
        user_text = get_multiline_input()

        if user_text.lower() in ['exit', 'quit']:
            console.print("[yellow]Closing session...[/yellow]")
            break
        
        if not user_text:
            continue

        messages.append({"role": "user", "content": user_text})

        try:
            start_time = time.time()
            ttft_time = None
            
            response = client.chat.completions.create(
                model="gemma", 
                messages=messages,
                temperature=1.0,
                stream=True
            )

            console.print("\n[bold magenta]Assistant:[/bold magenta]")
            
            full_response = ""
            with Live(console=console, refresh_per_second=10, vertical_overflow="visible") as live:
                for chunk in response:
                    # Capture Time to First Token
                    if ttft_time is None:
                        ttft_time = time.time() - start_time
                    
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        live.update(Markdown(full_response))
            
            total_time = time.time() - start_time
            
            # Display performance metrics in a small table
            stats_table = Table(show_header=False, box=None, padding=(0, 2))
            stats_table.add_row(
                f"[dim]TTFT: {ttft_time:.2f}s[/dim]", 
                f"[dim]Total: {total_time:.2f}s[/dim]",
                f"[dim]Speed: {len(full_response.split()) / total_time:.1f} words/s[/dim]"
            )
            console.print(stats_table)
            
            messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    chat()