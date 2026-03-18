Curated Briefing from "Accelerated Learning with Gemini Deep Research and Obsidian AI"
Exported on: 19/09/2025, 20:10:01

---

### User

please detail the knowledge graph creation automation with AI and the automation steps please?

---

### Model

> The Knowledge Graph creation automation process leverages AI (specifically via Cursor) to build the structured Obsidian notes, solving the pain point that manually building the graph is SLOW1. This entire process only involves two simple steps and is designed to extract knowledge points from the AI-generated learning road map and convert them into organized note cards for writing learning notes23.
> The Role of AI in Knowledge Graph Creation
> The automation utilizes an AI agent, such as Cloud Sonet 3.5 via Cursor, to operate the Obsidian file folders24. This automation ensures that the extensive road map created by Google Gemini's Deep Research is quickly and efficiently converted into the linked notes necessary for Obsidian's graph view25.
> The core goal of the AI automation is to extract knowledge points and make each one into a note card for the user to write their learning notes2.
> Automation Steps for Knowledge Graph Creation
> The knowledge graph creation is achieved through two major automation steps:
> Step 1: Creating Index Notes
> This step focuses on generating the foundational note files based on the topics outlined in the learning road map3.
> 1. Prompting the AI: The user provides a prompt based on the learning road map report, instructing the AI to perform the following actions4:
>     ◦ Action 1: Create a list of markdown files for each topic based on the learning road map4.
>     ◦ Action 2: For each topic file, write an introduction4.
>     ◦ Action 3 (Crucial Formatting): Include a list of knowledge points, ensuring that each knowledge point title is written in double square brackets ([[knowledge point]])46. The double square brackets are essential because they create the necessary links in Obsidian.
> 2. AI Execution and Review: The AI (e.g., Cloud Sonet 3.5) creates these notes4. The result is notes created with an introduction and the note card links listed inside6.
> 3. Acceptance: The user reviews the AI-created files and simply clicks "accept" to integrate them into the vault6.
> Step 2: Linking and Finalizing the Graph (Creating Backlinks)
> This step connects the newly created index notes back to the original road map file, making the entire structure navigable3.
> 1. Prompting the AI: The user provides a second prompt detailing the backlinking requirement6:
>     ◦ Action: Add the list of the created file names back into the road map file6.
>     ◦ Placement and Formatting: Place these file names under each related topic, ensuring they use double square brackets ([[]]) to quote the file names6.
> 2. AI Execution and Review: The AI executes the task, adding the links (e.g., "related detail notes") to the original road map node7.
> 3. Finalization: The user accepts the changes7.
> 4. Enabling Graph View: The final step to enable the visualization of the graph view is to move those index notes into the designated "notes" folder within Obsidian8.
> This automated process results in a clear learning road map where the user can click a link on the road map and jump directly to the index note, which lists all the key concepts for them to fulfill (write their learning notes)78.