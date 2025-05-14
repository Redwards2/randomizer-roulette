import streamlit as st
import random
import math  # Required for angle math
import streamlit.components.v1 as components
import time

# START: Circular layout renderer (JS Version)
def html_circle_layout_js(names):
    import json
    names_js = json.dumps(names)
    size = 380  # pixels, adjust as needed
    radius = 145
    html_code = f"""
    <div id='arena-root'></div>
    <script>
    const NAMES = {names_js};
    const SIZE = {size};
    const RADIUS = {radius};
    const ELIMINATION_INTERVAL = 1600; // ms
    const arena = document.createElement('div');
    arena.style.position = 'relative';
    arena.style.width = SIZE + 'px';
    arena.style.height = SIZE + 'px';
    arena.style.margin = 'auto';
    arena.style.background = 'white';
    arena.style.borderRadius = '50%';
    arena.style.overflow = 'hidden';
    arena.style.boxShadow = '0 0 30px #ddd';
    document.getElementById('arena-root').appendChild(arena);
    let activeNames = NAMES.map((name, idx) => ({{
        name,
        angle: (2 * Math.PI * idx) / NAMES.length + Math.random(), // slightly random
        speed: (Math.random() * 0.025 + 0.01) * (Math.random() < 0.5 ? 1 : -1), // random direction
        el: null,
    }}));
    function renderNames() {{
        arena.innerHTML = '';
        activeNames.forEach((obj, i) => {{
            if (obj.eliminated) return;
            let el = document.createElement('div');
            obj.el = el;
            el.innerText = obj.name;
            el.style.position = 'absolute';
            el.style.fontWeight = 'bold';
            el.style.left = (SIZE / 2 + Math.cos(obj.angle) * RADIUS) + 'px';
            el.style.top = (SIZE / 2 + Math.sin(obj.angle) * RADIUS) + 'px';
            el.style.transform = 'translate(-50%,-50%)';
            el.style.padding = '7px 13px';
            el.style.borderRadius = '11px';
            el.style.background = '#ffeb3b';
            el.style.boxShadow = '1px 1px 4px rgba(0,0,0,0.28)';
            el.style.transition = 'opacity 1s, filter 1.2s, left 0.4s, top 0.4s';
            el.style.zIndex = 3;
            el.style.userSelect = 'none';
            arena.appendChild(el);
        }});
    }}
    renderNames();
    // Animate movement
    let running = true;
    let standings = [];
    function animate() {{
        activeNames.forEach(obj => {{
            if (!obj.eliminated) {{
                obj.angle += obj.speed;
                if (obj.angle > 2 * Math.PI) obj.angle -= 2 * Math.PI;
                if (obj.angle < 0) obj.angle += 2 * Math.PI;
            }}
        }});
        renderNames();
        if (running) requestAnimationFrame(animate);
    }}
    animate();
    // Eliminate names one by one
    function eliminateNext() {{
        const stillIn = activeNames.filter(n => !n.eliminated);
        if (stillIn.length <= 1) {{
            // Winner: highlight & stop animation
            if (stillIn[0]) {{
                standings.unshift(stillIn[0].name); // Winner gets 1st place
                stillIn[0].el.style.background = '#4ee44e';
                stillIn[0].el.style.boxShadow = '0 0 16px #13c913, 1px 1px 4px rgba(0,0,0,0.22)';
                stillIn[0].el.style.filter = 'drop-shadow(0 0 6px #bfffbb)';
            }}
            // Save standings in browser storage
            window.localStorage.setItem('last_man_standing_results', JSON.stringify(standings));
            running = false;
            return;
        }}
        // Pick random to eliminate
        const toEliminate = stillIn[Math.floor(Math.random() * stillIn.length)];
        toEliminate.eliminated = true;
        toEliminate.el.style.transition = 'opacity 1s, filter 1.2s, left 0.7s, top 0.7s';
        // Animate flying out
        const flyAngle = toEliminate.angle;
        toEliminate.el.style.left = (SIZE / 2 + Math.cos(flyAngle) * (RADIUS + 110)) + 'px';
        toEliminate.el.style.top = (SIZE / 2 + Math.sin(flyAngle) * (RADIUS + 110)) + 'px';
        toEliminate.el.style.opacity = 0;
        toEliminate.el.style.filter = 'blur(6px)';
        standings.unshift(toEliminate.name); // Add to standings in reverse order
        setTimeout(() => {{
            toEliminate.el && toEliminate.el.remove();
        }}, 1100);
        setTimeout(eliminateNext, ELIMINATION_INTERVAL);
    }}
    setTimeout(eliminateNext, ELIMINATION_INTERVAL * 1.5); // wait a moment before first elimination
    </script>
    """
    components.html(html_code, height=size + 40)
# END

# START: Standings Button and Results Table
import pandas as pd

ddef show_standings():
    standings_code = """
    <script>
    const result = window.localStorage.getItem('last_man_standing_results');
    if (result) {
        const parsed = JSON.parse(result);
        const text = parsed.map((name, i) => `${i+1}. ${name}`).join('\\n');
        const input = document.createElement('input');
        input.type = 'hidden';
        input.id = 'standings-result';
        input.value = text;
        document.body.appendChild(input);
    }
    </script>
    """
    components.html(standings_code, height=0)
    st.info("If results do not appear instantly, click 'Show Results' again after a few seconds.")
    value = st.text_area("Paste results here if not auto-filled:")
    if value:
        lines = value.strip().split('\n')
        st.subheader("Final Standings:")
        df = pd.DataFrame([l.split('. ', 1) for l in lines if '. ' in l], columns=["Place", "Name"])
        st.dataframe(df)

if st.button("Show Results"):
    show_standings()
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

# START: Live elimination - JS arena version
if st.button("Start Elimination") and len(names) >= 2:
    st.success("Let the chaos begin!")
    html_circle_layout_js(names)
# END
