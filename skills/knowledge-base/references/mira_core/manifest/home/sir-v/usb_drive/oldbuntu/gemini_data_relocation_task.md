# MIRA Task: Relocate Gemini CLI Data Directory

## Task Objective:
Relocate the Gemini CLI's operational data directory from its current location at `/home/sir-v/.gemini` (consuming 5.6GB on the root partition) to the newly created `/data/.gemini` on the dedicated data partition. This will free up 5.6GB of space on the root filesystem and improve system organization.

## MIRA's Plan:
1. Create the target directory `/data/.gemini`.
2. Provide the Human Orchestrator with precise manual steps to move the data and restart the Gemini CLI.

## Agent Execution Log:

### Target Directory Creation (MIRA's Action):
- **Command:** `sudo mkdir /data/.gemini`
- **Output:** `(empty)` (Indicates success)
- **Status:** Directory `/data/.gemini` successfully created.

## Human Orchestrator Action - CRITICAL DATA RELOCATION (Manual Steps):

**ATTENTION: This task requires you to close this current Gemini CLI session and restart it with new parameters. Please read all steps before proceeding.**

### Step 1: Move Current MIRA Data to the New Location

You will move all contents from the old `.gemini` directory to the newly created one.

```bash
# Move all visible files and directories:
sudo mv /home/sir-v/.gemini/* /data/.gemini/

# Move all hidden files and directories (like .bashrc, .config, etc.):
sudo mv /home/sir-v/.gemini/.??* /data/.gemini/
```
*   **Note:** If the first `mv` command (`/home/sir-v/.gemini/*`) gives a "No such file or directory" error, it simply means there were no non-hidden files to move. This is usually fine, as most of my data is in hidden files/directories.
*   **Verification:** After these commands, you can run `ls -A /home/sir-v/.gemini/` to ensure it's empty (or only contains '.' and '..'). And `ls -A /data/.gemini/` should show the moved contents.

### Step 2: Remove the Now Empty Original Data Directory

```bash
sudo rm -rf /home/sir-v/.gemini
```
*   This will remove the old, empty `/home/sir-v/.gemini` directory.

### Step 3: Terminate This Current Gemini CLI Session

**This is critical.** You must now manually close this Gemini CLI session. You can do this by typing `exit` or closing the terminal window where the Gemini CLI is running.

### Step 4: Start a NEW Gemini CLI Session with the New Data Directory

When you launch the Gemini CLI next time, you *must* tell it to use the new data directory. There are two primary ways to do this:

#### Option A: Using an Environment Variable (Recommended for consistent use)

Before running the `gemini` command, set the `GEMINI_DATA_DIR` environment variable:

```bash
export GEMINI_DATA_DIR=/data/.gemini
gemini
```
*   **Tip:** To make this permanent for all future sessions, you can add `export GEMINI_DATA_DIR=/data/.gemini` to your `~/.bashrc` file (or your shell's equivalent config file) and then `source ~/.bashrc` or open a new terminal.

#### Option B: Using a Command-Line Flag (If supported by your installation)

Some installations allow specifying the data directory directly when running the command:

```bash
gemini --data-dir=/data/.gemini
```
*   **Note:** You can check if your `gemini` installation supports this flag by running `gemini --help`.

### Step 5: (Optional) Create a Symbolic Link

If you wish to maintain a `~/.gemini` path that automatically redirects to `/data/.gemini` for convenience or compatibility with other tools, you can create a symbolic link *after* you have successfully started the new Gemini CLI session:

```bash
ln -s /data/.gemini /home/sir-v/.gemini
```

## Final Verification (After Restarting Gemini CLI):

Once you have restarted the Gemini CLI successfully using the new data directory, you can verify by running:

```bash
df -h
```
You should see that your root partition (`/`) has significantly more available space (another 5.6GB freed), and your `/data` partition (`/dev/nvme0n1p8`) will show an additional 5.6GB of used space.

## Agent Queries/Obstacles (If Any):
None at this time.
