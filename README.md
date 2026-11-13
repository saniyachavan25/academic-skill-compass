# Academic & Skill Compass — Pro Edition

A student learning dashboard that combines academic progress, practical skill self-ratings,
career pathway exploration, weekly task tracking and learning resources.

## Features
- Professional dashboard styling and responsive Streamlit layout
- Editable subject marks with average, strongest/priority subject and chart
- Practical skill self-assessment chart
- Four career pathways: AI Engineer, Data Scientist, Data Analyst and Python Developer
- Indicative skill-match comparison with suggested target levels and skill gaps
- Portfolio project idea for each pathway
- Weekly task checklist with add/complete/clear actions
- Weekly progress percentage and progress bar
- SQLite persistence for weekly tasks (`compass_progress.db`)
- Subject-specific book, YouTube and practice resource links

## Setup
Open this folder in VS Code, then run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Important notes
- Default subject marks are sample values. Edit them to reflect your own results.
- Skill levels are self-assessments, not verified test scores.
- Career match percentages are simple comparisons against suggested skill levels. They are not hiring probabilities, employability guarantees or professional assessments.
- Weekly task progress is stored locally in `compass_progress.db`. Keep that file to retain progress on the same computer.
- If you move the project to another computer, copy the database file too if you want to keep your checklist.

## Suggested demo flow
1. Edit subject marks in Academic overview.
2. Change skill ratings in the sidebar.
3. Select a career in Career roadmap and discuss the skill gaps.
4. Add two tasks in Weekly progress, complete one and show the progress bar.
5. Open Learning resources and show the recommended learning sources.
