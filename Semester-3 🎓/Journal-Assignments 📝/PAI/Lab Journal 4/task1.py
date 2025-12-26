#Making dictonaries 
subj1 = {}
subj2 = {}

# Subject 1
subj1 = {}
for i in range(2):
    name = input("Enter student name for subject1: ")
    subj1[name] = 0
for student in subj1:
    subj1[student] = int(input(f"Enter marks for {student} in subject1: "))

# Subject 2
subj2 = {}
for i in range(2):
    name = input("Enter student name for subject2: ")
    subj2[name] = 0
for student in subj2:
    subj2[student] = int(input(f"Enter marks for {student} in subject2: "))

total ={}

for student in subj1:
    if student in subj2:
        total[student] = subj1[student] + subj2[student]
    else:
        total[student] = subj1[student]  # since no marks in subj2

for student in subj2:
    if student not in total:  # already handled above
        total[student] = subj2[student]

print(total)
