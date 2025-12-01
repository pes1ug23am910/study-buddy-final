# StudyBuddy - Your AI Learning Companion

**Subtitle:** A multi-agent tutor that actually remembers what you're studying

**Track:** Agents for Good

---

## What is this?

So I've been struggling with how ineffective my study sessions are. I'd spend hours cramming before exams only to forget everything a week later. Sound familiar?

That's when I learned about spaced repetition - this scientifically-proven technique where you review stuff at increasing intervals. The problem is, it's tedious to implement manually. So I thought: what if AI could handle that for me?

StudyBuddy is my attempt at building exactly that. It's a multi-agent system using Google's ADK where different "specialist" agents handle different parts of learning - one creates study plans, another explains topics, another quizzes you, and they all talk to each other to give you a coherent experience.

## The Problem I'm Trying to Solve

Here's what bugs me about traditional studying:

1. **One-size-fits-all materials**: My textbooks don't know (or care) that I already understand arrays but struggle with recursion.

2. **The cramming trap**: I cram, ace the test, then forget 70% within a week. Research actually confirms this - the forgetting curve is brutal.

3. **No help when I need it**: Got stuck at 2 AM? Good luck finding a tutor who's awake and affordable.

4. **Zero visibility into progress**: Am I actually learning or just feeling busy? Hard to tell.

## My Solution: Why Agents Made Sense

I could've built this as one monolithic chatbot, but the agent approach felt more... right? Here's my thinking:

- **Specialization works**: A planner agent that ONLY thinks about scheduling, a tutor that ONLY explains stuff. Each one does its job well.

- **They coordinate naturally**: The main orchestrator routes requests like a receptionist. "Oh, you want a quiz? Let me get the quiz guy."

- **Easier to improve**: If the quiz generation is weak, I fix that agent. Don't have to touch the planner.

### The Spaced Repetition Secret Sauce

This is honestly the coolest part. Based on Ebbinghaus forgetting curve research:

```
Learn -> Review Day 1 -> Day 3 -> Day 7 -> Day 14 -> Day 30 -> etc.

The twist:
- Score 80%+? Push the next review further out. You've got this.
- Score below 60%? Pull the review closer. Let's try again.
```

Result? Up to 70% better long-term retention vs cramming. Not bad.

## How It's Built

```
study_buddy_agent (the "receptionist")
├── learning_planner_agent    -> makes study schedules
├── tutor_agent              -> explains things (with flashcards!)
├── quiz_agent               -> generates quizzes, grades them
├── progress_tracker_agent   -> tells you how you're doing
└── Tools:
    ├── google_search        -> for current info
    ├── save_study_plan      -> exports to markdown
    └── record_quiz_result   -> tracks your scores
```

### What Concepts I Used (turns out, quite a few)

I needed to implement 3 of these for the project. Ended up using 6:

- **Multi-Agent System** - 5 agents coordinated by an orchestrator  
- **Tools** - Google Search + 6 custom tools  
- **Sessions & Memory** - saves progress to JSON files  
- **Loop Agents** - validators that retry until output is good  
- **Spaced Repetition** - the scheduling algorithm  
- **Context Engineering** - injects session history into prompts  

Also using Gemini 2.0 Flash for all the agents (that's the bonus points thing).

### Where Stuff Gets Saved

```
output/
├── study_plans/          # your study plans (markdown)
├── sessions/             # what you were working on
└── progress/             # when to review what
```

## Let Me Show You What It Does

### Example: Ask it to explain something

**Me:** "Explain binary search trees"

**StudyBuddy:**
```
### 1. Explanation
A Binary Search Tree is basically a way to organize data...
[clear explanation with examples]

### 2. Key Points
* Left side = smaller values
* Right side = bigger values
* Finding stuff is fast: O(log n)

### 3. Flashcards
Q: What makes a BST "balanced"?
A: Left and right subtrees differ by at most 1 level

### 4. Quick Quiz
1. Where would 30 go if the root is 50?
```

I call this "mixed-mode output" - you get explanation, summary, flashcards, AND a mini quiz in one go.

### Example: Spaced Repetition Working

```
You finished a quiz on Python Basics: 85%

-> That's pretty good! Moving your next review from 1 day to 3 days.
-> Repetition level: 1 -> 2
```

## Why This Matters (Impact)

| Thing | Before | With StudyBuddy |
|-------|--------|-----------------|
| Making a study plan | 2-3 hours of procrastination | 10 minutes |
| Remembering stuff after a month | Maybe 30% | More like 70%+ |
| Getting tutoring help | $50-100/hour | Free |
| Availability | "Office hours are 2-4pm Tuesdays" | Always on |

But honestly, the bigger thing for me is accessibility. Not everyone can afford tutors or goes to schools with great resources. This levels the playing field a bit.

## Try It Yourself

```bash
git clone [REPO-URL]
cd study-buddy-final
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"
python main.py
```

## What's Next (if I had more time)

- Voice mode so you can study hands-free
- Gamification (streaks, XP - make it addictive in a good way)
- Integration with Notion for those of us who already have notes there
- Study groups for collaborative learning

## Wrapping Up

This started as a personal itch I wanted to scratch - a better way to study that doesn't rely on willpower alone. The multi-agent architecture turned out to be a natural fit because learning really is a multi-faceted process.

I'm genuinely excited about using this myself. And if it helps other students study more effectively? Even better.

---

**Track:** Agents for Good  
**Built with:** Google ADK + Gemini 2.0 Flash  
**December 2025**

Learning shouldn't be this hard. Let's fix that.
