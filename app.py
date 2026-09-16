import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="SupportDesk | Gestión de Tickets",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CLASE TICKET
# =========================================================

class TicketSoporte:

    PRIORIDADES = ["Baja", "Media", "Alta", "Crítica"]
    ESTADOS = ["Abierto", "En proceso", "Resuelto", "Cerrado"]

    def __init__(
        self,
        codigo,
        usuario,
        descripcion,
        prioridad,
        tecnico="Sin asignar"
    ):
        self.codigo = codigo
        self.usuario = usuario
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.estado = "Abierto"
        self.tecnico = tecnico
        self.fecha_creacion = datetime.now()


# =========================================================
# CLASE GESTOR
# =========================================================

class GestorTickets:

    def __init__(self):
        self.tickets = {}


    # CREATE
    def crear_ticket(
        self,
        codigo,
        usuario,
        descripcion,
        prioridad,
        tecnico
    ):

        codigo = codigo.strip().upper()
        usuario = usuario.strip()
        descripcion = descripcion.strip()
        tecnico = tecnico.strip()

        if codigo == "":
            return False, "El código no puede estar vacío."

        if codigo in self.tickets:
            return False, "Ya existe un ticket con ese código."

        if usuario == "":
            return False, "El usuario no puede estar vacío."

        if descripcion == "":
            return False, "La descripción no puede estar vacía."

        if prioridad not in TicketSoporte.PRIORIDADES:
            return False, "Prioridad no válida."

        if tecnico == "":
            tecnico = "Sin asignar"

        ticket = TicketSoporte(
            codigo,
            usuario,
            descripcion,
            prioridad,
            tecnico
        )

        self.tickets[codigo] = ticket

        return True, "Ticket registrado correctamente."


    # READ
    def buscar_ticket(self, codigo):
        return self.tickets.get(codigo.strip().upper())


    def listar_tickets(self):
        return list(self.tickets.values())


    # UPDATE
    def actualizar_ticket(
        self,
        codigo,
        usuario,
        descripcion,
        prioridad,
        estado,
        tecnico
    ):

        ticket = self.tickets.get(codigo)

        if not ticket:
            return False, "Ticket no encontrado."

        if usuario.strip() == "":
            return False, "El usuario no puede estar vacío."

        if descripcion.strip() == "":
            return False, "La descripción no puede estar vacía."

        if prioridad not in TicketSoporte.PRIORIDADES:
            return False, "Prioridad no válida."

        if estado not in TicketSoporte.ESTADOS:
            return False, "Estado no válido."

        ticket.usuario = usuario.strip()
        ticket.descripcion = descripcion.strip()
        ticket.prioridad = prioridad
        ticket.estado = estado
        ticket.tecnico = (
            tecnico.strip()
            if tecnico.strip()
            else "Sin asignar"
        )

        return True, "Ticket actualizado correctamente."


    # DELETE
    def eliminar_ticket(self, codigo):

        if codigo in self.tickets:
            del self.tickets[codigo]
            return True, "Ticket eliminado correctamente."

        return False, "Ticket no encontrado."


# =========================================================
# SESSION STATE
# =========================================================

if "gestor" not in st.session_state:
    st.session_state.gestor = GestorTickets()

gestor = st.session_state.gestor


# =========================================================
# ESTILOS CSS GENERALES
# =========================================================

