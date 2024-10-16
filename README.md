# Timetable Generator

# Description
A Python-based Timetable Generator that automates the creation of class schedules for educational institutions. This project considers faculty availability, subject credits, and lab sessions to create a balanced timetable for multiple sections. Data such as subjects, faculty, and availability are provided in a structured JSON format, and the generator allocates classes efficiently based on these constraints.

# Features:
1.	Faculty Availability: Ensures that classes and labs are assigned according to each faculty's available slots.
2.	Subject Credits: Assigns the appropriate number of classes per subject per week based on its credit weightage.
3.	Lab Sessions: Schedules lab sessions in consecutive time slots to ensure smooth practical sessions.
4.	Balanced Timetable: Each section gets an evenly distributed timetable with 27 hours of engagement (23 class hours and 4 lab hours).
5.	JSON Integration: The generator reads from a JSON file to dynamically create timetables, making it easy to modify input data.

# Technologies Used:
1.  Python for the logic and timetable generation
2.  JSON for input data structure

# How It Works:
1.	The system reads data such as subjects, labs, and faculty availability from a JSON file.
2.	It then assigns classes and labs to different sections based on the number of credits and available slots.
3.	The resulting timetable is balanced, ensuring faculty are not double-booked, and each section has the correct number of total hours.

