from src.utils import get_positive_integer

# Get data
results = []

## Number of seats to allocate
num_seats = get_positive_integer("Enter the number of seats to allocate:")

## Number of parties
num_parties = get_positive_integer("Enter the number of parties:")

## Names and votes of each party
for i in range(num_parties):
    party_name = input(f"Enter the name of party {i + 1}: ")
    party_votes = get_positive_integer(f"Enter the number of votes for {party_name}: ")
    results.append((party_name, party_votes))


# Calculate the seats


# Print the result of seats
