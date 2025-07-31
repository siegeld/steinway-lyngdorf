#!/bin/bash
# Automated commit workflow for Steinway P100 project

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Parse arguments
BUMP_TYPE="patch"
CUSTOM_MESSAGE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --minor)
            BUMP_TYPE="minor"
            shift
            ;;
        --major)
            BUMP_TYPE="major"
            shift
            ;;
        -m|--message)
            CUSTOM_MESSAGE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--minor|--major] [-m 'commit message']"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}Starting commit workflow...${NC}"

# 1. Clean build artifacts
echo -e "${YELLOW}Cleaning build artifacts...${NC}"
make clean 2>/dev/null || true

# 2. Read current version
if [ ! -f VERSION ]; then
    echo -e "${RED}VERSION file not found!${NC}"
    exit 1
fi

CURRENT_VERSION=$(cat VERSION)
echo -e "Current version: ${YELLOW}$CURRENT_VERSION${NC}"

# 3. Bump version
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR="${VERSION_PARTS[0]}"
MINOR="${VERSION_PARTS[1]}"
PATCH="${VERSION_PARTS[2]}"

case $BUMP_TYPE in
    major)
        NEW_VERSION="$((MAJOR + 1)).0.0"
        ;;
    minor)
        NEW_VERSION="$MAJOR.$((MINOR + 1)).0"
        ;;
    patch)
        NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
        ;;
esac

echo -e "New version: ${GREEN}$NEW_VERSION${NC}"

# 4. Update VERSION file
echo "$NEW_VERSION" > VERSION

# 5. Update CHANGELOG.md
echo -e "${YELLOW}Updating CHANGELOG.md...${NC}"
DATE=$(date +"%Y-%m-%d")
TEMP_FILE=$(mktemp)

# Read the changelog and update it
awk -v version="$NEW_VERSION" -v date="$DATE" '
    /^## \[Unreleased\]/ {
        print $0
        print ""
        print "### Added"
        print "- Nothing yet"
        print ""
        print "### Changed"
        print "- Nothing yet"
        print ""
        print "### Fixed"
        print "- Nothing yet"
        print ""
        print "## [" version "] - " date
        in_unreleased = 1
        next
    }
    /^## \[/ && in_unreleased {
        in_unreleased = 0
    }
    !in_unreleased || /^## \[/ {
        print $0
    }
' CHANGELOG.md > "$TEMP_FILE"

mv "$TEMP_FILE" CHANGELOG.md

# 6. Rebuild to ensure everything works
echo -e "${YELLOW}Rebuilding project...${NC}"
make install >/dev/null 2>&1

# 7. Run basic test
echo -e "${YELLOW}Running basic test...${NC}"
if ./run_cli.sh --help >/dev/null 2>&1; then
    echo -e "${GREEN}✓ CLI test passed${NC}"
else
    echo -e "${RED}✗ CLI test failed${NC}"
    exit 1
fi

# 8. Git operations
echo -e "${YELLOW}Staging changes...${NC}"
git add -A

# Show what will be committed
echo -e "${YELLOW}Changes to be committed:${NC}"
git status --short

# 9. Create commit
if [ -n "$CUSTOM_MESSAGE" ]; then
    COMMIT_MESSAGE="$CUSTOM_MESSAGE

Version: $NEW_VERSION"
else
    COMMIT_MESSAGE="Release v$NEW_VERSION

- Updated VERSION to $NEW_VERSION
- Updated CHANGELOG.md
- Cleaned build artifacts"
fi

echo -e "${YELLOW}Creating commit...${NC}"
git commit -m "$COMMIT_MESSAGE"

# 10. Tag the release
echo -e "${YELLOW}Creating tag v$NEW_VERSION...${NC}"
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"

echo -e "${GREEN}✓ Commit workflow completed successfully!${NC}"
echo -e "Version bumped from ${YELLOW}$CURRENT_VERSION${NC} to ${GREEN}$NEW_VERSION${NC}"
echo -e "Tagged as: ${GREEN}v$NEW_VERSION${NC}"
echo ""
echo -e "Next steps:"
echo -e "  - Push changes: ${YELLOW}git push origin main${NC}"
echo -e "  - Push tags: ${YELLOW}git push origin v$NEW_VERSION${NC}"