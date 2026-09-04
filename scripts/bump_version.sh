#!/usr/bin/env bash
# scripts/bump_version.sh - Semantic Versioning release tool
# Usage: ./scripts/bump_version.sh [major|minor|patch] "Release summary"

set -e

BUMP_TYPE="${1:-patch}"
MSG="${2:-Release update}"
VERSION_FILE="VERSION"

if [ ! -f "$VERSION_FILE" ]; then
  echo "Error: $VERSION_FILE not found."
  exit 1
fi

CURRENT_VERSION=$(cat "$VERSION_FILE" | tr -d '[:space:]')
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

case "$BUMP_TYPE" in
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  patch)
    PATCH=$((PATCH + 1))
    ;;
  *)
    echo "Usage: $0 [major|minor|patch] [commit message]"
    exit 1
    ;;
esac

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
echo "Bumping version: v${CURRENT_VERSION} -> v${NEW_VERSION} ($BUMP_TYPE)"

# Update VERSION file
echo "$NEW_VERSION" > "$VERSION_FILE"

# Git commit and tag
git add "$VERSION_FILE" CHANGELOG.md 2>/dev/null || true
git commit -m "chore(release): v${NEW_VERSION} - ${MSG}" || true
git tag -a "v${NEW_VERSION}" -m "Release v${NEW_VERSION}: ${MSG}"

echo "✓ Successfully tagged v${NEW_VERSION}"
echo "To push to GitHub: git push origin main --tags"
