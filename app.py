import streamlit as st
import random
import math  # Required for angle math
import streamlit.components.v1 as components
import time

# START: Circular layout renderer

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
            # Add a randomized animation delay to desync float animations
            delay = round(random.uniform(0, 2), 2)
            animation_class = f"dvd-float float-delay-{i}"
            bg_color = "#ffeb3b"

        angle = 2 * 3.14159 * i / len(names)
        x = center + radius * math.cos(angle)
        y = center + radius * math.sin(angle)
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
                animation-delay: " + "{delay:.2f}s;
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

@keyframes dvd-bounce {{
    0%   {{ transform: translate(-50%, -50%) translate(0px, 0px); }}
    25%  {{ transform: translate(-50%, -50%) translate(20px, -20px); }}
    50%  {{ transform: translate(-50%, -50%) translate(-20px, 20px); }}
    75%  {{ transform: translate(-50%, -50%) translate(20px, 20px); }}
    100% {{ transform: translate(-50%, -50%) translate(0px, 0px); }}
}}
.dvd-float {{
    animation-name: dvd-bounce;
    animation-duration: 3s;
    animation-iteration-count: infinite;
    animation-timing-function: ease-in-out;
}}
</style>
<div style="position: relative; width: {size}px; height: {size}px; margin: auto; background: white; border-radius: 50%; overflow: hidden;">
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

# START: Live elimination with floating animation and bouncing effect
if "game_active" not in st.session_state:
    st.session_state.game_active = False
if "remaining" not in st.session_state:
    st.session_state.remaining = []
if "eliminated" not in st.session_state:
    st.session_state.eliminated = None

params = st.query_params

if st.button("Start Elimination") and len(names) >= 2:
    st.session_state.game_active = True
    st.session_state.remaining = names.copy()
    st.session_state.eliminated = None
    st.query_params.clear()
    st.query_params["step"] = "go"
    st.rerun()

if st.session_state.game_active and len(st.session_state.remaining) > 2:
    if st.session_state.eliminated:
        st.session_state.remaining.remove(st.session_state.eliminated)
        st.session_state.eliminated = None

    # Pick next name to eliminate
    st.session_state.eliminated = random.choice(st.session_state.remaining)

    st.markdown(f"💀 **{st.session_state.eliminated}** has been eliminated!")
    html_circle_layout(st.session_state.remaining, eliminated_name=st.session_state.eliminated)

    # Let animation show, then schedule next rerun
    time.sleep(1.3)
    st.query_params.clear()
    st.query_params["step"] = str(random.randint(1, 10000))
    st.rerun()

elif st.session_state.game_active and len(st.session_state.remaining) == 2:
    if st.session_state.eliminated:
        st.session_state.remaining.remove(st.session_state.eliminated)
        st.session_state.eliminated = None

    winner = st.session_state.remaining[0]
    st.balloons()
    st.success(f"🏆 The last person standing is: **{winner}**")
    html_circle_layout([winner])
    st.session_state.game_active = False
    st.query_params.clear()
# END
