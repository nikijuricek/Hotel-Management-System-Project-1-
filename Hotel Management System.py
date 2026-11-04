import json
import os
from datetime import date, timedelta

import streamlit as st
from PIL import Image

# ---------------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------------
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

PAGES = ["Home", "Who we are", "Rooms", "Log in", "Sign up"]

# Título e icono de la pestaña del navegador.
# Tiene que ser la PRIMERA instrucción de Streamlit del archivo.
st.set_page_config(page_title="Azure Bay Hotel", page_icon="🌊")

# ---------------------------------------------------------------
# PÁGINA ACTUAL
# ---------------------------------------------------------------
# session_state = la "memoria" de Streamlit entre una recarga y otra.
# Aquí guardamos en qué página estamos. Solo se crea la primera vez.
if "page" not in st.session_state:
    st.session_state.page = "Home"


def go_to(page_name):
    st.session_state.page = page_name


# Número de la pestaña activa (0 = Home, 1 = Who we are...)
active = PAGES.index(st.session_state.page)

# ---------------------------------------------------------------
# COLORES Y BARRA SUPERIOR FIJA (CSS)
# ---------------------------------------------------------------
BASE_CSS = """
<style>
/* Colores generales */
.stApp { background-color: #FAF7F2; }
h1, h2, h3, h4, p, label { color: #0B2545; }
hr { border-color: #8FD3C8; }

/* Título grande y centrado (el de cada página) */
h1 {
    text-align: center;
    font-family: Georgia, serif;
    font-size: 2.6rem;
    letter-spacing: 0.2em;
    color: #0B2545;
    padding: 0 0 1rem 0;
}

/* Botones normales (BOOK, LOG IN...) */
.stButton > button { background-color: #1F6F8B; border: none; }
.stButton > button p { color: #FFFFFF; }
.stButton > button:hover { background-color: #C9A24D; }

/* Campos de texto y listas desplegables */
div[data-baseweb="input"], div[data-baseweb="textarea"],
div[data-baseweb="select"] > div { background-color: #F2E8D5; }
input, textarea { color: #0B2545 !important; }

/* Imagen con esquinas redondeadas */
.stImage img { border-radius: 12px; }

/* Ocultar la cabecera por defecto de Streamlit para que no tape nuestra barra */
header[data-testid="stHeader"] { display: none; }

/* Espacio arriba para que el contenido no quede escondido bajo la barra fija.
   Si ves que la barra tapa algo, sube este número. */
.block-container { padding-top: 6rem; }


/* ===========================================================
   BARRA SUPERIOR FIJA (solo el menú)
   =========================================================== */
.st-key-topbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    box-sizing: border-box;
    z-index: 1000;
    background-color: #FAF7F2;
    border-bottom: 3px solid #C9A24D;
    box-shadow: 0 2px 10px rgba(11, 37, 69, 0.15);
    /* Los márgenes laterales hacen que el menú tenga el mismo ancho
       que el contenido de la página (46rem) y quede centrado. */
    padding: 0.8rem max(1rem, calc(50% - 23rem));
}

/* Todos los contenedores del menú ocupan el 100 % del ancho de su columna */
.st-key-topbar [data-testid="stElementContainer"],
.st-key-topbar [data-testid="stButton"],
.st-key-topbar .stButton {
    width: 100% !important;
    margin: 0;
}

/* Fila de columnas: una sola línea, mismo hueco entre botones, centrada en vertical */
.st-key-topbar [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    align-items: center;
    gap: 0.75rem;
}

/* Cada columna mide lo mismo */
.st-key-topbar [data-testid="stColumn"],
.st-key-topbar [data-testid="column"] {
    flex: 1 1 0 !important;
    min-width: 0 !important;
    width: auto !important;
}

/* Botones del menú (inactivos): fondo transparente, letra azul marino */
.st-key-topbar button {
    width: 100%;
    height: 2.6rem;
    min-height: 2.6rem;
    padding: 0 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: transparent !important;
    border: 1px solid #1F6F8B !important;
    border-radius: 999px;
    box-shadow: none !important;
    white-space: nowrap;
}
.st-key-topbar button,
.st-key-topbar button * {
    color: #0B2545 !important;
}
.st-key-topbar button p {
    margin: 0;
    line-height: 1;
    font-size: 0.95rem;
    font-weight: 600;
    text-align: center;
}
/* Al pasar el ratón o hacer clic: fondo verde agua, letra sigue azul marino */
.st-key-topbar button:hover,
.st-key-topbar button:active {
    background-color: #8FD3C8 !important;
}

/* Pantallas pequeñas (móvil) */
@media (max-width: 640px) {
    .st-key-topbar { padding: 0.8rem 0.5rem; }
    .st-key-topbar [data-testid="stHorizontalBlock"] { gap: 0.3rem; }
    .st-key-topbar button { padding: 0 0.1rem; }
    .st-key-topbar button p { font-size: 0.65rem; }
}
</style>
"""

