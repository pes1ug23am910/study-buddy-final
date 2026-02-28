# StudyBuddy — Multi-Agent AI Learning Companion

> A production-grade, multi-agent system built with **Google ADK** and **Gemini 2.0 Flash** that applies cognitive-science principles (spaced repetition, active recall) to deliver personalized tutoring, adaptive quizzing, and intelligent progress tracking.

Built as the capstone for Google's **5-Day AI Agents Intensive Course** (Track: *Agents for Good*).

---

## Why This Exists

Students lose up to **80 %** of newly learned material within 48 hours (Ebbinghaus, 1885). Existing study tools rarely adapt to the individual learner's pace. StudyBuddy addresses this by combining:

- **Spaced repetition scheduling** — algorithmically computed review intervals that combat the forgetting curve.
- **Multi-agent orchestration** — each pedagogical function (planning, tutoring, quizzing, progress analysis) is handled by a dedicated specialist agent coordinated via an LLM-powered orchestrator.
- **Mixed-mode tutoring** — every explanation is structured as *Concept → Key Points → Flashcards → Quick Quiz* to maximise encoding and retrieval practice in a single interaction.

---

## Architecture

```
study_buddy_agent  (Orchestrator — routes all user requests)
 │
 ├── learning_planner_agent   → Generates personalised study plans
 │     └── study_plan_validator  (Loop Agent — retries until plan meets quality bar)
 │
 ├── tutor_agent              → Mixed-mode explanations (4-section format)
 │     ├── explanation_validator (Loop Agent)
 │     └── google_search tool
 │
 ├── quiz_agent               → Generates & grades adaptive quizzes
 │     ├── quiz_validator      (Loop Agent)
 │     ├── record_quiz_result tool
 │     └── update_spaced_repetition_schedule tool
 │
 ├── progress_tracker_agent   → Analytics, review scheduling, recommendations
 │     ├── get_progress_summary tool
 │     ├── get_review_schedule tool
 │     └── save_study_plan_to_file tool
 │
 └── Shared tools
       ├── google_search
       ├── save_study_plan_to_file
       └── save_notes_to_file
```

A [Mermaid diagram](docs/architecture_diagram.md) with full detail is available in the `docs/` folder — it renders natively on GitHub.

### Design Highlights

