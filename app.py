import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Header Section
st.title("Meeting Agenda")

# Dropdown for meeting type
meeting_type = st.selectbox("Meeting Type", [
    "Branch Presidency Meeting Agenda",
    "Branch Council Meeting Agenda",
    "Branch Youth Council Meeting Agenda"
])

# Date Input
date = st.text_input("Date")

# Attendance Section
st.subheader("Attendance")
in_attendance = st.text_area("In Attendance")
apologies = st.text_area("Apologies")
presiding = st.selectbox("Presiding", ["Branch President", "First Counsellor", "Second Counsellor"])
conducting = st.selectbox("Conducting", ["Branch President", "First Counsellor", "Second Counsellor"])
time = st.text_input("Time")

# Opening Section
st.subheader("Opening")
opening_hymn = st.text_input("Opening Hymn")
opening_prayer = st.text_input("Opening Prayer")
spiritual_thought = st.text_input("Spiritual Thought")

# Agenda Items Section
st.subheader("Agenda Items")
if "agenda_items" not in st.session_state:
    st.session_state.agenda_items = [{"time": "", "item": "", "discussion": "", "lead": ""}]
for i, item in enumerate(st.session_state.agenda_items):
    col1, col2 = st.columns(2)
    with col1:
        item["time"] = st.number_input(f"Time Allocation (min) for Item {i+1}", min_value=0, key=f"time_{i}")
        item["item"] = st.text_input(f"Item {i+1}", key=f"item_{i}")
    with col2:
        item["discussion"] = st.text_area(f"Discussion Notes for Item {i+1}", key=f"discussion_{i}")
        item["lead"] = st.selectbox(f"Lead for Item {i+1}", ["Exec Sec", "BP", "1C", "2C", "RS", "EQ", "YW", "PRI", "SS"], key=f"lead_{i}")
if st.button("Add New Item"):
    st.session_state.agenda_items.append({"time": "", "item": "", "discussion": "", "lead": ""})
    st.rerun()  # Refresh to show new item

# Closing Section
st.subheader("Closing")
assignments = st.text_area("Assignments, counsel, concluding remarks")
closing_hymn = st.text_input("Closing Hymn")
closing_prayer = st.text_input("Closing Prayer")

# Action Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Save Agenda"):
        agenda_data = {
            "meeting_type": meeting_type,
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

with col2:
    if st.button("Generate PDF"):
        # Create PDF in memory
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        y_position = 750  # Start near the top of the page

        # Write to PDF
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, y_position, meeting_type)
        y_position -= 30

        c.setFont("Helvetica", 12)
        c.drawString(100, y_position, f"Date: {date}")
        y_position -= 20
        c.drawString(100, y_position, "Attendance")
        y_position -= 20
        c.drawString(100, y_position, f"In Attendance: {in_attendance}")
        y_position -= 20
        c.drawString(100, y_position, f"Apologies: {apologies}")
        y_position -= 20
        c.drawString(100, y_position, f"Presiding: {presiding}")
        y_position -= 20
        c.drawString(100, y_position, f"Conducting: {conducting}")
        y_position -= 20
        c.drawString(100, y_position, f"Time: {time}")
        y_position -= 20

        y_position -= 20
        c.drawString(100, y_position, "Opening")
        y_position -= 20
        c.drawString(100, y_position, f"Opening Hymn: {opening_hymn}")
        y_position -= 20
        c.drawString(100, y_position, f"Opening Prayer: {opening_prayer}")
        y_position -= 20
        c.drawString(100, y_position, f"Spiritual Thought: {spiritual_thought}")
        y_position -= 20

        y_position -= 20
        c.drawString(100, y_position, "Agenda Items")
        y_position -= 20
        for idx, item in enumerate(st.session_state.agenda_items, 1):
            c.drawString(100, y_position, f"{idx}. Time: {item['time']} min, Item: {item['item']}, Lead: {item['lead']}")
            y_position -= 20
            c.drawString(100, y_position, f"Discussion Notes: {item['discussion']}")
            y_position -= 20

        y_position -= 20
        c.drawString(100, y_position, "Closing")
        y_position -= 20
        c.drawString(100, y_position, f"Assignments: {assignments}")
        y_position -= 20
        c.drawString(100, y_position, f"Closing Hymn: {closing_hymn}")
        y_position -= 20
        c.drawString(100, y_position, f"Closing Prayer: {closing_prayer}")
        y_position -= 20

        c.save()
        buffer.seek(0)

        # Allow user to download the PDF
        st.download_button(
            label="Download PDF",
            data=buffer,
            file_name="agenda.pdf",
            mime="application/pdf"
        )
        st.success("PDF generated! Click the 'Download PDF' button to save it.")

# Note about hosting
st.markdown("**Note:** To use this online, deploy it using Streamlit Community Cloud (instructions provided earlier).")
