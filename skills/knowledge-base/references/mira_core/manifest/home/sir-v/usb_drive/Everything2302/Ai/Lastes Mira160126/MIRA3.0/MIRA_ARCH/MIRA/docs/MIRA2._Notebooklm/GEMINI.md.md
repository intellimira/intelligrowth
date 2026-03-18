---
sourceFile: "GEMINI.md"
exportedBy: "Kortex"
exportDate: "2025-12-22T17:40:00.527Z"
---

# GEMINI.md

4deee1b9-10ed-4b5c-aa32-85f169581388

67131ac5-f87f-4258-9289-1e8818ebed1e

Blinky - The MIRA Desktop Assistant

## Project Overview

Blinky is a local-first, AI-powered desktop assistant designed to help users with various tasks, provide insights, and even expand its own capabilities. It operates as a command-line-like interface within a dedicated

Key Components:

Blinky (UI):

The user-facing application, implemented with

, providing an input/output interface.

MIRA (Core AI):

The central AI logic, powered by a local GPT4All Large Language Model. MIRA employs a unique "persona-based" reasoning framework (e.g., First Principles, Scientific Method) to structure its responses.

The shell-based interface connecting Blinky to MIRA (though its direct code was not deeply explored, its role is noted).

Core Functionality:

Conversational AI:

Engages in dialogue with the user, leveraging its persona framework for nuanced responses.

Tool Execution:

MIRA can execute a predefined set of tools to interact with the local file system, perform web searches, send emails, and generate leads.

Dynamic Tool Creation:

A standout feature allowing users to interactively define new Python tools, which MIRA then integrates into its capabilities and prompt template.

Context Management:

Includes a "Context Restoration Protocol" (

/restore_blinky_context

) to quickly re-establish project understanding for MIRA across sessions.

## Sensitive operations like

require explicit user confirmation via a UI pop-up.

Main Technologies:

Primary development language.

Local Large Language Model for MIRA's intelligence.

Used for templating MIRA's prompts, including dynamic updates for new tools.

Python's standard GUI toolkit for Blinky's user interface.

Playwright:

Used within tools for browser automation (e.g.,

apollo_search

For making HTTP requests (e.g.,

## Building and Running

Dependencies:

## The project dependencies are listed in

requirements.txt

gpt4all
Jinja2
requests
playwright

## These can typically be installed using

pip install -r requirements.txt

Blinky includes an initial setup wizard (

src/main.py

function) to configure the application, primarily for setting the GPT4All model path. Refer to

INSTRUCTIONS.md

for detailed installation and initial launch steps.

Running the Application:

To start Blinky, execute the main Python script:

python src/main.py

## Development Conventions

Persona-Based Reasoning:

MIRA's responses are structured by insights from various "personas" (e.g., First Principles, Scientific Method), as defined in

prompts/mira_template.jinja2

Tool-Calling Mechanism:

MIRA communicates its intent to use tools by outputting a specific JSON format within a

[TOOL_CALL: {...}]

block, which is then parsed and executed by the application.

User Confirmation for Sensitive Operations:

Operations that modify the file system (e.g.,

) require explicit user confirmation through a

pop-up, enhancing security.

Dynamic Tool Creation:

## New tools can be defined interactively by the user via the

/create_tool

command. This process involves MIRA guiding the user to provide tool name, description, arguments, return type, and Python code. The tool's code is saved to

src/tools/user_defined/

and its definition is dynamically added to

prompts/mira_template.jinja2

. A restart of Blinky is required for new tools to become active.

Context Restoration Protocol:

/restore_blinky_context

command allows MIRA to quickly re-establish its understanding of the project by recalling long-term memory, reviewing

docs/MIRA_Methodologies.md

, and scanning core code files.

## User queries and tool executions are logged to

logs/queries

logs/tool_executions

respectively, aiding in debugging and review.

Security Considerations:

src/tools.py

file contains

## SECURITY WARNING

comments regarding hardcoded credentials for

apollo_search

, indicating areas that require secure credential management.

