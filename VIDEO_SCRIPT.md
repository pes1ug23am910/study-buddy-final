# StudyBuddy Video Script

**Total Time: 2:50 (under 3 minutes)**

---

## Part 1: Hook & Problem (0:00 - 0:20) [20 seconds]

**[SCREEN: Title slide - "StudyBuddy - AI Learning Companion"]**

**SAY:**
> "Ever spent hours studying for an exam, felt totally prepared, and then forgot most of it a week later? 
> 
> Research shows we lose 70% of what we learn within 24 hours without proper review. But there's a fix - spaced repetition. The problem is, doing it manually is tedious.
>
> So I built StudyBuddy - AI agents that handle the boring parts so you can actually learn."

---

## Part 2: Architecture + Why Agents (0:20 - 1:10) [50 seconds]

**[SCREEN: Show architecture diagram or switch to code editor showing agents folder]**

**SAY:**
> "My first version was one big chatbot. It kept getting confused - mixing up explanations with quizzes, giving study plans when I asked about progress.
>
> So I rebuilt it as a team of specialized agents:"

**[SCREEN: Point to each agent in diagram/code]**

> "The **Planner** only thinks about scheduling - builds study timelines with spaced repetition baked in.
>
> The **Tutor** only explains concepts - clear explanations, examples, flashcards.
>
> The **Quiz Agent** handles testing - generates questions, grades answers, tracks scores.
>
> The **Progress Tracker** analyzes how you're doing and tells you what needs work.
>
> They all work under a main orchestrator that routes your requests to the right agent. Just like a real school has counselors, teachers, and TAs - specialization works."

---

## Part 3: DEMO (1:10 - 2:20) [70 seconds]

### Demo A: Study Plan (1:10 - 1:35) [25 seconds]

**[SCREEN: Terminal running main.py or example_usage.py]**

**SAY:**
> "Let me show you how it works."

**[TYPE: "Create a study plan for learning Python in 4 weeks"]**

> "I ask for a study plan..."

**[WAIT for response, point to key parts]**

> "See how it breaks down topics week by week, and look here - review sessions scheduled at day 3, 7, 14, 21. That's spaced repetition built right in."

---

### Demo B: Tutoring (1:35 - 1:55) [20 seconds]

**[TYPE: "Explain recursion" or "Explain binary search"]**

**SAY:**
> "Now let's learn something."

**[WAIT for response]**

> "Notice it doesn't just explain - you get the concept, key points, flashcards for review, and a quick quiz. Everything you need in one shot."

---

### Demo C: Spaced Repetition in Action (1:55 - 2:20) [25 seconds]

**[TYPE: "Quiz me on Python basics" - answer some questions]**

**SAY:**
> "Let me take a quick quiz..."

**[After quiz completes, show the spaced repetition update]**

> "I scored 85%, so watch what happens - the system pushes my next review from 1 day to 3 days. Score high, wait longer. Score low, review sooner. The algorithm adapts to how well you're actually learning."

**[TYPE: "How am I doing?"]**

> "And I can check my overall progress anytime. It shows strengths, weaknesses, and what's overdue for review."

---

## Part 4: The Build & Impact (2:20 - 2:50) [30 seconds]

**[SCREEN: Quick scroll through code or back to architecture]**

**SAY:**
> "Built with Google's Agent Development Kit and Gemini 2.0 Flash.
>
> The system has loop agents with validators for quality control, session persistence so your progress saves, and a spaced repetition algorithm based on actual forgetting curve research.
>
> The impact? Studies show spaced repetition can improve long-term retention by 70%. Plus it's available 24/7 and completely free - making quality study help accessible to any student."

---

## Part 5: Outro (2:50 - 3:00) [10 seconds]

**[SCREEN: Title slide with GitHub link]**

**SAY:**
> "StudyBuddy - making learning stick with AI and science. Code's on GitHub, link in the description."

---

# Quick Reference Card

| Time | Section | What to Show | Duration |
|------|---------|--------------|----------|
| 0:00 | Hook | Title slide | 20s |
| 0:20 | Architecture | Diagram or code | 50s |
| 1:10 | Demo: Plan | Terminal | 25s |
| 1:35 | Demo: Tutor | Terminal | 20s |
| 1:55 | Demo: Spaced Rep | Terminal | 25s |
| 2:20 | Build | Code/architecture | 30s |
| 2:50 | Outro | Title + GitHub | 10s |

---

# Recording Tips

1. **Practice the script 2-3 times** before recording
2. **Increase terminal font size** (Ctrl + scroll or settings)
3. **Test audio first** - record 10 seconds, play back
4. **Don't rush** - pauses are fine, you can trim later
5. **If you mess up, just pause and restart that section**
6. **Keep API key hidden** in any terminal output

---

# Commands to Run During Demo

```powershell
# Navigate to project
cd "e:\Notepad++ Local\Personal\Google AI Course\study-buddy-final"

# Activate venv (if using one)
.\venv\Scripts\activate

# Set API key (do this BEFORE recording!)
$env:GEMINI_API_KEY = "your-key"

# Run the main app
python main.py

# Alternative: run example usage for predictable demo
python example_usage.py
```

---

# Demo Queries to Use

1. "Create a study plan for learning Python in 4 weeks"
2. "Explain recursion with examples"
3. "Quiz me on Python basics"
4. "How am I doing?"

---

# Backup Queries (if something goes wrong)

- "Help me plan for my CS finals"
- "Explain how binary search works"
- "Test me on data structures"
- "Show my progress"
