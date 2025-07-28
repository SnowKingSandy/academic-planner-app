import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# Import the calendar component. This must be installed: pip install streamlit-calendar
from streamlit_calendar import calendar

# --- Page Configuration ---
st.set_page_config(
    page_title="Academic Calendar Planner",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Initial Data ---
# Hardcoded data as a fallback if no file is uploaded.
# Note: pd.NaT cannot be directly represented here, so we'll use None and handle it later.
initial_event_data = [
    {'Subject': 'Hackathon', 'Title': 'Bajaj Finserv HackRx6.0', 'Category': 'Competition', 'Start Date': '2025-07-10', 'End Date': '2025-08-08', 'Notes': 'Pitch Deck Submission'},
    {'Subject': 'Ideathon', 'Title': 'AI4Youth: Registration Deadline', 'Category': 'Deadline', 'Start Date': '2025-08-01', 'End Date': '2025-08-01', 'Notes': 'Final day to register'},
    {'Subject': 'DSA', 'Title': 'CA1: MCQ Test', 'Category': 'Exam', 'Start Date': '2025-08-01', 'End Date': '2025-08-01', 'Notes': '10 Marks'},
    {'Subject': 'OS', 'Title': 'CA1: MCQ Quiz', 'Category': 'Exam', 'Start Date': '2025-08-04', 'End Date': '2025-08-08', 'Notes': '15 Marks (1st Week)'},
    {'Subject': 'PRP', 'Title': 'CA1: Quiz', 'Category': 'Exam', 'Start Date': '2025-08-04', 'End Date': '2025-08-08', 'Notes': '7 Marks (1st Week)'},
    {'Subject': 'Ideathon', 'Title': 'AI4Youth: Final Submission', 'Category': 'Competition', 'Start Date': '2025-08-12', 'End Date': '2025-08-12', 'Notes': 'Slides + Video Pitch'},
    {'Subject': 'DPEL', 'Title': 'Project: Phase 1', 'Category': 'Project', 'Start Date': '2025-08-26', 'End Date': '2025-08-30', 'Notes': '10 Marks'},
    {'Subject': 'DT', 'Title': 'CA1: MCQ', 'Category': 'Exam', 'Start Date': '2025-09-01', 'End Date': '2025-09-01', 'Notes': '20 Marks'},
    {'Subject': 'DCDSL', 'Title': 'Project: Phase 1', 'Category': 'Project', 'Start Date': '2025-09-01', 'End Date': '2025-09-05', 'Notes': '15 Marks'},
    {'Subject': 'DSA', 'Title': 'CA2: Mid-Term Test', 'Category': 'Exam', 'Start Date': '2025-09-08', 'End Date': '2025-09-13', 'Notes': '20 Marks (Mid-Term Week)'},
    {'Subject': 'DCDS', 'Title': 'CA1: Mid-Term Test', 'Category': 'Exam', 'Start Date': '2025-09-08', 'End Date': '2025-09-13', 'Notes': '10 Marks (Mid-Term Week)'},
    {'Subject': 'PRP', 'Title': 'CA2: Mid-Term Exam', 'Category': 'Exam', 'Start Date': '2025-09-08', 'End Date': '2025-09-13', 'Notes': '(Mid-Term Week)'},
    {'Subject': 'Competition', 'Title': 'CodeVita: Registration Deadline', 'Category': 'Deadline', 'Start Date': '2025-09-18', 'End Date': '2025-09-18', 'Notes': 'Final day to register'},
    {'Subject': 'DCDS', 'Title': 'CA2: HackerRank MongoDB', 'Category': 'Project', 'Start Date': '2025-10-01', 'End Date': '2025-10-31', 'Notes': '5 Marks each (Full Month)'},
    {'Subject': 'OS', 'Title': 'CA2: Case Study', 'Category': 'Exam', 'Start Date': '2025-10-13', 'End Date': '2025-10-17', 'Notes': '30 Marks (2nd Week)'},
    {'Subject': 'DSA', 'Title': 'CA3: Case Studies', 'Category': 'Exam', 'Start Date': '2025-10-27', 'End Date': '2025-10-31', 'Notes': '15 Marks (Last Week)'},
    {'Subject': 'PRP', 'Title': 'CA3: Mind Map and Viva', 'Category': 'Project', 'Start Date': '2025-10-27', 'End Date': '2025-10-31', 'Notes': '13 Marks (Last Week)'},
    {'Subject': 'DCDSL', 'Title': 'Quiz', 'Category': 'Exam', 'Start Date': '2025-10-28', 'End Date': '2025-10-31', 'Notes': '5 Marks'},
    {'Subject': 'DPEL', 'Title': 'Project: Final Submission', 'Category': 'Project', 'Start Date': '2025-11-03', 'End Date': '2025-11-08', 'Notes': '30 Marks (ESE Project Week)'},
    {'Subject': 'DCDSL', 'Title': 'Final Project', 'Category': 'Project', 'Start Date': '2025-11-03', 'End Date': '2025-11-08', 'Notes': '10 Marks (ESE Project Week)'},
    {'Subject': 'OS', 'Title': 'CA3: Swayam Course', 'Category': 'Project', 'Start Date': '2025-11-03', 'End Date': '2025-11-08', 'Notes': '30 Marks (ESE Project Week)'},
    {'Subject': 'DT', 'Title': 'CA2: Project + Viva', 'Category': 'Project', 'Start Date': '2025-11-11', 'End Date': '2025-11-11', 'Notes': '30 Marks'},
    {'Subject': 'OSL', 'Title': 'CA2: Lab Exam', 'Category': 'Exam', 'Start Date': '2025-11-11', 'End Date': '2025-11-17', 'Notes': '15 Marks (Practical Week)'},
    {'Subject': 'FOE', 'Title': 'CA1: Essay Writing', 'Category': 'Exam', 'Start Date': None, 'End Date': None, 'Notes': '15 Marks (Arbitrary Date)'},
    {'Subject': 'FOE', 'Title': 'CA2: MCQ', 'Category': 'Exam', 'Start Date': None, 'End Date': None, 'Notes': '10 Marks (Arbitrary Date)'},
]

# --- Helper Functions ---

@st.cache_data
def load_data(uploaded_file):
    """
    Loads data from an uploaded file (CSV or Excel) or uses the initial hardcoded data.
    It standardizes column names and converts date columns to datetime objects.
    """
    if uploaded_file is not None:
        try:
            # To read the file in memory, we use io.BytesIO
            bytes_data = uploaded_file.getvalue()
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(bytes_data))
            elif uploaded_file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(io.BytesIO(bytes_data))
            else:
                st.error("Unsupported file format. Please upload a CSV or Excel file.")
                return pd.DataFrame(initial_event_data)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return pd.DataFrame(initial_event_data)
    else:
        df = pd.DataFrame(initial_event_data)

    # Standardize date columns
    df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
    df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')
    
    # Ensure 'Notes' column is string type to prevent errors
    df['Notes'] = df['Notes'].astype(str).fillna('')

    return df

