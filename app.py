import sqlite3
from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Academic & Skill Compass — student learning and career planning dashboard
# Local progress is saved in a small SQLite database beside this app.

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "compass_progress.db"

st.set_page_config(
    page_title="Academic & Skill Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- Styling --------------------
st.markdown("""
<style>
    .stApp { background: #f5f7fb; }
    [data-testid="stHeader"] { background: rgba(245,247,251,0.9); }
    .block-container { padding-top: 1.7rem; padding-bottom: 3rem; max-width: 1250px; }
    .hero {
        padding: 1.6rem 1.8rem; border-radius: 18px;
        background: linear-gradient(115deg, #14213d 0%, #244b73 58%, #367b86 100%);
        color: white; margin-bottom: 1.2rem;
    }
    .hero h1 { color: white; font-size: 2.15rem; margin: 0 0 .3rem 0; }
    .hero p { color: #e6f0f7; margin: 0; font-size: 1rem; }
    .section-note { color: #64748b; font-size: .92rem; }
    div[data-testid="stMetric"] {
        background: white; border: 1px solid #e7ebf2;
        padding: 14px 16px; border-radius: 14px;
        box-shadow: 0 2px 8px rgba(20,33,61,.04);
    }
    div[data-testid="stTabs"] button { font-weight: 600; }
    .small-label { color: #64748b; font-size: .82rem; text-transform: uppercase; letter-spacing: .04em; }
    .resource-card {
        background: white; border: 1px solid #e7ebf2; padding: 1rem 1.1rem;
        border-radius: 13px; margin-bottom: .7rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- Local database --------------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_start TEXT NOT NULL,
                task TEXT NOT NULL,
                category TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                UNIQUE(week_start, task)
            )
        """)

def load_tasks(week_start):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            "SELECT id, task, category, completed FROM tasks WHERE week_start=? ORDER BY id",
            conn, params=(week_start,)
        )

def save_task(week_start, task, category):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO tasks (week_start, task, category, completed) VALUES (?, ?, ?, 0)",
            (week_start, task, category)
        )

def update_task(task_id, completed):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE tasks SET completed=? WHERE id=?", (int(completed), int(task_id)))

def delete_week_tasks(week_start):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM tasks WHERE week_start=?", (week_start,))

init_db()

