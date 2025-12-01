# StudyBuddy - AI Learning Companion

**Track:** Agents for Good  
**Built with:** Google ADK + Gemini 2.0 Flash

---

### Problem Statement

Students waste countless hours studying inefficiently. I know because I've been there - cramming the night before an exam, feeling confident walking in, then forgetting 70% of the material a week later.

The science backs this up. The Ebbinghaus forgetting curve shows that without proper review timing, we lose most of what we learn within days. But here's the thing: **spaced repetition** - reviewing material at scientifically-optimal intervals - can improve long-term retention by 70% or more.

So why doesn't everyone use it? Because it's tedious. You need to:
- Track what you've learned and when
- Calculate optimal review times based on your performance  
- Generate quality practice material
- Actually stick to the schedule

This is a problem worth solving because:
1. **Education equity**: Not everyone can afford tutors ($50-100/hour). AI can level the playing field.
2. **Scale**: A human tutor helps one student at a time. This helps unlimited students simultaneously.
3. **Availability**: Students get stuck at 2 AM. Office hours are 2-4 PM Tuesdays.
4. **Personalization**: Textbooks don't know you already understand arrays but struggle with recursion.

---

### Why Agents?

I could have built this as one big chatbot. But agents made more sense for a few reasons:

**1. Specialization works better**

Just like a school has different specialists (counselors for planning, teachers for explaining, TAs for grading), my system has:
- A **planner agent** that ONLY thinks about scheduling
- A **tutor agent** that ONLY focuses on clear explanations
- A **quiz agent** that ONLY handles assessment
- A **progress tracker** that ONLY analyzes performance

Each one does its job well because it's not trying to do everything.

**2. Natural coordination**

The main orchestrator routes requests like a receptionist:
- "I need a study plan" -> Planner
- "Explain recursion" -> Tutor  
- "Quiz me on Python" -> Quiz Agent
- "How am I doing?" -> Progress Tracker

This matches how learning actually works - it's not one thing, it's multiple related activities.

**3. Easier to improve**

If quiz generation is weak, I fix the quiz agent. Don't have to touch the planner. Modular design = easier maintenance.

**4. Quality assurance built-in**

Loop agents with validators ensure output quality. The study planner keeps trying until the plan has all required elements (goals, timeline, resources). No half-baked outputs.

---

### What You Created

**Architecture Overview:**

```
study_buddy_agent (Orchestrator)
|
|-- learning_planner_agent    [creates personalized study plans]
|       |-- study_plan_validator (Loop Agent pattern)
|
|-- tutor_agent               [explains concepts with mixed-mode output]
|       |-- google_search tool
|
|-- quiz_agent                [generates quizzes, grades answers]
|       |-- quiz_validator (Loop Agent pattern)
|       |-- record_quiz_result tool
|       |-- update_spaced_repetition tool
|
|-- progress_tracker_agent    [analyzes performance, manages reviews]
|       |-- get_progress_summary tool
|       |-- get_review_schedule tool
|
|-- Tools:
        |-- save_study_plan_to_file
        |-- save_notes_to_file
        |-- google_search
```

**Key Components:**

1. **SpacedRepetitionScheduler** - Calculates optimal review timing based on:
   - Performance score (0-100%)
   - Current repetition level (0-7)
   - Days since last review
   
   Formula adjusts intervals: Score 80%+ = longer wait, Score <60% = review sooner

2. **StudyBuddySession** - Persists student state:
   - Current topic being studied
   - Quiz history and scores
   - Review schedule
   - Interaction history

3. **Mixed-Mode Tutor Output** - Every explanation includes:
   - Clear explanation with examples
   - Key points summary
   - Flashcards for review
   - Quick quiz to check understanding

4. **Validators** - Quality checkers that ensure:
   - Study plans have goals, timeline, topics, resources
   - Quizzes have enough questions, answer keys, explanations

---

### Demo

**Example 1: Creating a Study Plan**

```
User: Create a study plan for learning Python in 4 weeks

StudyBuddy: 
### Overview
A 4-week intensive Python fundamentals course...

### Learning Goals
- Understand Python syntax and data types
- Master control flow and functions
- Work with files and error handling
- Build a small project

### Topics Breakdown
Week 1: Variables, Data Types, Operators
Week 2: Control Flow, Functions, Scope
Week 3: Data Structures (lists, dicts, sets)
Week 4: Files, Exceptions, Final Project

### Review Schedule
Day 3: Review Week 1 concepts
Day 7: First comprehensive review
Day 14: Second review + practice quiz
...

### Checkpoints
- End of Week 2: Complete 3 coding exercises
- End of Week 4: Build a CLI todo app
```

**Example 2: Mixed-Mode Tutoring**

