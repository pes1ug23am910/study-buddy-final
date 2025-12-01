# Humanization & Emoji Removal Checklist

This checklist helps you review all files to:
1. Remove emojis that could trigger AI detection
2. Make code comments and docs sound more natural/human
3. Add personal voice and varied phrasing

---

## Priority 1: Files to Remove from Git (Already in .gitignore)

- [x] `.gitignore` - Updated to exclude:
  - `docs/*.drawio` (diagram files)
  - `Card and thumbnail/` (image folder)
  - `MERGE_CHECKLIST.md` (internal doc)

---

## Priority 2: Python Files with Emojis

### agents/learning_planner_agent.py
Lines with emojis: 35, 38, 43, 48, 51, 54
- [ ] Line 35: `###  Overview` -> `### Overview`
- [ ] Line 38: `###  Learning Goals` -> `### Learning Goals`
- [ ] Line 43: `###  Topics Breakdown` -> `### Topics Breakdown`
- [ ] Line 48: `### 🔴 Priority Topics` -> `### Priority Topics`
- [ ] Line 51: `###  Review Schedule` -> `### Review Schedule`
- [ ] Line 54: `### [OK] Checkpoints` -> `### Checkpoints`

### agents/progress_tracker_agent.py
Lines with emojis: 42-44, 56, 63, 67, 71, 79
- [ ] Line 42: `[!] Topics overdue` -> `[OVERDUE] Topics`
- [ ] Line 43: ` Topics coming up` -> `[UPCOMING] Topics`
- [ ] Line 44: `[OK] Topics on track` -> `[ON TRACK] Topics`
- [ ] Line 56: `###  Your Learning Summary` -> `### Your Learning Summary`
- [ ] Line 63: `**Strengths **` -> `**Strengths**`
- [ ] Line 67: `**Needs Work **` -> `**Needs Work**`
- [ ] Line 71: `###  Review Schedule` -> `### Review Schedule`
- [ ] Line 79: `###  Recommendations` -> `### Recommendations`

### agents/quiz_agent.py
Lines with emojis: 61, 72
- [ ] Line 61: `###  Answer Key` -> `### Answer Key`
- [ ] Line 72: `[OK] Correct or [FAIL] Incorrect` -> `CORRECT or INCORRECT`

### agents/reflection_agent.py
- [ ] Line 53: `###  Learning Reflection` -> `### Learning Reflection`

### agents/study_buddy_agent.py
Lines with emojis: 39-58, 90, 102-107
- [ ] Remove arrows (->) or keep as plain text arrows (->)
- [ ] Line 90: `` -> remove
- [ ] Lines 102-107: Remove all emojis from greeting

### agents/tutor_agent.py
Lines with emojis: 26, 34, 41, 57, 79-80
- [ ] Line 26: `### 1.  Explanation` -> `### 1. Explanation`
- [ ] Line 34: `### 2.  Key Points` -> `### 2. Key Points`
- [ ] Line 41: `### 3.  Flashcards` -> `### 3. Flashcards`
- [ ] Line 57: `### 4.  Quick Quiz` -> `### 4. Quick Quiz`

### agents/validators.py
Lines with arrows: 28-29, 55-56, 81-82
- [ ] Replace `->` with `->` throughout

### memory/session_manager.py
- [ ] Line 88: `[!]` -> `[!]` or `WARNING:`

### memory/spaced_repetition.py
Lines with arrows: 18, 21
- [ ] Line 18: `->` -> `->`
- [ ] Line 21: `>=` -> `>=`

### observability/logger.py
Lines with emojis: 50, 68-69, 84, 105, 122-128, 143, 170, 178
- [ ] Replace emoji_map with text indicators:
  ```python
  emoji_map = {
      "start": "[START]",
      "end": "[END]",
      "save": "[SAVE]",
      "load": "[LOAD]",
      "error": "[ERROR]"
  }
  ```
- [ ] Remove , , ✓ from log formatting

### tools/progress_tools.py
- [ ] Line 291: `[!]` -> `WARNING:`

### example_usage.py
Lines with emojis: 45, 62, 79, 114, 131, 163, 198, 265-268, 275
- [ ] Replace `` with `Note:` or just remove
- [ ] Line 114: `` -> remove
- [ ] Line 275: `[!]` -> `WARNING:`
- [ ] Lines 265-268: Replace bullets with plain `-`

