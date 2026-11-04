import json
import os
from datetime import date, timedelta

import streamlit as st

ROOMS_FILE = "rooms.json"
RESERVATIONS_FILE = "reservations.json"

DEFAULT_ROOMS = [
    {"Number": "101", "Type": "Single", "Price": 70.0, "Active": True},
    {"Number": "102", "Type": "Single", "Price": 70.0, "Active": True},
    {"Number": "103", "Type": "Single", "Price": 70.0, "Active": True},
    {"Number": "104", "Type": "Single", "Price": 70.0, "Active": True},
    {"Number": "105", "Type": "Single", "Price": 70.0, "Active": True},
    {"Number": "201", "Type": "Double", "Price": 110.0, "Active": True},
    {"Number": "301", "Type": "Suite", "Price": 220.0, "Active": True},
]

st.set_page_config(page_title="The Velvet Crown Hotel")


def save_rooms(rooms):
    with open(ROOMS_FILE, "w") as f:
        json.dump(rooms, f, indent=4)


def load_rooms():
    if not os.path.exists(ROOMS_FILE):
        save_rooms(DEFAULT_ROOMS)
    with open(ROOMS_FILE) as f:
        return json.load(f)


def save_reservations(reservations):
    with open(RESERVATIONS_FILE, "w") as f:
        json.dump(reservations, f, indent=4)


def load_reservations():
    if not os.path.exists(RESERVATIONS_FILE):
        return []
    with open(RESERVATIONS_FILE) as f:
        return json.load(f)


def is_available(room_number, check_in, check_out):
    for r in load_reservations():
        if r["Room"] == room_number:
            old_in = date.fromisoformat(r["Check_in"])
            old_out = date.fromisoformat(r["Check_out"])
            if check_in < old_out and check_out > old_in:
                return False
    return True



def page_who_we_are():
    st.header("WHO WE ARE")

    st.subheader("Our mission")
    st.write("To provide an exceptional hotel experience built on comfort, "
             "personalized attention and genuine hospitality, making every "
             "guest feel valued from the moment they arrive.")
    st.divider()

    st.subheader("Our vision")
    st.write("To be recognized as the leading 5-star hotel in the region, "
             "known for excellence in service, elegance and innovation, "
             "and for creating memories our guests carry with them.")
    st.divider()

    st.subheader("Why choose us?")
    st.markdown("- **Luxury and comfort:** elegant rooms designed for your rest.\n"
                "- **Personalized service:** our team attends to every detail.\n"
                "- **Options for every traveler:** Single, Double and Suite rooms.\n"
                "- **Fair prices:** 5-star quality at transparent rates.\n"
                "- **Easy booking:** reserve your room in just a few steps.")


def page_rooms():
    st.header("OUR ROOMS")

    rooms = [room for room in load_rooms() if room["Active"]]

    for room in rooms:
        col1, col2, col3 = st.columns((1, 1, 1))
        with col1:
            st.markdown(f"**Room {room['Number']}**")
        with col2:
            st.text(room["Type"])
        with col3:
            st.text(f"${room['Price']:.2f} per night")

    st.divider()
    st.subheader("BOOK A ROOM")

#SELECT BOX "BOOK A ROOM"
    prices = {room["Number"]: room for room in rooms}
    room_number = st.selectbox(
        "Room:",
        options=list(prices.keys()),
        format_func=lambda n: f"{n} - {prices[n]['Type']} (${prices[n]['Price']:.2f})",
    )

#CALENDARIO (CHECK-IN Y CHECK-OUT)
    col1, col2 = st.columns(2)
    with col1:
        check_in = st.date_input("Check-in:", value=date.today(), min_value=date.today())
    with col2:
        check_out = st.date_input("Check-out:", value=date.today() + timedelta(days=1),
                                  min_value=date.today() + timedelta(days=1))

    guest_name = st.text_input("Your name: ", value="", key="book_name")
    guest_email = st.text_input("Email address: ", value="", key="book_email")

    if st.button("BOOK"):
        if guest_name.strip() == "" or guest_email.strip() == "":
            st.error("Please fill in your name and email.")
        elif check_out <= check_in:
            st.error("Check-out must be after check-in.")
        elif not is_available(room_number, check_in, check_out):
            st.error("Sorry, that room is not available on those dates.")
        else:
            nights = (check_out - check_in).days
            total = nights * prices[room_number]["Price"]

            reservations = load_reservations()
            reservations.append({
                "Room": room_number,
                "Guest": guest_name.strip(),
                "Email": guest_email.strip(),
                "Check_in": check_in.isoformat(),
                "Check_out": check_out.isoformat(),
                "Total": total,
            })
            save_reservations(reservations)

            st.success(f"Booked! Room {room_number} for {nights} night(s). Total: ${total:.2f}")
            st.balloons()


def page_log_in():
    st.header("LOG IN")
    st.text_input("Email address: ", value="", key="login_email")
    st.text_input("Password: ", value="", type="password", key="login_password")
    if st.button("LOG IN"):
        st.info("Log in feature coming soon...")


def page_sign_up():
    st.header("SIGN UP")
    st.text_input("Your name: ", value="", key="signup_name")
    st.text_input("Email address: ", value="", key="signup_email")
    st.text_input("Password: ", value="", type="password", key="signup_password")
    if st.button("SIGN UP"):
        st.info("Sign up feature coming soon...")


#MAIN CODE
st.title("👑 THE VELVET CROWN HOTEL")
st.caption("A 5-star hotel located at ...")


choice = tab1, tab2, tab3, tab4 = st.tabs(["Who we are", "View our rooms", "Log in", "Sign up"])

with tab1:
    page_who_we_are()
with tab2:
    page_rooms()
with tab3:
    page_log_in()
with tab4:
    page_sign_up()
