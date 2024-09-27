import random
from prettytable import PrettyTable

# Schedule constraints
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SLOTS = ["9:00-9:50", "9:50-10:40", "10:40-11:30", "11:30-12:20", "12:20-1:10", "1:10-2:00", "2:00-2:50", "2:50-3:40", "3:40-4:30", "4:30-5:20"]
LUNCH_SLOTS = ["12:20-1:10", "1:10-2:00"]

# Subjects and lab assignments
CLASSES_PER_SECTION = 23  # Each section should have 23 classes
LAB_HOURS_PER_SECTION = 4  # 4 hours of lab per section, each lab session is 2 consecutive hours
CLASSROOM = "Main Room"  # Shared classroom for theory classes
LAB_VENUE = "Lab Room"  # Labs occur in a separate venue

# Sample data for subjects and labs
subjects = ["DAA", "COA", "OS", "MP", "Python", "DC"]
labs = ["Python Lab", "MP Lab"]
sub_classes_A = []
sub_classes_B = []

# Initialize the timetable structure
def initialize_timetable():
    timetable = {
        "A": {day: ["Free"] * len(SLOTS) for day in DAYS},
        "B": {day: ["Free"] * len(SLOTS) for day in DAYS}
    }
    return timetable

# Check if the classroom is available for theory classes
def is_classroom_available(timetable, day, slot_index):
    return timetable["A"][day][slot_index] == "Free" and timetable["B"][day][slot_index] == "Free"

# Check if two consecutive slots are free for labs
def are_consecutive_slots_free(timetable, section, day, slot_index):
    return (timetable[section][day][slot_index] == "Free" and 
            timetable[section][day][slot_index + 1] == "Free")

# Assign classes for a section
def assign_classes(timetable, section, subjects):
    assigned_slots = 0
    available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS)) if is_classroom_available(timetable, day, i)]

    # Shuffle the available slots for random assignment
    random.shuffle(available_slots)

    # Assign classes ensuring we do not exceed the required number of slots
    for subject in subjects:
        num_classes = 4 if subject in ["DAA", "COA", "OS", "Python", "DC"] else 3  # Adjust as per credits
        for _ in range(num_classes):
            if assigned_slots < CLASSES_PER_SECTION:
                if available_slots:  # Check if there are available slots
                    day, slot_index = available_slots.pop()
                    timetable[section][day][slot_index] = subject
                    assigned_slots += 1

    return timetable

# Re-Assign classes which were overwritten due to assignment of lunch break
def reassign_classes(timetable, section, sub_classes):
    assigned_slots = 0
    available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS)) if is_classroom_available(timetable, day, i)]

    # Shuffle the available slots for random assignment
    random.shuffle(available_slots)

    # Assign classes ensuring we do not exceed the required number of slots
    for subject in sub_classes:
        num_classes = 1
        for _ in range(num_classes):
            if assigned_slots < len(sub_classes):
                if available_slots:  # Check if there are available slots
                    day, slot_index = available_slots.pop()
                    timetable[section][day][slot_index] = subject
                    assigned_slots += 1
    sub_classes.clear()
    return timetable

# Add labs for a section (consecutive 2-hour labs)
def assign_labs(timetable, section, labs):
    assigned_labs = 0
    available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS) - 1)]  # To accommodate 2-hour labs

    # Shuffle the available slots for random assignment
    random.shuffle(available_slots)

    # Assign 4 hours of labs (2 hours each for Python Lab and MP Lab)
    for lab in labs:
        while assigned_labs < LAB_HOURS_PER_SECTION:
            if available_slots:  # Check if there are available slots
                day, slot_index = available_slots.pop()
                # Check if both slots are free for the section
                if are_consecutive_slots_free(timetable, section, day, slot_index):
                    if slot_index != 4:
                        timetable[section][day][slot_index] = lab
                        timetable[section][day][slot_index + 1] = lab
                        assigned_labs += 2
                        # Ensure we break out once a lab is assigned
                        break  

    return timetable

# Add lunch break
def assign_lunch_break(timetable):
    for section in ["A", "B"]:
        for day in DAYS:
            if timetable[section][day][4:6] not in labs:
                lunch_slot = random.choice(LUNCH_SLOTS)
            else:
                lunch_slot = LUNCH_SLOTS[0]
            for recess in LUNCH_SLOTS:
                if timetable[section][day][SLOTS.index(recess)] == "Free":
                    lunch_slot = recess
            slot_index = SLOTS.index(lunch_slot)
            if section == "A":
                if timetable[section][day][slot_index] != "Free":
                    sub_classes_A.append(timetable[section][day][slot_index])
            else:
                if timetable[section][day][slot_index] != "Free":
                    sub_classes_B.append(timetable[section][day][slot_index])
            timetable[section][day][slot_index] = "Lunch Break"
    return timetable

# Display the timetable in horizontal format
def display_timetable(timetable, section):
    print(f"\nTimetable for Section {section}:")
    table = PrettyTable()
    table.field_names = ["Day"] + SLOTS

    for day in DAYS:
        row = [day] + timetable[section][day]
        table.add_row(row)

    print(table)

# Fill the timetable
def fill_timetable():
    timetable = initialize_timetable()
    
    # Assign classes and labs for both sections
    timetable = assign_classes(timetable, "A", subjects)
    timetable = assign_classes(timetable, "B", subjects)
    timetable = assign_labs(timetable, "A", labs)
    timetable = assign_labs(timetable, "B", labs)
    
    # Ensure lunch breaks
    timetable = assign_lunch_break(timetable)
    timetable = reassign_classes(timetable, "A", sub_classes_A)
    timetable = reassign_classes(timetable, "B", sub_classes_B)

    return timetable

# Main execution
def main():
    print("Filling timetable...")
    
    # Check if the timetable is complete (27 slots engaged)
    while True:
        timetable = fill_timetable()
        total_assigned_A = sum(slot not in ["Free", "Lunch Break"] for day in DAYS for slot in timetable["A"][day])
        total_assigned_B = sum(slot not in ["Free", "Lunch Break"] for day in DAYS for slot in timetable["B"][day])
        if (total_assigned_A == 27 and total_assigned_B == 27):
            # Display the timetables for both sections
            display_timetable(timetable, "A")
            display_timetable(timetable, "B")
            break
    

if __name__ == "__main__":
    main()
