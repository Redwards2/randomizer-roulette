import streamlit as st
import random
import math  # Required for angle math
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="Randomizer Roullette", layout="centered")

st.markdown(
    """
    <style>
    /* Remove Streamlit’s default background and padding */
    .stApp {
        background: linear-gradient(135deg, #232946 0%, #00cfff 100%) !important;
        min-height: 100vh !important;
        padding: 0 !important;
    }
    /* Remove white box shadow and border from main container */
    .block-container {
        box-shadow: none !important;
        background: transparent !important;
        padding-top: 16px !important;
    }
    /* Sidebar styling for consistency */
    section[data-testid="stSidebar"] {
        background: rgba(44, 48, 80, 0.94) !important;
        color: #fff !important;
        border-radius: 24px 0 0 24px;
        box-shadow: 0 8px 40px #0014, 0 0 0 2px #00cfff33;
    }
    /* Remove sidebar padding and add modern spacing */
    section[data-testid="stSidebar"] .css-1lcbmhc, .css-1d391kg {
        padding: 22px 18px 18px 18px !important;
    }
    /* App title styling */
    h1 {{
        font-family: 'Montserrat', 'Arial Black', sans-serif;
        letter-spacing: 1.2px;
        font-size: 2.4rem !important;
        font-weight: 800;
        color: #f5f5f7 !important;
        text-shadow: 0 2px 10px #1a254280, 0 1px 2px #2227;
        background: none !important;
        -webkit-background-clip: initial !important;
        -webkit-text-fill-color: initial !important;
        filter: none !important;
        text-align: center;
    }}
    /* Make disabled button text always visible and legible */
    button:disabled, .stButton>button[disabled] {{
        color: #000 !important;      /* Change to white (#fff) for dark sidebar, or #222 for light button */
        opacity: 0.7 !important;     /* Make it more opaque */
        background: #000 !important; /* Keep the lighter background */
        border: 1.5px solid #bbb !important;
        font-weight: 600;
        cursor: not-allowed !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# START: Circular layout renderer (JS Version)
def html_circle_layout_js(names):
    import json
    names_js = json.dumps(names)
    size = 400
    radius = 155
    html_code = f'''
    <style>
    #arena-root {{
        filter: drop-shadow(0 6px 18px #0007);
    }}
    #standings-root {{
        background: #222c;
        border-radius: 18px;
        padding: 22px 16px 22px 12px;
        box-shadow: 0 4px 24px #0016, 0 0 0 2px #66e4ff88;
        min-width: 175px;
    }}
       /* Standings header */
    #standings-root > div:first-child {{
        font-family: 'Montserrat', 'Arial Black', sans-serif;
        letter-spacing: 1px;
        font-weight: 800;
        font-size: 23px !important;
        margin-bottom: 18px !important;
        color: #f5f5f7 !important;
        background: none !important;
        -webkit-background-clip: initial !important;
        -webkit-text-fill-color: initial !important;
        filter: none !important;
        text-shadow: 0 2px 6px #0004, 0 1px 1px #0013;
        text-align: center;
    }}
    #standings-list li {{
        font-family: 'Montserrat', 'Arial Black', sans-serif;
        font-size: 18px;
        margin-bottom: 6px;
        transition: background 0.3s, color 0.3s;
        border-radius: 8px;
        padding: 1px 4px 1px 0;
        box-shadow: none;
    }}
    #standings-list li:first-child {{
        border-top-left-radius: 20px; border-top-right-radius: 20px;
    }}
    #standings-list li:last-child {{
        border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;
    }}
    @keyframes pop-out {{
      0% {{
          transform: translate(-50%,-50%) scale(1) rotate(0deg);
          opacity: 1;
          filter: none;
      }}
      60% {{
          transform: translate(-50%,-50%) scale(1.22) rotate(12deg);
          opacity: 1;
          filter: blur(0.5px) brightness(1.1);
      }}
      80% {{
          transform: translate(-50%,-50%) scale(0.85) rotate(-8deg);
          opacity: 0.7;
          filter: blur(2px) brightness(1.3);
      }}
      100% {{
          transform: translate(-50%,-50%) scale(2.0) rotate(-17deg);
          opacity: 0;
          filter: blur(12px) brightness(2);
      }}
    }}
    </style>
    <div style='display: flex; justify-content: center; align-items: flex-start; gap: 40px;'>
        <div id='arena-root'></div>
        <div id='standings-root'>
            <div>Standings</div>
            <ol id='standings-list' style='padding-left:0;font-size:16px;list-style-type:none; color:white; font-weight:bold;'></ol>
        </div>
    </div>
    <script>
    window.addEventListener('DOMContentLoaded', function() {{
        const NAMES = {names_js};
        const SIZE = {size};
        const RADIUS = {radius};
        function randomDelay() {{
            return Math.floor(Math.random() * 5000) + 5000;
        }}

        const arena = document.createElement('div');
        arena.style.position = 'relative';
        arena.style.width = SIZE + 'px';
        arena.style.height = SIZE + 'px';
        arena.style.margin = 'auto';
        arena.style.background = 'radial-gradient(ellipse at 60% 40%, #fffc 60%, #4ee1fa33 98%, #232946 120%)';
        arena.style.borderRadius = '50%';
        arena.style.overflow = 'hidden';
        arena.style.boxShadow = '0 6px 38px #0ad6, 0 1px 32px #0099ff44';
        arena.style.border = '6px solid #3df0fa';
        document.getElementById('arena-root').appendChild(arena);

        const emojis = ["🎲","😎","🦄","🐲","👾","🦸‍♂️","🧙‍♂️","🦖","🤠","👽","🐸","👻","🤖","🐼","🐧","🦊","🐻","🦕","🧟","👩‍🚀"];
        let emojiPool = emojis.slice(); // Clone the emoji array
        if (NAMES.length > emojiPool.length) {{
            // fallback: allow duplicates if more names than emojis
            while (emojiPool.length < NAMES.length) emojiPool = emojiPool.concat(emojis);
        }}
        emojiPool = emojiPool.slice(0, NAMES.length);
        for (let i = emojiPool.length - 1; i > 0; i--) {{
            // Shuffle to randomize emoji assignment
            const j = Math.floor(Math.random() * (i + 1));
            [emojiPool[i], emojiPool[j]] = [emojiPool[j], emojiPool[i]];
        }}
        let activeNames = NAMES.map((name, idx) => {{
            let theta = (2 * Math.PI * idx) / NAMES.length;
            let px = SIZE/2 + Math.cos(theta) * (RADIUS * 0.72);
            let py = SIZE/2 + Math.sin(theta) * (RADIUS * 0.72);
            let speed = Math.random() * 2.4 + 1.2;
            let dir = Math.random() * 2 * Math.PI;
            let vx = Math.cos(dir) * speed;
            let vy = Math.sin(dir) * speed;
            let emoji = emojiPool[idx];
            return {{
                name,
                emoji,
                x: px,
                y: py,
                vx: vx,
                vy: vy,
                el: null,
                eliminated: false
            }};
        }});

        let running = true;
        let standings = [];

        function sparkle(el) {{
            let s = document.createElement('div');
            s.style.position = 'absolute';
            s.style.left = '50%'; s.style.top = '50%';
            s.style.width = '36px'; s.style.height = '36px';
            s.style.pointerEvents = 'none';
            s.style.transform = 'translate(-50%,-50%)';
            s.style.borderRadius = '50%';
            s.style.zIndex = 6;
            s.innerHTML = '<svg width=\"36\" height=\"36\"><circle cx=\"18\" cy=\"18\" r=\"14\" fill=\"none\" stroke=\"#ffe52e\" stroke-width=\"4\" opacity=\"0.62\"/><circle cx=\"18\" cy=\"18\" r=\"10\" fill=\"#fffdbb99\" opacity=\"0.45\"/></svg>';
            el.appendChild(s);
            setTimeout(() => s.remove(), 900);
        }}

        function renderNames() {{
            // Only keep DOM nodes for all objects that aren't removed
            arena.innerHTML = '';
            activeNames.forEach(obj => {{
                if (obj.removed) return; // Skip removed
        
                // Only create the DOM node ONCE per object
                if (!obj.el) {{
                    let el = document.createElement('div');
                    obj.el = el;
                   el.innerHTML = `
                    <div style='display:flex; flex-direction:column; align-items:center; justify-content:center;'>
                      <div style='font-size:15px;font-weight:900;margin-bottom:1px;text-align:center; width:max-content;'>
                        ${{obj.name}}
                      </div>
                      <div style='font-size:32px;line-height:1;text-align:center;'>
                        ${{obj.emoji}}
                      </div>
                    </div>
                  `;

                    el.style.position = 'absolute';
                    el.style.fontWeight = '900';
                    el.style.left = obj.x + 'px';
                    el.style.top = obj.y + 'px';
                    el.style.transform = 'translate(-50%,-50%) scale(1)';
                    el.style.padding = '11px 20px';
                    el.style.borderRadius = '99px';
                    el.style.background = 'linear-gradient(95deg, #f1f7b4 0%, #faf8e4 80%)';
                    el.style.boxShadow = '0 3px 16px #f1f6bb88, 0 1px 8px #1b87f755';
                    el.style.border = '2.8px solid #20e7ef';
                    el.style.transition = 'opacity 1.2s, filter 1.3s, left 0.6s, top 0.6s, transform 0.3s cubic-bezier(.23,1.5,.32,1)';
                    el.style.fontFamily = 'Montserrat, Arial Black, sans-serif';
                    el.style.color = '#33394b';
                    el.style.textShadow = '0 2px 12px #fffcc960, 0 1px 1px #fff';
                    el.style.zIndex = 3;
                    el.style.userSelect = 'none';
                }}
        
                // Only update position for non-eliminated
                if (!obj.eliminated) {{
                    obj.el.style.left = obj.x + 'px';
                    obj.el.style.top = obj.y + 'px';
                }}
                // For eliminated: do nothing; let the pop-out animation run undisturbed!
        
                arena.appendChild(obj.el);
            }});
        }}

        function renderStandings() {{
            const ol = document.getElementById('standings-list');
            ol.innerHTML = '';
            ol.style.listStyleType = 'none';
            ol.style.paddingLeft = '0';
            const total = NAMES.length;
            standings.forEach((name, idx) => {{
                const li = document.createElement('li');
                let placeNum = total - idx;
                let placeStr =
                    placeNum === 1 ? '1st' :
                    placeNum === 2 ? '2nd' :
                    placeNum === 3 ? '3rd' : placeNum + 'th';
                let medal = '';
                if (placeNum === 1) medal = ' 🥇';
                else if (placeNum === 2) medal = ' 🥈';
                else if (placeNum === 3) medal = ' 🥉';
                li.innerText = placeStr + ' ' + name + medal;
                li.style.marginBottom = '4px';
                li.style.fontWeight = 'bold';
                li.style.color = placeNum === 1 ? '#ffdb57'
                    : placeNum === 2 ? '#bfe3ef'
                    : placeNum === 3 ? '#ffb55b'
                    : 'white';
                li.style.background = placeNum === 1 ? '#3d2c06'
                    : placeNum === 2 ? '#253942'
                    : placeNum === 3 ? '#3b2410'
                    : 'none';
                li.style.boxShadow = placeNum <= 3 ? '0 2px 10px #0ee8, 0 1px 2px #fff1' : 'none';
                ol.appendChild(li);
            }});
        }}

        renderNames();
        renderStandings();

        function animate() {{
            activeNames.forEach(obj => {{
                if (obj.eliminated || obj.removed) return;
                // Move by velocity
                obj.x += obj.vx;
                obj.y += obj.vy;
                // Bounce off edge of arena (circle)
                let cx = SIZE/2, cy = SIZE/2;
                let dx = obj.x - cx, dy = obj.y - cy;
                let dist = Math.sqrt(dx*dx + dy*dy);
                if (dist > RADIUS - 24) {{
                    // Bounce: reflect velocity and move inside boundary
                    let normX = dx / dist, normY = dy / dist;
                    let dot = obj.vx * normX + obj.vy * normY;
                    obj.vx -= 2 * dot * normX;
                    obj.vy -= 2 * dot * normY;
                    // Dampening for more realism
                    obj.vx *= 0.92;
                    obj.vy *= 0.92;
                    // Bring just inside edge
                    obj.x = cx + normX * (RADIUS - 25);
                    obj.y = cy + normY * (RADIUS - 25);
                }}
            }});
            renderNames();
            if (running) requestAnimationFrame(animate);
        }}

        animate();

        function eliminateNext() {{
            const stillIn = activeNames.filter(n => !n.eliminated && !n.removed);
            if (stillIn.length <= 1) {{
                if (stillIn[0]) {{
                    standings.push(stillIn[0].name);
                    stillIn[0].el.style.background = '#4ee44e';
                    stillIn[0].el.style.boxShadow = '0 0 24px #13c913, 0 1px 2px #fff1';
                    stillIn[0].el.style.filter = 'drop-shadow(0 0 14px #bfffbb)';
                    stillIn[0].el.style.transform = 'translate(-50%,-50%) scale(1.12)';
                    stillIn[0].el.style.color = '#111';
                    setTimeout(() => sparkle(stillIn[0].el), 250);
                }}
                renderStandings();
                running = false;
                window.localStorage.setItem('last_man_standing_results', JSON.stringify(standings));
                return;
            }}
            const toEliminate = stillIn[Math.floor(Math.random() * stillIn.length)];
            toEliminate.eliminated = true;
            toEliminate.el.style.animation = 'pop-out 1.1s cubic-bezier(.23,1.5,.32,1) forwards';
            toEliminate.el.style.zIndex = 9;
            toEliminate.el.popping = true;
            sparkle(toEliminate.el);
            standings.push(toEliminate.name);
            renderStandings();
            setTimeout(() => {{
                if (toEliminate.el) toEliminate.el.remove();
                toEliminate.removed = true; // Mark as fully removed!
                const stillLeft = activeNames.filter(n => !n.eliminated && !n.removed);
                if (stillLeft.length > 1) {{
                    setTimeout(eliminateNext, randomDelay());
                }} else {{
                    if (stillLeft[0]) {{
                        standings.push(stillLeft[0].name);
                        stillLeft[0].el.style.background = '#4ee44e';
                        stillLeft[0].el.style.boxShadow = '0 0 24px #13c913, 0 1px 2px #fff1';
                        stillLeft[0].el.style.filter = 'drop-shadow(0 0 14px #bfffbb)';
                        stillLeft[0].el.style.transform = 'translate(-50%,-50%) scale(1.12)';
                        stillLeft[0].el.style.color = '#111';
                        setTimeout(() => sparkle(stillLeft[0].el), 300);
                    }}
                    renderStandings();
                    running = false;
                    window.localStorage.setItem('last_man_standing_results', JSON.stringify(standings));
                }}
            }}, 1100);
        }}
        setTimeout(eliminateNext, randomDelay());
    }});
    </script>
    '''
    components.html(html_code, height=size + 60)
# END

# SIDEBAR INPUT ONLY VERSION
st.title("🎯 Randomizer Roullette")

with st.sidebar:
    st.header("Enter Names")
    names_input = st.text_area("Up to 10 names (one per line)", height=200)
    start = st.button("Start")
    st.markdown("**App by [Redwards]**", unsafe_allow_html=True)

names = [name.strip() for name in names_input.split("\n") if name.strip()]
if len(names) > 10:
    st.warning("Only the first 10 names will be used.")
    names = names[:10]

# START: Added session reset so each Start triggers a fresh round
if 'start_count' not in st.session_state:
    st.session_state['start_count'] = 0

if start:
    if len(names) >= 2:
        st.session_state['start_count'] += 1  # Force Streamlit to re-render component
        st.markdown(
            "<div style='text-align:center; color:#22711A; font-size:1.35rem; font-weight:bold; background:#e6ffed; border-radius:8px; padding:0.8em 0; margin-bottom:10px;'>"
            "May the odds be ever in your Favor!"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        st.info("Add at least 2 names in the sidebar and hit Start.")

# Always render component if "start_count" changes
if st.session_state.get('start_count', 0) > 0 and len(names) >= 2:
    html_circle_layout_js(names)
# END