st.markdown(
    """
    <style>

    /* ========================================
       FUENTE Y VARIABLES
    ======================================== */

    :root {
        --navy: #081B2C;
        --blue-dark: #123A63;
        --blue: #1976D2;
        --cyan: #21C7D9;
        --background: #F4F7FB;
        --white: #FFFFFF;
        --text: #172B3A;
        --muted: #6C7E8E;
        --border: #DCE6EF;
    }


    /* ========================================
       FONDO GENERAL
    ======================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 90% 5%,
                rgba(33, 199, 217, 0.07),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #F8FAFD 0%,
                #F2F6FA 100%
            );

        color: var(--text);
    }


    /* ========================================
       CONTENEDOR PRINCIPAL
    ======================================== */

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }


    /* ========================================
       SIDEBAR
    ======================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #071827 0%,
                #0B2741 45%,
                #123A63 100%
            );
        border-right: 1px solid rgba(255,255,255,0.08);
        box-shadow: 10px 0px 35px rgba(7, 24, 39, 0.10);
    }


    section[data-testid="stSidebar"] * {
        color: white;
    }


    section[data-testid="stSidebar"] .stRadio label {

        padding: 9px 12px;
        border-radius: 9px;
        transition: all 0.25s ease;
    }


    section[data-testid="stSidebar"] .stRadio label:hover {

        background: rgba(33, 199, 217, 0.12);
        transform: translateX(4px);
    }


    /* ========================================
       TÍTULOS
    ======================================== */

    h1, h2, h3 {
        color: #102F4B;
        font-weight: 700;
        letter-spacing: -0.02em;
    }


    /* ========================================
       TARJETAS
    ======================================== */

    .enterprise-card {

        background: rgba(255,255,255,0.95);

        border: 1px solid rgba(18,58,99,0.08);

        border-radius: 16px;

        padding: 22px;

        box-shadow:
            0 10px 35px rgba(25, 59, 92, 0.07);

        transition:
            transform 0.30s ease,
            box-shadow 0.30s ease,
            border 0.30s ease;

        position: relative;
        overflow: hidden;
    }


    .enterprise-card::before {

        content: "";

        position: absolute;

        width: 120px;
        height: 120px;

        top: -70px;
        right: -70px;

        background:
            radial-gradient(
                circle,
                rgba(33,199,217,0.20),
                transparent 70%
            );

        transition: all 0.35s ease;
    }


    .enterprise-card:hover {

        transform: translateY(-5px);

        box-shadow:
            0 18px 45px rgba(25,118,210,0.12);

        border:
            1px solid rgba(33,199,217,0.28);
    }


    .enterprise-card:hover::before {

        width: 180px;
        height: 180px;
    }


    /* ========================================
       KPI
    ======================================== */

    .kpi-title {

        font-size: 13px;

        color: #6C7E8E;

        text-transform: uppercase;

        letter-spacing: 1px;

        font-weight: 600;
    }


    .kpi-value {

        margin-top: 8px;

        font-size: 34px;

        font-weight: 700;

        color: #123A63;
    }


    .kpi-line {

        margin-top: 14px;

        width: 42px;
        height: 3px;

        border-radius: 10px;

        background:
            linear-gradient(
                90deg,
                #1976D2,
                #21C7D9
            );
    }


    /* ========================================
       FORMULARIOS
    ======================================== */

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {

        border-radius: 10px !important;

        border: 1px solid #D5E0EA;

        transition:
            border 0.25s ease,
            box-shadow 0.25s ease;
    }


    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within {

        border:
            1px solid #21C7D9 !important;

        box-shadow:
            0 0 0 3px rgba(33,199,217,0.10);
    }


    /* ========================================
       SELECTBOX
    ======================================== */

    div[data-baseweb="select"] > div {

        border-radius: 10px;

        transition: all 0.25s ease;
    }


    div[data-baseweb="select"] > div:hover {

        border-color: #21C7D9;

        box-shadow:
            0 0 0 3px rgba(33,199,217,0.08);
    }


    /* ========================================
       BOTONES
    ======================================== */

    div.stButton > button,
    div.stFormSubmitButton > button {

        border: none;

        border-radius: 10px;

        padding: 0.60rem 1.4rem;

        font-weight: 600;

        color: white;

        background:
            linear-gradient(
                100deg,
                #123A63 0%,
                #1976D2 55%,
                #21C7D9 100%
            );

        box-shadow:
            0 5px 18px rgba(25,118,210,0.18);

        transition:
            transform 0.20s ease,
            box-shadow 0.25s ease,
            filter 0.25s ease;
    }


    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 10px 28px rgba(25,118,210,0.28);

        filter: brightness(1.07);
    }


    div.stButton > button:active,
    div.stFormSubmitButton > button:active {

        transform: scale(0.98);
    }


    /* ========================================
       DATAFRAME
    ======================================== */

    [data-testid="stDataFrame"] {

        background: white;

        border-radius: 14px;

        padding: 5px;

        box-shadow:
            0 10px 32px rgba(25,59,92,0.06);

        border:
            1px solid rgba(18,58,99,0.07);
    }


    /* ========================================
       ALERTAS
    ======================================== */

    div[data-testid="stAlert"] {

        border-radius: 11px;

        border-left-width: 4px;

        box-shadow:
            0 5px 18px rgba(0,0,0,0.04);
    }


    /* ========================================
       SEPARADORES
    ======================================== */

    hr {

        border: none;

        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(18,58,99,0.18),
                transparent
            );
    }


    /* ========================================
       ANIMACIÓN DE ENTRADA
    ======================================== */

    @keyframes fadeUp {

        from {
            opacity: 0;
            transform: translateY(15px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }


    .block-container {

        animation:
            fadeUp 0.55s ease-out;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER HTML + CSS + JAVASCRIPT
# =========================================================

components.html(
    """
    <html>

    <head>

    <style>

    * {
        box-sizing: border-box;
    }


    body {

        margin: 0;

        background: transparent;

        font-family:
            Arial,
            Helvetica,
            sans-serif;
    }


    #hero {

        position: relative;

        overflow: hidden;

        min-height: 190px;

        border-radius: 20px;

        padding: 35px 42px;

        display: flex;

        align-items: center;

        background:
            linear-gradient(
                120deg,
                #071827 0%,
                #0D2D4B 42%,
                #124D78 100%
            );

        box-shadow:
            0 20px 55px rgba(8,27,44,0.25);

        color: white;

        cursor: default;
    }


    #light {

        position: absolute;

        width: 320px;
        height: 320px;

        border-radius: 50%;

        pointer-events: none;

        transform:
            translate(-50%, -50%);

        background:
            radial-gradient(
                circle,
                rgba(33,199,217,0.25) 0%,
                rgba(25,118,210,0.13) 30%,
                transparent 68%
            );

        transition:
            opacity 0.15s ease;

        opacity: 0;
    }


    .grid {

        position: absolute;

        inset: 0;

        opacity: 0.07;

        background-image:
            linear-gradient(
                rgba(255,255,255,0.5) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(255,255,255,0.5) 1px,
                transparent 1px
            );

        background-size:
            30px 30px;
    }


    .content {

        position: relative;

        z-index: 5;
    }


    .eyebrow {

        font-size: 12px;

        letter-spacing: 2.5px;

        text-transform: uppercase;

        color: #6DE1E9;

        font-weight: 700;

        margin-bottom: 10px;
    }


    h1 {

        margin: 0;

        font-size: 34px;

        font-weight: 700;

        letter-spacing: -0.5px;
    }


    p {

        margin-top: 12px;

        margin-bottom: 0;

        max-width: 760px;

        line-height: 1.55;

        color: rgba(255,255,255,0.76);

        font-size: 14px;
    }


    .badge {

        display: inline-block;

        margin-top: 18px;

        padding: 7px 12px;

        border-radius: 100px;

        border:
            1px solid rgba(109,225,233,0.25);

        background:
            rgba(33,199,217,0.08);

        color: #9EF5FA;

        font-size: 12px;
    }


    .pulse {

        display: inline-block;

        width: 7px;
        height: 7px;

        margin-right: 7px;

        border-radius: 50%;

        background: #49E7C6;

        box-shadow:
            0 0 0 rgba(73,231,198,0.5);

        animation:
            pulse 2s infinite;
    }


    @keyframes pulse {

        0% {
            box-shadow:
                0 0 0 0
                rgba(73,231,198,0.45);
        }

        70% {
            box-shadow:
                0 0 0 9px
                rgba(73,231,198,0);
        }

        100% {
            box-shadow:
                0 0 0 0
                rgba(73,231,198,0);
        }
    }

    </style>

    </head>


    <body>

        <div id="hero">

            <div class="grid"></div>

            <div id="light"></div>

            <div class="content">

                <div class="eyebrow">
                    IT SERVICE MANAGEMENT
                </div>

                <h1>
                    SupportDesk
                </h1>

                <p>
                    Plataforma centralizada para registrar,
                    administrar y dar seguimiento a solicitudes
                    de soporte técnico mediante un flujo CRUD.
                </p>

                <div class="badge">

                    <span class="pulse"></span>

                    Sistema operativo

                </div>

            </div>

        </div>


        <script>

        const hero =
            document.getElementById("hero");

        const light =
            document.getElementById("light");


        hero.addEventListener(
            "mousemove",
            function(event) {

                const rect =
                    hero.getBoundingClientRect();

                const x =
                    event.clientX - rect.left;

                const y =
                    event.clientY - rect.top;

                light.style.left =
                    x + "px";

                light.style.top =
                    y + "px";

                light.style.opacity =
                    "1";
            }
        );


        hero.addEventListener(
            "mouseleave",
            function() {

                light.style.opacity =
                    "0";
            }
        );

        </script>

    </body>

    </html>
    """,
    height=220
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            padding: 10px 5px 22px 5px;
        ">

            <div style="
                font-size: 22px;
                font-weight: 700;
                letter-spacing: -0.5px;
            ">
                SupportDesk
            </div>

            <div style="
                font-size: 12px;
                opacity: 0.65;
                margin-top: 4px;
            ">
                Gestión de soporte técnico
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    opcion = st.radio(
        "Navegación",
        [
            "Panel principal",
            "Crear ticket",
            "Consultar tickets",
            "Actualizar ticket",
            "Eliminar ticket"
        ]
    )

    st.markdown("---")

    st.caption(
        "Python · POO · CRUD · Streamlit"
    )


# =========================================================
# FUNCIONES DE INTERFAZ
# =========================================================

def tarjeta_kpi(titulo, valor):

    return f"""
    <div class="enterprise-card">

        <div class="kpi-title">
            {titulo}
        </div>

        <div class="kpi-value">
            {valor}
        </div>

        <div class="kpi-line"></div>

    </div>
    """


def tickets_dataframe(tickets):

    datos = []

    for ticket in tickets:

        datos.append({

            "Código":
                ticket.codigo,

            "Usuario":
                ticket.usuario,

            "Descripción":
                ticket.descripcion,

            "Prioridad":
                ticket.prioridad,

            "Estado":
                ticket.estado,

            "Técnico":
                ticket.tecnico,

            "Fecha":
                ticket.fecha_creacion.strftime(
                    "%d/%m/%Y %H:%M"
                )

        })

    return pd.DataFrame(datos)


# =========================================================
# PANEL PRINCIPAL
# =========================================================

if opcion == "Panel principal":

    st.subheader(
        "Panel de control"
    )

    st.caption(
        "Resumen general de las solicitudes de soporte."
    )

    tickets = gestor.listar_tickets()

    total = len(tickets)

    abiertos = sum(
        ticket.estado == "Abierto"
        for ticket in tickets
    )

    proceso = sum(
        ticket.estado == "En proceso"
        for ticket in tickets
    )

    resueltos = sum(
        ticket.estado == "Resuelto"
        for ticket in tickets
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:
        st.markdown(
            tarjeta_kpi(
                "Total tickets",
                total
            ),
            unsafe_allow_html=True
        )


    with col2:
        st.markdown(
            tarjeta_kpi(
                "Abiertos",
                abiertos
            ),
            unsafe_allow_html=True
        )


    with col3:
        st.markdown(
            tarjeta_kpi(
                "En proceso",
                proceso
            ),
            unsafe_allow_html=True
        )


    with col4:
        st.markdown(
            tarjeta_kpi(
                "Resueltos",
                resueltos
            ),
            unsafe_allow_html=True
        )


    st.write("")
    st.write("")

    st.subheader(
        "Tickets registrados"
    )


    if tickets:

        df = tickets_dataframe(tickets)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No existen tickets registrados. "
            "Puede crear el primero desde el menú lateral."
        )


# =========================================================
# CREATE
# =========================================================

elif opcion == "Crear ticket":

    st.subheader(
        "Crear nuevo ticket"
    )

    st.caption(
        "Registre una nueva solicitud de soporte técnico."
    )


    with st.form(
        "form_crear",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)


        with col1:

            codigo = st.text_input(
                "Código del ticket",
                placeholder="Ejemplo: TK001"
            )

            usuario = st.text_input(
                "Usuario solicitante",
                placeholder="Nombre del usuario"
            )


        with col2:

            prioridad = st.selectbox(
                "Prioridad",
                TicketSoporte.PRIORIDADES
            )

            tecnico = st.text_input(
                "Técnico asignado",
                placeholder="Opcional"
            )


        descripcion = st.text_area(
            "Descripción del problema",
            placeholder=(
                "Describa de manera breve "
                "el incidente o requerimiento..."
            ),
            height=130
        )


        guardar = st.form_submit_button(
            "Registrar ticket"
        )


    if guardar:

        resultado, mensaje = gestor.crear_ticket(
            codigo,
            usuario,
            descripcion,
            prioridad,
            tecnico
        )


        if resultado:
            st.success(mensaje)

        else:
            st.error(mensaje)


# =========================================================
# READ
# =========================================================

elif opcion == "Consultar tickets":

    st.subheader(
        "Consultar tickets"
    )

    st.caption(
        "Visualice todos los registros o "
        "localice un ticket específico."
    )


    tipo = st.radio(
        "Tipo de consulta",
        [
            "Todos los tickets",
            "Buscar por código"
        ],
        horizontal=True
    )


    if tipo == "Todos los tickets":

        tickets = gestor.listar_tickets()

        if tickets:

            df = tickets_dataframe(
                tickets
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No existen tickets registrados."
            )


    else:

        col1, col2 = st.columns(
            [3, 1]
        )


        with col1:

            codigo_busqueda = st.text_input(
                "Código del ticket",
                placeholder="Ejemplo: TK001"
            )


        with col2:

            st.write("")

            st.write("")

            buscar = st.button(
                "Buscar ticket",
                use_container_width=True
            )


        if buscar:

            ticket = gestor.buscar_ticket(
                codigo_busqueda
            )


            if ticket:

                st.success(
                    "Ticket localizado correctamente."
                )


                st.markdown(
                    f"""
                    <div class="enterprise-card">

                        <div style="
                            display:flex;
                            justify-content:
                            space-between;
                            align-items:center;
                            margin-bottom:20px;
                        ">

                            <div>

                                <div style="
                                    font-size:13px;
                                    color:#6C7E8E;
                                ">
                                    TICKET
                                </div>

                                <div style="
                                    font-size:25px;
                                    font-weight:700;
                                    color:#123A63;
                                ">
                                    {ticket.codigo}
                                </div>

                            </div>

                            <div style="
                                padding:7px 14px;
                                border-radius:100px;
                                background:
                                    rgba(25,118,210,0.08);
                                color:#1976D2;
                                font-weight:600;
                                font-size:13px;
                            ">
                                {ticket.estado}
                            </div>

                        </div>


                        <div style="
                            display:grid;
                            grid-template-columns:
                                repeat(2, 1fr);
                            gap:18px;
                        ">

                            <div>
                                <b>Usuario</b><br>
                                {ticket.usuario}
                            </div>

                            <div>
                                <b>Prioridad</b><br>
                                {ticket.prioridad}
                            </div>

                            <div>
                                <b>Técnico</b><br>
                                {ticket.tecnico}
                            </div>

                            <div>
                                <b>Fecha</b><br>
                                {
                                    ticket.fecha_creacion.strftime(
                                        "%d/%m/%Y %H:%M"
                                    )
                                }
                            </div>

                        </div>


                        <div style="
                            margin-top:20px;
                        ">

                            <b>
                                Descripción
                            </b>

                            <div style="
                                color:#5D7182;
                                margin-top:5px;
                                line-height:1.5;
                            ">
                                {ticket.descripcion}
                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            else:

                st.error(
                    "No existe un ticket "
                    "con ese código."
                )


