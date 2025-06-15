Please update the progress tracking in the appropriate CLAUDE.md file. Follow these steps:

1. **Identify current location**: Determine which CLAUDE.md file to update based on current directory
2. **Review recent commits**: Use `git log --oneline -10` to see recent work
3. **Update task status**: Move completed tasks to "Completed" section with completion date
4. **Update progress metrics**: Recalculate percentages
5. **Add new tasks if mentioned**: If new tasks are identified, add them to appropriate section
6. **Update timestamp**: Change the "Auto-Updated" date to today

Format for task status:
- `[ ]` for not started
- `[WIP]` for work in progress  
- `[BLOCKED]` for blocked tasks
- `[x]` for completed tasks

Always commit the updated CLAUDE.md with message: "docs: update progress tracking - [date]"