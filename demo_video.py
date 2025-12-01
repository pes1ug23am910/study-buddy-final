#!/usr/bin/env python3
"""
Demo Script for Video Recording

A simplified version that demonstrates StudyBuddy's core features
without the complex multi-agent orchestration (which has API compatibility issues).
This version works reliably for video demos.
"""

import asyncio
import os
from datetime import datetime, timedelta

from google.genai import Client
from google.genai.types import GenerateContentConfig

from memory.session_manager import StudyBuddySession, ProgressTracker
from memory.spaced_repetition import SpacedRepetitionScheduler


# Initialize Gemini client
client = Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL = "gemini-2.0-flash"


def divider(title: str):
    """Print a section divider."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


async def call_gemini(prompt: str, system_instruction: str = None) -> str:
    """Call Gemini API directly."""
    config = GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.7,
    )
    
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config
    )
    
    return response.text


# ============================================================================
# Demo 1: Study Plan with Spaced Repetition
# ============================================================================

async def demo_study_plan():
    """Demonstrate study plan creation."""
    divider("DEMO 1: Study Plan with Spaced Repetition")
    
    print("You: Create a study plan for learning Python in 4 weeks\n")
    print("Processing...\n")
    
    system_prompt = """You are a study planning specialist. Create personalized study plans
with spaced repetition scheduling built in.

Always respond with this structure:
### Overview
Brief 2-3 sentence summary

### Learning Goals
- Goal 1
- Goal 2
- Goal 3

### Weekly Breakdown
| Week | Topics | Daily Time | Focus Area |
|------|--------|------------|------------|

### Review Schedule (Spaced Repetition)
List review sessions at days 3, 7, 14, 21 based on forgetting curve research.

### Checkpoints
- Checkpoint milestones with dates

Be realistic with time estimates."""

    prompt = "Create a study plan for learning Python in 4 weeks, assuming 2 hours daily."
    
    response = await call_gemini(prompt, system_prompt)
    print(f"StudyBuddy:\n{response}\n")
    
    print("-" * 40)
    print("Notice the built-in review schedule at days 3, 7, 14, 21!")
    print("That's spaced repetition based on the forgetting curve.")


# ============================================================================
# Demo 2: Mixed-Mode Tutoring
# ============================================================================

async def demo_tutoring():
    """Demonstrate the tutor with mixed-mode output."""
    divider("DEMO 2: Mixed-Mode Tutoring")
    
    print("You: Explain recursion with examples\n")
    print("Processing...\n")
    
    system_prompt = """You are a patient tutor who explains concepts in 4 sections:

### 1. Explanation
Clear explanation with examples and analogies.

### 2. Key Points
3-5 most important takeaways as bullet points.

### 3. Flashcards
Create 3-4 Q/A pairs:
Q1: Question
A1: Answer

### 4. Quick Quiz
2-3 questions to check understanding with answer key.

