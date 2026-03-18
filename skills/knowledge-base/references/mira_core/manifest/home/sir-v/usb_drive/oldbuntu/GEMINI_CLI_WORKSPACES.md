# Gemini CLI Workspace Management Tips

This document outlines key aspects of managing your workspace with the Gemini CLI, based on common queries and best practices.

## 1. Understanding Workspace Boundaries

The Gemini CLI operates within explicitly defined workspace directories for security and system integrity. This means:
- **Restricted Access:** The CLI can only "see" and interact with files and directories located *within* the specified workspace paths.
- **Security:** This boundary prevents unintended access or modifications to other parts of your file system.

## 2. Defining Workspace Directories at Startup

To ensure the Gemini CLI has access to all necessary project files, you must specify all desired workspace directories when you start the CLI.

**Command Example:**
If your primary project is in `/home/sir-v/Documents/ai/Projects/P1` and you also need the CLI to access files in `/media/sir-v/OS/Users/rando/Documents/Ai`, you would start the CLI with the following command:

```bash
gemini start /home/sir-v/Documents/ai/Projects/P1 /media/sir-v/OS/Users/rando/Documents/Ai
```

**Important Notes:**
- Replace the example paths with your actual directory locations.
- You can include as many directories as needed, separated by spaces.

## 3. No Dynamic Workspace Changes During a Session

Once a Gemini CLI session has started, the defined workspace directories cannot be changed or expanded.
- **To add new directories:** You must restart the Gemini CLI session and include the new paths in the `gemini start` command as described above.
- **To work with files outside the current workspace:** Either restart the CLI with the new path included, or copy the relevant files into one of your existing workspace directories.