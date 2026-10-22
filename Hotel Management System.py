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


def show_who_we_are():
    print("\n" + "=" * 50)
    print("  WHO WE ARE")
    print("=" * 50)

    print("\n--- OUR MISSION ---\n")
    print("To provide an exceptional hotel experience built on comfort,\n"
          "personalized attention and genuine hospitality, making every\n"
          "guest feel valued from the moment they arrive.")

    print("\n--- OUR VISION ---\n")
    print("To be recognized as the leading 5-star hotel in the region,\n"
          "known for excellence in service, elegance and innovation,\n"
          "and for creating memories our guests carry with them.")

    print("\n--- WHY CHOOSE US? ---\n")
    print("  * Luxury and comfort: elegant rooms designed for your rest.")
    print("  * Personalized service: our team attends to every detail.")
    print("  * Options for every traveler: Single, Double and Suite rooms.")
    print("  * Fair prices: 5-star quality at transparent rates.")
    print("  * Easy booking: reserve your room in just a few steps.")
    print()

    input("Press Enter to return to the main menu...")


def show_rooms():
    rooms = load_rooms()
    print("\n--- OUR ROOMS ---\n")
    for room in rooms:
        if room["Active"]:
            print(f"Room {room['Number']} | {room['Type'].capitalize()} | ${room['Price']:.2f} per night")
    print()


def rooms_menu():
    """Submenu shown after the room list is displayed."""
    while True:
        print("[1] BOOK A ROOM\n"
              "[2] RETURN TO MAIN MENU\n")
        option = only_int("WHAT WOULD YOU LIKE TO DO? ")
        if option == 1:
            book_room()
            break
        elif option == 2:
            break
        else:
            print("\nInvalid choice, try again.\n")


def book_room():
    # Placeholder: connect your reservation logic here
    print("\nBooking feature coming soon...\n")


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
        show_who_we_are()
    elif choice == 2:
        show_rooms()
        rooms_menu()
    elif choice == 3:
        log_in()
    elif choice == 4:
        sign_up()
    elif choice == 0:
        end = "  GOODBYE!  "
        print("\n" + "-" * len(end))
        print(end)
        print("-" * len(end))
        break
    else:
        print("\nInvalid choice, try again.\n")