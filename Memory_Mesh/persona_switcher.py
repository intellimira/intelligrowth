#!/usr/bin/env python3
"""
MIRA Persona Switcher
Switch between trained persona models

Usage:
  python persona_switcher.py --list     # List personas
  python persona_switcher.py --set 🔬   # Set active persona
  python persona_switcher.py --current   # Show current persona
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from weaver import PersonaModels

PERSONA_STATE_FILE = Path("/home/sir-v/.mira/persona_state.json")


def load_persona_state():
    """Load persisted persona state."""
    if PERSONA_STATE_FILE.exists():
        with open(PERSONA_STATE_FILE) as f:
            return json.load(f)
    return {}


def save_persona_state(emoji):
    """Save persona state."""
    PERSONA_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PERSONA_STATE_FILE, "w") as f:
        json.dump({"current_persona": emoji}, f)


def main():
    parser = argparse.ArgumentParser(description="MIRA Persona Switcher")
    parser.add_argument("--list", action="store_true", help="List available personas")
    parser.add_argument("--set", metavar="EMOJI", help="Set persona (e.g., --set 🔬)")
    parser.add_argument("--current", action="store_true", help="Show current persona")
    parser.add_argument(
        "--status", action="store_true", help="Show persona model status"
    )

    args = parser.parse_args()

    persona_mgr = PersonaModels()
    persona_mgr.load_all()

    # Load persisted state
    state = load_persona_state()
    if state.get("current_persona"):
        persona_mgr.set_persona(state["current_persona"])

    if args.list:
        print("\n🎭 Available Personas")
        print("=" * 50)
        for emoji, name in PersonaModels.PERSONAS.items():
            print(f"   {emoji} {name}")
        print()

    elif args.set:
        emoji = args.set
        if persona_mgr.set_persona(emoji):
            name = PersonaModels.PERSONAS.get(emoji, "Unknown")
            save_persona_state(emoji)  # Persist
            print(f"\n✅ Persona set: {emoji} {name}")
            print("   Persona model weights loaded and ready")
        else:
            print(f"\n❌ Invalid persona: {emoji}")
            print("   Use --list to see available personas")

    elif args.current:
        current = persona_mgr.get_current_persona()
        if current:
            name = PersonaModels.PERSONAS.get(current, "Unknown")
            print(f"\n🎭 Current Persona: {current} {name}")
        else:
            print("\n🎭 No persona selected")
            print("   Use --set to select a persona")

    elif args.status:
        status = persona_mgr.status()
        current = persona_mgr.get_current_persona()
        print("\n🎭 Persona Model Status")
        print("=" * 50)
        print(f"   Loaded: {'✅ Yes' if status['loaded'] else '❌ No'}")
        print(f"   Current: {current or 'None'}")
        print(f"   Available: {', '.join(status['available'])}")
        print()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
