To instruct **OpenCode** to perform **Auto Research** on your behalf, you can use the following detailed prompt. This prompt is structured to turn OpenCode into a "meta-skill" agent that autonomously optimizes your local files by applying the three essential ingredients and the iterative loop described in the sources.

***

### **Auto Research Autonomous Optimizer Prompt**

**Objective:** Act as an autonomous **Researcher agent** to optimize the performance and reliability of the skill stored in `[Path to your Skill].md` using the **Auto Research methodology**.

**1. Core Methodology Framework**
*   **The Three Ingredients:** You are provided with an **objective metric** (Eval Pass Rate), an automated **measurement tool** (a test suite you will generate), and a **variable to change** (the prompt instructions within the markdown file).
*   **Architecture:** Treat the target markdown file as the `train.py` (the skill to be optimized) and your current instructions as the `program.md` (the agent’s logic).

**2. Step 1: Initialize the Evaluation (Eval) Suite**
*   Review the current instructions in `[Path to your Skill].md` and identify **4 to 6 granular, binary (Yes/No) criteria** for success.
*   Avoid subjective "vibes"; ensure criteria are simple and binary to prevent compounding probabilities.
*   *Example Criteria:* "Is the output in valid JSON?", "Is the tone professional?", "Does it include all required headers?".

**3. Step 2: Establish the Baseline (Benchmarking)**
*   Generate **10 unique outputs** using the current version of the skill.
*   Run each output through your **Eval Suite** (e.g., if there are 4 criteria across 10 runs, the max score is 40).
*   Calculate the **median and mode** of the results to account for AI "noise" and establish a statistically reliable baseline.

**4. Step 3: The Autonomous Optimization Loop**
*   **Mutate:** Rewrite and alter the prompt instructions in the target markdown file to improve the score.
*   **Evaluate:** Run 10 new generations using the mutated prompt and score them against the binary criteria.
*   **Select:** If the new score is higher than the previous baseline, **overwrite the file** with the "winner." If the score is lower, discard the mutation.
*   **Repeat:** Execute this loop autonomously every **2 to 5 minutes**.

**5. Operational Constraints & Tool Use**
*   **Autonomous Mode:** Use `bash` and file-writing tools to run the test suite and update the skill without requiring human approval for every iteration.
*   **Reporting:** Maintain a real-time log of test results, including legibility/accuracy scores and the current high-water mark.
*   **Goal:** Continue iterations until the skill reaches near-perfection (e.g., 39/40 or 97.5% accuracy).

***

### **Implementation Guide for OpenCode**
To ensure this works within your **`opencode.json`** architecture:
*   **Tool Permissions:** Ensure your `permission` block for this agent has `bash` and `write` set to `"allow"` so it can run the loop overnight without interruption.
*   **Model Selection:** Use a high-reasoning model (like Claude 3.5 Sonnet) for the **Mutation** phase and a faster, cost-effective model for the **Evaluation** phase (10–20 runs per cycle).
*   **Meta-Skill Application:** Once you verify this prompt works for one skill, you can instruct OpenCode to "perform this optimization for literally every skill in my repository".

-------------

Configuration Guide: Implementing Auto Research in OpenCode

1. The Auto Research Methodology Overview

The Auto Research methodology is an autonomous optimization framework derived from the work of Andre Karpathy and Nick Saraev. It treats prompt engineering as an iterative machine learning problem, where agentic workflows programmatically mutate instructions to maximize a specific objective metric.

To implement this loop within OpenCode, the system requires the "Three Ingredients" framework:

* Objective Metric: A quantifiable, non-subjective number (e.g., an evaluation pass rate) that serves as the ground truth for success.
* Measurement Tool: An automated, reliable testing suite that executes without human intervention to provide consistent feedback.
* Target for Mutation: The specific instruction set being iterated upon, specifically the skill.md or program.md files.

2. Statistical Rationale & Benchmarking Logic

AI outputs are inherently noisy distributions rather than static results. To achieve reliability, our framework moves away from "vibes-based" prompting and toward statistical noise reduction.

The 10-Run Baseline

To account for the variance in LLM outputs, every iteration must undergo a 10-run benchmark. This sample size is the minimum required to identify the median and mode of performance. A single successful run is insufficient; we optimize for the statistical likelihood of success across the entire distribution.

Binary Evaluation (The Yes/No Standard)

We utilize Binary Assessment (Yes/No) for all criteria. Unlike Likert scales (1–5 or 1–10), binary questions prevent "compounding probabilities"—a phenomenon where increased variability at each step of an evaluation chain leads to an unmanageable "optimization cone." By forcing a hard Pass/Fail, we provide the Researcher agent with high-signal, low-noise data.

