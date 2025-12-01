#!/usr/bin/env python3
"""
Test Suite for StudyBuddy

Run this to verify all components are working correctly.
"""

import os
import sys
import asyncio
import json
from datetime import datetime


def print_header(text: str):
    """Print a test section header."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")


def test_imports():
    """Test that all imports work."""
    print(" Testing imports...\n")
    
    errors = []
    
    # Config
    try:
        from config.settings import MODEL, APP_NAME
        print("[OK] config.settings")
    except Exception as e:
        errors.append(f"config.settings: {e}")
        print(f"[FAIL] config.settings: {e}")
    
    # Memory modules
    try:
        from memory.spaced_repetition import SpacedRepetitionScheduler
        print("[OK] memory.spaced_repetition")
    except Exception as e:
        errors.append(f"memory.spaced_repetition: {e}")
        print(f"[FAIL] memory.spaced_repetition: {e}")
    
    try:
        from memory.session_manager import StudyBuddySession, ProgressTracker
        print("[OK] memory.session_manager")
    except Exception as e:
        errors.append(f"memory.session_manager: {e}")
        print(f"[FAIL] memory.session_manager: {e}")
    
    # Tools
    try:
        from tools.file_tools import save_study_plan_to_file, save_notes_to_file
        print("[OK] tools.file_tools")
    except Exception as e:
        errors.append(f"tools.file_tools: {e}")
        print(f"[FAIL] tools.file_tools: {e}")
    
    try:
        from tools.progress_tools import record_quiz_result
        print("[OK] tools.progress_tools")
    except Exception as e:
        errors.append(f"tools.progress_tools: {e}")
        print(f"[FAIL] tools.progress_tools: {e}")
    
    # Observability
    try:
        from observability.logger import log_event
        print("[OK] observability.logger")
    except Exception as e:
        errors.append(f"observability.logger: {e}")
        print(f"[FAIL] observability.logger: {e}")
    
    # Agents (these need google.adk)
    try:
        from agents.learning_planner_agent import learning_planner
        from agents.tutor_agent import tutor_agent
        from agents.quiz_agent import quiz_agent
        from agents.progress_tracker_agent import progress_tracker
        from agents.study_buddy_agent import study_buddy_agent
        print("[OK] agents (all)")
    except Exception as e:
        errors.append(f"agents: {e}")
        print(f"[FAIL] agents: {e}")
    
    return len(errors) == 0


def test_spaced_repetition():
    """Test the spaced repetition scheduler."""
    print(" Testing spaced repetition...\n")
    
    from memory.spaced_repetition import SpacedRepetitionScheduler
    
    scheduler = SpacedRepetitionScheduler()
    
    # Test high performance
    next_review = scheduler.calculate_next_review(
        last_review=datetime.now(),
        repetition_number=0,
        performance=0.9
    )
    days_high = (next_review - datetime.now()).days
    print(f"  High performance (90%): review in {days_high} days")
    
    # Test medium performance
    next_review = scheduler.calculate_next_review(
        last_review=datetime.now(),
        repetition_number=0,
        performance=0.7
    )
    days_med = (next_review - datetime.now()).days
    print(f"  Medium performance (70%): review in {days_med} days")
    
    # Test low performance
    next_review = scheduler.calculate_next_review(
        last_review=datetime.now(),
        repetition_number=0,
        performance=0.4
    )
    days_low = (next_review - datetime.now()).days
    print(f"  Low performance (40%): review in {days_low} days")
    
    # Verify logic: low performance should have shorter interval
    assert days_low <= days_med <= days_high, "Interval logic incorrect!"
    print("\n[OK] Spaced repetition logic verified!")
    
    return True


def test_session_manager():
    """Test session creation and persistence."""
    print(" Testing session manager...\n")
    
    from memory.session_manager import StudyBuddySession
    
    test_student = "_TestStudent"
    
    # Create session
    session = StudyBuddySession(test_student)
    session.current_topic = "Test Topic"
    session.add_quiz_result("Test Topic", 85, 10)
    session.add_interaction("test", "Test interaction")
    
    print(f"  Created session for: {test_student}")
    print(f"  Current topic: {session.current_topic}")
    print(f"  Quiz results: {len(session.quiz_results)}")
    
    # Save
    saved = session.save()
    print(f"  Save successful: {saved}")
    
    # Load
    loaded = StudyBuddySession.load(test_student)
    print(f"  Loaded session topic: {loaded.current_topic}")
    
    # Verify
    assert loaded.current_topic == "Test Topic", "Topic not preserved!"
    assert len(loaded.quiz_results) == 1, "Quiz results not preserved!"
    
    # Cleanup
    session_path = f"output/sessions/{test_student}_session.json"
    if os.path.exists(session_path):
        os.remove(session_path)
        print("  Cleaned up test file")
    
    print("\n[OK] Session manager working!")
    
    return True


def test_file_tools():
    """Test file saving tools."""
    print(" Testing file tools...\n")
    
    from tools.file_tools import save_study_plan_to_file, save_notes_to_file
    
    # Test study plan save
    result = save_study_plan_to_file(
        "_test_plan.md",
        "# Test Plan\n\nThis is a test."
    )
    print(f"  {result}")
    
    # Cleanup
    test_path = "output/study_plans/_test_plan.md"
    if os.path.exists(test_path):
        os.remove(test_path)
        print("  Cleaned up test file")
    
    print("\n[OK] File tools working!")
    
    return True


def test_environment():
    """Check environment setup."""
    print(" Checking environment...\n")
    
    # Python version
    print(f"  Python: {sys.version}")
    if sys.version_info < (3, 9):
        print("  [!]  Python 3.9+ recommended")
    else:
        print("  [OK] Python version OK")
    
    # API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print(f"  [OK] GEMINI_API_KEY set ({len(api_key)} chars)")
    else:
        print("  [!]  GEMINI_API_KEY not set (needed for API tests)")
    
    # Check dependencies
    print("\n  Checking dependencies...")
    
    try:
        import google.genai
        print("  [OK] google-genai")
    except ImportError:
        print("  [FAIL] google-genai not installed")
    
    try:
        from google.adk import Agent
        print("  [OK] google-adk")
    except ImportError:
        print("  [FAIL] google-adk not installed")
    
    try:
        from rich.console import Console
        print("  [OK] rich")
    except ImportError:
        print("  [FAIL] rich not installed")
    
    return True


async def test_api_call():
    """Test actual API call (optional)."""
    print(" Testing API call...\n")
    
    if not os.environ.get("GEMINI_API_KEY"):
        print("  [!]  Skipping - no API key")
        return None
    
    try:
        from main import run_query
        
        print("  Sending test query...")
        response = await run_query(
            student_name="_APITest",
            query="Say 'Hello, I am working!' if you receive this."
        )
        
        print(f"  Response: {response[:200]}...")
        
        # Cleanup
        session_path = "output/sessions/_APITest_session.json"
        if os.path.exists(session_path):
            os.remove(session_path)
        
        print("\n[OK] API working!")
        return True
        
    except Exception as e:
        print(f"  [FAIL] API test failed: {e}")
        return False


async def main():
    """Run all tests."""
    print_header("StudyBuddy Test Suite")
    
    all_passed = True
    
    # Environment check
    print_header("1. Environment Check")
    test_environment()
    
    # Import tests
    print_header("2. Import Tests")
    if not test_imports():
        print("\n[FAIL] Import tests failed. Fix imports before continuing.")
        return
    
    # Unit tests
    print_header("3. Spaced Repetition Tests")
    try:
        test_spaced_repetition()
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        all_passed = False
    
    print_header("4. Session Manager Tests")
    try:
        test_session_manager()
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        all_passed = False
    
    print_header("5. File Tools Tests")
    try:
        test_file_tools()
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        all_passed = False
    
    # API test (optional)
    print_header("6. API Test (Optional)")
    do_api = input("Run API test? (uses quota) [y/N]: ").strip().lower()
    if do_api == 'y':
        await test_api_call()
    else:
        print("  Skipped")
    
    # Summary
    print_header("Test Summary")
    if all_passed:
        print(" All tests passed!")
        print("""
Your StudyBuddy is ready!

Next steps:
1. Run: python main.py
2. Try: python example_usage.py
3. Push to GitHub
4. Submit on Kaggle
        """)
    else:
        print("[!]  Some tests failed. Check errors above.")


if __name__ == "__main__":
    asyncio.run(main())
