import streamlit as st
from datetime import datetime


# =========================================================
# CONFIGURACIÓN DE LA APP
# =========================================================

st.set_page_config(
    page_title="Sistema de Soporte Técnico",
    page_icon="🛠️",
    layout="wide"
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
# CLASE GESTOR DE TICKETS
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

        codigo = codigo.strip()
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

        return True, "Ticket creado correctamente."


    # READ
    def buscar_ticket(self, codigo):

        return self.tickets.get(codigo)


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

        ticket.usuario = usuario
        ticket.descripcion = descripcion
        ticket.prioridad = prioridad
        ticket.estado = estado
        ticket.tecnico = tecnico if tecnico.strip() else "Sin asignar"

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
# ENCABEZADO
# =========================================================

st.title("🛠️ Sistema de Soporte Técnico")

st.write(
    """
    Aplicación para gestionar solicitudes de soporte mediante
    operaciones **CRUD: Crear, Consultar, Actualizar y Eliminar tickets**.
    """
)

st.divider()


# =========================================================
# MENÚ LATERAL
# =========================================================

opcion = st.sidebar.radio(
    "Menú",
    [
        "Inicio",
        "Crear ticket",
        "Consultar tickets",
        "Actualizar ticket",
        "Eliminar ticket"
    ]
)


# =========================================================
# INICIO
# =========================================================

if opcion == "Inicio":

    st.subheader("Panel principal")

    tickets = gestor.listar_tickets()

    total = len(tickets)

    abiertos = len([
        t for t in tickets
        if t.estado == "Abierto"
    ])

    proceso = len([
        t for t in tickets
        if t.estado == "En proceso"
    ])

    resueltos = len([
        t for t in tickets
        if t.estado == "Resuelto"
    ])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total tickets", total)

    col2.metric("Abiertos", abiertos)

    col3.metric("En proceso", proceso)

    col4.metric("Resueltos", resueltos)


    st.subheader("Tickets recientes")

    if tickets:

        datos = []

        for ticket in tickets:

            datos.append({
                "Código": ticket.codigo,
                "Usuario": ticket.usuario,
                "Prioridad": ticket.prioridad,
                "Estado": ticket.estado,
                "Técnico": ticket.tecnico,
                "Fecha": ticket.fecha_creacion.strftime(
                    "%d/%m/%Y %H:%M"
                )
            })

        st.dataframe(
            datos,
            use_container_width=True
        )

    else:

        st.info(
            "Todavía no existen tickets registrados."
        )


# =========================================================
# CREATE
# =========================================================

elif opcion == "Crear ticket":

    st.subheader("➕ Crear nuevo ticket")

    with st.form("form_crear_ticket"):

        codigo = st.text_input(
            "Código del ticket",
            placeholder="Ejemplo: TK001"
        )

        usuario = st.text_input(
            "Usuario solicitante",
            placeholder="Ejemplo: Carlos Carrillo"
        )

        descripcion = st.text_area(
            "Descripción del problema",
            placeholder="Describa el problema técnico..."
        )

        prioridad = st.selectbox(
            "Prioridad",
            TicketSoporte.PRIORIDADES
        )

        tecnico = st.text_input(
            "Técnico asignado",
            placeholder="Opcional"
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

    st.subheader("🔎 Consultar tickets")


    tipo_consulta = st.radio(
        "Seleccione una opción",
        [
            "Mostrar todos",
            "Buscar por código"
        ],
        horizontal=True
    )


    # -----------------------
    # MOSTRAR TODOS
    # -----------------------

    if tipo_consulta == "Mostrar todos":

        tickets = gestor.listar_tickets()

        if tickets:

            datos = []

            for ticket in tickets:

                datos.append({

                    "Código": ticket.codigo,

                    "Usuario": ticket.usuario,

                    "Descripción": ticket.descripcion,

                    "Prioridad": ticket.prioridad,

                    "Estado": ticket.estado,

                    "Técnico": ticket.tecnico,

                    "Fecha": ticket.fecha_creacion.strftime(
                        "%d/%m/%Y %H:%M"
                    )

                })

            st.dataframe(
                datos,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No existen tickets registrados."
            )


    # -----------------------
    # BUSCAR POR CÓDIGO
    # -----------------------

    else:

        codigo_busqueda = st.text_input(
            "Ingrese el código del ticket"
        )

        if st.button("Buscar"):

            ticket = gestor.buscar_ticket(
                codigo_busqueda
            )

            if ticket:

                st.success(
                    "Ticket encontrado"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        "**Código:**",
                        ticket.codigo
                    )

                    st.write(
                        "**Usuario:**",
                        ticket.usuario
                    )

                    st.write(
                        "**Prioridad:**",
                        ticket.prioridad
                    )


                with col2:

                    st.write(
                        "**Estado:**",
                        ticket.estado
                    )

                    st.write(
                        "**Técnico:**",
                        ticket.tecnico
                    )

                    st.write(
                        "**Fecha:**",
                        ticket.fecha_creacion.strftime(
                            "%d/%m/%Y %H:%M"
                        )
                    )


                st.write(
                    "**Descripción del problema:**"
                )

                st.info(
                    ticket.descripcion
                )

            else:

                st.error(
                    "Ticket no encontrado."
                )


# =========================================================
# UPDATE
# =========================================================

elif opcion == "Actualizar ticket":

    st.subheader("✏️ Actualizar ticket")

    if len(gestor.tickets) == 0:

        st.info(
            "No existen tickets para actualizar."
        )

    else:

        codigos = list(
            gestor.tickets.keys()
        )

        codigo = st.selectbox(
            "Seleccione un ticket",
            codigos
        )

        ticket = gestor.buscar_ticket(
            codigo
        )


        with st.form("form_actualizar"):

            usuario = st.text_input(
                "Usuario",
                value=ticket.usuario
            )

            descripcion = st.text_area(
                "Descripción",
                value=ticket.descripcion
            )


            prioridad = st.selectbox(
                "Prioridad",
                TicketSoporte.PRIORIDADES,
                index=TicketSoporte.PRIORIDADES.index(
                    ticket.prioridad
                )
            )


            estado = st.selectbox(
                "Estado",
                TicketSoporte.ESTADOS,
                index=TicketSoporte.ESTADOS.index(
                    ticket.estado
                )
            )


            tecnico = st.text_input(
                "Técnico asignado",
                value=ticket.tecnico
            )


            actualizar = st.form_submit_button(
                "Actualizar ticket"
            )


        if actualizar:

            resultado, mensaje = gestor.actualizar_ticket(
                codigo,
                usuario,
                descripcion,
                prioridad,
                estado,
                tecnico
            )

            if resultado:

                st.success(mensaje)

            else:

                st.error(mensaje)


# =========================================================
# DELETE
# =========================================================

elif opcion == "Eliminar ticket":

    st.subheader("🗑️ Eliminar ticket")


    if len(gestor.tickets) == 0:

        st.info(
            "No existen tickets para eliminar."
        )


    else:

        codigo = st.selectbox(
            "Seleccione el ticket",
            list(gestor.tickets.keys())
        )


        ticket = gestor.buscar_ticket(
            codigo
        )


        st.warning(
            f"""
            Está a punto de eliminar el ticket **{ticket.codigo}**
            correspondiente al usuario **{ticket.usuario}**.
            """
        )


        confirmar = st.checkbox(
            "Confirmo que deseo eliminar este ticket"
        )


        if st.button(
            "Eliminar ticket",
            type="primary"
        ):

            if confirmar:

                resultado, mensaje = gestor.eliminar_ticket(
                    codigo
                )

                if resultado:

                    st.success(mensaje)

                    st.rerun()

                else:

                    st.error(mensaje)

            else:

                st.warning(
                    "Debe confirmar la eliminación."
                )