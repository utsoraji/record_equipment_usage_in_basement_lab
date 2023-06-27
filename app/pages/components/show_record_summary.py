import streamlit as st

from app.datastore.protocol import NewUsageRecord
from app.model.usage_record import UsageRecord


def show_record_summary(record: UsageRecord | NewUsageRecord) -> None:
    if len(record.equipments) == 0:
        st.write("No Equipments are selected.")
    else:
        st.write("Equipments:")
        for eq in record.equipments:
            st.write(f"+ {eq.name}")
    st.text(f"Start at:{record.starting}")
