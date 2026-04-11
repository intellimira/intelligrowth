#!/usr/bin/env python3
"""
MIRA pi-mono Integration Layer
Unified API wrapper for LLM interactions - extends Ollama with pi-mono capabilities.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

# Configuration
MIRA_ROOT = Path("/home/sir-v/MiRA")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
PI_MONO_INTEGRATION = MIRA_ROOT / "Memory_Mesh" / "pi_mono_wrapper.py"
INTERACTION_LOG = MIRA_ROOT / "Memory_Mesh" / "llm_interactions.jsonl"


class PiMonoWrapper:
    """
    pi-mono style wrapper for MIRA's LLM interactions.
    Provides unified interface for:
    - Ollama (local, primary)
    - Fallback capabilities
    - Interaction logging for The Weave
    """

    def __init__(self, primary_provider: str = "ollama"):
        self.primary = primary_provider
        self.models = self._load_available_models()
        self.interaction_log = []

    def _load_available_models(self) -> Dict[str, Any]:
        """Load available models from Ollama"""
        models = {"ollama": [], "available": []}

        try:
            result = subprocess.run(
                ["ollama", "list"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")[1:]  # Skip header
                for line in lines:
                    if line.strip():
                        model_name = line.split()[0]
                        models["ollama"].append(model_name)
                        models["available"].append(model_name)
        except Exception as e:
            print(f"⚠️ Could not load Ollama models: {e}")

        return models

    def _log_interaction(self, interaction: Dict[str, Any]):
        """Log LLM interaction to The Weave"""
        interaction["timestamp"] = datetime.now().isoformat()

        with open(INTERACTION_LOG, "a") as f:
            f.write(json.dumps(interaction) + "\n")

        self.interaction_log.append(interaction)

    def infer(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Execute inference through the wrapper.
        Returns standardized response format.
        """
        # Select model (default: qwen3:8b)
        model = model or self._get_default_model()

        # Build prompt
        full_prompt = prompt
        if system:
            full_prompt = f"System: {system}\n\nUser: {prompt}"

        interaction = {
            "provider": self.primary,
            "model": model,
            "prompt_length": len(prompt),
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            # Run Ollama inference
            cmd = ["ollama", "run", model]
            if system:
                # Use -s for system prompt if available
                cmd.extend(["--system", system])

            # Pipe the prompt
            result = subprocess.run(
                cmd, input=prompt.encode(), capture_output=True, timeout=120
            )

            if result.returncode == 0:
                response_text = result.stdout.decode("utf-8", errors="ignore")
                interaction["status"] = "success"
                interaction["response"] = response_text[:4000]  # Limit log size
                interaction["response_length"] = len(response_text)
            else:
                interaction["status"] = "error"
                interaction["error"] = result.stderr.decode("utf-8", errors="ignore")[
                    :500
                ]

        except subprocess.TimeoutExpired:
            interaction["status"] = "timeout"
            interaction["error"] = "Model took too long to respond"
        except Exception as e:
            interaction["status"] = "error"
            interaction["error"] = str(e)[:500]

        # Log the interaction
        self._log_interaction(interaction)

        return interaction

    def _get_default_model(self) -> str:
        """Get default model for MIRA operations"""
        defaults = {
            "reasoning": "qwen3:8b",
            "coding": "qwen2.5-coder-7b-8k",
            "embedding": "nomic-embed-text",
        }
        return defaults.get("reasoning", "qwen3:8b")

    def batch_infer(
        self, prompts: List[str], model: Optional[str] = None, **kwargs
    ) -> List[Dict[str, Any]]:
        """Execute multiple inferences"""
        results = []
        for prompt in prompts:
            result = self.infer(prompt, model, **kwargs)
            results.append(result)
        return results

    def status(self) -> Dict[str, Any]:
        """Return wrapper status"""
        return {
            "primary_provider": self.primary,
            "ollama_connected": bool(self.models["ollama"]),
            "available_models": self.models["available"],
            "interactions_logged": len(self.interaction_log),
            "ollama_host": OLLAMA_HOST,
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="MIRA pi-mono Wrapper")
    parser.add_argument("--status", action="store_true", help="Show wrapper status")
    parser.add_argument("--prompt", type=str, help="Run prompt inference")
    parser.add_argument("--model", type=str, help="Model to use")
    parser.add_argument("--batch", type=str, help="Batch prompt file")

    args = parser.parse_args()

    wrapper = PiMonoWrapper()

    if args.status:
        status = wrapper.status()
        print("\n📊 MIRA pi-mono Wrapper Status")
        print("=" * 40)
        print(f"  Provider:      {status['primary_provider']}")
        print(
            f"  Ollama:       {'✅ Connected' if status['ollama_connected'] else '❌ Not connected'}"
        )
        print(f"  Models:       {len(status['available_models'])}")
        for m in status["available_models"]:
            print(f"    - {m}")
        print(f"  Interactions:  {status['interactions_logged']} logged")
        print("=" * 40)

    elif args.prompt:
        result = wrapper.infer(args.prompt, model=args.model)
        print(f"\n🤖 Response ({result['model']}):")
        print("-" * 40)
        if result["status"] == "success":
            print(result.get("response", "No response"))
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        print("-" * 40)

    elif args.batch:
        with open(args.batch) as f:
            prompts = [line.strip() for line in f if line.strip()]
        results = wrapper.batch_infer(prompts, model=args.model)
        print(f"✅ Batch complete: {len(results)} inferences")

    else:
        print("MIRA pi-mono Wrapper")
        print("  --status          Show wrapper status")
        print("  --prompt 'text'   Run single inference")
        print("  --model 'name'    Specify model")
        print("  --batch 'file'    Run batch prompts")


if __name__ == "__main__":
    main()
