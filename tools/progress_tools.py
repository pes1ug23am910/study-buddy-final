"""
progress_tools.py
==================
These are the tools that make the "adaptive" part of adaptive learning work.
They record quiz results, track which topics you're good at (and not so good at),
and figure out when you should review stuff based on spaced repetition.
"""

import json
from datetime import datetime
from typing import Any, Dict

try:
    from google.adk.tools.tool_context import ToolContext
except ImportError:
    # Allow import without ADK for testing
    ToolContext = Any


def record_quiz_result(
    topic: str,
    score: float,
    total_questions: int,
    notes: str,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Saves quiz results so we can track how someone's doing over time.
    This data feeds into the learning planner, quiz difficulty adjustments,
    and the spaced repetition scheduler. Basically, it's how we remember
    what you're good at and what needs more work.
    """
    state = tool_context.state
    
    # Initialize progress tracking if needed
    if "progress" not in state:
        state["progress"] = {}
    
    # Get or create topic stats
    topic_stats = state["progress"].get(topic, {
        "attempts": 0,
        "last_score": 0.0,
        "best_score": 0.0,
        "total_answered": 0,
        "notes": "",
    })
    
    # Update stats
    topic_stats["attempts"] += 1
    topic_stats["last_score"] = score
    topic_stats["best_score"] = max(topic_stats["best_score"], score)
    topic_stats["total_answered"] += total_questions
    topic_stats["notes"] = notes
    topic_stats["last_updated"] = datetime.now().isoformat()
    
    state["progress"][topic] = topic_stats
    
    # Determine improvement trend
    trend = "first_attempt"
    if topic_stats["attempts"] > 1:
        if score > topic_stats.get("previous_score", score):
            trend = "improving"
        elif score < topic_stats.get("previous_score", score):
            trend = "declining"
        else:
            trend = "stable"
    
    topic_stats["previous_score"] = score
    
    return {
        "status": "ok",
        "message": f"Recorded quiz result for '{topic}'",
        "topic_stats": topic_stats,
        "trend": trend,
        "recommendation": _get_recommendation(score, topic_stats["attempts"])
    }


def get_progress_summary(
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Get a summary of the student's overall progress.
    
    Args:
        tool_context: ADK tool context with session state
    
    Returns:
        Progress summary with statistics and recommendations
    """
    state = tool_context.state
    progress = state.get("progress", {})
    
    if not progress:
        return {
            "status": "no_data",
            "message": "No progress data yet. Take some quizzes to track progress!",
            "topics_studied": 0,
            "total_attempts": 0
        }
    
    # Calculate overall stats
    topics_studied = len(progress)
    total_attempts = sum(t.get("attempts", 0) for t in progress.values())
    total_questions = sum(t.get("total_answered", 0) for t in progress.values())
    
    # Find strengths and weaknesses
    sorted_topics = sorted(
        progress.items(),
        key=lambda x: x[1].get("last_score", 0),
        reverse=True
    )
    
    strengths = [t[0] for t in sorted_topics[:3] if t[1].get("last_score", 0) >= 70]
    weaknesses = [t[0] for t in sorted_topics[-3:] if t[1].get("last_score", 0) < 70]
    
    # Calculate average score
    scores = [t.get("last_score", 0) for t in progress.values()]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    return {
        "status": "ok",
        "topics_studied": topics_studied,
        "total_attempts": total_attempts,
        "total_questions_answered": total_questions,
        "average_score": round(avg_score, 1),
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendation": _get_overall_recommendation(avg_score, weaknesses)
    }


def update_spaced_repetition_schedule(
    topic: str,
    performance: float,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Update the spaced repetition schedule for a topic.
    
    Args:
        topic: The topic to schedule
        performance: Performance score (0-1, where 1 is perfect)
        tool_context: ADK tool context with session state
    
    Returns:
        Updated schedule information
    """
    from memory.spaced_repetition import SpacedRepetitionScheduler
    
    state = tool_context.state
    
    # Initialize spaced repetition data if needed
    if "spaced_repetition" not in state:
        state["spaced_repetition"] = {}
    
    sr_data = state["spaced_repetition"]
    
    # Initialize topic if new
    if topic not in sr_data:
        sr_data[topic] = {
            "repetition_number": 0,
            "last_review": datetime.now().isoformat(),
            "performance_history": []
        }
    
    topic_data = sr_data[topic]
    
    # Record this review
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
    
    # Update topic data
    topic_data["repetition_number"] += 1
    topic_data["last_review"] = datetime.now().isoformat()
    topic_data["next_review"] = next_review.isoformat()
    
    days_until = (next_review - datetime.now()).days
    
    return {
        "status": "ok",
        "topic": topic,
        "next_review": next_review.isoformat(),
        "days_until_review": days_until,
        "repetition_number": topic_data["repetition_number"],
        "message": f"Great! Review '{topic}' again in {days_until} days for optimal retention."
    }


def get_review_schedule(
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """
    Get the current spaced repetition review schedule.
    
    Args:
        tool_context: ADK tool context with session state
    
    Returns:
        Schedule with due and upcoming reviews
    """
    state = tool_context.state
    sr_data = state.get("spaced_repetition", {})
    
    if not sr_data:
        return {
            "status": "no_schedule",
            "message": "No review schedule yet. Complete some study sessions to build one!",
            "due_reviews": [],
            "upcoming_reviews": [],
            "total_due": 0
        }
    
    now = datetime.now()
    due_now = []
    coming_up = []
    
    for topic, data in sr_data.items():
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
            review_info["overdue_days"] = abs(days_until)
            due_now.append(review_info)
        else:
            coming_up.append(review_info)
    
    # Sort by urgency
    due_now.sort(key=lambda x: x.get("overdue_days", 0), reverse=True)
    coming_up.sort(key=lambda x: x["days_until"])
    
    return {
        "status": "ok",
        "due_reviews": due_now,
        "upcoming_reviews": coming_up[:5],
        "total_due": len(due_now),
        "message": _get_schedule_message(len(due_now), coming_up)
    }


def _get_recommendation(score: float, attempts: int) -> str:
    """Get a recommendation based on score and attempts."""
    if score >= 90:
        return "Excellent! You've mastered this topic. Move on or try harder questions."
    elif score >= 70:
        return "Good progress! Review weak areas and try again soon."
    elif score >= 50:
        if attempts >= 3:
            return "Consider reviewing the fundamentals before more quizzes."
        return "Keep practicing! Focus on the concepts you missed."
    else:
        return "Take time to study the material again before the next quiz."


def _get_overall_recommendation(avg_score: float, weaknesses: list) -> str:
    """Get overall study recommendation."""
    if avg_score >= 80:
        return "You're doing great! Focus on maintaining your knowledge with regular reviews."
    elif avg_score >= 60:
        if weaknesses:
            return f"Solid progress! Prioritize these topics: {', '.join(weaknesses[:2])}"
        return "Keep up the good work! Try increasing the difficulty level."
    else:
        return "Focus on building strong fundamentals. Don't rush - understanding is key."


def _get_schedule_message(due_count: int, upcoming: list) -> str:
    """Generate a message about the review schedule."""
    if due_count > 0:
        return f"[!] You have {due_count} topic(s) due for review. Review now for best retention!"
    elif upcoming:
        next_topic = upcoming[0]
        return f"Next review: {next_topic['topic']} in {next_topic['days_until']} day(s)."
    else:
        return "Your review schedule is clear. Keep studying to build it up!"
