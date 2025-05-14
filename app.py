import streamlit as st
import random
import time
import math  # Required for angle math

# START: Circular layout renderer
import streamlit.components.v1 as components

def html_circle_layout(names, eliminated_name=None):
    radius = 120
    size = 300
    center = size // 2

    divs = ""
    for i, name in enumerate(names):
        if name == eliminated_name:
            # START: Falling animation class for eliminated name
            animation_class = "fall-out"
            bg_color = "#ff4d4d"
            # END
        else:
            animation_class = ""
            bg_color = "#ffeb3b"

        angle = 2 * 3.14159 * i / len(names)
        x = center + radius * 0.9 * round(math.cos(angle), 4)
        y = center + radius * 0.9 * round(math.sin(angle), 4)
        divs += f'''
            <div class="{animation_class}" style="
                position: absolute;
                left: {x}px;
                top: {y}px;
                transform: translate(-50%, -50%);
                background-color: {bg_color};
                padding: 6px 12px;
                border-radius: 10px;
                font-weight: bold;
                box-shadow: 1px 1px 4px rgba(0,0,0,0.3);
                white-space: nowrap;
            ">
                {name}
            </div>
        '''

    html_code = f"""
<style>
@keyframes fall-out {{
    0% {{
        opacity: 1;
        transform: translate(-50%, -50%) scale(1);
    }}
    100% {{
        opacity: 0;
        transform: translate(-50%, -200%) scale(0.5);
    }}
}}
.fall-out {{
    animation: fall-out 1s ease-in-out forwards;
}}
</style>
<div style="position: relative; width: {size}px; height: {size}px; margin: auto;">
    {divs}
</div>
"""

    components.html(html_code, height=size + 40)
# END

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

        # First, show eliminated name with falling animation
        with placeholder.container():
            st.markdown(f"💀 **{eliminated}** has been eliminated!")
            html_circle_layout(remaining, eliminated_name=eliminated)

        time.sleep(1.2)  # Let the animation play before removing

        # Now remove it for the next frame
        remaining.remove(eliminated)

    with placeholder.container():
        st.balloons()
        st.success(f"🏆 The last person standing is: **{remaining[0]}**")
        html_circle_layout(remaining)

elif len(names) < 2:
    st.info("Enter at least 2 names to begin.")
# END
