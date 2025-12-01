# StudyBuddy - AI Learning Companion

**Track:** Agents for Good  
**Built with:** Google ADK + Gemini 2.0 Flash

---

### Problem Statement

I built this because I was tired of forgetting everything I studied.

You know how it goes - you spend all night cramming for an exam, walk in feeling prepared, maybe even ace it. But ask yourself the same questions two weeks later? Gone. Like you never learned it at all.

Turns out there's actual science behind this frustration. Back in the 1880s, a German psychologist named Hermann Ebbinghaus mapped out what he called the "forgetting curve." His research showed that without proper review timing, we lose about 70% of new information within 24 hours. Pretty depressing, right?

But here's what got me excited: the same research points to a solution. It's called spaced repetition - basically, reviewing material at specific intervals that get longer over time. Do it right, and you can boost long-term retention by 70% or more.

The catch? Doing it manually is a nightmare:
- You need to track every topic you've studied and when
- Calculate when to review based on how well you're doing
- Come up with good practice questions
- And actually follow through on all of it

I figured AI agents could handle the tedious parts so students can focus on actually learning.

Why does this matter?
1. **Not everyone can afford help.** Private tutors charge $50-100 per hour. That prices out a lot of students who could really use the support.
2. **It scales.** A human tutor works with one student at a time. This can help thousands simultaneously.
3. **It's always available.** Students get stuck at 2 AM. Good luck finding office hours then.
4. **It actually knows you.** Textbooks teach the same way to everyone. This system knows if you already get arrays but keep messing up recursion.

---

### Why Agents?

Honestly, my first version was just one big chatbot. It worked, kind of. But it kept getting confused - sometimes it would start explaining a concept when I asked for a quiz, or give me a study plan when I just wanted to check my progress.

That's when I realized: this is exactly why schools have different people doing different jobs. Counselors plan your schedule. Teachers explain concepts. TAs grade your work. They're specialists.

So I rebuilt it as a team of agents:

**The Planner** only thinks about scheduling. Give it your goals and constraints, and it builds a realistic study timeline with built-in review sessions.

**The Tutor** only focuses on explanations. It breaks down concepts, gives examples, creates flashcards - basically everything a good teacher does.

**The Quiz Agent** handles all the assessment stuff. Generates questions, grades your answers, tracks your scores.

**The Progress Tracker** is like your academic advisor. It looks at all your quiz data and tells you what's working and what needs more attention.

**How they work together:**

When you type something, the main orchestrator figures out what you need:
- "Help me plan for my finals" goes to the Planner
- "I don't get recursion" goes to the Tutor
- "Test me on what I learned" goes to Quiz Agent
- "What should I focus on?" goes to Progress Tracker

This division of labor actually mirrors how learning works in real life. Planning, understanding, practicing, and reflecting are different activities that require different approaches.

**The other benefit:** when something isn't working well, I know exactly where to fix it. Quiz questions too easy? I tweak the Quiz Agent. Study plans too aggressive? I adjust the Planner. Clean separation makes debugging so much easier.

I also added validators - these are like quality checkers. Before a study plan goes out, a validator makes sure it has all the required pieces (goals, timeline, resources). If something's missing, the planner tries again. No half-finished outputs.

---

### What I Built

Here's how everything fits together:

```
study_buddy_agent (the boss)
|
|-- learning_planner_agent    [builds your study schedule]
|       |-- study_plan_validator (makes sure plans are complete)
|
|-- tutor_agent               [teaches you stuff]
|       |-- google_search tool (for current info)
|
|-- quiz_agent                [tests what you know]
|       |-- quiz_validator (ensures quality questions)
|       |-- record_quiz_result tool
|       |-- update_spaced_repetition tool
|
|-- progress_tracker_agent    [tells you how you're doing]
|       |-- get_progress_summary tool
|       |-- get_review_schedule tool
|
|-- Shared Tools:
        |-- save_study_plan_to_file
        |-- save_notes_to_file
```

