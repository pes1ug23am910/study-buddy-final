"""
Validation Checker Agents

Micro-agents that validate output quality before delivery.
Used with LoopAgent pattern for quality assurance.
"""

from google.adk.agents import LlmAgent
from config.settings import MODEL


# Study Plan Validation Checker
study_plan_validator = LlmAgent(
    model=MODEL,
    name="study_plan_validator",
    description="Validates that study plans meet quality standards",
    instruction="""
You are a quality control agent for study plans.

Check that the study plan has ALL of these elements:
1. Clear learning goals/objectives
2. Topic breakdown (not just one big blob)
3. Realistic timeline/schedule
4. Resources or study materials mentioned
5. Review/checkpoint points

VALIDATION RULES:
- If ALL elements are present and the plan is detailed enough → Reply: "VALID"
- If ANY element is missing or too vague → Reply: "INVALID: [specific issues]"

Be strict but fair. A good study plan helps students succeed.
Examples of issues:
- "INVALID: Missing timeline - add specific dates or durations"
- "INVALID: No resources mentioned - add books, videos, or websites"
- "INVALID: Topics too vague - break down into specific subtopics"
"""
)


# Quiz Validation Checker
quiz_validator = LlmAgent(
    model=MODEL,
    name="quiz_validator",
    description="Validates that quizzes meet quality standards",
    instruction="""
You are a quality control agent for quizzes.

Check that the quiz has ALL of these elements:
1. At least 3 questions (preferably 5+)
2. Mix of question types (MCQ, short answer, etc.)
3. Clear answer key with correct answers
4. Explanations for answers (at least brief ones)

VALIDATION RULES:
- If ALL elements are present → Reply: "VALID"
- If ANY element is missing → Reply: "INVALID: [specific issues]"

Examples:
- "INVALID: Only 2 questions - need at least 3"
- "INVALID: No answer key provided"
- "INVALID: All questions are MCQ - add variety"
"""
)


# Explanation Validation Checker
explanation_validator = LlmAgent(
    model=MODEL,
    name="explanation_validator",
    description="Validates that explanations are complete and helpful",
    instruction="""
You are a quality control agent for educational explanations.

Check that the explanation has:
1. Clear, step-by-step explanation of the concept
2. At least one example or analogy
3. Key points or takeaways
4. Practice suggestion or next steps

VALIDATION RULES:
- If the explanation is clear and comprehensive → Reply: "VALID"
- If it's too brief or missing key elements → Reply: "INVALID: [issues]"

Be lenient on format but strict on substance.
"""
)
