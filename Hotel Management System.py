import pickle
import json
import os


ROOMS_FILE = "rooms.json"

DEFAULT_ROOMS = [
    {"Number": "101", "Type": "Single", "Price": 70.0, "Active": True},
    {"Number": "102", "Type": "Single", "Price": 70.0, "Active": True},
    {"Number": "103", "Type": "Single", "Price": 70.0, "Active": True},
    {"Number": "104", "Type": "Single", "Price": 70.0, "Active": True},
    {"Number": "105", "Type": "Single", "Price": 70.0, "Active": True},
    {"Number": "201", "Type": "Double", "Price": 110.0, "Active": True},
    {"Number": "301", "Type": "Suite",  "Price": 220.0, "Active": True},
]





def show_rooms():
    rooms = load_rooms()
    print("\n--- OUR ROOMS ---\n")
    for room in rooms:
        if room["Active"]:
            print(f"Room {room['Number']} | {room['Type'].capitalize()} | ${room['Price']:.2f} per night")
    print()

def save_rooms(rooms):
    with open(ROOMS_FILE, "w") as f:
        json.dump(rooms, f, indent=4)


def load_rooms():
    if not os.path.exists(ROOMS_FILE):
        save_rooms(DEFAULT_ROOMS)
    with open(ROOMS_FILE) as f:
        return json.load(f)



def only_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a number.")








#main code
while True:
    title = "  ***** THE VELVET CROWN HOTEL *****  "
    print ("=" * len(title))
    print(title)
    print ("=" * len(title))
    print("\nWelcome to The Velvet Crown Hotel, a 5-star Hotel located at ... \n")
    print("[1] WHO WE ARE?\n"
          "[2] VIEW OUR ROOMS\n"
          "[3] LOG IN\n"
          "[4] SIGN UP\n"
          "[0] EXIT\n")
    choice = only_int("HOW CAN WE HELP YOU TODAY? ")
    if choice == 1:
        ...
    elif choice == 2:
        show_rooms()
    elif choice == 3:
        ...
    elif choice == 4:
        ...
    elif choice == 0:
        end = "  GOODBYE!  "
        print("\n" + "-" * len(end))
        print(end)
        print("-" * len(end))
        break
    else:
        print("\nInvalid choice, try again.\n")