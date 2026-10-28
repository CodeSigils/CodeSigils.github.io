#!/usr/bin/env python3
import re
import sys

FORBIDDEN = [
    r'co-authored-by',
    r'ultraworked',
    r'sisyphus',
    r'clio-agent',
    r'claude',
    r'\[bot\]',
    r'assisted-by',
    r'generated-with',
    r'prompted-by',
    r'tool:',
]

def main():
    if len(sys.argv) < 2:
        sys.exit(0)
    msg_file = sys.argv[1]
    try:
        with open(msg_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading commit message: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove comment lines for validation
    lines = []
    for line in content.split('\n'):
        if line.strip().startswith('#'):
            continue
        lines.append(line)
    
    msg = '\n'.join(lines).strip()
    if not msg:
        print("Commit message is empty", file=sys.stderr)
        sys.exit(1)
    
    msg_lower = msg.lower()
    for pattern in FORBIDDEN:
        if re.search(pattern, msg_lower):
            print(f"Forbidden pattern found in commit message: {pattern}", file=sys.stderr)
            sys.exit(1)
    
    # Check subject line
    parts = msg.split('\n')
    subject = parts[0].strip()
    if len(subject) == 0:
        print("Subject line is empty", file=sys.stderr)
        sys.exit(1)
    if len(subject) > 50:
        print(f"Subject line too long ({len(subject)} chars, max 50)", file=sys.stderr)
        sys.exit(1)
    if subject.endswith('.'):
        print("Subject line should not end with a period", file=sys.stderr)
        sys.exit(1)
    
    # Check for what: and why: (required by this repo)
    if not re.search(r'^\s*what\s*:', msg, re.M):
        print("Missing required 'what:' field", file=sys.stderr)
        sys.exit(1)
    if not re.search(r'^\s*why\s*:', msg, re.M):
        print("Missing required 'why:' field", file=sys.stderr)
        sys.exit(1)
    
    sys.exit(0)

if __name__ == '__main__':
    main()
