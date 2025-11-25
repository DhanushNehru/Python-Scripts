def get_positive_integer(prompt: str) -> int:
    """Prompt the user to enter a positive integer."""
    
    valid_input: bool = False
    while not valid_input:
        print(prompt)
        try:
            value: int = int(input())
            if value <= 0:
                print("Please enter a positive integer.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def calculate_dhondt_seats(results: list[tuple[str, int]], num_seats: int) -> dict[str, int]:
    """Calculate the number of seats allocated to each party using the D'Hondt method."""
    
    seats_allocated: dict[str, int] = {party: 0 for party, _ in results}
    votes: dict[str, int] = {party: votes for party, votes in results}
    
    for _ in range(num_seats):
        # Calculate the highest quotient for each party
        quotients: dict[str, float] = {
            party: votes[party] / (seats_allocated[party] + 1) for party in votes
        }
        # Find the party with the highest quotient
        winning_party: str = max(quotients, key=lambda party: quotients[party])
        # Allocate a seat to that party
        seats_allocated[winning_party] += 1
    
    return seats_allocated
    