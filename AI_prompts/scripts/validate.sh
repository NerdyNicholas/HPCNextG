#!/usr/bin/env bash
for file in $(find prompts -name "*.md"); do
  grep -q "## Prompt" "$file" || echo "Missing Prompt: $file"
done
