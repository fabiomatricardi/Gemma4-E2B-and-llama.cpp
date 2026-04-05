# Local Gemma-4 MiniPC Chat

A lightweight, high-performance local LLM setup using **Gemma-4-E2B (GGUF)** hosted on a MiniPC, with two beautiful Python client interfaces (CLI and Web) for multi-turn conversation.

## 🚀 Overview

This repository demonstrates how to serve a state-of-the-art LLM on a low-resource MiniPC and interact with it from any device on your local network.

* **Server:** `llama-server.exe` (part of the llama.cpp project).
* **Model:** Gemma-4-E2B-it-Q4_K_S (quantized GGUF).
* **Clients:** * `ATEST_remoteGemma4.py`: A rich CLI application with Markdown rendering and streaming.
    * `GR_TEST_remoteGemma4.py`: A Gradio-based web interface accessible via browser.
* **Hardware Efficiency:** Only **1.2 GB RAM** usage on the host machine.

---

## 🛠️ Infrastructure Setup

### 1. The Server (MiniPC)
The MiniPC acts as the inference engine. Run the following command to expose the OpenAI-compatible API to your LAN:

```bash
.\llama-server.exe -m path\to\gemma-4-E2B-it-Q4_K_S.gguf -c 64000 -ngl 0 -ctk q4_0 -ctv q4_0 --mmap -temp 1.0 --top-p 0.95 --top-k 64 --port 8888 --host 0.0.0.0
```

* **Host:** `0.0.0.0` (makes it reachable at `192.168.1.75`).
* **Context:** `64,000` tokens.
* **Offloading:** `-ngl 0` (CPU-only execution).

### 2. Client Installation
On your workstation (or the same MiniPC), install the required dependencies:

```bash
pip install openai rich gradio
```

---

## 💻 Usage

### Terminal Interface (CLI)
For a fast, keyboard-centric experience with beautiful Markdown support in the terminal:

```bash
python ATEST_remoteGemma4.py
```
* **Features:** Multi-line input support (using `Ctrl+D` / `Ctrl+Z` to send) and real-time streaming using the `rich` library.

### Web Interface (Gradio)
For a modern UI accessible from your phone, tablet, or PC browser:

```bash
python GR_TEST_remoteGemma4.py
```
* **Access:** Open `http://<MiniPC-IP>:7860` (e.g., `http://192.168.1.75:7860`).
* **Features:** Chat history management, mobile-responsive design, and easy-to-use shareable links.

---

## 📊 Performance Tracking

Both apps are configured to measure and display hardware performance metrics after every turn:

* **TTFT (Time to First Token):** Measures the latency of the initial prompt processing (Prefill).
* **Total Generation Time:** The full duration from request to completion.
* **Speed (Tokens/sec):** Calculated generation speed to monitor CPU efficiency.

---

## 📝 License
This project is for educational purposes. Gemma-4 and llama.cpp belong to their respective creators.

---

### Pro-Tip
Since your server is running with `--host 0.0.0.0`, ensure your local firewall allows traffic on port `8888` (API) and `7860` (Gradio) if you want to access the UI from different machines!
