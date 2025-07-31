# Commit Workflow

This workflow handles the complete process for committing changes with version bumping.

## Overview

The commit process has two parts:
1. **Manual preparation** - Update documentation to describe your changes
2. **Automated execution** - Run commit.sh to handle versioning, committing, and pushing

## Part 1: Manual Preparation (You must do this first!)

1. **Ensure all code changes are complete**
   - All features implemented
   - All bugs fixed
   - Tests passing

2. **Update all relevant documentation**
   - **CHANGELOG.md**: Add your changes under `[Unreleased]` section
     - Organize into Added, Changed, Fixed categories
     - Be specific about what changed
   - **README.md**: Update if needed:
     - Feature list
     - Usage examples  
     - CLI command examples
     - Installation instructions
   - **CLAUDE.md**: Update if needed:
     - Current implementation status
     - Development notes
     - Common tasks
   - **.claude/commands/*.md**: Update any command documentation that changed

3. **Sync library to custom component (if library changed)**
   ```bash
   make sync-hacs
   ```

4. **Review your changes**
   ```bash
   git diff *.md **/*.md
   git status
   ```

## Part 2: Automated Execution (commit.sh handles this)

Once all markdown files are updated, run the commit script:

```bash
# For bug fixes and minor updates (0.1.0 → 0.1.1)
./commit.sh

# For new features (0.1.0 → 0.2.0)
./commit.sh --minor

# For breaking changes (0.1.0 → 1.0.0)
./commit.sh --major

# With custom commit message
./commit.sh --minor -m "Add media playback support"
```

### What commit.sh does automatically:

1. **Cleans build artifacts**
2. **Reads current version** from VERSION file
3. **Calculates new version** based on bump type
4. **Updates VERSION file** with new version
5. **Updates CHANGELOG.md**:
   - Creates new version section with today's date
   - Moves content from `[Unreleased]` to the new version section
   - Resets `[Unreleased]` section for future changes
6. **Rebuilds project** to ensure everything works
7. **Runs basic tests**
8. **Stages all changes** with git add -A
9. **Creates commit** with formatted message
10. **Tags the release** with version number
11. **Pushes to all remotes**:
    - Pushes to origin (if it exists)
    - Pushes to nfsrbr1
    - Pushes both main branch and version tag

## Important Notes

- **Always update documentation BEFORE running commit.sh**
- The script will move your `[Unreleased]` changes to a new version section
- The script will fail if any step fails, preventing incomplete commits
- Version tags are automatically created and pushed

## Example Workflow

After adding media playback support:

1. Update CHANGELOG.md:
   ```markdown
   ## [Unreleased]
   
   ### Added
   - HTTP API client for media information
   - Media playback controls (play, pause, next, previous)
   - CLI media commands
   ```

2. Update README.md with new features and examples

3. Update CLAUDE.md implementation status

4. Run: `./commit.sh --minor -m "Add media playback support"`

5. Done! The script handles version 0.2.0, creates commit, tags, and pushes.