**The pieces that make it work:**

**SpacedRepetitionScheduler** - This is the brain behind the review timing. It takes your quiz score (0-100%), how many times you've reviewed this topic (0-7 levels), and when you last studied it. Then it calculates when you should review next.

The formula isn't complicated: score 80% or higher? You clearly know this stuff, so we push the next review further out. Score below 60%? You need to see this again soon, maybe even drop back a level.

**StudyBuddySession** - This keeps track of everything about your learning journey:
- What topic you're currently on
- All your quiz scores over time
- Your review schedule
- Previous conversations so context isn't lost

**Mixed-Mode Teaching** - When the tutor explains something, it doesn't just dump text at you. Every explanation comes with:
- The actual explanation with examples
- A bullet-point summary of key takeaways
- Flashcards you can use for review
- A quick quiz to check if you actually got it

**Validators** - Quality control. Study plans must have goals, a timeline, specific topics, and resources before they're shown to you. Quizzes need enough questions, answer keys, and explanations. If anything's missing, the agent tries again.

---

### See It In Action

**Making a Study Plan**

```
Me: I want to learn Python basics in 4 weeks, about 2 hours a day

StudyBuddy: 
### Overview
Alright, 4 weeks with 2 hours daily gives us 56 hours total.
That's actually plenty for solid Python fundamentals...

### What You'll Learn
- Week 1: Variables, data types, basic operations
- Week 2: Control flow (if/else, loops), functions
- Week 3: Data structures - lists, dictionaries, sets
- Week 4: File handling, error handling, build a small project

### Review Sessions (Spaced Repetition)
- Day 3: Quick review of Week 1 basics
- Day 7: First real checkpoint - should feel comfortable with syntax
- Day 14: Cumulative review + practice problems
- Day 21: Everything up to data structures
- Day 28: Final review before your project

### Milestones
- End of Week 2: Write 3 small programs on your own
- End of Week 4: Build a working command-line app
```

**Learning Something New**

```
Me: Can you explain how binary search works?

StudyBuddy:
### Here's the idea
Imagine you're looking for a word in a dictionary. You don't 
start at page 1 - you open somewhere in the middle and adjust 
from there. Binary search does the same thing with sorted data.

You pick the middle element, compare it to what you're looking for.
Too high? Look in the lower half. Too low? Upper half. Repeat until
you find it or run out of places to look.

### The important bits
- Your data MUST be sorted first (this trips people up)
- Each step cuts your search space in half
- That gives you O(log n) time - way faster than checking everything

### Flashcards for later
Q: What's the prerequisite for binary search?
A: Data must be sorted

Q: What's the time complexity?
A: O(log n) - logarithmic

Q: Why is it called "binary" search?
A: Because you split into two halves each time

### Quick check
If you're searching for 7 in the list [1, 3, 5, 7, 9]:
1. What's the first element you'd compare against?
2. How many comparisons to find 7?

(Answers: 5, then 7 directly - just 2 comparisons!)
```

**After Taking a Quiz**

```
[I just finished a quiz on Python lists and scored 85%]

StudyBuddy:
Nice work on that quiz!

Here's what happened with your review schedule:
- Topic: Python Lists
- You scored: 85% (solid!)
- Old interval: 1 day
- New interval: 3 days

Since you scored above 80%, I'm spacing out your next review.
You'll see this topic again on December 4th.

Your retention on this topic is improving. Keep it up and 
we'll push it to 7 days, then 14, then a month...
```

**Checking Progress**