# -------------------- Reference data --------------------
SUBJECT_DEFAULTS = {
    "Python Programming": 68, "Mathematics": 62, "Data Structures": 55,
    "DBMS": 72, "Statistics": 60, "Computer Networks": 70,
    "AI & Machine Learning": 58,
}
SKILL_DEFAULTS = {
    "Python": 3, "SQL": 2, "Problem solving": 3, "Statistics": 2,
    "Data visualization": 2, "Git & GitHub": 1, "Communication": 3,
    "Teamwork": 4,
}
ROLE_SKILLS = {
    "AI Engineer": {
        "Python": 5, "Mathematics": 4, "Machine Learning": 4,
        "Deep Learning": 3, "SQL": 3, "Git & GitHub": 3,
    },
    "Data Scientist": {
        "Python": 4, "Statistics": 5, "SQL": 4,
        "Data visualization": 4, "Machine Learning": 4, "Communication": 3,
    },
    "Data Analyst": {
        "SQL": 5, "Excel": 4, "Statistics": 4,
        "Data visualization": 5, "Python": 3, "Communication": 4,
    },
    "Python Developer": {
        "Python": 5, "Problem solving": 4, "SQL": 3,
        "Git & GitHub": 4, "APIs": 3, "Testing": 3,
    },
}
ROLE_DESCRIPTIONS = {
    "AI Engineer": "Builds AI-powered applications and works with machine-learning or deep-learning systems.",
    "Data Scientist": "Uses statistics, programming and machine learning to find patterns and support decisions.",
    "Data Analyst": "Turns data into useful reports, dashboards and business insights.",
    "Python Developer": "Builds applications, scripts, APIs and backend services using Python.",
}
ROLE_PROJECTS = {
    "AI Engineer": "Image classifier or FAQ assistant using a small, clearly documented dataset.",
    "Data Scientist": "Exploratory analysis and a prediction experiment with model evaluation.",
    "Data Analyst": "Sales or student-performance dashboard with SQL queries and clear insights.",
    "Python Developer": "Task manager or expense tracker with file/database storage and tests.",
}
RESOURCE_GUIDE = {
    "Python Programming": [
        ("Book", "Automate the Boring Stuff with Python", "https://automatetheboringstuff.com/"),
        ("YouTube", "Corey Schafer", "https://www.youtube.com/@coreyms"),
        ("Practice", "Kaggle Learn: Python", "https://www.kaggle.com/learn/python"),
    ],
    "Data Structures": [
        ("Book", "Open Data Structures", "https://opendatastructures.org/"),
        ("YouTube", "Abdul Bari", "https://www.youtube.com/@abdul_bari"),
        ("Practice", "VisuAlgo", "https://visualgo.net/en"),
    ],
    "DBMS": [
        ("Book", "Database System Concepts", "https://db-book.com/"),
        ("YouTube", "Neso Academy", "https://www.youtube.com/@nesoacademy"),
        ("Practice", "SQLBolt", "https://sqlbolt.com/"),
    ],
    "Statistics": [
        ("Book", "OpenIntro Statistics", "https://www.openintro.org/book/os/"),
        ("YouTube", "StatQuest", "https://www.youtube.com/@statquest"),
        ("Practice", "Kaggle Learn", "https://www.kaggle.com/learn"),
    ],
    "Mathematics": [
        ("Learning", "Khan Academy", "https://www.khanacademy.org/math"),
        ("YouTube", "3Blue1Brown", "https://www.youtube.com/@3blue1brown"),
        ("Practice", "Khan Academy exercises", "https://www.khanacademy.org/math"),
    ],
    "Computer Networks": [
        ("Book", "Computer Networking: A Top-Down Approach", "https://gaia.cs.umass.edu/kurose_ross/"),
        ("YouTube", "Neso Academy", "https://www.youtube.com/@nesoacademy"),
        ("Practice", "Cisco Skills for All", "https://skillsforall.com/"),
    ],
    "AI & Machine Learning": [
        ("Book", "An Introduction to Statistical Learning", "https://www.statlearning.com/"),
        ("YouTube", "StatQuest", "https://www.youtube.com/@statquest"),
        ("Practice", "Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course"),
    ],
}

# -------------------- Sidebar profile --------------------
st.sidebar.markdown("## Your learning profile")
student_name = st.sidebar.text_input("Name", "Student")
st.sidebar.caption("Edit your current self-ratings. Be honest; these are not formal test scores.")
skill_ratings = {}
for skill, default in SKILL_DEFAULTS.items():
    skill_ratings[skill] = st.sidebar.slider(skill, 1, 5, default)
st.sidebar.markdown("---")
st.sidebar.caption("Progress checklists are saved locally in compass_progress.db.")

# -------------------- Header and overview --------------------
st.markdown("""
<div class="hero">
  <h1>🧭 Academic &amp; Skill Compass</h1>
  <p>Understand your academic progress, build practical skills and plan your next career step.</p>
</div>
""", unsafe_allow_html=True)

st.write(f"Welcome back, **{student_name}**. Use the tabs below to plan, practise and track your progress.")

tab_overview, tab_career, tab_progress, tab_resources = st.tabs([
    "📊 Academic overview", "🚀 Career roadmap", "✅ Weekly progress", "📚 Learning resources"
])

