#!/usr/bin/env python3
"""
Example Usage for StudyBuddy

Demonstrates all the features of the StudyBuddy agent system.
Run individual examples or all at once.
"""

import asyncio
import os
import json
from datetime import datetime

from main import run_query
from memory.session_manager import StudyBuddySession, ProgressTracker
from memory.spaced_repetition import SpacedRepetitionScheduler


def divider(title: str):
    """Print a section divider."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


# ============================================================================
# Example 1: Create a Study Plan
# ============================================================================

async def demo_study_plan():
    """Demonstrate study plan creation."""
    divider("Demo: Study Plan with Spaced Repetition")
    
    response = await run_query(
        student_name="Demo_User",
        query="""
        I want to learn Data Structures and Algorithms for coding interviews.
        I'm a B.Tech CSE student with basic programming knowledge.
        I can study about 2 hours daily for 6 weeks.
        Create a study plan for me with spaced repetition built in.
        """
    )
    
    print(response)
    print("\n✨ Notice the built-in review schedule!\n")


# ============================================================================
# Example 2: Get a Topic Explained
# ============================================================================

async def demo_explanation():
    """Demonstrate the tutor agent's mixed-mode explanation."""
    divider("Demo: Topic Explanation (Mixed Mode)")
    
    response = await run_query(
        student_name="Demo_User",
        query="Explain binary search trees with examples"
    )
    
    print(response)
    print("\n✨ Notice the 4-section format: Explanation → Key Points → Flashcards → Quiz\n")


# ============================================================================
# Example 3: Take a Quiz
# ============================================================================

async def demo_quiz():
    """Demonstrate quiz generation."""
    divider("Demo: Quiz Generation")
    
    response = await run_query(
        student_name="Demo_User",
        query="Give me a quiz on Python data types and structures. Make it intermediate level."
    )
    
    print(response)
    print("\n✨ Quizzes include varied question types and answer keys!\n")


# ============================================================================
# Example 4: Spaced Repetition System
# ============================================================================

async def demo_spaced_repetition():
    """Demonstrate the spaced repetition algorithm."""
    divider("Demo: Spaced Repetition System")
    
    student = "Demo_SR"
    tracker = ProgressTracker(student)
    
    print("Simulating study sessions with different performance levels...\n")
    
    topics_and_scores = [
        ("Arrays", 0.95, "Excellent recall!"),
        ("Linked Lists", 0.72, "Good but some gaps"),
        ("Trees", 0.45, "Needs more practice"),
    ]
    
    for topic, performance, comment in topics_and_scores:
        result = tracker.update_review_schedule(topic, performance)
        print(f"Topic: {topic}")
        print(f"  Performance: {performance * 100:.0f}% - {comment}")
        print(f"  Next review in: {result['days_until_review']} days")
        print()
    
    print("-" * 40)
    print("\nNotice how low-performing topics are scheduled sooner!")
    
    schedule = tracker.get_review_schedule()
    print("\nCurrent Review Schedule:")
    for item in schedule.get('upcoming_reviews', []):
        print(f"  📅 {item['topic']}: in {item['days_until']} day(s)")


# ============================================================================
# Example 5: Progress Tracking
# ============================================================================

async def demo_progress():
    """Demonstrate progress tracking."""
    divider("Demo: Progress Tracking")
    
    response = await run_query(
        student_name="Demo_User",
        query="Show me my learning progress and what I should review"
    )
    
    print(response)
    print("\n✨ Progress tracking helps identify strengths and weaknesses!\n")


# ============================================================================
# Example 6: Session Persistence
# ============================================================================

async def demo_sessions():
    """Demonstrate session management."""
    divider("Demo: Session Persistence")
    
    student = "Session_Demo"
    
    # Create a new session
    session = StudyBuddySession(student)
    session.current_topic = "Machine Learning Basics"
    session.add_quiz_result("Linear Regression", 85, 10)
    session.add_quiz_result("Logistic Regression", 72, 10)
    session.add_interaction("query", "Explain gradient descent")
    
    # Save it
    session.save()
    print(f"Created and saved session for {student}")
    print(f"Current topic: {session.current_topic}")
    print(f"Quiz results: {len(session.quiz_results)}")
    
    # Load it back
    loaded = StudyBuddySession.load(student)
    print(f"\nLoaded session back:")
    print(f"Current topic: {loaded.current_topic}")
    print(f"Quiz results: {loaded.quiz_results}")
    
    print("\n✨ Sessions persist across restarts!\n")


# ============================================================================
# Example 7: Full Learning Cycle
# ============================================================================

async def demo_full_cycle():
    """Demonstrate a complete learning cycle."""
    divider("Demo: Complete Learning Cycle")
    
    student = "FullCycle_Demo"
    
    print("Step 1: Create a quick study plan...")
    print("-" * 40)
    r1 = await run_query(student, 
        "Make me a 1-week plan to learn Python basics")
    print(r1[:500] + "...\n" if len(r1) > 500 else r1)
    
    await asyncio.sleep(1)
    
    print("Step 2: Learn a concept...")
    print("-" * 40)
    r2 = await run_query(student,
        "Explain Python lists with examples")
    print(r2[:500] + "...\n" if len(r2) > 500 else r2)
    
    await asyncio.sleep(1)
    
    print("Step 3: Take a quiz...")
    print("-" * 40)
    r3 = await run_query(student,
        "Give me 3 quick questions on Python lists")
    print(r3[:500] + "...\n" if len(r3) > 500 else r3)
    
    print("\n✨ Complete learning cycle: Plan → Learn → Practice!")


# ============================================================================
# Main Menu
# ============================================================================

async def main():
    """Interactive demo menu."""
    
    print("\n" + "=" * 60)
    print("  StudyBuddy - Demo Examples")
    print("=" * 60)
    
    print("""
These demos showcase different features:

  1. Study Plan with Spaced Repetition
  2. Topic Explanation (Mixed Mode Output)
  3. Quiz Generation
  4. Spaced Repetition Algorithm
  5. Progress Tracking
  6. Session Persistence
  7. Full Learning Cycle
  
  0. Run ALL demos (takes a while)
  q. Quit
""")
    
    demos = [
        demo_study_plan,
        demo_explanation,
        demo_quiz,
        demo_spaced_repetition,
        demo_progress,
        demo_sessions,
        demo_full_cycle,
    ]
    
    choice = input("Pick a demo (1-7, 0 for all, q to quit): ").strip().lower()
    
    if choice == "q":
        print("Bye!")
        return
    
    if choice == "0":
        print("\nRunning all demos...\n")
        for demo in demos:
            try:
                await demo()
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Error in demo: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(demos):
        try:
            await demos[int(choice) - 1]()
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice!")
        return
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60)
    print("""
Check the output/ folder for saved data:
  • output/study_plans/  - Study plans
  • output/sessions/     - Session data
  • output/progress/     - Progress tracking
  • output/spaced_repetition/ - Review schedules
""")


if __name__ == "__main__":
    # Check API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("\n⚠️  GEMINI_API_KEY not set!")
        print("Some demos (4, 6) work without it, others need it.\n")
    
    asyncio.run(main())
