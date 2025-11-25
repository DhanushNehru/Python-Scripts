import src.utils as utils

# Get data
results: list[tuple[str, int]] = []

## Number of seats to allocate
num_seats: int = utils.get_positive_integer("Enter the number of seats to allocate:")

## Number of parties
num_parties: int = utils.get_positive_integer("Enter the number of parties:")

## Names and votes of each party
for i in range(num_parties):
    party_name: str = input(f"Enter the name of party {i + 1}: ")
    party_votes: int = utils.get_positive_integer(f"Enter the number of votes for {party_name}: ")
    results.append((party_name, party_votes))

# Calculate the seats
seats_allocated: dict[str, int] = utils.calculate_dhondt_seats(results, num_seats)

# Print the result of seats
print("\nSeat allocation results:")
for party, seats in seats_allocated.items():
    print(f"{party}: {seats} seats")
