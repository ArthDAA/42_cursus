def print_days(i):
    if (i != 1):
        print_days(i - 1)
    print(f"Day {i}")

def ft_count_harvest_recursive():
    i = int(input("Days until harvest: "))
    print_days(i)
    print("Harvest time")
