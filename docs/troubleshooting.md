# Troubleshooting

## Common Issues

### 1. `GEMINI_API_KEY not found`

**Symptom:** The application exits immediately with a message about a missing API key.

**Fix:** Ensure the key is available in one of these ways:

```bash
# Option A — .env file in project root
echo "GEMINI_API_KEY=your-key-here" > .env

# Option B — environment variable (PowerShell)
$env:GEMINI_API_KEY = "your-key-here"

# Option B — environment variable (bash)
export GEMINI_API_KEY="your-key-here"
```

Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).

---

### 2. `ModuleNotFoundError: No module named 'google.adk'`

**Symptom:** Import error on startup.

**Fix:**

```bash
pip install --upgrade google-adk google-genai google-generativeai
```

If you're inside a virtual environment, make sure it's activated first.

---

### 3. `ModuleNotFoundError: No module named 'rich'`

```bash
pip install -r requirements.txt
```

---

### 4. Rate limit / quota errors from Gemini API

**Symptom:** `429 Resource Exhausted` or similar.

**Fix:**
- The free tier has a per-minute request cap. Wait 60 seconds and retry.  
- For heavier usage, enable billing in Google Cloud Console.

---

### 5. `output/` directory missing

The `output/` folder and its sub-directories (`sessions/`, `progress/`, `spaced_repetition/`, `study_plans/`) are created automatically at runtime. If you cloned the repo fresh, they don't exist yet — that's expected.

---

### 6. Tests fail with `ConnectionError`

The offline test suite (`python test_agent.py`) does **not** require network access. If you see connection errors, you may be running the live integration test:

```bash
# Offline only (default)
python test_agent.py

# With live API call (requires key + network)
python test_agent.py --live
```

---

### 7. Windows: `venv\Scripts\activate` is not recognised

Use the PowerShell-specific activation command:

```powershell
.\venv\Scripts\Activate.ps1
```

If execution policy blocks it:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Still stuck?

Open an issue on the [GitHub repository](https://github.com/pes1ug23am910/study-buddy-final/issues) with:

1. Your OS and Python version (`python --version`)
2. The full error traceback
3. Steps to reproduce
