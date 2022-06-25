from utils.export_data import *
from utils.cp_model import *
from utils.data_processing import *

# Build the list of shifts
shifts = BuildShiftDictionary()

# Read in the individual volunteer data
individual_volunteers = ReadInIndividualVolunteerData()

# Read in the volunteer group data
group_volunteers = ReadInGroupVolunteerData()

# Break the volunteer groups down into individuals
DisaggregateVolunteerGroups(group_volunteers, individual_volunteers, shifts)

# Calculate the number of preference points each volunteer associates with each shift
for v in individual_volunteers:
    v.CalculateShiftPreferencePoints(shifts)

# Build the constraint programming model
(model, assignment) = BuildModel(individual_volunteers, shifts)

# Create the solver and solve
solver = cp_model.CpSolver()
solver.Solve(model)

# Print out the results
PrintShiftAssignments(solver, assignment, shifts, individual_volunteers)
PrintSummaryStatistics(solver, assignment, shifts, individual_volunteers)

# Write the results to a CSV file
ExportShiftFocusedSchedule(solver, assignment, shifts, individual_volunteers)
ExportVolunteerFocusedSchedule(solver, assignment, shifts, individual_volunteers)