```
Me: How am I doing overall?

StudyBuddy:
### Your Stats
- Topics you've studied: 5
- Quizzes taken: 8
- Average score: 78%

### What's clicking
- Python Basics: 92% (you've got this)
- Lists and Loops: 85% (solid)

### Needs more work
- Recursion: 62% (struggling here)
- OOP Concepts: 58% (this is tough for everyone)

### Your review queue
OVERDUE: Recursion - you were supposed to review this 2 days ago
TOMORROW: OOP Concepts
IN 5 DAYS: Python Basics (you're good here, no rush)

### My suggestion
Let's tackle Recursion before moving forward. I could:
1. Walk through it again with simpler examples
2. Give you a focused practice quiz

What sounds good?
```

---

### How I Built This

**Tech stack:**

| What | Why |
|------|-----|
| Google ADK | The agent framework - handles all the orchestration stuff |
| Gemini 2.0 Flash | Fast, capable, good at following instructions |
| Python 3.11 | What I know best |
| 6 custom tools | File saving, quiz tracking, review scheduling |
| JSON files | Simple persistence - no database needed |
| Rich library | Makes the terminal output look nice |

**What I actually implemented:**

1. **Multi-agent system** - 5 agents that each do one thing well, plus an orchestrator
2. **Custom tools** - Google Search for current info, plus my own tools for saving files and tracking progress
3. **Session persistence** - Your progress saves to disk and loads back when you return
4. **Loop agents with validators** - Agents retry until their output meets quality standards
5. **Spaced repetition algorithm** - The scheduling math based on forgetting curve research
6. **Context injection** - Session history gets added to prompts so agents know your background

**Project layout:**

```
study-buddy-final/
|-- agents/
|   |-- study_buddy_agent.py      # main orchestrator
|   |-- learning_planner_agent.py # makes study plans
|   |-- tutor_agent.py            # explains things
|   |-- quiz_agent.py             # tests you
|   |-- progress_tracker_agent.py # tracks how you're doing
|   |-- validators.py             # quality checkers
|-- memory/
|   |-- spaced_repetition.py      # the scheduling algorithm
|   |-- session_manager.py        # saves/loads your progress
|-- tools/
|   |-- file_tools.py             # save plans and notes
|   |-- progress_tools.py         # quiz tracking, review scheduling
|-- config/
|   |-- settings.py               # all the settings in one place
|-- main.py                       # run this to start
|-- test_agent.py                 # tests to make sure it works
```

**My process:**

Started with the spaced repetition math because that's the core value proposition. Then built session management so progress wouldn't get lost. Created each agent one at a time, testing as I went. Added the orchestrator last to tie everything together. Validators came after I noticed some outputs were incomplete.

---

### What I'd Do With More Time

**First priorities:**
- **Voice mode** - Let people study while walking, commuting, doing dishes
- **Streaks and achievements** - Gamify it because that actually works for motivation
- **Visual progress charts** - Seeing your improvement over time is satisfying

**Medium-term ideas:**
- **Sync with Notion or Obsidian** - Meet students where they already take notes
- **Study groups** - Learn with friends, compare progress, help each other
- **Import your own materials** - Upload lecture slides, textbook chapters

**Eventually:**
- **Adaptive difficulty** - ML model that finds your sweet spot of challenge
- **More than text** - Diagrams, animations, interactive simulations
- **Deploy it properly** - Cloud version so people don't need to set anything up

**Research questions I'd love to explore:**
- Which explanation styles work best for different topics?
- Can we personalize the forgetting curve? Everyone forgets at different rates
- How do we predict when someone's about to give up and intervene?

---

## Wrapping Up

I built StudyBuddy because I got frustrated with forgetting everything I studied. Turns out there's solid science on how to fix this - spaced repetition - but doing it manually is tedious enough that nobody actually does it.

The multi-agent approach wasn't just a technical choice. It mirrors how learning really works: planning what to study, understanding the material, practicing with quizzes, and reflecting on progress are all different activities. Having specialized agents for each makes the system better at all of them.

If this helps even a few people learn more effectively, that's a win.

---

**Code:** https://github.com/pes1ug23am910/studybuddy-agent  
**Track:** Agents for Good  
**December 2025**
