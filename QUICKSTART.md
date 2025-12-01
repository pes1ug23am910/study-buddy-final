# StudyBuddy v2.0 - Quick Start Guide

## ⚡ Get Running in 5 Minutes

### Step 1: Setup (2 min)

```powershell
# Navigate to project
cd study-buddy-final

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: API Key (1 min)

```powershell
# Set your Gemini API key
$env:GEMINI_API_KEY = "your-key-here"

# Or create .env file
copy .env.example .env
# Edit .env and add your key
```

### Step 3: Test (1 min)

```powershell
python test_agent.py
```

### Step 4: Run (1 min)

```powershell
python main.py
```

---

## 📋 Common Commands

| Command | Description |
|---------|-------------|
| `python main.py` | Start interactive mode |
| `python example_usage.py` | Run demo examples |
| `python test_agent.py` | Run test suite |

---

## 🎯 Try These Queries

```
"Create a study plan for learning Python in 4 weeks"
"Explain recursion with examples"
"Quiz me on data structures"
"What should I review today?"
"Show my progress"
```

---

## 🔧 Troubleshooting

### "Module not found"
```powershell
# Make sure venv is active
.\venv\Scripts\activate
pip install -r requirements.txt
```

### "API key not found"
```powershell
$env:GEMINI_API_KEY = "your-key"
```

### Import errors
Make sure you're running from the `study-buddy-final` directory.

---

**You're ready! 🎓**