### main.py
Lines with emojis: 31, 59, 63-68, 81, 85, 124, 128, 186
- [ ] Line 31: `` -> remove or use `***`
- [ ] Lines 63-68: Remove all emojis from greeting
- [ ] Line 81: `` -> remove
- [ ] Line 85: `` -> remove
- [ ] Line 124: `` -> remove
- [ ] Line 128, 186: `[!]` -> `WARNING:`

### test_agent.py
Lines with emojis: 24, 31, 34, etc. (many)
- [ ] Replace all `[OK]` with `[OK]` or `PASS:`
- [ ] Replace all `[FAIL]` with `[FAIL]` or `ERROR:`
- [ ] Replace `` with `Testing:` or remove
- [ ] Replace `[!]` with `WARNING:`
- [ ] Replace `` with `SUCCESS:` or remove

---

## Priority 3: Markdown Files with Emojis

### README.md
Heavy emoji usage throughout - replace:
- [ ] `#  StudyBuddy` -> `# StudyBuddy`
- [ ] `##  Key Features` -> `## Key Features`
- [ ] All table emojis (, , , , , , )
- [ ] `## 🧠 How Spaced Repetition` -> `## How Spaced Repetition`
- [ ] `## 🏗️ Architecture` -> `## Architecture`
- [ ] All checkmarks in concepts list
- [ ] `##  Quick Start` -> `## Quick Start`
- [ ] `## 💬 Example Interactions` -> `## Example Interactions`
- [ ] `## 📁 Project Structure` -> `## Project Structure`
- [ ] `##  Value Proposition` -> `## Value Proposition`
- [ ] `##  Future Roadmap` -> `## Future Roadmap`
- [ ] `## 📜 License` -> `## License`
- [ ] `## 🙏 Acknowledgments` -> `## Acknowledgments`
- [ ] Final line emoji

### QUICKSTART.md
- [ ] `## ⚡ Get Running` -> `## Get Running`
- [ ] `##  Common Commands` -> `## Common Commands`
- [ ] `##  Try These Queries` -> `## Try These Queries`
- [ ] `##  Troubleshooting` -> `## Troubleshooting`
- [ ] `` at end -> remove

### KAGGLE_WRITEUP.md
- [ ] Already cleaned, but check arrows (->) throughout

### MERGE_CHECKLIST.md
- [ ] This file is in .gitignore now, no need to clean

---

## Priority 4: Humanization Tips

After removing emojis, also review for:

### Variable/Function Names
- [x] Already natural (like `calculate_next_review`, `get_due_topics`)

### Comments
- [x] Already humanized in key files
- [ ] Review remaining files for overly formal docstrings

### Docstrings to Humanize
Look for patterns like:
- "This function does X" -> "Does X" or just explain directly
- "Args:" formal blocks -> Keep for Python convention, but make descriptions casual
- Triple-quoted formal descriptions -> Add personal notes

### Text Variations
Add variety to avoid repetitive patterns:
- "Returns X" -> Sometimes use "Gives back X" or "You get X"
- "Handles X" -> "Takes care of X" or "Deals with X"
- "Implements X" -> "This is how we do X"

---

## Quick Sed/Replace Commands

For bulk emoji removal in PowerShell:

```powershell
# Remove common emojis from Python files
Get-ChildItem -Recurse -Include *.py | ForEach-Object {
    (Get-Content $_) -replace '|||[OK]|[FAIL]|[!]||||||||||||||||||||', '' |
    Set-Content $_
}
```

---

## Verification Checklist

After making changes:
- [ ] Run `python test_agent.py` to ensure code still works
- [ ] Check no Python syntax errors from removed characters
- [ ] Verify markdown files render correctly
- [ ] Commit and push changes
- [ ] Re-run emoji detection: `Get-ChildItem -Recurse -Include *.py,*.md | Select-String '[^\x00-\x7F]'`

---

## Files That Are Fine (No Changes Needed)

- `config/settings.py` - Clean
- `config/__init__.py` - Clean
- `memory/__init__.py` - Clean
- `memory/profile_schema.json` - Clean
- `tools/__init__.py` - Clean
- `observability/__init__.py` - Clean
- `agents/__init__.py` - Clean
- `.env.example` - Clean
- `requirements.txt` - Clean
- `LICENSE` - Clean
