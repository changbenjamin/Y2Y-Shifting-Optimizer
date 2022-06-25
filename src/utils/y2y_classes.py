class Volunteer():
    # This class describes individual volunteers

    def __init__(self):
        self.ID_Number = 0
        self.Name = ''
        self.IsPreferredVolunteer = False
        self.PreferredShifts = []
        self.ShiftPreferencePoints = {}

    def CalculateShiftPreferencePoints(self, Shifts):

        # Instantiate the dictionary of shift preference points
        self.ShiftPreferencePoints = {}

        # Initialize a point value of zero for each shift
        for s in Shifts:
            self.ShiftPreferencePoints[s] = 0

        # Assign preference points for each of the volunteer's preferred shifts
        for s in Shifts:

            # Check if the current shift is in the volunteer's list of preferred shifts
            if not s in self.PreferredShifts:  # then it's not there

                # Assign 0 preference points to this shift for this volunteer
                self.ShiftPreferencePoints[s] = 0

            else:  # the shift *is* in the volunteer's list of preferred shifts

                # Find the position of the shift in the list
                index = self.PreferredShifts.index(s)

                # Find the length of the list
                list_length = len(self.PreferredShifts)

                # Calculate the number of points corresponding to this index
                self.ShiftPreferencePoints[
                    s] = list_length - index  # Index = 0 ==> max points,  Index = Max Index ==> 1 point

                # Check if this is a preferred volunteer
                if self.IsPreferredVolunteer == True:
                    # Increase the points
                    self.ShiftPreferencePoints[s] = self.ShiftPreferencePoints[
                                                        s] * 2  # This ensures preferential treatment for preferred volunteers


class VolunteerGroup():
    # This class describes volunteer groups

    def __init__(self):
        self.ID_Number = 0
        self.GroupName = ''
        self.AssignedShift = ''
        self.Volunteers = 0


class Shift():
    # This class describes shifts

    def __init__(self):
        self.shift_name = ''
        self.required_volunteers = 0


class Period():
    # This class describes periods

    def __init__(self, Name, RequiredVolunteers):
        self.Name = Name
        self.RequiredVolunteers = RequiredVolunteers