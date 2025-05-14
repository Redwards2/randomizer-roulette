import streamlit as st
import random
import time

# START: Streamlit setup
st.set_page_config(page_title="Last Man Standing", layout="centered")
st.title("🎯 Last Man Standing - Randomizer")
# END

# START: Name entry
names_input = st.text_area("Enter up to 10 names (one per line)", height=200)
names = [name.strip() for name in names_input.split("\n") if name.strip()]

if len(names) > 10:
    st.warning("Only the first 10 names will be used.")
    names = names[:10]
# END

# START: Elimination simulation
if st.button("Start Elimination") and len(names) >= 2:
    st.success("Starting elimination round...")
    
    placeholder = st.empty()
    remaining = names.copy()
    
    while len(remaining) > 1:
        time.sleep(1.5)
        eliminated = random.choice(remaining)
        remaining.remove(eliminated)
        placeholder.markdown(f"💀 **{eliminated}** has been eliminated!")
        st.write("Remaining:", remaining)
    
    st.balloons()
    st.success(f"🏆 The last person standing is: **{remaining[0]}**")

elif len(names) < 2:
    st.info("Enter at least 2 names to begin.")
# END