| Concept | How It's Implemented |
|---|---|
| **Multi-agent orchestration** | 5 specialist `LlmAgent`s wrapped as `AgentTool`s; the orchestrator decides routing via function-calling |
| **Custom tools (6)** | File I/O, progress recording, spaced-repetition scheduling — all ADK `FunctionTool` declarations |
| **Session & Memory** | Dual persistence: ADK in-memory state for the active session + JSON file store for cross-session recall |
| **Loop Agents (3)** | Validator micro-agents (`study_plan_validator`, `quiz_validator`, `explanation_validator`) enforce quality via retry loops |
| **Spaced repetition** | Interval sequence `[1, 3, 7, 14, 30, 60, 120]` days with performance-based multipliers and Ebbinghaus retention estimation $R = e^{-t/S}$ |
| **Context engineering** | Session history (last 50 interactions) and progress data are injected into every agent prompt |

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI framework | [Google Agent Development Kit (ADK)](https://github.com/google/adk-python) |
| LLM | Gemini 2.0 Flash (`gemini-2.0-flash`) |
| Language | Python 3.9+ |
| Console UI | `rich` — tables, panels, colour-coded logging |
| Persistence | JSON file-based (no external DB required) |
| Async | `asyncio` / `aiohttp` |
| Env management | `python-dotenv` |
| Testing | `pytest`, `pytest-asyncio` |
| License | MIT |

---

## Repository Structure

```
study-buddy-final/
├── agents/
│   ├── study_buddy_agent.py        # Orchestrator — routes to sub-agents
│   ├── learning_planner_agent.py   # Personalised study plans
│   ├── tutor_agent.py              # Mixed-mode concept explanations
│   ├── quiz_agent.py               # Quiz generation & grading
│   ├── progress_tracker_agent.py   # Progress analytics
│   ├── reflection_agent.py         # Meta-learning coach (optional)
│   └── validators.py               # Loop-Agent quality validators
├── memory/
│   ├── spaced_repetition.py        # Forgetting-curve algorithm
│   ├── session_manager.py          # Session & progress persistence
│   └── profile_schema.json         # JSON Schema for student profiles
├── tools/
│   ├── file_tools.py               # Save plans, notes, flashcards
│   └── progress_tools.py           # Quiz results, review scheduling
├── config/
│   └── settings.py                 # Model, feature flags, intervals
├── observability/
│   └── logger.py                   # Rich-formatted structured logging
├── docs/
│   └── architecture_diagram.md     # Mermaid + ASCII architecture diagrams
├── output/                         # (gitignored) runtime-generated data
├── main.py                         # CLI entry point
├── example_usage.py                # Interactive demo menu (7 demos)
├── test_agent.py                   # Unit & integration test suite
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Getting Started

### Prerequisites

| Requirement | Details |
|---|---|
| Python | 3.9 or later |
| Gemini API key | Free tier available at [Google AI Studio](https://aistudio.google.com/app/apikey) |
| OS | Windows, macOS, or Linux |
| RAM | 2 GB minimum (all inference is cloud-based; no local model weights) |

### 1. Clone & install

```bash
git clone https://github.com/pes1ug23am910/study-buddy-final.git
cd study-buddy-final

python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 2. Configure the API key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your-key-here
```

Or export directly:

```bash
# Linux / macOS
export GEMINI_API_KEY="your-key-here"
# Windows (PowerShell)
$env:GEMINI_API_KEY="your-key-here"
```

### 3. Verify the setup

```bash
python test_agent.py
```

The test suite validates imports, the spaced repetition scheduler, session persistence, and file tools — all without making live API calls (unless opted in).

### 4. Run StudyBuddy

```bash
python main.py
```

```
StudyBuddy - AI Learning Companion
=====================================

What's your name? Alex

Welcome, Alex! Study Buddy is ready.
Type 'exit' to quit, 'help' for commands.
```

---

## Usage Examples

| Intent | What to type |
|---|---|
| Create a study plan | *"Create a 2-week study plan for DSA for coding interviews"* |
| Learn a concept | *"Explain binary search trees"* |
| Take a quiz | *"Quiz me on Python data structures"* |
| Check progress | *"How am I doing?"* |
| Review schedule | *"What should I review today?"* |
| Save notes | *"Save notes on sorting algorithms"* |

Every tutoring response follows the **4-section format**: Explanation → Key Points → Flashcards → Quick Quiz — maximising encoding variety in a single interaction.

---

## Spaced Repetition Algorithm

The scheduler implements a modified Leitner system with performance-adjusted intervals:

```
Base intervals (days):  1 → 3 → 7 → 14 → 30 → 60 → 120

Performance multipliers:
  Score >= 80%  → interval × 1.2  (advance faster)
  Score 60–79%  → interval × 1.0  (standard pace)
  Score <  60%  → interval × 0.7  + step back one level

Beyond preset intervals: exponential growth (ease factor 2.5)
Retention estimate:  R = e^(−t / S)
```

---

## Excluded Assets

The following are **generated at runtime** and intentionally excluded from version control:

| Path | Contents |
|---|---|
| `output/sessions/` | Per-student session JSON files |
| `output/progress/` | Quiz scores, per-topic analytics |
| `output/spaced_repetition/` | Review schedules and performance history |
| `output/study_plans/` | Exported study plan Markdown files |
| `.env` | API keys |

No large model weights or binaries are required — all inference is performed via the Gemini API.

---

## Running Tests

```bash
# Full test suite (offline — no API key needed)
python test_agent.py

# With live API integration test (requires GEMINI_API_KEY)
python test_agent.py --live
```

---

## Skills Demonstrated

- **LLM application engineering** — prompt design, agent orchestration, tool-use contracts
- **Multi-agent systems** — task decomposition, specialist delegation, loop-based quality assurance
- **Cognitive science in software** — spaced repetition, active recall, mixed-mode learning
- **Software architecture** — clean module boundaries, JSON Schema-validated data, feature-flag configuration
- **Async Python** — `asyncio` event loops, non-blocking I/O
- **Observability** — structured logging with Rich, colour-coded severity levels

---

## Future Roadmap

- [ ] Voice interface for conversational learning
- [ ] Gamification — streaks, XP, achievements
- [ ] Progress visualization dashboard (Matplotlib / Streamlit)
- [ ] Export to Notion / Obsidian
- [ ] Collaborative study groups
- [ ] LMS integration (Canvas, Google Classroom)

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

**Author:** [Yash Verma](https://github.com/pes1ug23am910)  
**Track:** Agents for Good — Google 5-Day AI Agents Intensive Course
