"""
Observability and Logging for StudyBuddy

Provides logging and monitoring capabilities for debugging and observability.
"""

import datetime
from typing import Any, Dict, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config.settings import USE_OBSERVABILITY

console = Console()


def log_event(
    agent_name: str,
    action: str,
    metadata: Optional[Dict[str, Any]] = None,
    level: str = "info"
) -> None:
    """
    Log an agent event with rich formatting.
    
    Args:
        agent_name: Name of the agent
        action: Description of the action
        metadata: Additional context data
        level: Log level (info, warning, error, success)
    """
    if not USE_OBSERVABILITY:
        return
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Color coding by level
    level_colors = {
        "info": "cyan",
        "warning": "yellow",
        "error": "red",
        "success": "green"
    }
    color = level_colors.get(level, "white")
    
    console.log(
        f"[{color}]{timestamp}[/] | "
        f"[bold green]{agent_name}[/] -> "
        f"[yellow]{action}[/]"
    )
    
    if metadata:
        console.log(f"  [dim]{metadata}[/]")


def log_agent_call(
    from_agent: str,
    to_agent: str,
    query: str
) -> None:
    """Log when one agent calls another."""
    if not USE_OBSERVABILITY:
        return
    
    console.log(
        f"[bold blue] Agent Call[/]: "
        f"[green]{from_agent}[/] -> [cyan]{to_agent}[/]"
    )
    console.log(f"  Query: [dim]{query[:100]}{'...' if len(query) > 100 else ''}[/]")


def log_tool_call(
    agent_name: str,
    tool_name: str,
    args: Dict[str, Any]
) -> None:
    """Log when an agent uses a tool."""
    if not USE_OBSERVABILITY:
        return
    
    console.log(
        f"[bold magenta] Tool Call[/]: "
        f"[green]{agent_name}[/] using [yellow]{tool_name}[/]"
    )
    
    # Show args (sanitized)
    safe_args = {k: str(v)[:50] + "..." if len(str(v)) > 50 else v 
                 for k, v in args.items()}
    console.log(f"  Args: [dim]{safe_args}[/]")


def log_response(
    agent_name: str,
    response_preview: str,
    tokens_used: Optional[int] = None
) -> None:
    """Log agent response."""
    if not USE_OBSERVABILITY:
        return
    
    preview = response_preview[:150] + "..." if len(response_preview) > 150 else response_preview
    
    console.log(f"[bold green]✓ Response[/] from [cyan]{agent_name}[/]:")
    console.log(f"  [dim]{preview}[/]")
    
    if tokens_used:
        console.log(f"  [dim]Tokens: {tokens_used}[/]")


def log_session_event(
    event_type: str,
    student_name: str,
    details: Optional[str] = None
) -> None:
    """Log session-related events."""
    if not USE_OBSERVABILITY:
        return
    
    emoji_map = {
        "start": "[START]",
        "end": "[END]",
        "save": "[SAVE]",
        "load": "[LOAD]",
        "error": "[FAIL]"
    }
    emoji = emoji_map.get(event_type, "")
    
    console.log(
        f"{emoji} [bold]Session {event_type}[/]: "
        f"[cyan]{student_name}[/]"
    )
    if details:
        console.log(f"  [dim]{details}[/]")


def display_progress_summary(progress_data: Dict[str, Any]) -> None:
    """Display a formatted progress summary."""
    if not USE_OBSERVABILITY:
        return
    
    table = Table(title="Learning Progress", show_header=True)
    table.add_column("Topic", style="cyan")
    table.add_column("Attempts", justify="right")
    table.add_column("Last Score", justify="right")
    table.add_column("Best Score", justify="right", style="green")
    
    for topic, stats in progress_data.items():
        table.add_row(
            topic,
            str(stats.get("attempts", 0)),
            f"{stats.get('last_score', 0):.0f}%",
            f"{stats.get('best_score', 0):.0f}%"
        )
    
    console.print(table)


def display_review_schedule(schedule: Dict[str, Any]) -> None:
    """Display formatted review schedule."""
    if not USE_OBSERVABILITY:
        return
    
    due = schedule.get("due_reviews", [])
    upcoming = schedule.get("upcoming_reviews", [])
    
    if due:
        console.print(Panel(
            "\n".join([f"[!] {r['topic']} (overdue by {r.get('overdue_days', 0)} days)" 
                      for r in due]),
            title="[red]Due for Review[/]",
            border_style="red"
        ))
    
    if upcoming:
        console.print(Panel(
            "\n".join([f"- {r['topic']} in {r['days_until']} day(s)" 
                      for r in upcoming]),
            title="[blue]Upcoming Reviews[/]",
            border_style="blue"
        ))