# -------------------- Academic overview --------------------
with tab_overview:
    st.subheader("Subject-wise progress")
    st.caption("The starting marks are sample values. Edit them to reflect your own results.")
    subjects_df = pd.DataFrame(
        [{"Subject": subject, "Marks (%)": marks} for subject, marks in SUBJECT_DEFAULTS.items()]
    )
    edited = st.data_editor(
        subjects_df, num_rows="dynamic", use_container_width=True,
        column_config={
            "Subject": st.column_config.TextColumn(required=True),
            "Marks (%)": st.column_config.NumberColumn(min_value=0, max_value=100, step=1, required=True),
        },
        key="subject_marks_editor",
    )
    edited["Marks (%)"] = pd.to_numeric(edited["Marks (%)"], errors="coerce")
    clean = edited.dropna(subset=["Subject", "Marks (%)"]).copy()
    clean["Marks (%)"] = clean["Marks (%)"].clip(0, 100)
    if not clean.empty:
        avg = clean["Marks (%)"].mean()
        best = clean.loc[clean["Marks (%)"].idxmax()]
        priority = clean.loc[clean["Marks (%)"].idxmin()]
        c1, c2, c3 = st.columns(3)
        c1.metric("Average marks", f"{avg:.1f}%")
        c2.metric("Strongest subject", str(best["Subject"]))
        c3.metric("Focus subject", str(priority["Subject"]))
        fig, ax = plt.subplots(figsize=(9, 4))
        chart = clean.sort_values("Marks (%)")
        ax.barh(chart["Subject"], chart["Marks (%)"])
        ax.set_xlim(0, 100)
        ax.set_xlabel("Marks (%)")
        ax.set_title("Subject progress")
        ax.grid(axis="x", alpha=.2)
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Practical skill snapshot")
    skill_df = pd.DataFrame([{"Skill": k, "Level": v} for k, v in skill_ratings.items()])
    fig, ax = plt.subplots(figsize=(9, 3.6))
    chart = skill_df.sort_values("Level")
    ax.barh(chart["Skill"], chart["Level"])
    ax.set_xlim(0, 5)
    ax.set_xlabel("Self-rating (1 = beginner, 5 = confident)")
    ax.set_title("Current skill map")
    ax.grid(axis="x", alpha=.2)
    st.pyplot(fig)
    plt.close(fig)

    st.info("Tip: Update your marks and skill ratings as you learn. These visuals are planning aids, not formal academic assessments.")

# -------------------- Career roadmap --------------------
with tab_career:
    st.subheader("Explore a career pathway")
    role = st.selectbox("Choose a role to explore", list(ROLE_SKILLS.keys()))
    st.write(ROLE_DESCRIPTIONS[role])
    required = ROLE_SKILLS[role]
    # Map related subjects to skill estimates only where reasonable; otherwise ask for self-rating.
    extra_defaults = {"Mathematics": 3, "Machine Learning": 2, "Deep Learning": 1,
                      "Excel": 2, "APIs": 1, "Testing": 1}
    current = {**skill_ratings}
    for skill in required:
        if skill not in current:
            current[skill] = extra_defaults.get(skill, 2)

    rows = []
    for skill, target in required.items():
        level = current.get(skill, 2)
        gap = max(0, target - level)
        rows.append({
            "Skill": skill,
            "Your level": level,
            "Suggested target": target,
            "Gap": gap,
            "Priority": "High" if gap >= 3 else ("Medium" if gap >= 1 else "Maintain"),
        })
    roadmap_df = pd.DataFrame(rows).sort_values(["Gap", "Skill"], ascending=[False, True])
    readiness = sum(min(current.get(s, 2), target) for s, target in required.items()) / sum(required.values()) * 100
    r1, r2 = st.columns([1, 2])
    r1.metric("Indicative skill match", f"{readiness:.0f}%")
    r2.caption("This is a simple comparison of your self-ratings with suggested skill levels. It is not a hiring probability or employability score.")
    st.dataframe(roadmap_df, use_container_width=True, hide_index=True)

    biggest_gaps = roadmap_df[roadmap_df["Gap"] > 0].head(3)
    st.markdown("#### Suggested next steps")
    if biggest_gaps.empty:
        st.success("Your current self-ratings meet the suggested levels for this pathway. Build deeper projects and keep practising.")
    else:
        for _, row in biggest_gaps.iterrows():
            st.write(f"- **{row['Skill']}** — move from level {row['Your level']} towards level {row['Suggested target']}. Make this a learning priority.")

    st.markdown("#### Portfolio project to try")
    st.success(ROLE_PROJECTS[role])
    st.caption("Choose one small project, document your contribution and explain what you learned. A completed, understandable project is more valuable than a long list of unfinished tools.")

