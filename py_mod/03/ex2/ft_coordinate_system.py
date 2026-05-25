import math


def get_player_pos():
    while True:
        str_gcs = input("Enter new coordinates as floats in format 'x,y,z': ")
        tab_gcs = str_gcs.split(',')
        gcs = []
        i = 0

        try:
            while len(gcs) < 3:
                try:
                    gcs.append(float(tab_gcs[i].strip()))
                except ValueError as e:
                    print(f"Error on parameter '{tab_gcs[i].strip()}': {e}")
                i += 1
        except IndexError:
            print("Invalid syntax")
            continue

        return tuple(gcs)


if __name__ == "__main__":
    print("=== Game Coordinate System ===\n"
          "Get a first set of coordinates\n")
    fc = get_player_pos()
    from_0 = math.sqrt((0-fc[0])**2 + (0-fc[1])**2 + (0-fc[2])**2)
    print(f"Got a first tuple: {fc}\n"
          f"It includes: "
          f"X={fc[0]}, "
          f"Y={fc[1]}, "
          f"Z={fc[2]}"
          f"\nDistance to center: {from_0:.4f}\n"
          )
    print("Get a second set of coordinates:")
    sc = get_player_pos()
    diff = math.sqrt((sc[0]-fc[0])**2 + (sc[1]-fc[1])**2 + (sc[2]-fc[2])**2)
    print(f"Distance between the 2 sets of coordinates: {diff:.4f}")
