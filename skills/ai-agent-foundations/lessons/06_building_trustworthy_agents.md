# Lesson 06: Building Trustworthy AI Agents

## Introduction

This lesson covers building and deploying safe and effective AI Agents, including security considerations and data privacy.

## Key Topics

### Safety: Building System Message Framework

1. **Meta System Message**: Template for generating agent prompts
2. **Basic Prompt**: Describe agent role and tasks
3. **Optimized System Message**: LLM-enhanced prompt structure
4. **Iterate and Improve**: Continuous refinement

### Understanding Threats

| Threat | Description | Mitigation |
|--------|-------------|------------|
| Task/Instruction | Changing agent instructions via inputs | Validation checks, limit conversation turns |
| Access to Critical Systems | Compromising agent-system communication | Need-only access, authentication |
| Resource Overloading | High volume of requests via agent | Rate limiting policies |
| Knowledge Base Poisoning | Corrupting data agent uses | Regular data verification |
| Cascading Errors | Errors spreading across systems | Docker containers, fallback mechanisms |

### Human-in-the-Loop
Users provide feedback during agent runs, acting as agents in a multi-agent system.

## MIRA Integration Notes

This lesson informs MIRA's:
- **Security Architecture**: Trustworthy agent design
- **Self-Anneal Watchdog**: Threat monitoring and mitigation
- **Sovereign Operation**: Human oversight integration

---
*Source: [Microsoft AI Agents for Beginners - Lesson 06](https://microsoft.github.io/ai-agents-for-beginners/06-building-trustworthy-agents/)*
