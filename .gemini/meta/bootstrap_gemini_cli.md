# Gemini CLI Bootstrap Protocol 

**Instructions for the User:**
Copy the prompt below and paste it into your Gemini CLI session when you want to spin up a new MIRA/Weave environment. Make sure `start.md` and `sop.md` are in the same directory.

---

### Terminal Command Example:
```bash
gemini "Please read bootstrap_gemini_cli.md and follow the prompt."
```

---

## The Prompt to Gemini:

PLEASE LOAD the `start.md` and `sop.md` files from this directory into your memory. 

I am initializing a new project using the Weave v4.0 architecture. You are now the Master Architect (Build Model).

**Step 1. Agentic Instantiation**
Before answering, proactively execute the terminal commands listed in `sop.md` Section 3.1 to generate the `.gemini`, `.brain`, `.mira`, and `skills` workspace scaffolding. 

**Step 2. The Goal**
My goal for this project is: 
**[INSERT YOUR VIBE / GOAL HERE]**

**Step 3. Vibe Graphing**
Apply the 3-Stage Vibe Graphing pipeline to design the solution. Create the initial `.gemini/first_intent.gemini` file and the `graph_design.json` blueprint. Default the runtime worker model to `opencode:ollama` (or an equivalent cost-down model) in the execution scripts.
