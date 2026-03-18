# Opencode Bootstrap Protocol 

**Instructions for the User:**
Load this file into your Opencode agent session when you want to spin up a new MIRA/Weave environment natively. Make sure `start.md` and `sop.md` are in your Opencode workspace.

---

## The Prompt to the Opencode Agent:

PLEASE LOAD the `start.md` and `sop.md` files from my workspace into your memory. 

I am initializing a new autonomous agent project inside Opencode using the Weave v4.0 architecture. You are acting as the Master Architect (Build Model).

**Step 1. Agentic Instantiation**
Using your ability to run bash commands, proactively execute the commands listed in `sop.md` Section 3.1 to construct the `.gemini`, `.brain`, `.mira`, and `skills` directory scaffolding right now. 

**Step 2. The Goal**
My goal for this Opencode project is: 
**[INSERT YOUR VIBE / GOAL HERE]**

**Step 3. Vibe Graphing**
Once the directories exist, apply the 3-Stage Vibe Graphing pipeline (Role Assignment -> Structure Design -> Semantic Completion) to design the agentic solution. Create the `graph_design.json` blueprint. Ensure that your output sets `opencode:ollama` as the default Invoke Model/Worker for execution to preserve local inference cost constraints.
