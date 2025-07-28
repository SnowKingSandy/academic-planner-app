# 🎓 Academic Calendar & Focus Planner

An interactive web application built with Streamlit to help students visualize their academic schedule, identify important deadlines, and get smart suggestions on what to focus on next.

This tool is designed to turn a simple list of events from a CSV or Excel file into a powerful, interactive, and visually appealing planning dashboard.

-----

## ✨ Core Features

  * **🗓️ Interactive Calendar View:** Displays all scheduled events on a full-page calendar with monthly, weekly, and list views. Events are color-coded by category.
  * **⬆️ File Upload:** Don't like the sample data? Upload your own schedule as a `.csv` or `.xlsx` file and the planner will instantly adapt.
  * **🔍 Dynamic Filtering:** Easily filter the displayed events by category (Exam, Project, etc.), subject, or a specific date range directly from the sidebar.
  * **🤔 Smart Focus Suggestions:** The "Suggested Focus" sidebar uses a priority algorithm to analyze upcoming events. It highlights the most pressing tasks within the next seven days based on category, duration, and keywords like "Final," "Submission," or "Marks."
  * **📋 Organized Event Lists:** View all filtered events in a clean, sortable table. Events happening today are automatically highlighted for quick visibility.
  * **⏰ TBD Task Tracking:** A separate section neatly lists all events that have been logged but do not yet have a scheduled date.

-----

## 🛠️ How to Run This Project Locally

To get this application running on your own machine, follow these simple steps.

### Prerequisites

Make sure you have Python 3.8+ installed on your system.

### 1\. Clone the Repository

First, clone this repository to your local machine.

```bash
git clone https://github.com/SnowKingSandy/academic-planner-app.git
cd academic-planner-app
```

### 2\. Install Dependencies

Install the required Python packages using the `requirements.txt` file. It's highly recommended to do this within a virtual environment.

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install packages
pip install -r requirements.txt
```

### 3\. Run the Application

Launch the Streamlit application from your terminal.

```bash
streamlit run planner_app.py
```

A new tab should automatically open in your web browser with the planner running.

-----

## 💻 Technologies Used

  * **Python:** The core programming language.
  * **Streamlit:** For building and deploying the interactive web application.
  * **Pandas:** For data manipulation and processing of the event schedules.
  * **Streamlit-Calendar:** The component used to render the interactive calendar view.
