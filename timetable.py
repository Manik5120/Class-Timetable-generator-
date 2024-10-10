import random
from prettytable import PrettyTable
import json

# File path for data.json
file_path = "c:/Users/MANIK/OneDrive/Desktop/Timetable generator/data.json"

# Schedule constraints
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SLOTS = ["9:00-9:50", "9:50-10:40", "10:40-11:30", "11:30-12:20", "12:20-1:10", "1:10-2:00", "2:00-2:50", "2:50-3:40", "3:40-4:30", "4:30-5:20"]
LUNCH_SLOTS = ["12:20-1:10", "1:10-2:00"]

#Keep track of booked slots using sets for both sections
BOOKED_SLOTS = {"A": set(), "B": set()}

# Subjects and lab assignments
CLASSES_PER_SECTION = 23
LAB_HOURS_PER_SECTION = 4
subjects = ["DAA", "COA", "OS", "MP", "Python", "DC"]
labs = ["Python Lab", "MP Lab"]
sub_classes_A = [] #classes to be reassigned to sec-A
sub_classes_B = [] #classes to be reassigned to sec-B

# Initialize the timetable structure
def initialize_timetable():
    return {
        "A": {day: ["Free"] * len(SLOTS) for day in DAYS},
        "B": {day: ["Free"] * len(SLOTS) for day in DAYS}
    }

# Check availability of slot
def is_slot_available(timetable, section, day, slot_index):
    return timetable[section][day][slot_index] == "Free"

# Check whether the slot is a lab
def is_lab(timetable, section, day, slot_index):
    return timetable[section][day][slot_index] in labs

# Check faculty availability for a slot
def is_faculty_available(faculty, day, slot_index):
    return data["faculty_availability"][faculty][day][slot_index] != ""

# Check for consecutive free slots
def are_consecutive_slots_free(timetable, section, day, slot_index):
    return (is_slot_available(timetable, section, day, slot_index) and
            is_slot_available(timetable, section, day, slot_index + 1))
    


# Initial allocation of subject classes
def assign_classes(timetable, section):
    for subject in subjects:
        faculty = data["subjects"][subject]["faculty"]
        num_classes = 4 if subject in ["DAA", "COA", "OS", "Python", "DC"] else 3
        # Variable to keep track of number of allotments made for each subject
        allotted = 0
        for _ in range(num_classes):
            if section == "A":
                # Available slots for section-A if slot is free for both sections and faculty is available
                available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS)) 
                                if (is_slot_available(timetable, "A", day, i) and is_slot_available(timetable, "B", day, i)) and
                                is_faculty_available(faculty, day, i)]
            else:
                # Available slots for section-B if slot is free for both sections and faculty is available or if the slot is a lab class in section-A with faculty available and slot free in section-B
                available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS)) 
                                if ((is_slot_available(timetable, "A", day, i) and is_slot_available(timetable, "B", day, i)) and
                                is_faculty_available(faculty, day, i)) or ((is_lab(timetable, "A", day, i) and
                                is_faculty_available(faculty, day, i)) and is_slot_available(timetable, "B", day, i))]
            if available_slots:
                day, slot_index = random.choice(available_slots)
                timetable[section][day][slot_index] = subject
                BOOKED_SLOTS[section].add((day, slot_index, subject))
                allotted += 1
        left_classes = num_classes - allotted
        # If some subject classes remain unassigned then add them for reassignment
        if left_classes:
            for i in range(left_classes):
                if section == "A":
                    sub_classes_A.append(subject)
                elif section == "B":
                    sub_classes_B.append(subject)


