# Example usage
class Horario:
    def __init__(self, arregloDias, arregloHoras):
        self.arregloDias = arregloDias
        self.arregloHoras = arregloHoras

    def __str__(self):
        return f"Horario(arregloDias={self.arregloDias}, arregloHoras={self.arregloHoras})"


def conversionMinutos(time_str):
    """Converts a time string HH:MM to minutes, with input validation."""
    if ':' not in time_str:
        print(f"Invalid time format: {time_str}. Expected format: HH:MM.")
        return None
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def agregaNoTraslapados(arr, new_horario):
    """Adds new_horario to arr if it doesn't overlap with existing horarios by day and hour."""
    # Convert the new_horario's start and end times to minutes
    new_start, new_end = map(conversionMinutos, new_horario.arregloHoras)
    
    for existing_horario in arr:
        # Check for day overlap
        day_overlap = any(day in new_horario.arregloDias for day in existing_horario.arregloDias)
        if not day_overlap:
            # No day overlap, continue to the next existing_horario
            continue
        
        # Convert the existing_horario's start and end times to minutes
        existing_start, existing_end = map(conversionMinutos, existing_horario.arregloHoras)
        
        # Check for time overlap
        if not (new_end <= existing_start or new_start >= existing_end):
            # Overlap detected, do not add new_horario
            return False
    
    # No overlap detected, add new_horario
    arr.append(new_horario)
    return True

Horario1 = Horario([1, 2, 3, 4], ['13:00', '15:00'])
# Horario2 = Horario([1, 2, 3, 4], ['15:00', '17:00'])
# Horario3 = Horario([1, 2, 3, 4], ['17:00', '19:00'])
Horario4 = Horario([5,6], ['14:00', '16:00'])
Horario5 = Horario([1, 2, 3, 4], ['16:00', '18:00'])
arr = []

# agregaNoTraslapados(arr, horario0)
# agregaNoTraslapados(arr, horario1)

agregaNoTraslapados(arr, Horario1)
# agregaNoTraslapados(arr, Horario2)
# agregaNoTraslapados(arr, Horario3)
agregaNoTraslapados(arr, Horario4)
agregaNoTraslapados(arr, Horario5)


print(arr)
def generate_days_dict(arr):
    # Step 1: Initialize the dictionary with days as keys and empty lists as values
    days_dict = {day: [] for day in range(1, 7)}
    
    # Step 2: Iterate over each Horario object in arr
    for horario in arr:
        # Step 3: Iterate over each day in the Horario object's arregloDias
        for day in horario.arregloDias:
            # Step 4: Append the Horario object to the corresponding list in days_dict
            days_dict[day].append(horario.arregloHoras)
    
    # Step 5: Return or print the dictionary
    return days_dict

# Assuming arr is your list of Horario objects
days_dict = generate_days_dict(arr)
print(days_dict)