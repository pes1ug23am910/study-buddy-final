# Video Recording Checklist

## Before Recording

### Environment Setup
- [ ] Close unnecessary apps (notifications, chat apps, email)
- [ ] Clean desktop (hide personal files/icons)
- [ ] Set terminal font size to 16-18pt (large enough to read on video)
- [ ] Dark theme enabled (easier on eyes)
- [ ] API key set in environment (NOT visible in any files)

### Test Run
- [ ] Run `python main.py` once to verify it works
- [ ] Test each demo query:
  - [ ] "Create a study plan for learning Python in 4 weeks"
  - [ ] "Explain recursion"  
  - [ ] "Quiz me on Python basics"
  - [ ] "How am I doing?"
- [ ] Check API responses are fast (< 5 seconds)

### Audio/Video Check
- [ ] Test microphone - record 10 seconds, listen back
- [ ] No background noise (fan, AC, typing from other room)
- [ ] Screen recording software ready (OBS, Loom, or built-in)
- [ ] Recording resolution set to 1080p

### Script Ready
- [ ] Script printed or on second monitor
- [ ] Practiced reading through 2-3 times
- [ ] Timed yourself (should be ~2:50)

---

## Recording Sequence

### 1. Title Slide (0:00 - 0:05)
- [ ] Create simple slide: "StudyBuddy - AI Learning Companion"
- [ ] Or use terminal with figlet/ASCII art title

### 2. Hook (0:05 - 0:20)
- [ ] Stay on title slide or show architecture
- [ ] Speak clearly, not too fast
- [ ] Hit key points: 70% forgotten, spaced repetition, AI agents

### 3. Architecture (0:20 - 1:10)
- [ ] Show architecture diagram OR
- [ ] Show VS Code with agents/ folder open
- [ ] Point out each agent as you mention it
- [ ] Explain specialization benefit

### 4. Demo - Study Plan (1:10 - 1:35)
- [ ] Terminal open, main.py running
- [ ] Type: "Create a study plan for learning Python in 4 weeks"
- [ ] Wait for response
- [ ] Point out: weekly breakdown, review schedule

### 5. Demo - Tutoring (1:35 - 1:55)
- [ ] Type: "Explain recursion with examples"
- [ ] Wait for response  
- [ ] Point out: explanation, key points, flashcards, quiz

### 6. Demo - Spaced Repetition (1:55 - 2:20)
- [ ] Type: "Quiz me on Python basics"
- [ ] Answer some questions
- [ ] Show spaced repetition update
- [ ] Type: "How am I doing?"
- [ ] Show progress summary

### 7. The Build (2:20 - 2:50)
- [ ] Switch to architecture or code view
- [ ] Mention: ADK, Gemini 2.0, loop agents, session persistence
- [ ] Mention impact: 70% better retention, 24/7, free

### 8. Outro (2:50 - 3:00)
- [ ] Back to title slide
- [ ] Mention GitHub link
- [ ] End recording

---

## After Recording

### Edit (if needed)
- [ ] Trim dead air at start/end
- [ ] Speed up slow API responses (1.25x-1.5x)
- [ ] Cut any mistakes
- [ ] Total time under 3:00

### Export
- [ ] Format: MP4
- [ ] Resolution: 1080p (minimum)
- [ ] Frame rate: 30 fps

### Upload to YouTube
- [ ] Set to **Unlisted**
- [ ] Title: "StudyBuddy - AI Learning Companion | Google ADK + Gemini 2.0"
- [ ] Description:
  ```
  Multi-agent study system with spaced repetition for better learning retention.
  
  Built for Google's 5-Day AI Agents Intensive Capstone
  Track: Agents for Good
  
  Features:
  - Personalized study planning with spaced repetition
  - Mixed-mode tutoring (explanation + flashcards + quiz)
  - Adaptive quiz system
  - Progress tracking and recommendations
  
  GitHub: https://github.com/pes1ug23am910/studybuddy-agent
  
  Built with Google Agent Development Kit and Gemini 2.0 Flash
  ```
- [ ] Add tags: AI, agents, education, spaced repetition, Gemini, Google ADK
- [ ] Copy video URL for Kaggle submission

---

## Kaggle Submission

- [ ] Video URL added to submission
- [ ] GitHub link: https://github.com/pes1ug23am910/studybuddy-agent
- [ ] KAGGLE_SUBMISSION.md content pasted
- [ ] Card image uploaded
- [ ] Track: "Agents for Good" selected
- [ ] Double-check everything before final submit

---

## Troubleshooting

### API is slow
- Wait a few seconds, Gemini sometimes has cold starts
- If very slow, re-record that section

### Terminal text too small
- Ctrl + mouse scroll to zoom
- Or change font size in terminal settings

### Audio issues
- Use headset mic if laptop mic has echo
- Record in quiet room
- Remove background noise in post (Audacity, DaVinci)

### Video too long
- Speed up API wait times in editing
- Cut any unnecessary pauses
- Speak slightly faster (but still clear)

---

## Emergency Queries (if demo fails)

If the agent gives an unexpected response, try these safe fallbacks:

1. "Help me create a study schedule for finals"
2. "Teach me about sorting algorithms"
3. "Give me a quiz on programming basics"
4. "What's my learning progress?"

These are generic enough that any reasonable response works for the demo.