def reassign_classes_A(timetable):
    # Accessing the subjects for reassignment from the sub_classes_A
    for subject in sub_classes_A:
        faculty = data["subjects"][subject]["faculty"]
        available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS)) 
                               if ((is_slot_available(timetable, "A", day, i) and is_slot_available(timetable, "B", day, i)) and
                               is_faculty_available(faculty, day, i)) or is_lab(timetable, "B", day, i)]
        for day in DAYS:
            # Consider the slots 12:20-1:10 and 1:10-2:00 as available if they are either free or lunch slots in both the sections
            if (timetable["A"][day][4] in ["Free", "Lunch Break"] and timetable["A"][day][5] in ["Free", "Lunch Break"]) and (timetable["B"][day][4] in ["Free", "Lunch Break"] and timetable["B"][day][5] in ["Free", "Lunch Break"]):
                available_slots.append((day, 4))
                available_slots.append((day, 5))
            # Consider the slot 12:20-1:10 as available if 12:20-2:00 is either free or lunch slot in section-A and only 12:20-1:10 is either free or lunch slot in section-B
            elif (timetable["A"][day][4] in ["Free", "Lunch Break"] and timetable["A"][day][5] in ["Free", "Lunch Break"]) and (timetable["B"][day][4] in ["Free", "Lunch Break"]):
                available_slots.append((day, 4))
            # Consider the slot 1:10-2:00 as available if 12:20-2:00 is either free or lunch slot in section-A and only 1:10-2:00 is either free or lunch slot in section-B
            elif (timetable["A"][day][4] in ["Free", "Lunch Break"] and timetable["A"][day][5] in ["Free", "Lunch Break"]) and (timetable["B"][day][5] in ["Free", "Lunch Break"]):
                available_slots.append((day, 5))
        if available_slots:
            day, slot_index = random.choice(available_slots)
            timetable["A"][day][slot_index] = subject
            BOOKED_SLOTS["A"].add((day, slot_index, subject))
    # Clear the reassignment list once the allocations have been completed
    sub_classes_A.clear()
    
    
def reassign_classes_B(timetable):
    # Accessing the subjects for reassignment from the sub_classes_B
    for subject in sub_classes_B:
        faculty = data["subjects"][subject]["faculty"]
        available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS)) 
                                if ((is_slot_available(timetable, "A", day, i) and is_slot_available(timetable, "B", day, i)) and
                                is_faculty_available(faculty, day, i)) or ((is_lab(timetable, "A", day, i) and
                                is_faculty_available(faculty, day, i)) and is_slot_available(timetable, "B", day, i))]
        for day in DAYS:
            # Consider the slots 12:20-1:10 and 1:10-2:00 as available if they are either free or lunch slots in both the sections
            if (timetable["B"][day][4] in ["Free", "Lunch Break"] and timetable["B"][day][5] in ["Free", "Lunch Break"]) and (timetable["A"][day][4] in ["Free", "Lunch Break"] and timetable["A"][day][5] in ["Free", "Lunch Break"]):
                available_slots.append((day, 4))
                available_slots.append((day, 5))
            # Consider the slot 12:20-1:10 as available if 12:20-2:00 is either free or lunch slot in section-B and only 12:20-1:10 is either free or lunch slot in section-A
            elif (timetable["B"][day][4] in ["Free", "Lunch Break"] and timetable["B"][day][5] in ["Free", "Lunch Break"]) and (timetable["A"][day][4] in ["Free", "Lunch Break"]):
                available_slots.append((day, 4))
            # Consider the slot 1:10-2:00 as available if 12:20-2:00 is either free or lunch slot in section-B and only 1:10-2:00 is either free or lunch slot in section-A
            elif (timetable["B"][day][4] in ["Free", "Lunch Break"] and timetable["B"][day][5] in ["Free", "Lunch Break"]) and (timetable["A"][day][5] in ["Free", "Lunch Break"]):
                available_slots.append((day, 5))
        if available_slots:
            day, slot_index = random.choice(available_slots)
            timetable["B"][day][slot_index] = subject
            BOOKED_SLOTS["B"].add((day, slot_index, subject))
    # Clear the reassignment list once the allocations have been completed
    sub_classes_B.clear()



# Allocation of lab classes in the beginning
def assign_labs(timetable, section):
    assigned_labs = 0
    available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS) - 1)]

    for lab in labs:
        faculty = data["labs"][lab]["faculty"]
        while assigned_labs < LAB_HOURS_PER_SECTION:
            random.shuffle(available_slots)
            for (day, slot_index) in available_slots:
                # Check if consecutive slots are free and faculty is available for both the slots
                if (are_consecutive_slots_free(timetable, section, day, slot_index) and
                    is_faculty_available(faculty, day, slot_index) and
                    is_faculty_available(faculty, day, slot_index + 1)):
                    
                    # Ensure lab is not assigned to the other section at the same time
                    if (timetable["A"][day][slot_index] != lab and timetable["B"][day][slot_index] != lab):
                        timetable[section][day][slot_index] = lab
                        timetable[section][day][slot_index + 1] = lab
                        assigned_labs += 2
                        BOOKED_SLOTS[section].add((day, slot_index, lab))
                        # Update the faculty availability timings so that the faculty is not considered to be available for a subject class at the same time
                        data["faculty_availability"][faculty][day][slot_index] = ""
                        data["faculty_availability"][faculty][day][slot_index+1] = ""
                        break
            else:
                continue
            break

