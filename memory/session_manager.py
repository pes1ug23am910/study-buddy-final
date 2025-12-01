"""
Session Management for StudyBuddy

Handles session persistence, context tracking, and long-term memory.
Combines file-based persistence with ADK's session services.
"""

import os
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from config.settings import (
    SESSIONS_DIR, PROGRESS_DIR, SPACED_REPETITION_DIR,
    USE_FILE_PERSISTENCE
)


class StudyBuddySession:
    """
    Manages session state for a student.
    
    Tracks:
    - Current learning topic
    - Active study plan
    - Quiz results history
    - Spaced repetition schedule
    - Interaction history
    """
    
    def __init__(self, student_name: str):
        self.student_name = student_name
        self.session_history: List[Dict[str, Any]] = []
        self.current_topic: Optional[str] = None
        self.study_plan: Optional[str] = None
        self.quiz_results: List[Dict[str, Any]] = []
        self.review_schedule: Optional[Dict[str, Any]] = None
        self.created_at = datetime.now().isoformat()
        self.last_active = datetime.now().isoformat()
    
    def add_interaction(self, interaction_type: str, content: str) -> None:
        """Record an interaction in the session history."""
        self.session_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": interaction_type,
            "content": content[:500] if len(content) > 500 else content  # Truncate long content
        })
        self.last_active = datetime.now().isoformat()
    
    def add_quiz_result(self, topic: str, score: float, total: int) -> None:
        """Record a quiz result."""
        self.quiz_results.append({
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "score": score,
            "total": total
        })
    
    def get_context(self) -> str:
        """
        Build context string for agent prompts.
        
        Returns:
            Formatted context about the student's current state
        """
        context_parts = [f"Student: {self.student_name}"]
        
        if self.current_topic:
            context_parts.append(f"Currently studying: {self.current_topic}")
        
        if self.study_plan:
            context_parts.append("Has an active study plan")
        
        if self.quiz_results:
            # Calculate average score (score is already a percentage 0-100)
            if self.quiz_results:
                total_score = sum(r.get('score', 0) for r in self.quiz_results)
                avg = total_score / len(self.quiz_results) / 100  # Convert to 0-1 for formatting
                context_parts.append(
                    f"Completed {len(self.quiz_results)} quizzes (avg: {avg:.0%})"
                )
        
        # Check for pending reviews
        if self.review_schedule:
            due_count = self.review_schedule.get('total_due', 0)
            if due_count > 0:
                context_parts.append(f"⚠️ {due_count} topic(s) due for review!")
        
        return "\n".join(context_parts)
    
    def save(self) -> bool:
        """Persist session to disk."""
        if not USE_FILE_PERSISTENCE:
            return False
        
        try:
            os.makedirs(SESSIONS_DIR, exist_ok=True)
            filepath = os.path.join(SESSIONS_DIR, f"{self.student_name}_session.json")
            
            data = {
                "student_name": self.student_name,
                "current_topic": self.current_topic,
                "study_plan": self.study_plan,
                "quiz_results": self.quiz_results,
                "history": self.session_history[-50:],  # Keep last 50 interactions
                "created_at": self.created_at,
                "last_active": self.last_active
            }
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    @classmethod
    def load(cls, student_name: str) -> "StudyBuddySession":
        """Load a previous session or create a new one."""
        filepath = os.path.join(SESSIONS_DIR, f"{student_name}_session.json")
        
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                session = cls(student_name)
                session.current_topic = data.get("current_topic")
                session.study_plan = data.get("study_plan")
                session.quiz_results = data.get("quiz_results", [])
                session.session_history = data.get("history", [])
                session.created_at = data.get("created_at", session.created_at)
                return session
            except Exception as e:
                print(f"Error loading session: {e}")
        
        return cls(student_name)


