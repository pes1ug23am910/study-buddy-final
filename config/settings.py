"""
StudyBuddy Configuration Settings

Central configuration for model selection, agent settings, and feature toggles.
"""

# Model Configuration
MODEL = "gemini-2.0-flash"  # Main model for all agents
EMBED_MODEL = "text-embedding-004"  # For embeddings if needed

# Feature Toggles
USE_SPACED_REPETITION = True  # Enable spaced repetition scheduling
USE_FILE_PERSISTENCE = True   # Save sessions/progress to files
USE_OBSERVABILITY = True      # Enable logging/observability

# Spaced Repetition Settings
SPACED_REPETITION_INTERVALS = [1, 3, 7, 14, 30, 60, 120]  # Days
EASE_FACTOR = 2.5  # Growth factor for intervals

# Session Settings
APP_NAME = "study_buddy_app"
DEFAULT_USER_ID = "demo_user"
DEFAULT_SESSION_ID = "demo_session"

# Output Directories
OUTPUT_DIR = "output"
STUDY_PLANS_DIR = "output/study_plans"
SESSIONS_DIR = "output/sessions"
PROGRESS_DIR = "output/progress"
SPACED_REPETITION_DIR = "output/spaced_repetition"

# Agent Settings
MAX_LOOP_ITERATIONS = 3  # For LoopAgent validation retries
