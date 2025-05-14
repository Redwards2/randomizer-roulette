import streamlit as st

# START: Basic UI for entering names
st.set_page_config(page_title="Last Man Standing", layout="centered")

st.title("🎯 Last Man Standing - Randomizer")

names_input = st.text_area("Enter up to 10 names (one per line)", height=200)
names = [name.strip() for name in names_input.split("\n") if name.strip()]

if len(names) > 10:
    st.warning("Only the first 10 names will be used.")
    names = names[:10]

if st.button("Start Elimination") and len(names) >= 2:
    st.success("Starting elimination round...")
    st.write(names)
else:
    st.info("Enter at least 2 names to begin.")
# END