class ProgressTracker:
    """
    Tracks learning progress and manages spaced repetition schedules.
    """
    
    def __init__(self, student_name: str):
        self.student_name = student_name
        self.progress_data: Dict[str, Any] = {}
        self.review_data: Dict[str, Any] = {}
        self._load()
    
    def _load(self) -> None:
        """Load existing progress and review data."""
        # Load progress
        progress_path = os.path.join(PROGRESS_DIR, f"{self.student_name}_progress.json")
        if os.path.exists(progress_path):
            try:
                with open(progress_path, "r") as f:
                    self.progress_data = json.load(f)
            except:
                pass
        
        # Load review schedule
        review_path = os.path.join(SPACED_REPETITION_DIR, f"{self.student_name}_reviews.json")
        if os.path.exists(review_path):
            try:
                with open(review_path, "r") as f:
                    self.review_data = json.load(f)
            except:
                pass
    
    def update_topic_progress(
        self,
        topic: str,
        score: float,
        total_questions: int,
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        Update progress for a topic after a quiz/review.
        
        Returns:
            Updated topic statistics
        """
        if topic not in self.progress_data:
            self.progress_data[topic] = {
                "attempts": 0,
                "last_score": 0.0,
                "best_score": 0.0,
                "total_answered": 0,
                "notes": ""
            }
        
        stats = self.progress_data[topic]
        stats["attempts"] += 1
        stats["last_score"] = score
        stats["best_score"] = max(stats["best_score"], score)
        stats["total_answered"] += total_questions
        if notes:
            stats["notes"] = notes
        stats["last_updated"] = datetime.now().isoformat()
        
        self._save_progress()
        return stats
    
    def update_review_schedule(
        self,
        topic: str,
        performance: float
    ) -> Dict[str, Any]:
        """
        Update spaced repetition schedule for a topic.
        
        Returns:
            Updated review information
        """
        from memory.spaced_repetition import SpacedRepetitionScheduler
        
        if topic not in self.review_data:
            self.review_data[topic] = {
                "repetition_number": 0,
                "last_review": datetime.now().isoformat(),
                "performance_history": []
            }
        
        topic_data = self.review_data[topic]
        
        # Record performance
        topic_data["performance_history"].append({
            "date": datetime.now().isoformat(),
            "score": performance
        })
        
        # Calculate next review
        scheduler = SpacedRepetitionScheduler()
        last_review = datetime.fromisoformat(topic_data["last_review"])
        next_review = scheduler.calculate_next_review(
            last_review=last_review,
            repetition_number=topic_data["repetition_number"],
            performance=performance
        )
        
        topic_data["repetition_number"] += 1
        topic_data["last_review"] = datetime.now().isoformat()
        topic_data["next_review"] = next_review.isoformat()
        
        self._save_reviews()
        
        days_until = (next_review - datetime.now()).days
        return {
            "topic": topic,
            "next_review": next_review.isoformat(),
            "days_until_review": days_until,
            "repetition_number": topic_data["repetition_number"]
        }
    
    def get_review_schedule(self) -> Dict[str, Any]:
        """Get current review schedule status."""
        now = datetime.now()
        due_now = []
        coming_up = []
        
        for topic, data in self.review_data.items():
            next_review_str = data.get("next_review")
            if not next_review_str:
                continue
            
            next_review = datetime.fromisoformat(next_review_str)
            days_until = (next_review - now).days
            
            review_info = {
                "topic": topic,
                "next_review": next_review_str,
                "days_until": days_until,
                "times_reviewed": data.get("repetition_number", 0)
            }
            
            if next_review <= now:
                due_now.append(review_info)
            else:
                coming_up.append(review_info)
        
        due_now.sort(key=lambda x: x["days_until"])
        coming_up.sort(key=lambda x: x["days_until"])
        
        return {
            "due_reviews": due_now,
            "upcoming_reviews": coming_up[:5],
            "total_due": len(due_now)
        }
    
    def _save_progress(self) -> None:
        """Save progress data to file."""
        if not USE_FILE_PERSISTENCE:
            return
        
        try:
            os.makedirs(PROGRESS_DIR, exist_ok=True)
            filepath = os.path.join(PROGRESS_DIR, f"{self.student_name}_progress.json")
            with open(filepath, "w") as f:
                json.dump(self.progress_data, f, indent=2)
        except Exception as e:
            print(f"Error saving progress: {e}")
    
    def _save_reviews(self) -> None:
        """Save review schedule to file."""
        if not USE_FILE_PERSISTENCE:
            return
        
        try:
            os.makedirs(SPACED_REPETITION_DIR, exist_ok=True)
            filepath = os.path.join(SPACED_REPETITION_DIR, f"{self.student_name}_reviews.json")
            with open(filepath, "w") as f:
                json.dump(self.review_data, f, indent=2)
        except Exception as e:
            print(f"Error saving reviews: {e}")