def calculate_priority(row):
    """
    Calculates a priority score for an event based on category, duration, and keywords in notes.
    """
    # 1. Base priority from Category
    category_priority = {
        'Exam': 40,
        'Project': 30,
        'Competition': 20,
        'Deadline': 25  # Deadlines are often critical
    }
    score = category_priority.get(row['Category'], 10)

    # 2. Duration bonus
    if pd.notna(row['Start Date']) and pd.notna(row['End Date']):
        duration = (row['End Date'] - row['Start Date']).days
        score += duration * 2 # Add 2 points for each day of duration

    # 3. Keyword bonus from Notes
    keyword_bonuses = {
        'final': 30,
        'submission': 25,
        'marks': 10,
        'high weightage': 20,
        'viva': 15,
        'ese': 20,
        'mid-term': 15
    }
    notes_lower = row['Notes'].lower()
    for keyword, bonus in keyword_bonuses.items():
        if keyword in notes_lower:
            score += bonus
            
    # Bonus for high marks mentioned
    try:
        # Extract numbers from notes
        numbers = [int(s) for s in notes_lower.split() if s.isdigit()]
        if numbers:
            marks = max(numbers)
            if marks >= 20:
                score += 15
            elif marks >= 10:
                score += 10
    except:
        pass # Ignore if no numbers found

    return score

# --- Main App ---

