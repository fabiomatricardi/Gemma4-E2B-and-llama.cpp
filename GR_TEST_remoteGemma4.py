import gradio as gr
import time
from openai import OpenAI

# Your MiniPC configuration
client = OpenAI(
    base_url="http://192.168.1.75:8888/v1",
    api_key="sk-no-key-required"
)

def predict(message, history):
    """
    Gradio passes the current message and the chat history.
    History is a list of lists: [[user_msg1, bot_msg1], [user_msg2, bot_msg2]]
    """
    # Convert Gradio history to OpenAI format
    openai_history = [{"role": "system", "content": "You are a helpful assistant. Respond in Markdown."}]
    for human, assistant in history:
        openai_history.append({"role": "user", "content": human})
        openai_history.append({"role": "assistant", "content": assistant})
    
    openai_history.append({"role": "user", "content": message})

    # Timing variables
    start_time = time.time()
    ttft = None
    full_response = ""

    try:
        stream = client.chat.completions.create(
            model="gemma",
            messages=openai_history,
            temperature=1.0,
            stream=True
        )

        for chunk in stream:
            # Capture TTFT on the very first chunk with content
            if ttft is None:
                ttft = time.time() - start_time
            
            delta = chunk.choices[0].delta.content
            if delta:
                full_response += delta
                # Yield current text to update the UI in real-time
                yield full_response

        # Calculate final generation time
        total_time = time.time() - start_time
        
        # Append stats to the end of the markdown response
        stats_footer = f"\n\n---\n**Stats:** TTFT: `{ttft:.2f}s` | Total: `{total_time:.2f}s` | Speed: `{len(full_response.split())/total_time:.1f} w/s`"
        yield full_response + stats_footer

    except Exception as e:
        yield f"**Error:** {str(e)}"

# Create the UI
demo = gr.ChatInterface(
    predict,
    title="Gemma-4 Local Chat",
    description="Running on MiniPC (192.168.1.75)",
    theme="soft",
    examples=["Explain quantum computing in simple terms.", "Write a Python script to scrape a website."],
    type="messages" # Optimized for newer Gradio versions
)

if __name__ == "__main__":
    # Setting server_name="0.0.0.0" allows other devices on your LAN to see the UI
    demo.launch(server_name="0.0.0.0", server_port=7860)
    