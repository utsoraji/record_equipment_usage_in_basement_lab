from typing import Iterable

import streamlit as st

from app.model.equipment import Equipment


def state_key(eq: Equipment) -> str:
    return f"selected_state_{eq.id}"


def eqipments_grid(
    equipments: Iterable[Equipment], column_count: int = 4
) -> list[Equipment]:
    rooms = list(set(eq.location for eq in equipments))
    selected_rooms: list[str] = st.multiselect(
        "Select equipments to use", rooms, default=rooms
    )
    filter = lambda eq: eq.location in selected_rooms

    cols = st.columns(column_count)

    for idx, eq in enumerate(eq for eq in equipments if filter(eq)):
        col = cols[idx % column_count]
        col.image(eq.image_url, width=150)
        col.checkbox(eq.name, value=False, key=state_key(eq))

    return [eq for eq in equipments if st.session_state[state_key(eq)]]