Always use all 4 sections."""

    prompt = "Explain recursion with examples"
    
    response = await call_gemini(prompt, system_prompt)
    print(f"StudyBuddy:\n{response}\n")
    
    print("-" * 40)
    print("Notice the 4-section format: Explanation, Key Points, Flashcards, Quiz!")


# ============================================================================
# Demo 3: Spaced Repetition Algorithm
# ============================================================================

async def demo_spaced_repetition():
    """Demonstrate the spaced repetition algorithm."""
    divider("DEMO 3: Spaced Repetition Algorithm in Action")
    
    print("Simulating quiz results and spaced repetition scheduling...\n")
    
    scheduler = SpacedRepetitionScheduler()
    
    # Simulate different performance levels
    scenarios = [
        ("Python Lists", 0.85, "Good performance"),
        ("Recursion", 0.65, "Needs practice"),
        ("Binary Search", 0.45, "Struggling"),
    ]
    
    print("Quiz Results and Next Review Dates:")
    print("-" * 50)
    
    for topic, score, comment in scenarios:
        next_review = scheduler.calculate_next_review(
            last_review=datetime.now(),
            repetition_number=1,
            performance=score
        )
        days_until = (next_review - datetime.now()).days
        
        print(f"\nTopic: {topic}")
        print(f"  Score: {score * 100:.0f}% ({comment})")
        print(f"  Next Review: in {days_until} days")
        
        if score >= 0.8:
            print(f"  -> High score! Interval increased.")
        elif score < 0.6:
            print(f"  -> Low score! Review scheduled sooner.")
    
    print("\n" + "-" * 50)
    print("\nThe algorithm adapts intervals based on performance:")
    print("  - Score >= 80%: Longer wait (you know it well)")
    print("  - Score 60-79%: Standard interval")
    print("  - Score < 60%: Shorter wait + potential step back")


# ============================================================================
# Demo 4: Progress Tracking
# ============================================================================

async def demo_progress():
    """Demonstrate progress tracking."""
    divider("DEMO 4: Progress Tracking")
    
    print("You: How am I doing?\n")
    
    # Create sample progress data
    tracker = ProgressTracker("DemoStudent")
    
    # Simulate some quiz history
    tracker.update_topic_progress("Python Basics", 92, 10, "Strong fundamentals")
    tracker.update_topic_progress("Lists and Loops", 85, 10, "Good understanding")
    tracker.update_topic_progress("Recursion", 62, 10, "Needs more practice")
    tracker.update_topic_progress("OOP Concepts", 58, 10, "Struggling with inheritance")
    
    # Also add to review schedule
    tracker.update_review_schedule("Python Basics", 0.92)
    tracker.update_review_schedule("Recursion", 0.62)
    
    print("StudyBuddy:\n")
    print("### Your Learning Summary")
    print(f"- Topics studied: 4")
    print(f"- Total quizzes: 4")
    print(f"- Average score: 74%")
    
    print("\n**Strengths**")
    print("- Python Basics (92%)")
    print("- Lists and Loops (85%)")
    
    print("\n**Needs Work**")
    print("- Recursion (62%)")
    print("- OOP Concepts (58%)")
    
    schedule = tracker.get_review_schedule()
    
    print("\n### Review Schedule")
    if schedule["due_reviews"]:
        for item in schedule["due_reviews"]:
            print(f"[OVERDUE] {item['topic']}")
    
    for item in schedule.get("upcoming_reviews", [])[:3]:
        print(f"[UPCOMING] {item['topic']} - in {item['days_until']} day(s)")
    
    print("\n### Recommendations")
    print("Focus on Recursion before moving forward. Would you like me to:")
    print("1. Explain recursion again with simpler examples?")
    print("2. Give you a focused practice quiz?")


# ============================================================================
# Main Menu
# ============================================================================

async def main():
    """Interactive demo menu for video recording."""
    
    print("\n" + "=" * 60)
    print("  StudyBuddy - Video Demo")
    print("=" * 60)
    
    print("""
Select a demo to run:

  1. Study Plan with Spaced Repetition
  2. Mixed-Mode Tutoring (Explain a concept)
  3. Spaced Repetition Algorithm
  4. Progress Tracking
  
  0. Run ALL demos
  q. Quit
""")
    
    demos = [
        demo_study_plan,
        demo_tutoring,
        demo_spaced_repetition,
        demo_progress,
    ]
    
    while True:
        choice = input("\nPick a demo (1-4, 0 for all, q to quit): ").strip().lower()
        
        if choice == "q":
            print("\nGoodbye!")
            break
        
        if choice == "0":
            print("\nRunning all demos...\n")
            for demo in demos:
                try:
                    await demo()
                    input("\nPress Enter for next demo...")
                except Exception as e:
                    print(f"Error in demo: {e}")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            try:
                await demos[int(choice) - 1]()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid choice. Enter 1-4, 0, or q.")


if __name__ == "__main__":
    # Check API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("\n[!] GEMINI_API_KEY not set!")
        print("Run: $env:GEMINI_API_KEY = 'your-key'\n")
    else:
        print("\nAPI Key: Set")
        asyncio.run(main())
