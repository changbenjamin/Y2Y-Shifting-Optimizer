from ortools.sat.python import cp_model

def BuildModel(IndividualVolunteers, Shifts):
    # This function builds the constraint programming model for the problem
    # Inputs:
    #   IndividualVolunteers = a list of volunteer objects.
    #   Shifts = a dictionary of shift objects, indexed by shift names
    # Outputs:
    #   model = a CP model object populated with decision variables, constraints, and an objective.

    # Instantiate the CP model
    model = cp_model.CpModel()

    # Create the model variables
    # Primary decision variables
    assignment = {}
    for v in IndividualVolunteers:
        for s in Shifts:
            assignment[(v, s)] = model.NewBoolVar('Volunteer %s assigned to %s shift' % (v.ID_Number, s))

    # Create the constraints
    # Each shift has a maximum number of volunteers assigned to it
    for s in Shifts:
        model.Add(
            sum(assignment[(v, s)] for v in IndividualVolunteers) <= Shifts[s].required_volunteers
        )

    # Each volunteer is assigned to at most one shift
    for v in IndividualVolunteers:
        model.Add(
            sum(assignment[(v, s)] for s in Shifts) <= 1
        )

    # Each volunteer can only be assigned to the one of the shifts they indicated in their preference list
    for v in IndividualVolunteers:
        for s in Shifts:
            if not s in v.PreferredShifts:
                model.Add(
                    assignment[(v, s)] == 0
                )

    # Set the objective
    # Define the weights of the various objectives
    weight = {
        'Maximize the shift coverage': 10,
        'Respect the volunteer preferences': 1,
    }

    # Calculate the scalar required to make everything integer
    scalar = CalcObjectiveScalar(
        Shifts)  # This is multiplied in because the CP solver insists on the data being integer.

    # Define the objective
    model.Maximize(

        # Maximize the number of covered shifts
        weight['Maximize the shift coverage'] *
        sum(
            int(scalar / Shifts[s].required_volunteers) *
            sum(
                assignment[(v, s)]
                for v in IndividualVolunteers
            )
            for s in Shifts
        )

        +

        # Maximize the number of realized shift preference points
        weight['Respect the volunteer preferences'] *
        scalar *
        sum(
            sum(
                assignment[(v, s)] * v.ShiftPreferencePoints[s]
                for v in IndividualVolunteers
            )
            for s in Shifts
        )
    )

    # Return the model
    return (model, assignment)


def CalcObjectiveScalar(Shifts):
    # Get the list of unique "Required Volunteer" numbers
    unique_list = GetUniqueListElements(
        [Shifts[s].required_volunteers for s in Shifts]
    )

    # Calculate the product of this list
    p = ListProd(unique_list)

    # Round the product to an integer
    scalar = int(p)

    # Return the scalar
    return scalar


def ListProd(List):
    # Initialize the product
    p = 1

    # Loop over the elements of the list
    for e in List:
        p = p * e

    return p


def GetUniqueListElements(List):
    # Initialize the list of unique elements
    unique_list = []

    # Loop over the list
    for e in List:

        # Check if it's in the Unique list
        if not e in unique_list:  # it's not there

            # Add it
            unique_list.append(e)

    # Return the unique list
    return unique_list