import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        margin-top: 0.2rem;
        margin-bottom: 0.5rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid #e5e7eb;
        padding: 10px;
        border-radius: 12px;
        background: #ffffff;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    .app-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .app-subtitle {
        color: #6b7280;
        margin-top: -6px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GRADE FUNCTION
# ============================================================

def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"


# ============================================================
# SESSION STATE
# ============================================================

if "students" not in st.session_state:
    st.session_state.students = []


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">🎓 Student Grade Manager</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'Manage student marks and class performance from one screen.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TOP LAYOUT
# ============================================================

left_col, right_col = st.columns(
    [1, 2.2],
    gap="large"
)


# ============================================================
# LEFT SIDE - ADD STUDENT
# ============================================================

with left_col:

    st.subheader("➕ Add Student")

    with st.form("student_form"):

        name = st.text_input(
            "Student Name",
            placeholder="Enter name"
        )

        mark = st.number_input(
            "Mark",
            min_value=0,
            max_value=100,
            step=1
        )

        submitted = st.form_submit_button(
            "Add Student",
            use_container_width=True
        )

    if submitted:

        clean_name = name.strip()

        if not clean_name:

            st.warning(
                "Please enter a student name."
            )

        else:

            duplicate = any(
                student["Name"].lower()
                == clean_name.lower()
                for student
                in st.session_state.students
            )

            if duplicate:

                st.error(
                    "Student already exists."
                )

            else:

                st.session_state.students.append(
                    {
                        "Name": clean_name,
                        "Mark": mark,
                        "Grade": get_grade(mark)
                    }
                )

                st.success(
                    f"{clean_name} added."
                )

                st.rerun()


    st.divider()

    search_text = st.text_input(
        "🔎 Search",
        placeholder="Search student"
    )

    grade_filter = st.selectbox(
        "Grade Filter",
        ["All", "A", "B", "C", "D", "F"]
    )

    if st.button(
        "🗑 Clear All",
        use_container_width=True
    ):
        st.session_state.students = []
        st.rerun()


# ============================================================
# RIGHT SIDE - DASHBOARD
# ============================================================

with right_col:

    students = st.session_state.students

    if students:

        marks = [
            student["Mark"]
            for student in students
        ]

        average = sum(marks) / len(marks)
        highest = max(marks)
        lowest = min(marks)

        top_student = max(
            students,
            key=lambda student: student["Mark"]
        )

        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        metric1, metric2, metric3, metric4, metric5 = st.columns(5)

        metric1.metric(
            "Students",
            len(students)
        )

        metric2.metric(
            "Average",
            f"{average:.1f}"
        )

        metric3.metric(
            "Highest",
            highest
        )

        metric4.metric(
            "Lowest",
            lowest
        )

        metric5.metric(
            "Top",
            top_student["Name"]
        )


        # ----------------------------------------------------
        # FILTER DATA
        # ----------------------------------------------------

        filtered_students = students

        if search_text:

            filtered_students = [
                student
                for student in filtered_students
                if search_text.lower()
                in student["Name"].lower()
            ]

        if grade_filter != "All":

            filtered_students = [
                student
                for student in filtered_students
                if student["Grade"]
                == grade_filter
            ]


        # ----------------------------------------------------
        # TABS
        # ----------------------------------------------------

        tab1, tab2, tab3 = st.tabs(
            [
                "📋 Students",
                "📊 Grade Chart",
                "⬇ Export"
            ]
        )


        # ====================================================
        # TAB 1 - STUDENT TABLE
        # ====================================================

        with tab1:

            if filtered_students:

                df = pd.DataFrame(
                    filtered_students
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    height=280
                )

                delete_name = st.selectbox(
                    "Select student to delete",
                    [
                        student["Name"]
                        for student
                        in filtered_students
                    ]
                )

                if st.button(
                    "Delete Selected Student"
                ):

                    st.session_state.students = [
                        student
                        for student
                        in st.session_state.students
                        if student["Name"]
                        != delete_name
                    ]

                    st.rerun()

            else:

                st.info(
                    "No students match your filter."
                )


        # ====================================================
        # TAB 2 - GRADE DISTRIBUTION
        # ====================================================

        with tab2:

            grade_counts = {
                "A": 0,
                "B": 0,
                "C": 0,
                "D": 0,
                "F": 0
            }

            for student in students:

                grade_counts[
                    student["Grade"]
                ] += 1

            chart_data = pd.DataFrame(
                {
                    "Grade": list(
                        grade_counts.keys()
                    ),
                    "Students": list(
                        grade_counts.values()
                    )
                }
            )

            st.bar_chart(
                chart_data,
                x="Grade",
                y="Students",
                height=300
            )


        # ====================================================
        # TAB 3 - EXPORT
        # ====================================================

        with tab3:

            csv = pd.DataFrame(
                students
            ).to_csv(
                index=False
            )

            st.download_button(
                "Download CSV Report",
                data=csv,
                file_name="student_grade_report.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.caption(
                "Download the complete student report as CSV."
            )

    else:

        st.info(
            "Add a student to begin."
        )