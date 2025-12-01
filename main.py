#!/usr/bin/env python3
"""
StudyBuddy - AI-Powered Learning Companion

Main entry point for running the Study Buddy agent.
Supports both interactive CLI mode and programmatic usage.
"""

import asyncio
import os
from typing import Optional

from google.genai.types import Content, Part
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService

from agents.study_buddy_agent import study_buddy_agent
from memory.session_manager import StudyBuddySession
from observability.logger import log_session_event, log_event
from config.settings import APP_NAME, DEFAULT_USER_ID, DEFAULT_SESSION_ID


async def run_interactive():
    """
    Starts the interactive chat mode. Just keeps asking for input
    until you type 'exit'. Saves your progress automatically.
    """
    # Get student name
    print("\n" + "=" * 60)
    print("  🎓 StudyBuddy - AI Learning Companion")
    print("=" * 60)
    
    student_name = input("\nWhat's your name? ").strip() or DEFAULT_USER_ID
    
    # Load or create session
    session = StudyBuddySession.load(student_name)
    log_session_event("start", student_name)
    
    # Initialize ADK services
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    # Create ADK session
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=student_name,
        session_id=f"{student_name}_session",
    )
    
    # Create runner
    runner = Runner(
        agent=study_buddy_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )
    
    print(f"\n🎓 Welcome, {student_name}! Study Buddy is ready.")
    print("Type 'exit' to quit, 'help' for commands.\n")
    
    # Show greeting
    print("StudyBuddy: Hey! I'm your AI learning companion. 🤖")
    print("I can help you:")
    print("  📚 Create personalized study plans")
    print("  🧑‍🏫 Explain any topic with flashcards")
    print("  ✏️ Quiz you and track your progress")
    print("  🔄 Manage your spaced repetition reviews")
    print("\nWhat would you like to work on today?\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in {"exit", "quit", "bye"}:
                session.save()
                log_session_event("end", student_name)
                print("\nStudyBuddy: Good luck with your studies! 📚✨\n")
                break
            
            if user_input.lower() == "help":
                print("\n📖 Commands:")
                print("  'explain [topic]' - Get an explanation with flashcards")
                print("  'quiz [topic]' - Take a practice quiz")
                print("  'plan [goal]' - Create a study plan")
                print("  'progress' - Check your learning progress")
                print("  'review' - See what topics need review")
                print("  'exit' - Save and quit")
                print()
                continue
            
            # Add context from session
            context = session.get_context()
            full_query = f"Context:\n{context}\n\nUser: {user_input}"
            
            # Create message
            content = Content(role="user", parts=[Part.from_text(full_query)])
            
            # Run agent
            log_event("study_buddy", "Processing request", {"query": user_input[:50]})
            
            final_text = ""
            async for event in runner.run(
                user_id=student_name,
                session_id=f"{student_name}_session",
                new_message=content,
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        final_text = event.content.parts[0].text
            
            # Record interaction
            session.add_interaction("query", user_input)
            session.add_interaction("response", final_text[:200])
            
            print(f"\nStudyBuddy: {final_text}\n")
            
        except KeyboardInterrupt:
            session.save()
            log_session_event("end", student_name, "Interrupted by user")
            print("\n\nStudyBuddy: Session saved. See you next time! 👋\n")
            break
        except Exception as e:
            log_event("study_buddy", "Error", {"error": str(e)}, level="error")
            print(f"\n⚠️ Something went wrong: {e}")
            print("Let's try again.\n")


async def run_query(student_name: str, query: str) -> str:
    """
    Send a single question/request to Study Buddy and get a response.
    Handy if you want to use this from another script or notebook.
    """
    # Load session
    session = StudyBuddySession.load(student_name)
    
    # Initialize ADK services
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=student_name,
        session_id=f"{student_name}_session",
    )
    
    runner = Runner(
        agent=study_buddy_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )
    
    # Add context
    context = session.get_context()
    full_query = f"Context:\n{context}\n\nUser: {query}"
    
    content = Content(role="user", parts=[Part.from_text(full_query)])
    
    # Run and collect response
    final_text = ""
    async for event in runner.run(
        user_id=student_name,
        session_id=f"{student_name}_session",
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_text = event.content.parts[0].text
    
    # Save interaction
    session.add_interaction("query", query)
    session.add_interaction("response", final_text[:200])
    session.save()
    
    return final_text


def main():
    """Entry point for CLI usage."""
    # Check for API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("\n⚠️  GEMINI_API_KEY environment variable not set!")
        print("Please set it before running:")
        print("  export GEMINI_API_KEY='your-key-here'  # Linux/Mac")
        print("  set GEMINI_API_KEY=your-key-here       # Windows")
        print()
        return
    
    asyncio.run(run_interactive())


if __name__ == "__main__":
    main()
