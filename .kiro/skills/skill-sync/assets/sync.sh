#!/usr/bin/env bash
#
# sync.sh - Sync skill metadata to AGENTS.md Auto-invoke section
#
# Usage:
#   ./skills/skill-sync/assets/sync.sh           # Update AGENTS.md
#   ./skills/skill-sync/assets/sync.sh --dry-run # Preview changes
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
AGENTS_MD="$REPO_ROOT/AGENTS.md"

DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--dry-run]"
      exit 1
      ;;
  esac
done

# Extract auto_invoke from SKILL.md frontmatter
extract_auto_invoke() {
  local skill_file="$1"
  local skill_name="$2"
  
  # Read file content
  local content
  content=$(cat "$skill_file")
  
  # Check if file has frontmatter
  if [[ ! "$content" =~ ^--- ]]; then
    return
  fi
  
  # Extract frontmatter (between first two ---)
  local frontmatter
  frontmatter=$(echo "$content" | sed -n '/^---$/,/^---$/p' | sed '1d;$d')
  
  # Check for auto_invoke
  if ! echo "$frontmatter" | grep -q "auto_invoke"; then
    return
  fi
  
  # Parse auto_invoke - handle both string and list formats
  local in_auto_invoke=false
  local indent=""
  
  while IFS= read -r line; do
    # Single line format: auto_invoke: "action"
    if [[ "$line" =~ ^[[:space:]]*auto_invoke:[[:space:]]*[\"\'](.+)[\"\'][[:space:]]*$ ]]; then
      echo "| ${BASH_REMATCH[1]} | \`$skill_name\` |"
      return
    fi
    
    # Single line format without quotes: auto_invoke: action
    if [[ "$line" =~ ^[[:space:]]*auto_invoke:[[:space:]]*([^-\"\'][^[:space:]].*)$ ]]; then
      echo "| ${BASH_REMATCH[1]} | \`$skill_name\` |"
      return
    fi
    
    # List format start: auto_invoke:
    if [[ "$line" =~ ^[[:space:]]*auto_invoke:[[:space:]]*$ ]]; then
      in_auto_invoke=true
      continue
    fi
    
    # List item: - "action" or - action
    if $in_auto_invoke; then
      if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*[\"\'](.+)[\"\'][[:space:]]*$ ]]; then
        echo "| ${BASH_REMATCH[1]} | \`$skill_name\` |"
      elif [[ "$line" =~ ^[[:space:]]*-[[:space:]]*(.+)[[:space:]]*$ ]]; then
        echo "| ${BASH_REMATCH[1]} | \`$skill_name\` |"
      elif [[ ! "$line" =~ ^[[:space:]]*- ]] && [[ -n "$line" ]] && [[ ! "$line" =~ ^[[:space:]]*$ ]]; then
        # End of list
        break
      fi
    fi
  done <<< "$frontmatter"
}

# Generate Auto-invoke table
generate_table() {
  echo "| Action | Skill |"
  echo "|--------|-------|"
  
  for skill_dir in "$SKILLS_DIR"/*/; do
    local skill_name
    skill_name=$(basename "$skill_dir")
    local skill_file="$skill_dir/SKILL.md"
    
    if [[ -f "$skill_file" ]]; then
      extract_auto_invoke "$skill_file" "$skill_name"
    fi
  done
}

# Main
main() {
  if [[ ! -d "$SKILLS_DIR" ]]; then
    echo "Error: Skills directory not found: $SKILLS_DIR"
    exit 1
  fi
  
  if [[ ! -f "$AGENTS_MD" ]]; then
    echo "Error: AGENTS.md not found: $AGENTS_MD"
    exit 1
  fi
  
  # Generate new table
  local new_table
  new_table=$(generate_table)
  
  if $DRY_RUN; then
    echo "=== DRY RUN - Would update Auto-invoke section with: ==="
    echo ""
    echo "## Auto-invoke Skills"
    echo ""
    echo "When performing these actions, ALWAYS invoke the corresponding skill FIRST:"
    echo ""
    echo "$new_table"
    echo ""
    echo "=== END DRY RUN ==="
    exit 0
  fi
  
  # Create temp file with updated content
  local temp_file
  temp_file=$(mktemp)
  
  # Replace Auto-invoke section
  awk -v table="$new_table" '
    /^## Auto-invoke Skills/ {
      print "## Auto-invoke Skills"
      print ""
      print "When performing these actions, ALWAYS invoke the corresponding skill FIRST:"
      print ""
      print table
      print ""
      # Skip until next ## or ---
      while ((getline line) > 0) {
        if (line ~ /^## / || line ~ /^---/) {
          print line
          break
        }
      }
      next
    }
    { print }
  ' "$AGENTS_MD" > "$temp_file"
  
  # Check if anything changed
  if diff -q "$AGENTS_MD" "$temp_file" > /dev/null 2>&1; then
    echo "No changes needed - AGENTS.md is already in sync"
    rm "$temp_file"
  else
    mv "$temp_file" "$AGENTS_MD"
    echo "Updated AGENTS.md Auto-invoke section"
  fi
}

main "$@"