Warning: Avoid overly narrow or stringent constraints (e.g., exact word counts or character exclusions) in your evaluation criteria. If the evaluation is too rigid, the model may begin "parroting" the criteria—effectively passing the test without improving the actual quality of the output. This is the "student who doesn't understand the material" paradox. Ensure criteria focus on output integrity rather than superficial formatting.

3. Core Configuration: opencode.json Agent Modes

The optimization loop relies on two specialized agent personas: the Researcher (Optimization Logic) and the Evaluator (Validation Logic).

{
  "agent_modes": [
    {
      "name": "Researcher",
      "role": "Mutation and Noise Control Specialist",
      "system_prompt": "You are a Researcher Agent. Your mission is to evolve the instructions in 'skill.md' to maximize performance across a 10-run distribution. Analyze the 10x4 evaluation matrix and identify patterns of failure. Do not react to isolated anomalies; focus on mutations that stabilize the 'Mode' and 'Median' of successful runs. Your goal is to eliminate noise and ensure the prompt is airtight against the specific failure reasons provided by the Evaluator."
    },
    {
      "name": "Evaluator",
      "role": "Binary Assessment Specialist",
      "system_prompt": "You are an Evaluator Agent. Perform a strict binary assessment of 10 skill outputs against four criteria: 1. Legibility (text is clear/correct), 2. Color Palette (pastel/soft colors only; no neons/bright reds), 3. Linearity (left-to-right/top-to-bottom flow), and 4. Absence of Ordinals (no '1, 2, 3, 4' numbering). Output a 10x4 results matrix in Markdown. For every 'Fail,' you MUST provide a specific failure reason to guide the Researcher's mutation logic. Final score is out of 40."
    }
  ]
}


4. Granular Tool Permissions

Autonomous loops require elevated permissions to bridge the gap between analysis and execution.

{
  "tools": [
    {
      "name": "bash",
      "enabled": true,
      "description": "Required to execute 'setup.sh', trigger the 10-run benchmark suite, and manage the optimization loop state."
    },
    {
      "name": "write",
      "enabled": true,
      "description": "Required for the Researcher to mutate 'skill.md' and to archive 'research_log.json' for future model handoffs."
    }
  ]
}


5. Custom CLI Commands for the Optimization Loop

These commands define the automated workflow, incorporating state management to ensure only "Global Best" versions are retained.

{
  "scripts": {
    "benchmark": "run-skill --count 10 --output stats.json",
    "optimize": "
      export GLOBAL_BEST=0;
      while true; do
        ./setup.sh;
        researcher-mutate --target skill.md --logs research_log.json;
        npm run benchmark;
        evaluator-test --input stats.json --output current_eval.md;
        SCORE=$(grep 'Total Score:' current_eval.md | awk '{print $3}');
        if [ \"$SCORE\" -gt \"$GLOBAL_BEST\" ]; then
          export GLOBAL_BEST=$SCORE;
          cp skill.md skill_winner.md;
        fi;
        echo \"Score: $SCORE | Best: $GLOBAL_BEST\" >> research_log.json;
        [ \"$GLOBAL_BEST\" -ge 39 ] && break;
        sleep 120;
      done"
  },
  "custom_commands": [
    {
      "name": "benchmark",
      "description": "Executes 10 parallel runs of the target skill to generate a statistical distribution for the Evaluator."
    },
    {
      "name": "optimize",
      "description": "Triggers the autonomous Researcher-Evaluator loop. Compares current scores against the Global Best and archives research data until a target score of 39/40 is achieved."
    }
  ]
}


6. Implementation Workflow (The Three-File Structure)

This structure maps the Andre Karpathy auto-research repository directly into the OpenCode DevOps environment.

Andre Karpathy Repo	OpenCode Equivalent	Function
train.py	skill.md	The target prompt/code being optimized.
program.md	Agent Instructions	The system prompts for Researcher and Evaluator.
prepare.py	setup.sh	Environment configuration, API key injection (e.g., Nano Banana Pro 2), and workspace cleanup.

7. Optimization Targets & Success Metrics

The framework is designed for high-stakes prompt optimization across diverse applications:

1. Diagram Generator: Optimizing for visual consistency, pastel aesthetics, and structural linearity.
2. Proposal Generator: Refining professional tone, document structure, and factual accuracy.
3. Cold Emailing: Iterating on copy variants to maximize reply rates through statistical split-testing.

The Meta-Skill & Future-Proofing

The final output of this configuration is more than just a refined prompt; it is a Research Log. This log contains the history of every failed mutation, every success, and the statistical shifts observed over hundreds of runs.

In the "Meta-Skill" paradigm, this log is a long-term asset. When next-generation models like GPT-6 or Opus 5.0 are released, you do not start from scratch. You feed the Research Log to the new model, allowing it to pick up exactly where the previous model reached its limit (e.g., 39/40 or 97.5% accuracy), ensuring your autonomous agents are perpetually evolving.

