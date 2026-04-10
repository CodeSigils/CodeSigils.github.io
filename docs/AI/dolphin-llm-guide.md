---
title: Dolphin LLM Guide
icon: lucide/fish
description: Guide to Dolphin LLM - an open source, uncensored, and steerable large language model family. Learn about installation, usage, and model options.
keywords:
  - dolphin
  - LLM
  - open source
  - uncensored
  - Ollama
  - LM Studio
  - Hugging Face
  - local AI
---

![Dolphin LLM](/assets/images/dolphin-llm.png){ width=900 }

The Dolphin family of LLMs — open source, uncensored, and steerable models from the community.

## What is Dolphin?

Dolphin is a family of open-source LLMs developed by [Eric Hartford](https://huggingface.co/dphn), [Cognitive Computations](https://huggingface.co/cognitivecomputations), and collaborators. 

### Key Characteristics

- **Uncensored** — Dolphin removes alignment and bias filters, making the model more compliant and steerable
- **Steerable** — You set the system prompt, you decide the alignment, you have control of your data
- **Open Source** — Fully open weights under various licenses (Llama, Apache 2.0)
- **Community Driven** — Trained on curated datasets from the open source community
- **General Purpose** — Designed to be similar to ChatGPT, Claude, and Gemini but with full user control

### The Philosophy

!!! tip "Why Dolphin?"

    Unlike commercial models:
    1. No hidden system prompts that change without notice
    2. Your data stays private — Dolphin can't see or use your queries
    3. Full steerability — You control the model's behavior and ethics
    4. No imposed guidelines — You decide what's appropriate

## Dolphin Model Family

### Recent Models

| Model | Size | Base Model | Context | License |
| :--- | :--- | :--- | :--- | :--- |
| **Dolphin 3.0 Llama 3.1 8B** | 8B | Llama 3.1 | 8K+ | Meta Llama 3.1 |
| **Dolphin 3.0 Llama 3.2 1B** | 1B | Llama 3.2 | 8K+ | Meta Llama 3.2 |
| **Dolphin 3.0 Llama 3.2 3B** | 3B | Llama 3.2 | 8K+ | Meta Llama 3.2 |
| **Dolphin 3.0 Qwen 2.5 3B** | 3B | Qwen 2.5 | 8K+ | Apache 2.0 |
| **Dolphin X1 8B** | 8B | Llama 3.1 8B | 32K | Meta Llama 3.1 |
| **Dolphin X1 405B** | 405B | Llama 3.1 405B | 32K | Meta Llama 3.1 |
| **Dolphin 2.9 Llama 3 8B** | 8B | Llama 3 | 8K | Meta Llama 3 |
| **Dolphin 2.9 Mistral 7B** | 7B | Mistral | 8K+ | Apache 2.0 |
| **Dolphin 2.8 Mistral 7B** | 7B | Mistral | 8K+ | Apache 2.0 |

### Available Quantizations

Dolphin models are available in various GGUF formats for different use cases:

- **Q4_K_M** — Balance of size and quality
- **Q5_K_S** — Higher quality  
- **Q8_0** — Best quality, larger size
- **EXL2** — Various bit widths (2-8bpw)

## Pricing

!!! tip "Free and Open"

    Dolphin is **free** to use! But you'll need some hardware or an API provider.

### Cost Options

| Method | Cost | Requirements |
| :--- | :--- | :--- |
| **Self-hosted (Ollama/LM Studio)** | Free | GPU with 4-24GB VRAM |
| **Hugging Face Inference** | Varies | API credits |
| **Cloud vLLM** | Compute cost | GPU rental |

### Hardware Requirements

| Model Size | Minimum VRAM | Recommended |
| :--- | :--- | :--- |
| 1B parameters | 2GB | 4GB |
| 3B parameters | 6GB | 8GB |
| 8B parameters | 16GB | 24GB |
| 70B parameters | 140GB | 8x A100/H100 |
| 405B parameters | 800GB+ | Multi-GPU cluster |

## Video Overview

<div class="youtube-video-wrapper">
  <iframe src="https://www.youtube.com/embed/xSqnWcLFd6Y" 
          allowfullscreen>
  </iframe>
</div>

## How to Use

### Using Ollama

```bash
# Pull a Dolphin model
ollama pull dolphin

# Or specific version
ollama pull dolphin3.0-llama3.1-8b
```

### Using LM Studio

1. Download LM Studio from [lmstudio.ai](https://lmstudio.ai/)
2. Search for "dolphin" in the model browser
3. Download your desired model
4. Load and chat locally

### Using Hugging Face Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "cognitivecomputations/Dolphin3.0-Llama3.1-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
```

### Using vLLM (Production)

```bash
vllm serve cognitivecomputations/Dolphin3.0-Llama3.1-8B
```

## Resources

- [Dolphin Collection](https://huggingface.co/collections/GGUF-Models/dolphin)
- [Dolphin 3.0 Hub](https://dphn.ai)
- [Eric Hartford's Blog](https://erichartford.com/uncensored-models)
- [Discord Community](https://discord.gg/cognitivecomputations)

---

> **Disclaimer:** Dolphin is an uncensored model. You're responsible for the content you create using it.