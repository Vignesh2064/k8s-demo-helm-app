#########################
# AUTHOR      : Vigneshwaran S
# DATE        : 17-06-2025
# DESCRIPTION : Python test - Print string in reverse with index
#########################

#input string
a = "abcde"

# Print characters in reverse order with their index
print("Reversed String with Index:")
for i, c in enumerate(a[::-1]):
    print(f"Index: {i}, Character: {c}")

# reversed string
reversed_str = a[::-1]
print("\nReversed String:", reversed_str)
