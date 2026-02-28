# Quick Start

Get StudyBuddy running in under 5 minutes.

## 1. Environment setup

```bash
cd study-buddy-final
python -m venv venv

# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## 2. API key

```bash
# Option A — .env file (recommended)
cp .env.example .env        # then edit .env and paste your key

# Option B — shell variable
export GEMINI_API_KEY="your-key-here"          # bash
$env:GEMINI_API_KEY = "your-key-here"          # PowerShell
```

Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).

## 3. Verify

```bash
python test_agent.py
```

## 4. Run

```bash
python main.py
```

## Useful commands

| Command | Purpose |
|---|---|
| `python main.py` | Interactive chat mode |
| `python example_usage.py` | Guided demo menu (7 scenarios) |
| `python test_agent.py` | Offline test suite |

## Sample queries

```
Create a study plan for learning Python in 4 weeks
Explain recursion with examples
Quiz me on data structures
What should I review today?
Show my progress
```

## Problems?

See [docs/troubleshooting.md](docs/troubleshooting.md).
