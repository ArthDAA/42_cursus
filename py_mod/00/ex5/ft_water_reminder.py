def ft_water_reminder():
    last_w = int(input("Days since last watering: "))
    if (last_w > 2):
        print("Water the plants!")
    else:
        print("Plants are fine")