```
User: Explain binary search

StudyBuddy:
### 1. Explanation
Binary search finds items in a sorted list by repeatedly 
dividing the search space in half...
[detailed explanation with visual example]

### 2. Key Points
- Only works on SORTED data
- O(log n) time complexity
- Compare middle element, eliminate half each time

### 3. Flashcards
Q: What's the prerequisite for binary search?
A: Data must be sorted

Q: What's the time complexity?
A: O(log n)

### 4. Quick Quiz
1. [Multiple Choice] If you're searching for 7 in [1,3,5,7,9], 
   what's the first element you compare?
   A) 1  B) 5  C) 7  D) 9
```

**Example 3: Spaced Repetition in Action**

```
User: [Completes quiz on Python Lists - scores 85%]

StudyBuddy:
Quiz recorded! Here's your spaced repetition update:

Topic: Python Lists
Score: 85% (Good!)
Previous interval: 1 day
New interval: 3 days (increased due to strong performance)
Next review: December 4, 2025

Your retention is improving! Keep it up.
```

**Example 4: Progress Tracking**

```
User: How am I doing?

StudyBuddy:
### Your Learning Summary
- Topics studied: 5
- Quizzes completed: 8  
- Average score: 78%

**Strengths**
- Python Basics (92%)
- Lists and Loops (85%)

**Needs Work**
- Recursion (62%)
- OOP Concepts (58%)

### Review Schedule
[OVERDUE] Recursion - was due 2 days ago
[UPCOMING] OOP Concepts - due tomorrow
[ON TRACK] Python Basics - due in 5 days

### Recommendations
Focus on Recursion before moving forward. Want me to:
1. Explain recursion again with simpler examples?
2. Give you a focused practice quiz?
```

---

### The Build

**Technologies Used:**

| Component | Technology |
|-----------|------------|
| Framework | Google Agent Development Kit (ADK) |
| LLM | Gemini 2.0 Flash |
| Language | Python 3.11 |
| Tools | google_search (built-in) + 6 custom tools |
| Storage | File-based JSON persistence |
| Logging | Rich library for formatted output |

**Concepts Implemented (6 of 3 required):**

1. **Multi-Agent System** - 5 specialized agents coordinated by orchestrator
2. **Tools** - Google Search + custom tools for file I/O, progress tracking
3. **Sessions & Memory** - StudyBuddySession class with JSON persistence
4. **Loop Agents** - Validators that retry until quality standards met
5. **Spaced Repetition Algorithm** - Based on Ebbinghaus forgetting curve
6. **Context Engineering** - Session history injected into agent prompts

**Project Structure:**

```
study-buddy-final/
├── agents/
|   ├── study_buddy_agent.py      # Main orchestrator
|   ├── learning_planner_agent.py # Study plan generation
|   ├── tutor_agent.py            # Mixed-mode explanations
|   ├── quiz_agent.py             # Quiz generation + grading
|   ├── progress_tracker_agent.py # Analytics + recommendations
|   └── validators.py             # Quality assurance agents
├── memory/
|   ├── spaced_repetition.py      # Forgetting curve algorithm
|   └── session_manager.py        # State persistence
├── tools/
|   ├── file_tools.py             # Save plans/notes
|   └── progress_tools.py         # Record results, manage schedule
├── config/
|   └── settings.py               # Centralized configuration
├── main.py                       # CLI entry point
├── test_agent.py                 # Test suite
└── requirements.txt
```

**How I Built It:**

1. Started with the spaced repetition algorithm - this is the core value
2. Built the session manager for state persistence
3. Created specialized agents one by one, testing each
4. Added the orchestrator to coordinate everything
5. Implemented validators for quality assurance
6. Built comprehensive tests to verify everything works

---

### If I Had More Time

**Immediate improvements:**
- **Voice interface** - Study hands-free while commuting or exercising
- **Gamification** - Streaks, XP, achievements to make learning addictive (in a good way)
- **Progress visualization** - Charts showing retention over time

**Medium-term goals:**
- **Notion/Obsidian integration** - Sync with existing note-taking workflows
- **Collaborative study groups** - Learn with friends, share progress
- **Custom content import** - Upload your own study materials

**Long-term vision:**
- **Adaptive difficulty** - ML model that learns your optimal challenge level
- **Multi-modal learning** - Diagrams, videos, interactive simulations
- **Deployment** - Cloud-hosted version anyone can use without setup

**Research directions:**
- **A/B testing** - Which explanation styles work best for different topics?
- **Forgetting curve personalization** - Everyone forgets at different rates
- **Motivation modeling** - Predict when students will disengage

---

## Summary

StudyBuddy solves a real problem I've personally experienced: inefficient studying. By combining multi-agent architecture with spaced repetition science, it provides personalized, accessible learning support that adapts to each student.

The agent approach wasn't just a technical choice - it mirrors how effective learning actually works: planning, teaching, practicing, and reflecting are distinct but coordinated activities.

If this helps even a few students learn more effectively, it's worth it.

---

**GitHub:** https://github.com/pes1ug23am910/studybuddy-agent  
**Track:** Agents for Good  
**December 2025**
