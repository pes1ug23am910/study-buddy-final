# StudyBuddy Architecture Diagram

## Mermaid Diagram (renders on GitHub)

```mermaid
flowchart LR
    subgraph main["study_buddy_agent (Orchestrator)"]
        SB[("study_buddy")]
    end
    
    subgraph planner_loop["robust_study_planner (Loop Agent)"]
        LP[("learning_planner")]
        SPV[("study_plan_validator")]
        LP <--> SPV
    end
    
    subgraph tutor_section["Tutor"]
        TA[("tutor_agent")]
        GS1{{"google_search"}}
        TA --> GS1
    end
    
    subgraph quiz_loop["robust_quiz_agent (Loop Agent)"]
        QA[("quiz_agent")]
        QV[("quiz_validator")]
        QA <--> QV
        RQR{{"record_quiz_result"}}
        USR{{"update_spaced_rep"}}
        QA --> RQR
        QA --> USR
    end
    
    subgraph progress_section["Progress Tracker"]
        PT[("progress_tracker")]
        GPS{{"get_progress_summary"}}
        GRS{{"get_review_schedule"}}
        PT --> GPS
        PT --> GRS
    end
    
    subgraph tools["Tools"]
        SSP{{"save_study_plan"}}
        SN{{"save_notes"}}
    end
    
    SB --> planner_loop
    SB --> tutor_section
    SB --> quiz_loop
    SB --> progress_section
    SB --> tools
```

## Text Diagram (for draw.io or similar)

```
                    ┌─────────────────────────────────────────────────────────┐
                    │           robust_study_planner (Loop Agent)             │
                    │  ┌─────────────────┐      ┌──────────────────────────┐  │
                    │  │ learning_planner │◄────►│ study_plan_validator     │  │
                    │  └─────────────────┘      └──────────────────────────┘  │
                    └─────────────────────────────────────────────────────────┘
                                              ▲
                                              │
                    ┌─────────────────────────────────────────────────────────┐
                    │                    tutor_agent                          │
                    │  ┌─────────────────┐      ┌──────────────────────────┐  │
                    │  │   tutor_agent   │─────►│     google_search        │  │
                    │  └─────────────────┘      └──────────────────────────┘  │
                    └─────────────────────────────────────────────────────────┘
                                              ▲
                                              │
┌──────────────────────┐                      │
│                      │──────────────────────┤
│  study_buddy_agent   │                      │
│    (Orchestrator)    │──────────────────────┤
│                      │                      │
└──────────────────────┘                      │
          │                                   ▼
          │           ┌─────────────────────────────────────────────────────────┐
          │           │             robust_quiz_agent (Loop Agent)              │
          │           │  ┌─────────────────┐      ┌──────────────────────────┐  │
          │           │  │   quiz_agent    │◄────►│    quiz_validator        │  │
          │           │  └────────┬────────┘      └──────────────────────────┘  │
          │           │           │                                             │
          │           │           ├──► record_quiz_result                       │
          │           │           └──► update_spaced_repetition                 │
          │           └─────────────────────────────────────────────────────────┘
          │
          │           ┌─────────────────────────────────────────────────────────┐
          │           │                  progress_tracker                       │
          │           │  ┌─────────────────┐                                    │
          └──────────►│  │progress_tracker │──► get_progress_summary            │
                      │  └─────────────────┘──► get_review_schedule             │
                      └─────────────────────────────────────────────────────────┘
          │
          │           ┌─────────────────────────────────────────────────────────┐
          └──────────►│                      Tools                              │
                      │     save_study_plan_to_file    save_notes_to_file       │
                      └─────────────────────────────────────────────────────────┘
```

## Simple Version (like the example image)

To recreate in draw.io or similar tool:

1. **Main Node (Green oval):** `study_buddy_agent` (Orchestrator)

2. **Loop Agent Box 1:** `robust_study_planner (Loop Agent)`
   - Contains: `learning_planner` ◄──► `study_plan_validator`

3. **Tutor Node:** `tutor_agent`
   - Connected to: `google_search` (tool)

4. **Loop Agent Box 2:** `robust_quiz_agent (Loop Agent)`  
   - Contains: `quiz_agent` ◄──► `quiz_validator`
   - Tools: `record_quiz_result`, `update_spaced_rep`

5. **Progress Node:** `progress_tracker`
   - Tools: `get_progress_summary`, `get_review_schedule`

6. **Tool Nodes:**
   - `save_study_plan_to_file`
   - `save_notes_to_file`

## Color Scheme Suggestion

- **Orchestrator:** Green (like the example)
- **Agents:** White/light gray ovals with robot icon
- **Tools:** White ovals with wrench icon
- **Loop Agent boxes:** Rounded rectangle borders
- **Background:** Dark gray (#2d2d2d)
