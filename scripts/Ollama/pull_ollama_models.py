#!/usr/bin/env python3
# =============================
# pull_ollama_models.py
# Pull multiple Ollama models automatically
# =============================

import subprocess

# List of Ollama models to pull
models = [
    "deepseek-coder:6.7b",
    "qwen2-coder:7b",
    "codegemma:7b",
    "codellama:7b",
    "codellama:13b"
]

for model in models:
    print(f"\nPulling model: {model} ...")
    try:
        result = subprocess.run(
            ["ollama", "pull", model],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ Successfully pulled {model}")
        else:
            print(f"❌ Failed to pull {model} (exit code {result.returncode})")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Exception pulling {model}: {e}")

print("\nAll models attempted.")
