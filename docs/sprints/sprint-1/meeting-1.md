# Meeting Notes

- ### Meeting Date: *07/11/2025*

- ### Meeting Recording: [Link](https://drive.google.com/file/d/1CSEhXdarh2dbiwM_1_hlwVPIL82ShLTn/view?usp=drive_link)

## Meeting Summary

- The tool should analyze and summarize code differences between commits, not just commit messages or code lines, to help users quickly understand what changed without reading code.

- It should provide information on contributors who made changes and highlight important modifications like deleted or rewritten code.

- Users want to specify the language model provider (e.g., Gemini) for summarization and be warned when feeding very large code diffs due to token/cost limits.

- The tool should support working on local Git repositories first, with potential future integration of GitHub/GitLab for cloning repos.

- Output will be simple text summaries in the CLI, with possible later enhancements like JSON output.

- The project stack will likely use Python for ease of development and maintenance, with preferences for modern Python packaging.

- Prototyping involves creating an interactive CLI demo showing what commands to type and example outputs, with a help command considered essential.

- The architecture will be simple with core components for command parsing, Git diff extraction, and connecting to the selected LLM provider.

- Additional features might include chunking large diffs for summarization and showing change histories per contributor.

---
