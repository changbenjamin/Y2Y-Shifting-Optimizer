import pandas as pd
from utils.y2y_classes import *

def ReadInIndividualVolunteerData():
    # This function reads the preferences into a data frame

    # Specify the name of the csv file
    csv_name = '../data/Updated Preferences.csv'

    # Read in the data
    data = pd.read_csv(csv_name)

    # Instantiate the list of volunteers
    volunteers = []

    # Loop over the rows of data
    for (_, row) in data.iterrows():
        # Instantiate a new volunteer
        v = Volunteer()

        # Assign an ID Number to the volunteer
        v.ID_Number = len(volunteers)

        # Read in most of the volunteer's properties
        v.Name = row['Name']
        v.IsPreferredVolunteer = row['Preferred Applicants']

        columns = data.columns

        shift_pref = []

        # list of all preferences
        for i in columns:
            shift_pref.append(str(row[i]))

        shift_pref.remove(shift_pref[0]) # remove the name of the person

        shift_pref = [x for x in shift_pref if x != 'nan']

        shift_pref.sort()

        # until all preferences are found
        while len(shift_pref) != 0:
            for c in columns:  # go through all items in the row
                if row[c] == shift_pref[0]:  # check to see if it is the next preference
                    v.PreferredShifts.append(c)  # add to the list
                    shift_pref.remove(shift_pref[0])  # remove that preference
                    break

        volunteers.append(v)

    # Return the list of volunteers
    return volunteers


def ReadInGroupVolunteerData():
    # This function reads the preferences into a data frame

    # Specify the name of the csv file
    csv_name = '../data/Group Volunteers.csv'

    # Read in the data
    data = pd.read_csv(csv_name)

    # Instantiate the list of volunteer groups
    volunteer_groups = []

    # Loop over the rows of data
    for (_, row) in data.iterrows():
        # Instantiate a new volunteer group
        v = VolunteerGroup()

        # Populate the volunteer's properties
        v.ID_Number = len(volunteer_groups) + 1
        v.GroupName = row['Group']
        v.AssignedShift = row['Shift']
        v.Volunteers = row['Volunteers']

        # Add this volunteer group to the growing list
        volunteer_groups.append(v)

    # Return the list of volunteer groups
    return volunteer_groups


def DisaggregateVolunteerGroups(GroupVolunteers, IndividualVolunteers, shifts):
    # Inputs:
    #   GroupVolunteers = a list of VolunteerGroup objects
    #   IndividualVolunteers = a list of individual volunteer objects
    # Outputs:
    #   Creates a number of individual volunteers for each VolunteerGroup and adds these individuals to the list of individual volunteers

    # Loop over the volunteer groups
    for g in GroupVolunteers:

        # Cap the number of volunteers in this group at the number required by their preferred shift
        g.Volunteers = min(g.Volunteers, shifts[g.AssignedShift].required_volunteers)

        # Create an individual volunteer object for each volunteer in this group
        for VolunteerIndex in range(g.Volunteers):

            # Instantiate a new individual volunteer
            v = Volunteer()

            # Assign an ID Number to the volunteer
            v.ID_Number = len(IndividualVolunteers)

            # Create a placeholder for the name of the volunteer
            v.Name = str(g.GroupName + ' Volunteer %d' % (VolunteerIndex + 1))

            # Specify them as a preferred volunteer
            v.IsPreferredVolunteer = True

            # Specify their first preference for a shift as the group's preference
            v.PreferredShifts = [g.AssignedShift]

            # Specify their other preferences as empty
            for _ in range(4):
                v.PreferredShifts.append('')

            # Add this individual to the list of volunteers
            IndividualVolunteers.append(v)


def BuildShiftDictionary():
    # This function builds a dictionary of shift objects, where the dictionary keys are the shift names

    # Specify the days of the week
    weekdays = [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
    ]

    # Create the list of periods
    periods = [
        Period(Name='Breakfast', RequiredVolunteers=3),
        Period(Name='Dinner', RequiredVolunteers=3),
        Period(Name='Evening', RequiredVolunteers=3),
        Period(Name='Overnight', RequiredVolunteers=1),
    ]

    # Initialize the dictionary of shifts
    shifts = {}
    for w in weekdays:
        for p in periods:
            # Construct the shift name corresponding to this weekday and period
            ShiftName = '%s %s' % (w, p.Name)

            # Instantiate a new shift object
            s = Shift()

            # Add the shift's properties
            s.shift_name = ShiftName
            s.required_volunteers = p.RequiredVolunteers

            # Add the shift to the growing dictionary of shifts
            shifts[ShiftName] = s

    # Return the list of shifts
    return shifts