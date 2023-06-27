from collections import OrderedDict
from typing import Iterable

import streamlit as st
from streamlit_pills import pills

import app.session as session
from app.model.equipment import Equipment


def eqipments_grid(
    equipments: Iterable[Equipment], key: str, column_count: int = 4
) -> list[Equipment]:
    # filter by location
    rooms = list(set(eq.location for eq in equipments))
    rooms.sort()
    selected_rooms: list[str] = pills("Select equipments to use", rooms)

    def location_filer(eq: Equipment) -> bool:
        return eq.location in selected_rooms

    selected: list[Equipment] = st.session_state.get(key, [])
    check_states: OrderedDict[str, bool] = OrderedDict(
        {eq.id: True for eq in selected}
    )  # add selected # sustain selection order

    cols = st.columns(column_count)
    for idx, eq in enumerate(eq for eq in equipments if location_filer(eq)):
        col = cols[idx % column_count]
        image = session.get_svcs().static_resource_provider.get_image(eq.image_id)
        col.image(image)
        check_states[eq.id] = col.checkbox(
            eq.name, value=check_states.get(eq.id, False)
        )

    # add in order of selection
    eq_dict = {eq.id: eq for eq in equipments}
    selected = [eq_dict[id] for id in check_states.keys() if check_states[id]]

    st.session_state[key] = selected

    return selected