# -------------------- Weekly progress tracking --------------------
with tab_progress:
    st.subheader("Your weekly learning tracker")
    today = date.today()
    week_start_date = today - timedelta(days=today.weekday())
    week_start = week_start_date.isoformat()
    st.caption(f"Week starting {week_start_date.strftime('%d %b %Y')}. Your checklist is saved locally on this computer.")

    with st.form("add_task_form", clear_on_submit=True):
        task_text = st.text_input("Add a learning task", placeholder="e.g. Complete 5 SQL JOIN exercises")
        category = st.selectbox("Category", ["Subject study", "Technical skill", "Project", "Career preparation"])
        add_clicked = st.form_submit_button("Add task")
    if add_clicked:
        if task_text.strip():
            save_task(week_start, task_text.strip(), category)
            st.success("Task added to this week's plan.")
            st.rerun()
        else:
            st.warning("Enter a task before adding it.")

    tasks = load_tasks(week_start)
    if tasks.empty:
        st.info("Your checklist is empty. Add 2–3 realistic tasks to get started.")
    else:
        total = len(tasks)
        done = int(tasks["completed"].sum())
        percent = int(done / total * 100)
        m1, m2, m3 = st.columns(3)
        m1.metric("Tasks this week", total)
        m2.metric("Completed", done)
        m3.metric("Weekly progress", f"{percent}%")
        st.progress(percent / 100)

        st.markdown("#### Update your tasks")
        for _, row in tasks.iterrows():
            left, middle, right = st.columns([0.12, 0.66, 0.22])
            checked = left.checkbox(
                "Done", value=bool(row["completed"]),
                key=f"task_{int(row['id'])}", label_visibility="collapsed"
            )
            middle.write(f"**{row['task']}**")
            right.caption(row["category"])
            if checked != bool(row["completed"]):
                update_task(row["id"], checked)
                st.rerun()

        if st.button("Clear this week's checklist", type="secondary"):
            delete_week_tasks(week_start)
            st.rerun()

        if percent == 100:
            st.balloons()
            st.success("Great work — you've completed every task in this week's checklist!")

    st.caption("Note: Progress is stored in a local SQLite file beside app.py. Keep compass_progress.db if you want to retain your checklist between app restarts.")

# -------------------- Learning resources --------------------
with tab_resources:
    st.subheader("Books, videos and practice platforms")
    subject = st.selectbox("Choose a subject", list(RESOURCE_GUIDE.keys()))
    for kind, label, url in RESOURCE_GUIDE[subject]:
        st.markdown(f'<div class="resource-card"><span class="small-label">{kind}</span><br><a href="{url}" target="_blank">{label}</a></div>', unsafe_allow_html=True)
    st.markdown("#### A simple 7-day study rhythm")
    weekly_rhythm = [
        "Day 1: Review one concept and write short notes.",
        "Day 2: Watch one focused lesson and reproduce the example.",
        "Day 3: Practise 5–10 questions or exercises.",
        "Day 4: Work through one harder example without copying.",
        "Day 5: Apply the concept to a tiny practical task.",
        "Day 6: Review mistakes and improve your task.",
        "Day 7: Explain what you learned and add the result to your portfolio.",
    ]
    for item in weekly_rhythm:
        st.write("• " + item)

st.divider()
st.caption("Academic & Skill Compass | Built with Python, Streamlit, Pandas, Matplotlib and SQLite")
