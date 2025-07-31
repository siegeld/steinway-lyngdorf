# Commit Workflow

This workflow prepares and commits changes with automatic version bumping.

## Steps:

1. **Clean build artifacts**
   ```bash
   make clean
   ```

2. **Read current version**
   ```bash
   current_version=$(cat VERSION)
   ```

3. **Bump version (patch by default)**
   - For patch bump (0.1.0 → 0.1.1): Use when provided
   - For minor bump (0.1.0 → 0.2.0): Use with --minor flag
   - For major bump (0.1.0 → 1.0.0): Use with --major flag

4. **Update VERSION file**
   ```bash
   echo "$new_version" > VERSION
   ```

5. **Update CHANGELOG.md**
   - Add new version section with date
   - Move unreleased items to new version

6. **Rebuild to ensure everything works**
   ```bash
   make install
   ```

7. **Run basic tests**
   ```bash
   ./run_cli.sh --help
   ```

8. **Stage all changes**
   ```bash
   git add -A
   ```

9. **Create commit**
   ```bash
   git commit -m "Release v$new_version

   - Updated VERSION to $new_version
   - Updated CHANGELOG.md
   - Cleaned build artifacts
   "
   ```

10. **Tag the release**
    ```bash
    git tag -a "v$new_version" -m "Release v$new_version"
    ```

## Usage:
```bash
# Patch version bump (0.1.0 → 0.1.1)
./commit.sh

# Minor version bump (0.1.0 → 0.2.0)
./commit.sh --minor

# Major version bump (0.1.0 → 1.0.0)
./commit.sh --major

# Custom commit message
./commit.sh -m "Add monitor mode and improve CLI"
```