# =========================================================
# UPDATE
# =========================================================

elif opcion == "Actualizar ticket":

    st.subheader(
        "Actualizar ticket"
    )

    st.caption(
        "Modifique la información y "
        "el estado de una solicitud existente."
    )


    if not gestor.tickets:

        st.info(
            "No existen tickets disponibles "
            "para actualizar."
        )


    else:

        codigo = st.selectbox(
            "Seleccione un ticket",
            list(gestor.tickets.keys())
        )


        ticket = gestor.buscar_ticket(
            codigo
        )


        with st.form(
            "form_actualizar"
        ):

            col1, col2 = st.columns(2)


            with col1:

                usuario = st.text_input(
                    "Usuario",
                    value=ticket.usuario
                )

                prioridad = st.selectbox(
                    "Prioridad",
                    TicketSoporte.PRIORIDADES,
                    index=(
                        TicketSoporte.PRIORIDADES
                        .index(ticket.prioridad)
                    )
                )


            with col2:

                tecnico = st.text_input(
                    "Técnico",
                    value=ticket.tecnico
                )

                estado = st.selectbox(
                    "Estado",
                    TicketSoporte.ESTADOS,
                    index=(
                        TicketSoporte.ESTADOS
                        .index(ticket.estado)
                    )
                )


            descripcion = st.text_area(
                "Descripción",
                value=ticket.descripcion,
                height=130
            )


            actualizar = (
                st.form_submit_button(
                    "Guardar cambios"
                )
            )


        if actualizar:

            resultado, mensaje = (
                gestor.actualizar_ticket(
                    codigo,
                    usuario,
                    descripcion,
                    prioridad,
                    estado,
                    tecnico
                )
            )


            if resultado:
                st.success(mensaje)

            else:
                st.error(mensaje)