# --- Sidebar ---
with st.sidebar:
    st.header("🗓️ Planner Controls")
    
    uploaded_file = st.file_uploader(
        "Upload Your Events (CSV or Excel)",
        type=['csv', 'xlsx']
    )
    
    if uploaded_file:
        st.success("File uploaded successfully!")
    else:
        st.info("Showing default sample data. Upload a file to see your own events.")

    # Load and process data
    df = load_data(uploaded_file)

    # Separate TBD events
    tbd_events = df[df['Start Date'].isna()].copy()
    scheduled_events = df.dropna(subset=['Start Date']).copy()
    
    # Sort by start date
    scheduled_events = scheduled_events.sort_values(by='Start Date').reset_index(drop=True)

    # --- Filters ---
    st.header("🔍 Filters")
    
    # Filter by Category
    all_categories = scheduled_events['Category'].unique().tolist()
    selected_categories = st.multiselect(
        "Filter by Category",
        options=all_categories,
        default=all_categories
    )

    # Filter by Subject
    all_subjects = scheduled_events['Subject'].unique().tolist()
    selected_subjects = st.multiselect(
        "Filter by Subject",
        options=all_subjects,
        default=all_subjects
    )

    # Filter by Date Range
    min_date = scheduled_events['Start Date'].min().date() if not scheduled_events.empty else datetime.today().date()
    max_date = scheduled_events['End Date'].max().date() if not scheduled_events.empty else datetime.today().date() + timedelta(days=365)

    selected_date_range = st.date_input(
        "Filter by Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key='date_range_picker'
    )
    
    # Apply filters
    if len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
        # Convert to datetime for comparison
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)
        
        filtered_df = scheduled_events[
            (scheduled_events['Category'].isin(selected_categories)) &
            (scheduled_events['Subject'].isin(selected_subjects)) &
            (scheduled_events['Start Date'] <= end_datetime) &
            (scheduled_events['End Date'] >= start_datetime)
        ]
    else:
        # Default to all if date range is not set properly
        filtered_df = scheduled_events[
            (scheduled_events['Category'].isin(selected_categories)) &
            (scheduled_events['Subject'].isin(selected_subjects))
        ]


    # --- Suggested Focus Section ---
    st.header("🤔 Suggested Focus")
    
    today = pd.to_datetime(datetime.today().date())
    
    # Find events happening now or in the next 7 days
    upcoming_window = today + timedelta(days=7)
    active_events = scheduled_events[
        (scheduled_events['Start Date'] <= upcoming_window) & (scheduled_events['End Date'] >= today)
    ].copy()

    if not active_events.empty:
        active_events['priority'] = active_events.apply(calculate_priority, axis=1)
        focus_suggestions = active_events.sort_values(by='priority', ascending=False).head(5)

        for _, row in focus_suggestions.iterrows():
            emoji_map = {'Exam': '🔥', 'Project': '🛠️', 'Competition': '🏆', 'Deadline': '❗'}
            emoji = emoji_map.get(row['Category'], '⭐')
            
            # Calculate days remaining
            days_left = (row['End Date'] - today).days
            if days_left < 0:
                status = " (Ended)"
            elif days_left == 0:
                status = " (Ends Today!)"
            else:
                status = f" (Ends in {days_left} days)"

            with st.container(border=True):
                st.markdown(f"**{emoji} {row['Subject']}: {row['Title']}**")
                st.markdown(f"*{row['Category']}*{status}")
                if pd.notna(row['Notes']):
                    st.caption(f"Notes: {row['Notes']}")

    else:
        st.info("No pressing events in the next 7 days. Time to relax or plan ahead!")


# --- Main Content Area ---
st.title("🎓 Academic Calendar & Focus Planner")
st.markdown("Visualize your schedule, identify overlaps, and get smart suggestions on what to focus on.")

# --- Calendar View ---
st.header("📅 Calendar View")

# Define colors for categories
category_colors = {
    'Exam': '#FF6B6B',       # Red
    'Project': '#4ECDC4',     # Teal
    'Competition': '#45B7D1',  # Blue
    'Deadline': '#FFA07A'      # Light Salmon
}

# Format events for the calendar component
calendar_events = []
for _, event in filtered_df.iterrows():
    # For the calendar, the end date is exclusive. Add one day.
    end_date_exclusive = (event['End Date'] + timedelta(days=1)).strftime('%Y-%m-%d')
    
    calendar_events.append({
        "title": f"{event['Subject']}: {event['Title']}",
        "color": category_colors.get(event['Category'], '#808080'), # Default to gray
        "start": event['Start Date'].strftime('%Y-%m-%d'),
        "end": end_date_exclusive,
        "resourceId": event['Category'], # For potential future resource views
    })

# Display the calendar
calendar_instance = calendar(
    events=calendar_events,
    options={
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,listWeek",
        },
        "initialView": "dayGridMonth",
        "resourceGroupField": "Category",
    },
    custom_css="""
    .fc-event-past {
        opacity: 0.7;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 500;
    }
    .fc-list-event-dot {
        border-color: var(--fc-event-border-color, #808080) !important;
    }
    """,
)


# --- List Views ---
st.header("📋 Event Lists")

# Use columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    # --- Scheduled Events List ---
    with st.expander("All Scheduled & Filtered Events", expanded=True):
        if not filtered_df.empty:
            # Highlight events happening today
            def highlight_today(row):
                style = ''
                if row['Start Date'] <= today <= row['End Date']:
                    style = 'background-color: #FFFACD;' # LemonChiffon
                return [style] * len(row)

            st.dataframe(
                filtered_df[['Subject', 'Title', 'Category', 'Start Date', 'End Date', 'Notes']].style.apply(highlight_today, axis=1),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Start Date": st.column_config.DateColumn("Start", format="YYYY-MM-DD"),
                    "End Date": st.column_config.DateColumn("End", format="YYYY-MM-DD"),
                }
            )
            
            # --- Export to CSV ---
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
               label="📥 Download Filtered View as CSV",
               data=csv,
               file_name='filtered_events.csv',
               mime='text/csv',
            )

        else:
            st.warning("No events match the current filter settings.")

with col2:
    # --- To Be Scheduled Events ---
    with st.expander("⏰ To Be Scheduled (TBD)"):
        if not tbd_events.empty:
            st.dataframe(
                tbd_events[['Subject', 'Title', 'Category', 'Notes']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No 'To Be Scheduled' events found.")
