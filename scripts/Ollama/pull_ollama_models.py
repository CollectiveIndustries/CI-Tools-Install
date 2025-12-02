#!/usr/bin/env python3
# =============================
# pull_ollama_models.py
# Pull multiple Ollama models automatically from LLM_List.conf
# =============================

import subprocess
import os

# Path to model list file
model_list_file = os.path.join(os.path.dirname(__file__), "LLM_List.conf")

# Check if file exists
if not os.path.isfile(model_list_file):
    print(f"❌ Model list file not found: {model_list_file}")
    exit(1)

# Read models from file, ignoring empty lines
with open(model_list_file, "r") as f:
    models = [line.strip() for line in f if line.strip()]

# Pull each model
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
