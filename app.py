import streamlit as st

# Title
st.title("Branch Council Meeting Agenda")

# Date Input
date = st.text_input("Date")

# Attendance Section
st.subheader("Attendance")
in_attendance = st.text_area("In Attendance")
apologies = st.text_area("Apologies")
presiding = st.text_input("Presiding")
conducting = st.text_input("Conducting")
time = st.text_input("Time")

# Opening Section
st.subheader("Opening")
opening_hymn = st.text_input("Opening Hymn")
opening_prayer = st.text_input("Opening Prayer")
spiritual_thought = st.text_input("Spiritual Thought")

# Agenda Items Section
st.subheader("Agenda Items")
agenda_items = []
if "agenda_items" not in st.session_state:
    st.session_state.agenda_items = [{"time": "", "item": "", "discussion": "", "lead": ""}]
for i, item in enumerate(st.session_state.agenda_items):
    col1, col2 = st.columns(2)
    with col1:
        item["time"] = st.number_input(f"Time Allocation (min) for Item {i+1}", min_value=0, key=f"time_{i}")
        item["item"] = st.text_input(f"Item {i+1}", key=f"item_{i}")
    with col2:
        item["discussion"] = st.text_area(f"Discussion Notes for Item {i+1}", key=f"discussion_{i}")
        item["lead"] = st.selectbox(f"Lead for Item {i+1}", ["Exec Sec", "BP"], key=f"lead_{i}")
if st.button("Add New Item"):
    st.session_state.agenda_items.append({"time": "", "item": "", "discussion": "", "lead": ""})
    st.rerun()  # Updated from st.experimental_rerun() to st.rerun()

# Closing Section
st.subheader("Closing")
assignments = st.text_area("Assignments, counsel, concluding remarks")
closing_hymn = st.text_input("Closing Hymn")
closing_prayer = st.text_input("Closing Prayer")

# Save Button
if st.button("Save Agenda"):
    agenda_data = {
        "date": date,
        "in_attendance": in_attendance,
        "apologies": apologies,
        "presiding": presiding,
        "conducting": conducting,
        "time": time,
        "opening_hymn": opening_hymn,
        "opening_prayer": opening_prayer,
        "spiritual_thought": spiritual_thought,
        "agenda_items": st.session_state.agenda_items,
        "assignments": assignments,
        "closing_hymn": closing_hymn,
        "closing_prayer": closing_prayer
    }
    with open("agenda.txt", "w") as f:
        f.write(str(agenda_data))
    st.success("Agenda saved to agenda.txt locally!")

# Note about hosting
st.markdown("**Note:** To use this online, deploy it using Streamlit Community Cloud (instructions below).")