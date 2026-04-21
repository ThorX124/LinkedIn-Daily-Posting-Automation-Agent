#!/usr/bin/env python3
"""
Daily Fresh Agentic AI Poster
Fetches daily news and posts to LinkedIn
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).parent


def fetch_and_generate_content():
    """Fetch news and generate content"""
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "agentic_ai_news_content_generator.py")],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )

        # Extract content between markers
        output = result.stdout
        start_marker = "===POST_CONTENT_START==="
        end_marker = "===POST_CONTENT_END==="

        if start_marker in output and end_marker in output:
            content = output.split(start_marker)[1].split(end_marker)[0].strip()
            return content
        else:
            # Fallback: parse from the output
            lines = output.split('\n')
            content_lines = []
            capture = False
            for line in lines:
                if line.strip() == 'GENERATED POST:':
                    capture = True
                    continue
                if capture and line.startswith('---'):
                    continue
                if capture and line.startswith('==='):
                    break
                if capture:
                    content_lines.append(line)
            return '\n'.join(content_lines).strip()

    except Exception as e:
        print(f"[ERROR] Could not generate content: {e}")
        return None


def post_to_linkedin(text):
    """Post to LinkedIn using the autonomous poster"""
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "autonomous_linkedin_poster.py"), text],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=300  # 5 minute timeout
        )

        print(result.stdout)
        if result.stderr:
            print("[STDERR]", result.stderr)

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("[ERROR] Posting timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to post: {e}")
        return False


def main():
    print("=" * 60)
    print("DAILY FRESH AGENTIC AI POSTER")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    # Step 1: Fetch news and generate content
    print("[*] Fetching today's Agentic AI news...")
    print("[*] Generating content...")
    content = fetch_and_generate_content()

    if not content:
        print("[ERROR] Failed to generate content")
        sys.exit(1)

    print("[OK] News-based content generated!")
    print()

    # Show preview
    if '--auto' not in sys.argv:
        print("=" * 60)
        print("POST PREVIEW:")
        print("=" * 60)
        print(content[:500] + "..." if len(content) > 500 else content)
        print("=" * 60)
        print()

        response = input("Post this to LinkedIn? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("[INFO] Post cancelled")
            sys.exit(0)

    # Post to LinkedIn
    print("\n[*] Posting to LinkedIn...")
    print("[*] This may take 1-2 minutes...")
    print()

    success = post_to_linkedin(content)

    if success:
        print("\n" + "=" * 60)
        print("SUCCESS! News posted to LinkedIn!")
        print("=" * 60)
        print(f"Posted at: {datetime.now().strftime('%H:%M')}")
        print("Tomorrow's post will feature fresh news!")
    else:
        print("\n[!] Post may have failed. Check output above.")
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Cancelled by user")
        sys.exit(0)