# =========================================================
# DELETE
# =========================================================

elif opcion == "Eliminar ticket":

    st.subheader(
        "Eliminar ticket"
    )

    st.caption(
        "Elimine definitivamente "
        "un registro del sistema."
    )


    if not gestor.tickets:

        st.info(
            "No existen tickets disponibles "
            "para eliminar."
        )


    else:

        codigo = st.selectbox(
            "Seleccione un ticket",
            list(gestor.tickets.keys())
        )


        ticket = gestor.buscar_ticket(
            codigo
        )


        st.markdown(
            f"""
            <div class="enterprise-card">

                <div style="
                    font-size:13px;
                    color:#6C7E8E;
                    margin-bottom:6px;
                ">
                    TICKET SELECCIONADO
                </div>

                <div style="
                    font-size:24px;
                    font-weight:700;
                    color:#123A63;
                ">
                    {ticket.codigo}
                </div>

                <div style="
                    margin-top:10px;
                    color:#5D7182;
                ">
                    {ticket.usuario}
                    ·
                    {ticket.prioridad}
                    ·
                    {ticket.estado}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.write("")


        confirmar = st.checkbox(
            "Confirmo que deseo eliminar "
            "permanentemente este ticket."
        )


        if st.button(
            "Eliminar ticket"
        ):

            if confirmar:

                resultado, mensaje = (
                    gestor.eliminar_ticket(
                        codigo
                    )
                )


                if resultado:

                    st.success(
                        mensaje
                    )

                    st.rerun()


                else:

                    st.error(
                        mensaje
                    )


            else:

                st.warning(
                    "Debe confirmar la eliminación."
                )