# CSS de la pestaña ACTIVA: se genera con su número (menu_0, menu_1...).
# Va después del CSS base, así que lo sobrescribe: fondo azul y letra blanca.
ACTIVE_CSS = f"""
<style>
.st-key-topbar .st-key-menu_{active} button,
.st-key-topbar .st-key-menu_{active} button:hover,
.st-key-topbar .st-key-menu_{active} button:active {{
    background-color: #1F6F8B !important;
}}
.st-key-topbar .st-key-menu_{active} button,
.st-key-topbar .st-key-menu_{active} button * {{
    color: #FFFFFF !important;
}}
</style>
"""

st.markdown(BASE_CSS + ACTIVE_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------
# FUNCIONES DE ARCHIVOS
# ---------------------------------------------------------------
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
    """Devuelve False si la habitación ya está reservada en esas fechas."""
    for r in load_reservations():
        if r["Room"] == room_number:
            old_in = date.fromisoformat(r["Check_in"])
            old_out = date.fromisoformat(r["Check_out"])
            # Dos reservas se solapan si una empieza antes de que la otra termine
            if check_in < old_out and check_out > old_in:
                return False
    return True


# ---------------------------------------------------------------
# TÍTULO (se llama al principio de cada página, menos en Home)
# ---------------------------------------------------------------
def show_title():
    st.title("AZURE BAY HOTEL")


# ---------------------------------------------------------------
# PÁGINAS (cada una es una función)
# ---------------------------------------------------------------
def page_home():
    # CSS que solo se aplica en Home: la imagen ocupa el ancho
    st.markdown("""
    <style>
    .block-container { max-width: 100%; padding: 4.2rem 0 2rem 0; }
    div[data-testid="stImage"] { width: 100% !important; }
    div[data-testid="stImage"] img { width: 100% !important; height: auto; border-radius: 0; }
    .st-key-home_text { padding: 1rem 4rem; }
    </style>
    """, unsafe_allow_html=True)

    image = Image.open("AzureTitle.png")
    st.image(image)

    # Contenedor con nombre para darle márgenes al texto
    with st.container(key="home_text"):
        st.subheader("Welcome to Azure Bay Hotel")
        st.write("Wake up to the sound of the waves, relax by the infinity pool and "
                 "enjoy the sunset from your own balcony. Browse our rooms and "
                 "book your stay in just a few clicks.")


def page_who_we_are():
    show_title()
    st.header("WHO WE ARE")

    st.subheader("Our mission")
    st.write("To provide an exceptional hotel experience built on comfort, "
             "personalized attention and genuine hospitality, making every "
             "guest feel valued from the moment they arrive.")
    st.divider()

    st.subheader("Our vision")
    st.write("To be recognized as the leading 5-star hotel on the coast, "
             "known for excellence in service, elegance and innovation, "
             "and for creating memories our guests carry with them.")
    st.divider()

    st.subheader("Why choose us?")
    st.markdown("- **Sea views and comfort:** elegant rooms steps away from the bay.\n"
                "- **Personalized service:** our team attends to every detail.\n"
                "- **Options for every traveler:** Single, Double and Suite rooms.\n"
                "- **Fair prices:** 5-star quality at transparent rates.\n"
                "- **Easy booking:** reserve your room in just a few steps.")


def page_rooms():
    show_title()
    st.header("OUR ROOMS")

    rooms = [room for room in load_rooms() if room["Active"]]

    # Una fila con 3 columnas por cada habitación
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

    prices = {room["Number"]: room for room in rooms}
    room_number = st.selectbox(
        "Room:",
        options=list(prices.keys()),
        format_func=lambda n: f"{n} - {prices[n]['Type']} (${prices[n]['Price']:.2f})",
    )

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
    show_title()
    st.header("LOG IN")
    st.text_input("Email address: ", value="", key="login_email")
    st.text_input("Password: ", value="", type="password", key="login_password")
    if st.button("LOG IN"):
        st.info("Log in feature coming soon...")


def page_sign_up():
    show_title()
    st.header("SIGN UP")
    st.text_input("Your name: ", value="", key="signup_name")
    st.text_input("Email address: ", value="", key="signup_email")
    st.text_input("Password: ", value="", type="password", key="signup_password")
    if st.button("SIGN UP"):
        st.info("Sign up feature coming soon...")


# ---------------------------------------------------------------
# MENÚ SUPERIOR (barra fija)
# ---------------------------------------------------------------
with st.container(key="topbar"):
    columns = st.columns(len(PAGES))                      # una columna por página
    for i, (col, name) in enumerate(zip(columns, PAGES)):  # i = 0, 1, 2, 3, 4
        with col:
            # key=f"menu_{i}" -> el CSS usa este nombre para pintar la pestaña activa.
            # on_click ejecuta go_to(name) ANTES de recargar la página.
            st.button(name, key=f"menu_{i}", on_click=go_to, args=(name,))

# ---------------------------------------------------------------
# MOSTRAR LA PÁGINA ELEGIDA
# ---------------------------------------------------------------
page = st.session_state.page

if page == "Home":
    page_home()
elif page == "Who we are":
    page_who_we_are()
elif page == "Rooms":
    page_rooms()
elif page == "Log in":
    page_log_in()
elif page == "Sign up":
    page_sign_up()
