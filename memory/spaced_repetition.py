"""
Spaced Repetition Scheduler

Implementation of spaced repetition algorithm based on the Ebbinghaus forgetting curve.
This helps students retain information by scheduling reviews at optimal intervals.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List
from config.settings import SPACED_REPETITION_INTERVALS, EASE_FACTOR


class SpacedRepetitionScheduler:
    """
    Spaced repetition scheduler based on forgetting curve research.
    
    The algorithm schedules reviews at increasing intervals:
    1 day → 3 days → 7 days → 14 days → 30 days → 60 days → 120 days
    
    Performance-based adjustments:
    - High performance (≥80%): Longer intervals (1.2x)
    - Medium performance (60-79%): Standard intervals  
    - Low performance (<60%): Shorter intervals (0.7x), step back if needed
    """
    
    def __init__(self):
        self.intervals = SPACED_REPETITION_INTERVALS
        self.ease_factor = EASE_FACTOR
    
    def calculate_next_review(
        self,
        last_review: datetime,
        repetition_number: int,
        performance: float
    ) -> datetime:
        """
        Calculate when the next review should happen.
        
        Args:
            last_review: When the topic was last reviewed
            repetition_number: How many times reviewed (0 = first time)
            performance: Score from 0-1 (1 = perfect)
        
        Returns:
            datetime for the next scheduled review
        """
        # Adjust based on performance
        if performance >= 0.8:
            # Did well - can wait longer
            ease_adjustment = 1.2
        elif performance >= 0.6:
            # Decent - standard interval
            ease_adjustment = 1.0
        else:
            # Struggled - review sooner and step back
            ease_adjustment = 0.7
            repetition_number = max(0, repetition_number - 1)
        
        # Get base interval
        if repetition_number < len(self.intervals):
            base_interval = self.intervals[repetition_number]
        else:
            # Beyond preset intervals - use exponential growth
            extra_reps = repetition_number - len(self.intervals) + 1
            base_interval = self.intervals[-1] * (self.ease_factor ** extra_reps)
        
        # Apply adjustment
        adjusted_interval = base_interval * ease_adjustment
        next_review = last_review + timedelta(days=adjusted_interval)
        
        return next_review
    
    def get_due_topics(
        self,
        topics: List[Dict[str, Any]],
        current_time: datetime = None
    ) -> List[Dict[str, Any]]:
        """
        Get all topics that are due for review.
        
        Args:
            topics: List of topic dictionaries with 'next_review' field
            current_time: Current time (defaults to now)
        
        Returns:
            List of topics that need review, sorted by urgency
        """
        if current_time is None:
            current_time = datetime.now()
        
        due_now = []
        
        for topic in topics:
            next_review_str = topic.get('next_review')
            
            if next_review_str:
                next_review = datetime.fromisoformat(next_review_str)
                if next_review <= current_time:
                    due_now.append(topic)
            else:
                # Never reviewed - definitely due
                due_now.append(topic)
        
        # Sort by most overdue first
        due_now.sort(key=lambda x: x.get('next_review', current_time.isoformat()))
        
        return due_now
    
    def get_retention_estimate(self, days_since_review: int, strength: float = 1.0) -> float:
        """
        Estimate current retention based on forgetting curve.
        
        Uses simplified Ebbinghaus formula: R = e^(-t/S)
        where t = time elapsed, S = memory strength
        
        Args:
            days_since_review: Days since last review
            strength: Memory strength factor (higher = better retention)
        
        Returns:
            Estimated retention percentage (0-1)
        """
        from math import exp
        
        # Stability factor (higher = slower forgetting)
        stability = strength * 10  # Base stability of 10 days
        
        retention = exp(-days_since_review / stability)
        return max(0, min(1, retention))
