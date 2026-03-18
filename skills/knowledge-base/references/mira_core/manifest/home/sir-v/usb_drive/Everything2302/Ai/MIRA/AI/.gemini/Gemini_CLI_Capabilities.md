# Gemini CLI Capabilities

This document provides a comprehensive overview of the Gemini CLI's capabilities.

## 1. Core Functionality

### 1.1. Interactive Chat

The primary function of the Gemini CLI is to provide an interactive chat interface with Google's Gemini models. You can ask questions, provide instructions, and have a conversation with the AI.

### 1.2. Non-Interactive Prompts

You can execute non-interactive prompts directly from the command line. This is useful for scripting and automation.

## 2. Commands

The Gemini CLI is organized into several commands:

### 2.1. `gemini`

This is the main command to launch the interactive CLI or execute a non-interactive prompt.

**Usage:**

```bash
gemini [options] [promptWords...]
```

### 2.2. `gemini mcp`

This command is used to manage MCP (Multi-turn Conversation Protocol) servers.

**Subcommands:**

*   `add <name> <commandOrUrl> [args...]`: Add a server.
*   `remove <name>`: Remove a server.
*   `list`: List all configured MCP servers.

### 2.3. `gemini extensions`

This command allows you to manage Gemini CLI extensions.

**Subcommands:**

*   `install [<source>] [--path] [--ref] [--auto-update]`: Installs an extension from a git repository URL or a local path.
*   `uninstall <name>`: Uninstalls an extension.
*   `list`: Lists installed extensions.
*   `update [<name>] [--all]`: Updates all extensions or a named extension to the latest version.
*   `disable [--scope] <name>`: Disables an extension.
*   `enable [--scope] <name>`: Enables an extension.
*   `link <path>`: Links an extension from a local path.
*   `new <path> <template>`: Create a new extension from a boilerplate example.

## 3. Command Options

The Gemini CLI provides a rich set of options to customize its behavior:

| Option | Description |
| --- | --- |
| `-m, --model` | Specify the model to use. |
| `-p, --prompt` | Provide a non-interactive prompt. (Deprecated) |
| `-i, --prompt-interactive` | Execute a prompt and continue in interactive mode. |
| `-s, --sandbox` | Run in a sandbox for security. |
| `--sandbox-image` | URI for the sandbox image. (Deprecated) |
| `-d, --debug` | Run in debug mode. |
| `-a, --all-files` | Include all files in the context. (Deprecated) |
| `--show-memory-usage` | Show memory usage in the status bar. (Deprecated) |
| `-y, --yolo` | Automatically accept all actions. |
| `--approval-mode` | Set the approval mode (`default`, `auto_edit`, `yolo`). |
| `--telemetry` | Enable telemetry. (Deprecated) |
| `--telemetry-target` | Set the telemetry target (`local` or `gcp`). (Deprecated) |
| `--telemetry-otlp-endpoint` | Set the OTLP endpoint for telemetry. (Deprecated) |
| `--telemetry-otlp-protocol` | Set the OTLP protocol (`grpc` or `http`). (Deprecated) |
| `--telemetry-log-prompts` | Enable or disable logging of user prompts. (Deprecated) |
| `--telemetry-outfile` | Redirect all telemetry output to a file. (Deprecated) |
| `-c, --checkpointing` | Enable checkpointing of file edits. (Deprecated) |
| `--experimental-acp` | Start the agent in ACP mode. |
| `--allowed-mcp-server-names` | Allowed MCP server names. |
| `--allowed-tools` | Tools that are allowed to run without confirmation. |
| `-e, --extensions` | A list of extensions to use. |
| `-l, --list-extensions` | List all available extensions and exit. |
| `--proxy` | Proxy for the Gemini client. (Deprecated) |
| `--include-directories` | Additional directories to include in the workspace. |
| `--screen-reader` | Enable screen reader mode. |
| `-o, --output-format` | The format of the CLI output (`text` or `json`). |
| `-v, --version` | Show version number. |
| `-h, --help` | Show help. |

## 4. Context Management

You can provide context to the Gemini CLI from your files.

### 4.1. `@` Includes

You can include files in the context of your prompt using the `@` symbol followed by the file path. This is the recommended way to provide file content to the AI.

**Example:**

```
gemini "Summarize the following file: @/path/to/your/file.txt"
```

## 5. Configuration

The Gemini CLI can be configured using a `settings.json` file, which is typically located in the `.gemini` directory in your user's home folder. Many of the deprecated command-line options can be set permanently in this file.

**Example `settings.json`:**

```json
{
  "telemetry.enabled": true,
  "telemetry.logPrompts": true,
  "telemetry.outfile": "/path/to/your/chatlog.txt",
  "proxy": "http://your-proxy-server:port"
}
```

## 6. Extensions

Gemini CLI's functionality can be extended with custom extensions. You can create, install, and manage extensions to add new tools and capabilities.

## 7. Proxy Support

If you are behind a firewall, you can configure the Gemini CLI to use a proxy server.

## 8. Output Formatting

You can control the output format of the CLI, choosing between plain text and JSON. This is particularly useful for scripting and integrating the Gemini CLI with other tools.
