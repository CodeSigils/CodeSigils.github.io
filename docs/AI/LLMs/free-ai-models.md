---
title: Free AI Models Guide
description: Guide to free AI models for coding with OpenCode - including Big Pickle, Google AI Studio, Hugging Face, and other free LLM providers.
keywords:
  - free AI models
  - Big Pickle
  - Gemini
  - Google AI Studio
  - Hugging Face
  - free LLM
  - no-cost AI
---

<div class="image-wrapper">
  <img src="/assets/images/opencode-screenshot.webp"
       alt="AI Models" />
</div>

> **Last Updated:** April 2026

---

## Table of Contents

1. [Hugging Face Inference Providers](#hugging-face-inference-providers)
2. Other Free Tiers
3. [Recommendations by Use Case](#recommendations-by-use-case)
4. [Model Comparison Tables](#model-comparison-tables)

---

## Free AI Models Overview

<div class="youtube-video-wrapper">
  <iframe src="https://www.youtube.com/embed/XNm1pVab8-A" allowfullscreen></iframe>
</div>

## Hugging Face Inference Providers

OpenCode natively supports Hugging Face Inference Providers - giving you access to open models from 17+ providers.

<div class="youtube-video-wrapper">
  <iframe src="https://www.youtube.com/embed/b665B04CWkI" allowfullscreen></iframe>
</div>

### Quick Setup

!!! tip "Hugging Face Setup"

    ```bash
    # 1. Create token at huggingface.co/settings/tokens
    #    (needs "Make calls to Inference Providers" permission)

    # 2. Run auth login
    opencode auth login

    # 3. Select Hugging Face when prompted
    # Enter your token: hf_

    # 4. Select a model
    /models
    ```

### Best Coding Models

| Model                 | Best For          | Provider    | Context | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Qwen2.5-Coder-32B** | Code reasoning    | Featherless | 131K    | Good for complex code tasks |

### Other Notable Models

**For Reasoning:**

- DeepSeek-R1 - Chain-of-thought reasoning, great for complex logic
- Kimi-K2.5 - Fast, good for general tasks
- GLM-4.7 - Free tier available

**For General Use:**

- Llama 3.1 8B - Fast, cheapest
- Qwen2.5 7B - Good balance
- Gemma 4 31B - Google's best

**Resources:**

- [HF Supported Models](https://huggingface.co/inference/models)
- [HF Inference Providers](https://huggingface.co/docs/inference-providers/en/index)

---

## OpenCode Free Models

OpenCode offers built-in free models through **OpenCode Zen** - a curated set of models developed by [Zen Labs](https://zenlabs.ai/) that have been tested and benchmarked specifically for coding agents.

!!! tip "Getting Started"

    OpenCode comes with free models ready to use. Just run:
    ```bash
    opencode
    /models
    # Select from available free models
    ```

### Available Free Models

| Model                  | Context | Best For           | Notes                                   |
| :--- | :------ | :----------------- | :-------------------------------------- |
| **Big Pickle**         | 200K    | Complex coding     | Stealth model, optimized for agents    |
| **MiniMax M2.5 Free**  | 128K+   | General coding    | Strong at tool use                     |
| **Qwen3.6 Plus Free**  | 131K+   | Complex tasks      | High performance, reasoning capable    |
| **MiMo V2 Pro Free**   | 131K+   | Fast inference     | One of the fastest available           |
| **Nemotron 3 Super Free** | 1M    | Long context       | NVIDIA's open-weight agent model       |

!!! note "Limited Time"

    These free models are available while OpenCode collects feedback. During this period, data may be used to improve the model. For sensitive code, consider paid options or local models (Ollama).

### About Big Pickle

**Big Pickle** is a stealth model developed by [Zen Labs](https://zenlabs.ai/), the team behind OpenCode. It's optimized specifically for coding agents with a 200K token context window - the largest among free options.

<div class="youtube-video-wrapper">
  <iframe src="https://www.youtube.com/embed/tuW0IKNZ2UI" allowfullscreen></iframe>
</div>

### How to Access

```bash
opencode

# In terminal:
/models

# Select from available free models
```

---

## Other Free Tiers

### Free Tier Comparison

| Provider             | Free Credits     | Best Models          | Sign Up             |
| :------- | :----------- | :---------- | :------ |
| **Google AI Studio** | 15 RPM, 250K TPM | Gemini 2.5 Pro/Flash | aistudio.google.com |
| **GitHub Models**    | 50-150 req/day   | o3-mini, GPT-4.1          | github.com/models   |
| **NVIDIA NIM**       | 1,000 credits    | DeepSeek R1, Llama   | build.nvidia.com    |
| **Hugging Face**     | Monthly credits  | 300+ models          | huggingface.co      |
| **Groq**             | Low-cost   | Llama 3.3, DeepSeek R1, Qwen QwQ    | console.groq.com    |
| **xAI**              | $25 credits      | Grok 4               | x.ai                |

### Google AI Studio (Recommended for Free)

!!! tip "Best Free Option"

    - Gemini 2.5 Pro (best free model)
    - Gemini 2.5 Flash (fastest)
    - 1M token context
    - Sign up at aistudio.google.com

### GitHub Models

- GPT-4.1 (excellent coding)
- o3-mini (reasoning)
- Direct integration with OpenCode via /connect

**Resources:**

- [Awesome Free AI APIs](https://awesomeagents.ai/tools/free-ai-inference-providers-2026/)

### Groq (Fastest Inference)

!!! tip "Fastest Inference Available"

    Groq is not free - but it offers the **fastest inference speed** available (~1000+ tokens/second). It's low-cost and integrates natively with OpenCode.

    | Model                 | Context | Notes                    |
    | :--- | :------- | :----------------------- |
    | llama-3.3-70b-versatile | 128K   | Best overall             |
    | deepseek-r1-distill-llama-70b | 128K | Strong reasoning        |
    | qwen-qwq-32b           | 128K   | Fast reasoning           |
    | gemma-2-9b-it          | 8K     | Lightweight              |

#### Setup

1. Get a free API key at [console.groq.com/keys](https://console.groq.com/keys)
2. In OpenCode, run `/connect` → search for "Groq" → paste your API key
3. Run `/models` to select a Groq model

---

## Recommendations by Use Case

### Best for Coding Tasks

1. **Qwen2.5-Coder-32B** (HF) - Code reasoning
2. **GPT-4.1** (GitHub Models) - General coding
3. **Gemini 2.5 Pro** (Google AI Studio) - Long context

### Best for Reasoning

1. **DeepSeek-R1** (HF Hyperbolic) - Chain-of-thought
2. **o3-mini** (GitHub Models) - Reasoning
3. **Gemini 2.5 Pro** (Google) - Long context

### Best for Speed

1. **Groq** - Fastest inference (1000+ t/s)
2. **Qwen3-Coder-Next** - 128 t/s

### Best for Free Tier (No Credit Card)

1. **Big Pickle** (OpenCode built-in)
2. **GLM-4.7 Flash** (HF)
3. **Gemini 2.5 Flash** (Google)

---

## Model Comparison Tables

### Coding Models Comparison

| Model             | Provider    | Context | Speed   | Notes              | Best For          |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Qwen2.5-Coder-32B | Featherless | 131K    | Medium  | Good code reasoning| Code reasoning    |
| DeepSeek-R1       | Hyperbolic  | 131K    | Medium  | Chain-of-thought   | Complex reasoning |
| GPT-4.1           | GitHub      | 32K     | Fast    | Free tier          | General coding    |

### Free Models Comparison

| Model            | Source       | Notes                    |
| :--- | :--- | :--- |
| Big Pickle       | OpenCode     | Works out of box         |
| GLM 4.7 Flash    | Hugging Face | Slower                   |
| Gemini 2.5 Flash | Google       | Generous free tier       |
| Gemma 4 31B      | Hugging Face | Google's best open model |

---

## TODO: Review Schedule

- [ ] Review monthly - check for new models
- [ ] Check free tier limits changed
- [ ] Update recommendations based on benchmarks

---

## Resources

- [OpenCode + Hugging Face](https://huggingface.co/docs/inference-providers/main/integrations/opencode)
- [HF Inference Providers Pricing](https://huggingface.co/docs/inference-providers/en/pricing)
- [OpenCode Providers](https://opencode.ai/docs/providers/)
- [Awesome Free AI APIs](https://awesomeagents.ai/tools/free-ai-inference-providers-2026/)

---

_This is a living document. Revisit and update regularly._
