
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Record Management",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Record Management System")
st.write("Manage student records easily using CRUD operations.")

# Initialize student data
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(
        columns=["Roll No", "Name", "Age", "Course", "Marks"]
    )

# Sidebar menu
st.sidebar.title("Menu")
menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.subheader("➕ Add New Student")

    with st.form("add_form"):
        roll = st.number_input("Roll Number", min_value=1, step=1)
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        course = st.text_input("Course")
        marks = st.number_input("Marks", min_value=0, max_value=100)

        submit = st.form_submit_button("Add Student")

        if submit:
            if not name.strip() or not course.strip():
                st.error("Please enter name and course.")
            elif roll in st.session_state.students["Roll No"].values:
                st.error("Roll number already exists!")
            else:
                new_student = pd.DataFrame([{
                    "Roll No": roll,
                    "Name": name,
                    "Age": age,
                    "Course": course,
                    "Marks": marks
                }])

                st.session_state.students = pd.concat(
                    [st.session_state.students, new_student],
                    ignore_index=True
                )

                st.success("Student added successfully!")

# READ
elif menu == "View Students":
    st.subheader("📋 All Student Records")

    if not st.session_state.students.empty:
        st.dataframe(
            st.session_state.students,
            use_container_width=True,
            hide_index=True
        )
        st.info(f"Total Students: {len(st.session_state.students)}")
    else:
        st.warning("No student records found.")

# UPDATE
elif menu == "Update Student":
    st.subheader("✏️ Update Student Details")

    df = st.session_state.students

    if not df.empty:
        roll = st.selectbox("Select Roll Number", df["Roll No"].tolist())

        student = df[df["Roll No"] == roll].iloc[0]

        with st.form("update_form"):
            name = st.text_input("Name", value=student["Name"])
            age = st.number_input(
                "Age", min_value=1, max_value=100,
                value=int(student["Age"])
            )
            course = st.text_input("Course", value=student["Course"])
            marks = st.number_input(
                "Marks", min_value=0, max_value=100,
                value=int(student["Marks"])
            )

            update = st.form_submit_button("Update Student")

            if update:
                if not name.strip() or not course.strip():
                    st.error("Name and course cannot be empty.")
                else:
                    idx = st.session_state.students[
                        st.session_state.students["Roll No"] == roll
                    ].index[0]

                    st.session_state.students.loc[
                        idx, ["Name", "Age", "Course", "Marks"]
                    ] = [name, age, course, marks]

                    st.success("Student updated successfully!")
    else:
        st.warning("No records available to update.")

# DELETE
elif menu == "Delete Student":
    st.subheader("🗑️ Delete Student Record")

    df = st.session_state.students

    if not df.empty:
        roll = st.selectbox(
            "Select Roll Number to Delete",
            df["Roll No"].tolist()
        )

        if st.button("Delete Student"):
            st.session_state.students = (
                st.session_state.students[
                    st.session_state.students["Roll No"] != roll
                ].reset_index(drop=True)
            )

            st.success("Student deleted successfully!")
    else:
        st.warning("No records available to delete.")

st.sidebar.markdown("---")
st.sidebar.caption("Student Record Management System")
