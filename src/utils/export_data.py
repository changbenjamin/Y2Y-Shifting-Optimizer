def PrintShiftAssignments(solver, assignment, shifts, individual_volunteers):
    # This function prints out a shift-centric view of the shift assignments
    # Inputs:
    #   solver = the CP solver object, which has already solved the model.
    #   Assignment = a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables
    #   Shifts = a dictionary of Shift objects

    # Loop over the shifts
    for s in shifts:

        # Print the name of the shift
        print(s)

        for v in individual_volunteers:

            if solver.Value(assignment[(v, s)]) == 1:
                # Print the volunteer's first and last name
                print('\t' + v.Name)


def PrintSummaryStatistics(solver, assignment, shifts, individual_volunteers):
    # This function prints out several statistics summarizing the quality of the shift assignment found by the optimizer
    # Inputs:
    #   solver = the CP solver object, which has already solved the model.
    #   Assignment = a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables
    #   Shifts = a dictionary of Shift objects

    # Calculate the fraction of the staffing requirements that have been fulfilled
    # Initialize the count of desired assignments
    assignments_required = 0

    # Initialize the count of assignments realized
    assignments_realized = 0

    # Initialize the count of preferred assignments realized
    preferred_assignments_realized = 0

    # Count the number of preferred volunteers
    preferred_volunteers = 0
    for v in individual_volunteers:

        # Check if this is a preferred volunteer
        if v.IsPreferredVolunteer == True:
            # Increment the count of preferred volunteers
            preferred_volunteers += 1

    # Initialize the count of under-staffed shifts
    under_staffed_shifts = 0

    # Loop over the shifts
    for s in shifts:

        # Increment the staffing requirements
        assignments_required += shifts[s].required_volunteers

        # Initialize the count of volunteers assigned to this shift
        assignments_for_shift = 0

        # Loop over each of the volunteers
        for v in individual_volunteers:

            # Check if they were assigned to the current shift
            if solver.Value(assignment[(v, s)]) == 1:  # They were assigned to the current shfit

                # Increment the count of assignments realized
                assignments_realized += 1

                # Increment the count of assignments for this particular shift
                assignments_for_shift += 1

                # Check if this is a preferred volunteer
                if v.IsPreferredVolunteer == True:
                    # Increment the count of preferred assignments realized
                    preferred_assignments_realized += 1

        # Check if this shift is under-staffed
        if assignments_for_shift < shifts[s].required_volunteers:  # this shift is under-staffed

            # Increment the count of under-staffed shifts
            under_staffed_shifts += 1

    # Calculate the fraction of required assignments that were realized
    fraction_of_requirements_realized = assignments_realized / assignments_required

    # Calculate the fraction of under-staffed shifts
    fraction_of_under_staffed_shifts = under_staffed_shifts / len(shifts)

    # Calculate the fraction of volunteers assigned
    fraction_of_volunteers_assigned = assignments_realized / len(individual_volunteers)

    # Calculate the fraction of preferred volunteers assigned
    fraction_of_preferred_volunteers_assigned = preferred_assignments_realized / preferred_volunteers

    # Print the results
    print('\nStaffing requirements covered: %1.1f%%.' % (fraction_of_requirements_realized * 100))

    print('Shifts fully covered: %1.1f%%.' % ((1 - fraction_of_under_staffed_shifts) * 100))

    print('Volunteers assigned to a shift: %1.1f%%.' % (fraction_of_volunteers_assigned * 100))

    print('Preferred volunteers assigned to a shift: %1.1f%%.' % (fraction_of_preferred_volunteers_assigned * 100))


def ExportVolunteerFocusedSchedule(solver, Assignment, Shifts, IndividualVolunteers):
    # This function exports a shift-centric CSV of the shift assignments
    # Inputs:
    #   solver = the CP solver object, which has already solved the model.
    #   Assignment = a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables
    #   Shifts = a dictionary of Shift objects

    # Import the necessary libraries
    import csv
    import sys

    # Specify the name of the file to be exported
    file_name = '../exported_files/Volunteer-Focused Schedule.csv'

    # Create the file
    with open(file_name, mode='w') as f:

        # Instantiate the csv writer
        if 'win' in sys.platform:  # Check for windows
            writer = csv.writer(f, delimiter=',', lineterminator='\n')
        else:
            writer = csv.writer(f, delimiter=',')

        # Add the header line
        # Initialize the header line
        header_line = ['Volunteer', 'Assignment']

        # Write the header line to the csv
        writer.writerow(header_line)

        # Add the line for each volunteer
        for v in IndividualVolunteers:

            # Initialize the line with the volunteer's first and last name
            line = ['%s' % (v.Name)]

            # Initialize the flag indicating whether an assignment has been found
            assignment_found = False

            # Loop over each shift
            for s in Shifts:

                # Check if the volunteer was assigned to the current shift
                if solver.Value(Assignment[(v, s)]) == 1:  # They were assigned to the current shift

                    # Print the shift's name
                    line.append('%s' % s)

                    # Raise the flag indicating that an assignment has been found
                    assignment_found = True

            # Check if an assignment was found
            if not assignment_found:
                # Print a message indicating that no assignment was found
                line.append('Unassigned')

            # Write out the line for the current volunteer
            writer.writerow(line)


def ExportShiftFocusedSchedule(solver, Assignment, Shifts, IndividualVolunteers):
    # This function exports a shift-centric CSV of the shift assignments
    # Inputs:
    #   solver = the CP solver object, which has already solved the model.
    #   Assignment = a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables
    #   Shifts = a dictionary of Shift objects

    # Import the necessary libraries
    import csv
    import sys

    # Specify the name of the file to be exported
    file_name = '../exported_files/Shift-Focused Schedule.csv'

    # Create the file
    with open(file_name, mode='w') as f:

        # Instantiate the csv writer
        if 'win' in sys.platform:  # Check for windows
            writer = csv.writer(f, delimiter=',', lineterminator='\n')
        else:
            writer = csv.writer(f, delimiter=',')

        # Construct the header line
        # Intialize the header line
        HeaderLine = ['Shift']

        # Calculate the maximum number of volunteers required in any given shift
        max_volunteers_per_shift = max([s.required_volunteers for s in Shifts.values()])

        # Add a column for each possible volunteer
        for v in range(1, max_volunteers_per_shift + 1):
            # Add the header for the vth volunteer
            HeaderLine.append('Volunteer %s' % str(v))

        # Add a column for notes
        HeaderLine.append('Notes')

        # Write the header line to the csv
        writer.writerow(HeaderLine)

        # Add the line for each shift
        for s in Shifts:

            # Initialize the line with the name of the shift
            line = [s]

            # Initialize the count of volunteers assigned to this shift
            volunteers_assigned = 0

            # Loop over the volunteers
            for v in IndividualVolunteers:

                # Check if they were assigned to the current shift
                if solver.Value(Assignment[(v, s)]) == 1:  # They were assigned to the current shfit

                    # Print the volunteer's first and last name
                    line.append('%s' % (v.Name))

                    # Increment the count of volunteers assigned
                    volunteers_assigned += 1

            # Check for under-staffing
            if volunteers_assigned < Shifts[s].required_volunteers:  # this is an under-staffed shift

                # Add the appropriate number of empty strings
                for _ in range(max_volunteers_per_shift - volunteers_assigned):
                    line.append(' ')

                # Add the warning about under-staffing
                line.append('Warning: this shift is under-staffed.')

            # Write out the line for the current shift
            writer.writerow(line)
