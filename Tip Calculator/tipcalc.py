name = input("What's your name? ")

print(name)

total = float(input("What is your bill sub-total?").replace('$',''))

print(total)

tip_15 = total * 0.15
tip_18 = total * 0.18
tip_20 = total * 0.20

print(f"15% is ${tip_15:.2f}")
print(f"18% is ${tip_18:.2f}")
print(f"20% is ${tip_20:.2f}")