# Add lunch break
def assign_lunch_break(timetable):
    for section in ["A", "B"]:
        for day in DAYS:
            # If lunch break is already assigned, move on to check for the next day
            if timetable[section][day][4] == "Lunch Break" or timetable[section][day][5] == "Lunch Break":
                continue
            # If labs do not lie in the lunch intervals then select a random slot for lunch break
            elif timetable[section][day][4:6] not in labs:
                lunch_slot = random.choice(LUNCH_SLOTS)
            #If a lab slot lies from 12:20-1:10 then allocate lunch break from 1:10-2:00
            elif timetable[section][day][4] in labs:
                lunch_slot = LUNCH_SLOTS[1]
            # If a lab slot lies from 1:10-2:00 then allocate lunch break from 12:20-1:10
            elif timetable[section][day][5] in labs:
                lunch_slot = LUNCH_SLOTS[0]
            # If a slot is free within the lunch intervals, then allocate lunch break to that slot. If both are free then lunch slot is allocated to the later slot, i.e., 1:10-2:00
            for recess in LUNCH_SLOTS:
                if timetable[section][day][SLOTS.index(recess)] == "Free":
                    lunch_slot = recess
            slot_index = SLOTS.index(lunch_slot)
            # If the allocated slot is not free and contains some subject class, overwrite it and add the subject to the reassignment list
            if section == "A":
                if timetable[section][day][slot_index] != "Free":
                    sub_classes_A.append(timetable[section][day][slot_index])
            else:
                if timetable[section][day][slot_index] != "Free":
                    sub_classes_B.append(timetable[section][day][slot_index])
            timetable[section][day][slot_index] = "Lunch Break"

# Display the timetable in tabular format using PrettyTable
def display_timetable(timetable, section):
    print(f"\nTimetable for Section {section}:")
    table = PrettyTable()
    table.field_names = ["Day"] + SLOTS

    for day in DAYS:
        row = [day] + timetable[section][day]
        table.add_row(row)

    print(table)

# Call the lab assignment, class assignment, reassignment and lunch assignment operations to form the timetables for both the sections
def fill_timetable():
    # Set maximum number of attempts for generating the desired timetable
    max_attempts = 10000
    for attempt in range(max_attempts):
        # Access the data.json file for generating the timetable with the provided data
        global data
        with open(file_path, 'r+') as file:
            data = json.load(file)
        # Generate a timetable with all free slots
        timetable = initialize_timetable()
        # Assign labs to section-A
        assign_labs(timetable, "A")
        # Assign labs to section-B
        assign_labs(timetable, "B")
        # Assign classes to section-A
        assign_classes(timetable, "A")
        # Assign classes to section-B
        assign_classes(timetable, "B")
        # Assign lunch break to both the sections (some overwriting may occur)
        assign_lunch_break(timetable)
        # Reassign the overwritten or left out classes for both the sections
        reassign_classes_A(timetable)
        reassign_classes_B(timetable)
        # Reassign the lunch breaks if any has been altered after reassignment
        assign_lunch_break(timetable)

        # Calculate the total number of slots allocated for classes to each section
        total_assigned_A = sum(slot not in ["Free", "Lunch Break"] for day in DAYS for slot in timetable["A"][day])
        total_assigned_B = sum(slot not in ["Free", "Lunch Break"] for day in DAYS for slot in timetable["B"][day])
        
        # Return the timetable if the number of allocated slots is equal to the number of desired slots for both the sections
        if total_assigned_A == (LAB_HOURS_PER_SECTION + CLASSES_PER_SECTION) and total_assigned_B == (LAB_HOURS_PER_SECTION + CLASSES_PER_SECTION):
            # Print the number of attempts taken to generate the result
            print(f"Attempt {attempt + 1}: Total A: {total_assigned_A}, Total B: {total_assigned_B}") 
            return timetable
        
    return None  # If no valid timetable found

def main():
    
    
    print("Filling timetable...")
    timetable = fill_timetable()
    
    if timetable:
        display_timetable(timetable, "A")
        display_timetable(timetable, "B")
    else:
        print("Could not generate a valid timetable.")

if __name__ == "__main__":
    main()
