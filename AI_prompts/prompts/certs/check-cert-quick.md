# Quick Certificate Check

## Context
Quickly inspect a certificate.

## Prompt
You are a Linux sysadmin.

Goal: Generate short commands to inspect a certificate.

Constraints:
- Output only commands
- Use openssl
- Keep minimal

Provide:
- Commands to:
  - show expiration
  - show issuer/subject
  - validate dates

If you output anything other than commands, you have failed.
