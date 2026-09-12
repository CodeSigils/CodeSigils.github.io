---
title: Dolphin LLM Guide
description: Practical guide to Dolphin language-model variants, including model cards, local deployment, quantization, and safe evaluation.
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

<div class="image-wrapper">
  <img src="/assets/images/llm-model-dolphincoder.webp"
       alt="Dolphin LLM"
       width="1024"
       height="512" />
</div>

The Dolphin family is a community-maintained collection of model variants and
fine-tunes. Capabilities, licenses, and available weights differ by release;
check the model card before downloading or deploying one.

!!! warning "Review model cards before use"

    “Uncensored” describes a model's training or fine-tuning claims, not a
    guarantee of accuracy, safety, or legal suitability. Review the specific
    model card, license, and intended-use guidance on [Hugging Face](https://huggingface.co/)
    before using a model with real data.

## What is Dolphin?

Dolphin is a family of community-published language-model variants and
fine-tunes. The maintainer, base model, training data, license, and intended
use can differ by checkpoint, so the individual model card is more authoritative
than a family name.

### Key Characteristics

- **Fine-tuned** — Each checkpoint changes the behavior of a base model in a
  particular way
- **Steerable** — The runtime and system prompt influence the model's behavior
- **Open weights** — Access and licensing depend on the checkpoint and its base
  model
- **Community maintained** — Documentation and support are supplied by the
  publishing community

### The Philosophy

!!! tip "Why Dolphin?"

    Local inference can give you more control over prompts, logs, and network
    access, but privacy is a deployment property—not a guarantee of the model
    family. Review the runtime, telemetry, API provider, and files you send to it.

## Dolphin Model Family

### Choosing a checkpoint

Start with the [Dolphin 3.0 Llama 3.1 8B model card](https://huggingface.co/dphn/Dolphin3.0-Llama3.1-8B)
as a concrete example. For another checkpoint, compare its base model,
license, context limit, quantization files, prompt format, and evaluation notes
before downloading it.

### Available Quantizations

Dolphin checkpoints may be published in quantized formats such as GGUF:

- **Q4_K_M** — Smaller download and lower memory use, with a quality tradeoff
- **Q5_K_S** — A larger quantized representation with a different quality/memory tradeoff
- **Q8_0** — Higher precision and larger memory use
- **EXL2** — A format used by compatible runtimes; follow that runtime's guidance

!!! info "Technical jargon → In plain language"

    **Technical jargon:** Quantization changes how model weights are stored.

    **In plain language:** It can make a model smaller and easier to run, but
    the choice may affect quality and supported runtimes.

    **Why it matters:** Choose a file that your runtime supports, then test the
    responses on your own prompts before relying on it.

## Deployment options

!!! tip "Choose a deployment that fits your constraints"

    Model weights may be available for local use, but running them still
    requires suitable hardware or an API provider. Check the specific model
    license and provider terms.

### Common deployment paths

| Method | Requirements |
| :----- | :----------- |
| **Self-hosted (Ollama/LM Studio)** | Hardware suitable for the selected model |
| **Hugging Face Inference** | A configured provider account |
| **Cloud vLLM** | A compatible hosted GPU environment |

### Hardware planning

There is no universal VRAM table: requirements depend on parameter count,
quantization, context length, runtime overhead, and whether the model is split
across devices. Start with the model card and runtime estimate, leave headroom
for the context window, and measure load time and generation speed on the
machine that will run the workload.

## Video Overview

<div class="youtube-video-wrapper">
  <iframe src="https://www.youtube.com/embed/xSqnWcLFd6Y"
          title="Dolphin LLM overview video"
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

model_name = "dphn/Dolphin3.0-Llama3.1-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
```

### Using vLLM (Production)

```bash
vllm serve dphn/Dolphin3.0-Llama3.1-8B
```

## Verification

- **Last reviewed:** 2026-09-09
- **Primary sources:** [Dolphin 3.0 Llama 3.1 8B model card](https://huggingface.co/dphn/Dolphin3.0-Llama3.1-8B), [Hugging Face model-loading documentation](https://huggingface.co/docs/transformers/models)
- **Scope:** Model-card ownership, checkpoint naming, Transformers loading, licensing cautions, and deployment guidance were reviewed. Other Dolphin checkpoints and runtime commands require their own current model-card verification.

## Resources

- [Dolphin Collection](https://huggingface.co/collections/GGUF-Models/dolphin)
- [Dolphin 3.0 Hub](https://dphn.ai)
- [Eric Hartford's Blog](https://erichartford.com/uncensored-models)
- [Discord Community](https://discord.gg/cognitivecomputations)

---

> **Disclaimer:** You are responsible for evaluating model outputs, complying
> with the applicable model license, and keeping unsafe or sensitive workloads
> within an environment you control.
