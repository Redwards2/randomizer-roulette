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
                stillIn[0].el.style.background = '#4ee44e';
                stillIn[0].el.style.boxShadow = '0 0 16px #13c913, 1px 1px 4px rgba(0,0,0,0.22)';
                stillIn[0].el.style.filter = 'drop-shadow(0 0 6px #bfffbb)';
            }}
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
                animation-delay: {delay:.2f}s;
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

# START: Live elimination - JS arena version
if st.button("Start Elimination") and len(names) >= 2:
    st.success("Let the chaos begin!")
    html_circle_layout_js(names)
# END
