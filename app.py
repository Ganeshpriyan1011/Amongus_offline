import streamlit as st

from players import PlayerManager
from game import GameManager


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Among Us — Mission Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CSS — Space / Sci-Fi Theme
# ---------------------------------------------------

st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');

/* ── Palette ──
   Deep void:   #0a0d1a
   Panel bg:    #111526
   Card bg:     #1a1f35
   Neon cyan:   #00f5ff
   Neon red:    #ff3860
   Neon green:  #00ff88
   Gold:        #ffd700
   Muted text:  #8892b0
*/

/* ── Base ── */
html, body, [data-testid="stApp"] {
    background: #0a0d1a !important;
    color: #ccd6f6 !important;
    font-family: 'Exo 2', sans-serif !important;
}

/* Animated starfield pseudo-background */
[data-testid="stApp"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(1px 1px at 10% 20%, rgba(0,245,255,.35) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 50%, rgba(255,255,255,.20) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 15%, rgba(0,255,136,.25) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 70%, rgba(255,56,96,.20) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 35%, rgba(255,215,0,.15) 0%, transparent 100%),
        radial-gradient(1px 1px at 45% 85%, rgba(0,245,255,.20) 0%, transparent 100%),
        radial-gradient(2px 2px at 20% 80%, rgba(255,255,255,.12) 0%, transparent 100%),
        radial-gradient(1px 1px at 65% 45%, rgba(0,245,255,.30) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1123 0%, #111526 100%) !important;
    border-right: 1px solid rgba(0,245,255,.15) !important;
}

[data-testid="stSidebar"] * {
    color: #ccd6f6 !important;
}

/* ── Sidebar radio ── */
[data-testid="stSidebar"] .stRadio > div {
    gap: 6px;
    display: flex;
    flex-direction: column;
}

[data-testid="stSidebar"] .stRadio label {
    background: rgba(0,245,255,.04) !important;
    border: 1px solid rgba(0,245,255,.10) !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    cursor: pointer !important;
    transition: all .2s !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: .03em !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(0,245,255,.10) !important;
    border-color: rgba(0,245,255,.40) !important;
    box-shadow: 0 0 12px rgba(0,245,255,.15) !important;
}

/* ── Page title ── */
h1 {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 900 !important;
    font-size: 2.2rem !important;
    background: linear-gradient(90deg, #00f5ff 0%, #00ff88 60%, #ffd700 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: .06em !important;
    margin-bottom: .25rem !important;
}

h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: .04em !important;
    color: #00f5ff !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,245,255,.08) 0%, rgba(0,245,255,.15) 100%) !important;
    color: #00f5ff !important;
    border: 1px solid rgba(0,245,255,.40) !important;
    border-radius: 10px !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 700 !important;
    font-size: .9rem !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    padding: 12px 20px !important;
    transition: all .25s ease !important;
    box-shadow: 0 0 0px rgba(0,245,255,0) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,245,255,.18) 0%, rgba(0,245,255,.30) 100%) !important;
    border-color: #00f5ff !important;
    box-shadow: 0 0 20px rgba(0,245,255,.30), inset 0 0 20px rgba(0,245,255,.05) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Start / confirm CTA */
button[kind="primary"],
.cta-btn > button {
    background: linear-gradient(135deg, #00b4cc 0%, #00f5ff 100%) !important;
    color: #0a0d1a !important;
    border: none !important;
    box-shadow: 0 0 24px rgba(0,245,255,.40) !important;
    font-size: 1rem !important;
}

button[kind="primary"]:hover,
.cta-btn > button:hover {
    box-shadow: 0 0 40px rgba(0,245,255,.55) !important;
    transform: translateY(-2px) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: rgba(17,21,38,.80) !important;
    border: 1px solid rgba(0,245,255,.20) !important;
    border-radius: 8px !important;
    color: #ccd6f6 !important;
    font-family: 'Exo 2', sans-serif !important;
    transition: border-color .2s !important;
}

.stTextInput > div > div > input:focus {
    border-color: #00f5ff !important;
    box-shadow: 0 0 12px rgba(0,245,255,.20) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(26,31,53,.80) !important;
    border: 1px solid rgba(0,245,255,.15) !important;
    border-radius: 14px !important;
    padding: 20px !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif !important;
    color: #00f5ff !important;
}

/* ── Divider ── */
hr {
    border-color: rgba(0,245,255,.12) !important;
    margin: 1.5rem 0 !important;
}

/* ── Alerts (st.success / st.error / st.info / st.warning) ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 4px !important;
}

/* ── Custom cards ── */
.card {
    background: rgba(26,31,53,.85);
    border-radius: 14px;
    padding: 20px 24px;
    border: 1px solid rgba(0,245,255,.12);
    margin-bottom: 16px;
    backdrop-filter: blur(6px);
}

.card-danger {
    background: rgba(40,10,20,.85);
    border-color: rgba(255,56,96,.35);
}

.card-success {
    background: rgba(10,35,22,.85);
    border-color: rgba(0,255,136,.30);
}

.card-warning {
    background: rgba(35,30,10,.85);
    border-color: rgba(255,215,0,.30);
}

/* ── Banner text ── */
.banner-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.6rem;
    font-weight: 900;
    letter-spacing: .08em;
    margin-bottom: 6px;
}

.banner-cyan  { color: #00f5ff; }
.banner-red   { color: #ff3860; }
.banner-green { color: #00ff88; }
.banner-gold  { color: #ffd700; }

/* ── Player chips ── */
.player-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0,245,255,.07);
    border: 1px solid rgba(0,245,255,.20);
    border-radius: 50px;
    padding: 6px 16px;
    font-family: 'Exo 2', sans-serif;
    font-weight: 600;
    font-size: .88rem;
    color: #ccd6f6;
    margin: 4px 0;
    transition: background .2s;
}

.player-chip:hover {
    background: rgba(0,245,255,.14);
}

.player-chip-dead {
    border-color: rgba(255,56,96,.35);
    background: rgba(255,56,96,.06);
    color: #8892b0;
    text-decoration: line-through;
}

/* ── Glow pulse animation ── */
@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 12px rgba(0,245,255,.30); }
    50%       { box-shadow: 0 0 30px rgba(0,245,255,.60); }
}

.glow-pulse {
    animation: glowPulse 2.4s ease-in-out infinite;
}

/* ── Alarm animation ── */
@keyframes alarmFlash {
    0%, 100% { background: rgba(40,10,20,.85); }
    50%       { background: rgba(255,56,96,.12); }
}

.alarm-card {
    animation: alarmFlash 1.2s ease-in-out infinite;
    border: 1px solid rgba(255,56,96,.50) !important;
    border-radius: 14px;
    padding: 20px 24px;
}

/* ── Checkbox ── */
.stCheckbox span {
    color: #8892b0 !important;
    font-family: 'Exo 2', sans-serif !important;
}

/* ── Selectbox label ── */
.stSelectbox label, .stTextInput label {
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 600 !important;
    color: #8892b0 !important;
    font-size: .82rem !important;
    text-transform: uppercase !important;
    letter-spacing: .08em !important;
}

/* ── Sidebar title ── */
.sidebar-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.05rem;
    font-weight: 900;
    color: #00f5ff;
    letter-spacing: .10em;
    margin-bottom: 4px;
}

.sidebar-sub {
    font-family: 'Exo 2', sans-serif;
    font-size: .72rem;
    color: #8892b0;
    letter-spacing: .06em;
    text-transform: uppercase;
    margin-bottom: 18px;
}

/* ── Vote bar ── */
.vote-bar-wrap {
    margin: 4px 0 10px;
}

.vote-bar-bg {
    background: rgba(255,255,255,.06);
    border-radius: 6px;
    height: 10px;
    overflow: hidden;
    margin-top: 4px;
}

.vote-bar-fill {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #00f5ff, #00ff88);
    transition: width .4s ease;
}

/* ── Info tag ── */
.tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 50px;
    font-size: .72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .07em;
}

.tag-cyan  { background: rgba(0,245,255,.12); color: #00f5ff; border: 1px solid rgba(0,245,255,.25); }
.tag-red   { background: rgba(255,56,96,.12);  color: #ff3860; border: 1px solid rgba(255,56,96,.30); }
.tag-green { background: rgba(0,255,136,.10);  color: #00ff88; border: 1px solid rgba(0,255,136,.25); }
.tag-gold  { background: rgba(255,215,0,.10);  color: #ffd700; border: 1px solid rgba(255,215,0,.25); }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "player_manager" not in st.session_state:
    st.session_state.player_manager = PlayerManager()

if "game_manager" not in st.session_state:
    st.session_state.game_manager = GameManager()

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "mediator" not in st.session_state:
    st.session_state.mediator = ""

if "use_mediator" not in st.session_state:
    st.session_state.use_mediator = False

if "locations" not in st.session_state:
    st.session_state.locations = [
        "Cafeteria", "MedBay", "Electrical", "Upper Engine",
        "Lower Engine", "Security", "Reactor", "Navigation",
        "O2", "Weapons", "Shields", "Communications",
        "Storage", "Admin", "Laboratory"
    ]

if "use_custom_tasks" not in st.session_state:
    st.session_state.use_custom_tasks = False

if "custom_crewmate_tasks" not in st.session_state:
    st.session_state.custom_crewmate_tasks = []

if "custom_impostor_tasks" not in st.session_state:
    st.session_state.custom_impostor_tasks = []


pm = st.session_state.player_manager
gm = st.session_state.game_manager


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 6px;">
        <div style="font-size:3rem; margin-bottom:4px;">🚀</div>
        <div class="sidebar-title">AMONG US</div>
        <div class="sidebar-sub">Mission Control v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.game_started:
        alive = gm.get_alive_players()
        dead  = gm.get_dead_players()
        st.markdown(f"""
        <div style="display:flex; gap:8px; justify-content:center; margin-bottom:14px;">
            <span class="tag tag-green">🟢 {len(alive)} Alive</span>
            <span class="tag tag-red">☠ {len(dead)} Dead</span>
        </div>
        """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigate",
        ["⚙️  Game Setup", "🕵️  Role Reveal",
         "☠️  Dead Body Report", "🗳️  Voting", "📊  Game Status"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("""
    <div style="font-size:.72rem; color:#8892b0; text-align:center; line-height:1.6;">
        Offline Among Us Manager<br>
        Built with Streamlit · 2025
    </div>
    """, unsafe_allow_html=True)


# ===================================================
# GAME SETUP
# ===================================================

if menu == "⚙️  Game Setup":

    st.markdown("# ⚙️ MISSION SETUP")
    st.markdown("""
    <div class="card">
        <span class="tag tag-cyan">PRE-GAME</span>
        <p style="margin-top:10px; color:#8892b0; font-size:.9rem;">
            Recruit your crew, designate a mediator, configure ship locations, and assign mission tasks before launching the game.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Add Player ──────────────────────────────
    st.markdown("### 👤 Recruit Crew Members")

    col1, col2 = st.columns([4, 1])
    with col1:
        player_name = st.text_input(
            "Player Name",
            placeholder="Enter callsign…",
            key="player_name_input",
            label_visibility="collapsed"
        )
    with col2:
        st.write("")
        if st.button("➕ Add", key="add_player_btn", use_container_width=True):
            success, message = pm.add_player(player_name)
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"⚠️ {message}")

    # Player list
    players = pm.get_players()
    player_count = len(players)

    if player_count == 0:
        st.markdown("""
        <div class="card" style="text-align:center; padding: 30px;">
            <div style="font-size:2.5rem;">👥</div>
            <div style="color:#8892b0; margin-top:8px;">No crew members yet — add at least 4 to launch.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols_per_row = 2
        rows = [players[i:i+cols_per_row] for i in range(0, len(players), cols_per_row)]
        for row in rows:
            rcols = st.columns(cols_per_row)
            for i, p in enumerate(row):
                with rcols[i]:
                    c1, c2 = st.columns([5, 1])
                    c1.markdown(f'<div class="player-chip">🧑‍🚀 {p}</div>', unsafe_allow_html=True)
                    if c2.button("✕", key=f"remove_{p}", help=f"Remove {p}"):
                        pm.remove_player(p)
                        st.rerun()

    st.divider()

    # ── Impostor count preview ───────────────────
    st.markdown("### 🔴 Impostor Assignment")
    if player_count >= 4:
        if player_count <= 5:
            auto_impostors = 1
        elif player_count <= 8:
            auto_impostors = 2
        else:
            auto_impostors = 3

        pct = auto_impostors / player_count if player_count else 0
        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-family:'Exo 2',sans-serif; font-weight:600;">
                    <span class="tag tag-green">{player_count} Players</span> &nbsp;→&nbsp;
                    <span class="tag tag-red">{auto_impostors} Impostor{'s' if auto_impostors > 1 else ''}</span>
                </span>
                <span style="color:#8892b0; font-size:.82rem;">{100*pct:.0f}% impostor ratio</span>
            </div>
            <div class="vote-bar-bg" style="margin-top:12px;">
                <div class="vote-bar-fill" style="width:{pct*100}%; background:linear-gradient(90deg,#ff3860,#ff6b8a);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card card-warning">
            <span class="tag tag-gold">⚠️ MINIMUM NOT MET</span>
            <p style="margin-top:8px; color:#8892b0;">Add at least 4 crew members to see impostor assignment.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Mediator ────────────────────────────────
    st.markdown("### 👨‍⚖️ Mediator (Optional)")
    use_mediator = st.checkbox("Assign a Mediator", value=st.session_state.use_mediator)
    st.session_state.use_mediator = use_mediator

    if use_mediator:
        mediator = st.text_input(
            "Mediator Name",
            value=st.session_state.mediator,
            placeholder="Enter mediator callsign…",
            key="mediator_input"
        )
        st.session_state.mediator = mediator
        st.markdown("""
        <div class="card">
            <span class="tag tag-cyan">ℹ️ INFO</span>
            <p style="color:#8892b0; margin-top:8px;">The mediator oversees the game but does not play. They can see all roles and manage meetings.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.session_state.mediator = ""
        st.markdown("""
        <div class="card">
            <span class="tag tag-cyan">ℹ️ INFO</span>
            <p style="color:#8892b0; margin-top:8px;">No mediator — all registered crew members will participate in the game.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Locations ────────────────────────────────
    st.markdown("### 🗺️ Ship Locations")

    col1, col2 = st.columns([4, 1])
    with col1:
        new_location = st.text_input(
            "New Location",
            placeholder="Enter room/area name…",
            key="new_location_input",
            label_visibility="collapsed"
        )
    with col2:
        st.write("")
        if st.button("➕ Add", key="add_location_btn", use_container_width=True):
            if new_location.strip():
                if new_location not in st.session_state.locations:
                    st.session_state.locations.append(new_location.strip())
                    st.success(f"📍 {new_location} added!")
                    st.rerun()
                else:
                    st.error("Location already exists.")
            else:
                st.error("Enter a location name.")

    if st.session_state.locations:
        # Display as compact grid
        loc_cols = st.columns(3)
        for idx, loc in enumerate(st.session_state.locations):
            with loc_cols[idx % 3]:
                c1, c2 = st.columns([4, 1])
                c1.markdown(f'<div class="player-chip" style="font-size:.80rem;">📍 {loc}</div>', unsafe_allow_html=True)
                if c2.button("✕", key=f"remove_loc_{loc}"):
                    st.session_state.locations.remove(loc)
                    st.rerun()
    else:
        st.markdown("""
        <div class="card card-warning">
            <span class="tag tag-gold">⚠️</span>
            <span style="color:#8892b0; margin-left:8px;">No locations configured.</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Tasks ────────────────────────────────────
    st.markdown("### 📋 Mission Tasks")
    use_custom_tasks = st.checkbox("Use Custom Tasks", value=st.session_state.use_custom_tasks)
    st.session_state.use_custom_tasks = use_custom_tasks

    if use_custom_tasks:
        t1, t2 = st.tabs(["🟢 Crewmate Tasks", "🔴 Impostor Tasks"])

        with t1:
            col1, col2 = st.columns([4, 1])
            with col1:
                new_crew_task = st.text_input(
                    "Task", placeholder="Describe crewmate task…",
                    key="new_crewmate_task", label_visibility="collapsed"
                )
            with col2:
                st.write("")
                if st.button("➕ Add", key="add_crewmate_task", use_container_width=True):
                    if new_crew_task.strip():
                        st.session_state.custom_crewmate_tasks.append(new_crew_task.strip())
                        st.success("Task added!")
                        st.rerun()
                    else:
                        st.error("Enter a task description.")

            if st.session_state.custom_crewmate_tasks:
                for i, task in enumerate(st.session_state.custom_crewmate_tasks):
                    c1, c2 = st.columns([8, 1])
                    c1.markdown(f'<div class="player-chip" style="border-color:rgba(0,255,136,.25);">✅ {task}</div>', unsafe_allow_html=True)
                    if c2.button("✕", key=f"remove_crew_{i}"):
                        st.session_state.custom_crewmate_tasks.pop(i)
                        st.rerun()
            else:
                st.info("No crewmate tasks yet.")

        with t2:
            col1, col2 = st.columns([4, 1])
            with col1:
                new_imp_task = st.text_input(
                    "Task", placeholder="Describe impostor task…",
                    key="new_impostor_task", label_visibility="collapsed"
                )
            with col2:
                st.write("")
                if st.button("➕ Add", key="add_impostor_task", use_container_width=True):
                    if new_imp_task.strip():
                        st.session_state.custom_impostor_tasks.append(new_imp_task.strip())
                        st.success("Task added!")
                        st.rerun()
                    else:
                        st.error("Enter a task description.")

            if st.session_state.custom_impostor_tasks:
                for i, task in enumerate(st.session_state.custom_impostor_tasks):
                    c1, c2 = st.columns([8, 1])
                    c1.markdown(f'<div class="player-chip" style="border-color:rgba(255,56,96,.30);">💀 {task}</div>', unsafe_allow_html=True)
                    if c2.button("✕", key=f"remove_imp_{i}"):
                        st.session_state.custom_impostor_tasks.pop(i)
                        st.rerun()
            else:
                st.info("No impostor tasks yet.")

        dup = set(st.session_state.custom_crewmate_tasks) & set(st.session_state.custom_impostor_tasks)
        if dup:
            st.markdown(f"""
            <div class="card card-warning">
                <span class="tag tag-gold">⚠️ DUPLICATE TASKS</span>
                <p style="color:#8892b0; margin-top:8px;">{', '.join(dup)} — remove duplicates before starting.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card">
            <span class="tag tag-cyan">DEFAULT TASKS</span>
            <p style="color:#8892b0; margin-top:8px;">The game will use the built-in task list. Enable custom tasks above to configure your own.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Launch Button ────────────────────────────
    if st.button("🚀 LAUNCH MISSION", use_container_width=True, key="start_game_btn", type="primary"):

        if player_count < 4:
            st.error("⚠️ Minimum 4 crew members required to launch.")

        elif use_mediator and st.session_state.mediator.strip() == "":
            st.error("⚠️ Enter a mediator name or disable the mediator option.")

        elif use_custom_tasks and (
            len(st.session_state.custom_crewmate_tasks) == 0 or
            len(st.session_state.custom_impostor_tasks) == 0
        ):
            st.error("⚠️ Add at least one crewmate and one impostor task.")

        elif use_custom_tasks and (
            set(st.session_state.custom_crewmate_tasks) & set(st.session_state.custom_impostor_tasks)
        ):
            dup = set(st.session_state.custom_crewmate_tasks) & set(st.session_state.custom_impostor_tasks)
            st.error(f"⚠️ Remove duplicate tasks first: {', '.join(dup)}")

        else:
            try:
                custom_tasks = None
                if use_custom_tasks:
                    custom_tasks = {
                        "crewmate": st.session_state.custom_crewmate_tasks,
                        "impostor": st.session_state.custom_impostor_tasks
                    }

                gm.start_game(
                    players,
                    st.session_state.mediator if use_mediator else None,
                    custom_tasks
                )

                st.session_state.game_started = True
                st.success("🚀 Mission launched! Head to Role Reveal to assign roles.")
                st.balloons()

            except Exception as e:
                st.error(str(e))


# ===================================================
# ROLE REVEAL
# ===================================================

elif menu == "🕵️  Role Reveal":

    st.markdown("# 🕵️ ROLE REVEAL")

    if not st.session_state.game_started:
        st.markdown("""
        <div class="card card-warning">
            <span class="tag tag-gold">⚠️ NOT STARTED</span>
            <p style="color:#8892b0; margin-top:8px;">Launch the mission from Game Setup first.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="card glow-pulse">
            <span class="tag tag-cyan">🔐 CLASSIFIED</span>
            <p style="color:#8892b0; margin-top:8px;">
                Each player selects their name and privately views their role.
                Make sure <strong>only that player</strong> can see the screen before revealing!
            </p>
        </div>
        """, unsafe_allow_html=True)

        reveal_players = list(gm.get_roles().keys())
        player = st.selectbox("Select your callsign", reveal_players, key="role_reveal_select")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("👁️ REVEAL MY ROLE", use_container_width=True, key="reveal_role_btn"):
                info = gm.reveal_player(player)
                st.divider()

                if info["role"] == "Impostor":
                    st.markdown("""
                    <div class="card card-danger" style="text-align:center; padding:30px;">
                        <div style="font-size:3.5rem; margin-bottom:8px;">🔴</div>
                        <div class="banner-title banner-red">IMPOSTOR</div>
                        <div style="color:#8892b0; margin-top:6px; font-size:.88rem;">
                            Eliminate crewmates without being caught.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="card card-success" style="text-align:center; padding:30px;">
                        <div style="font-size:3.5rem; margin-bottom:8px;">🟢</div>
                        <div class="banner-title banner-green">CREWMATE</div>
                        <div style="color:#8892b0; margin-top:6px; font-size:.88rem;">
                            Complete your tasks and identify the impostors.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="card" style="margin-top:12px;">
                    <span class="tag tag-cyan">MISSION BRIEF</span>
                    <p style="margin-top:10px; font-family:'Exo 2',sans-serif; color:#ccd6f6;">
                        {info["task"]}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="card card-warning" style="margin-top:8px;">
                    <span class="tag tag-gold">⚠️ REMEMBER!</span>
                    <p style="color:#8892b0; margin-top:6px; font-size:.85rem;">
                        Memorize your role and task. Click <strong>Hide</strong> when done.
                    </p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            if st.button("🙈 HIDE", use_container_width=True, key="hide_role_btn"):
                st.success("✅ Screen cleared. Next player can proceed.")
                st.rerun()


# ===================================================
# DEAD BODY REPORT
# ===================================================

elif menu == "☠️  Dead Body Report":

    st.markdown("# ☠️ DEAD BODY REPORT")

    if not st.session_state.game_started:
        st.markdown("""
        <div class="card card-warning">
            <span class="tag tag-gold">⚠️ NOT STARTED</span>
            <p style="color:#8892b0; margin-top:8px;">Launch the mission from Game Setup first.</p>
        </div>
        """, unsafe_allow_html=True)

    elif gm.is_body_reported():
        st.markdown(f"""
        <div class="alarm-card">
            <div style="text-align:center; padding:10px 0;">
                <div style="font-size:3rem; margin-bottom:8px;">🚨</div>
                <div class="banner-title banner-red">EMERGENCY MEETING!</div>
                <p style="color:#8892b0; margin-top:10px;">
                    <strong style="color:#ff3860;">{gm.get_reporter()}</strong>
                    discovered the body of
                    <strong style="color:#ff3860;">{gm.get_victim()}</strong>
                    in <strong style="color:#ffd700;">{gm.get_location()}</strong>.
                </p>
                <p style="color:#8892b0; font-size:.88rem; margin-top:4px;">
                    Proceed to the <strong>Voting</strong> tab to begin the meeting.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        if st.button("🔄 Reset Report", key="reset_report_btn"):
            gm.dead_body_reported = False
            gm.reported_by = None
            gm.victim = None
            gm.location = None
            st.success("Report cleared.")
            st.rerun()

    else:
        st.markdown("""
        <div class="card">
            <span class="tag tag-red">☠ BODY FOUND</span>
            <p style="color:#8892b0; margin-top:8px;">
                A crew member found a dead body. Log the report below — the victim will be marked as eliminated.
            </p>
        </div>
        """, unsafe_allow_html=True)

        alive_players = gm.get_alive_players()

        if not alive_players:
            st.markdown("""
            <div class="card card-warning">
                <span class="tag tag-gold">⚠️</span>
                <span style="color:#8892b0; margin-left:8px;">No alive players remaining.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            col1, col2, col3 = st.columns(3)

            with col1:
                reporter = st.selectbox(
                    "Who found the body?",
                    alive_players,
                    key="dead_body_reporter"
                )

            with col2:
                potential_victims = [p for p in alive_players if p != reporter]
                victim = st.selectbox(
                    "Who died?",
                    potential_victims,
                    key="dead_body_victim"
                )

            with col3:
                location = st.selectbox(
                    "Location found",
                    st.session_state.locations,
                    key="dead_body_location"
                )

            st.write("")
            if st.button("🚨 REPORT DEAD BODY", use_container_width=True, key="report_body_btn", type="primary"):
                kill_success, kill_message = gm.kill_player(victim)

                if not kill_success:
                    st.error(kill_message)
                else:
                    success, message = gm.report_dead_body(reporter, victim, location)

                    if success:
                        st.markdown(f"""
                        <div class="alarm-card" style="text-align:center; margin-top:16px;">
                            <div style="font-size:2.5rem;">🚨</div>
                            <div class="banner-title banner-red" style="margin-top:8px;">{message}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                    else:
                        st.error(message)


# ===================================================
# VOTING
# ===================================================

elif menu == "🗳️  Voting":

    st.markdown("# 🗳️ EMERGENCY MEETING")

    if not st.session_state.game_started:
        st.markdown("""
        <div class="card card-warning">
            <span class="tag tag-gold">⚠️ NOT STARTED</span>
            <p style="color:#8892b0; margin-top:8px;">Launch the mission from Game Setup first.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        if gm.is_body_reported():
            st.markdown(f"""
            <div class="card card-danger">
                <span class="tag tag-red">🚨 MEETING IN PROGRESS</span>
                <div style="display:flex; gap:24px; margin-top:12px; flex-wrap:wrap;">
                    <div>
                        <div style="color:#8892b0; font-size:.72rem; text-transform:uppercase; letter-spacing:.07em;">Reported by</div>
                        <div style="font-family:'Exo 2',sans-serif; font-weight:700; font-size:1rem; color:#ccd6f6;">{gm.get_reporter()}</div>
                    </div>
                    <div>
                        <div style="color:#8892b0; font-size:.72rem; text-transform:uppercase; letter-spacing:.07em;">Victim</div>
                        <div style="font-family:'Exo 2',sans-serif; font-weight:700; font-size:1rem; color:#ff3860;">{gm.get_victim()}</div>
                    </div>
                    <div>
                        <div style="color:#8892b0; font-size:.72rem; text-transform:uppercase; letter-spacing:.07em;">Location</div>
                        <div style="font-family:'Exo 2',sans-serif; font-weight:700; font-size:1rem; color:#ffd700;">{gm.get_location()}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card">
                <span class="tag tag-cyan">📢 OPEN MEETING</span>
                <p style="color:#8892b0; margin-top:8px;">Discuss and vote to eject a suspected impostor from the airlock.</p>
            </div>
            """, unsafe_allow_html=True)

        alive = gm.get_alive_players()

        if len(alive) <= 2:
            st.markdown("""
            <div class="card card-warning">
                <span class="tag tag-gold">⚠️</span>
                <span style="color:#8892b0; margin-left:8px;">Not enough players alive to hold a vote.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            col1, col2 = st.columns(2)

            with col1:
                voter = st.selectbox("Voter", alive, key="voter_select")

            with col2:
                options = [p for p in alive if p != voter]
                voted = st.selectbox("Vote to eject", options, key="vote_against_select")

            if st.button("✅ SUBMIT VOTE", use_container_width=True, key="submit_vote_btn"):
                success, msg = gm.vote(voter, voted)
                if success:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"⚠️ {msg}")

            st.divider()

            if st.button("🔔 END MEETING & TALLY VOTES", use_container_width=True, key="end_meeting_btn", type="primary"):
                eliminated, tie, votes = gm.end_meeting()

                st.markdown("### 📊 Vote Tally")

                if not votes:
                    st.info("No votes were cast.")
                else:
                    max_votes = max(votes.values()) if votes else 1
                    for player, count in sorted(votes.items(), key=lambda x: -x[1]):
                        pct = (count / max_votes) * 100
                        st.markdown(f"""
                        <div style="margin-bottom:10px;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                                <span style="font-family:'Exo 2',sans-serif; font-weight:600;">{player}</span>
                                <span class="tag tag-cyan">{count} vote{'s' if count != 1 else ''}</span>
                            </div>
                            <div class="vote-bar-bg">
                                <div class="vote-bar-fill" style="width:{pct}%;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                st.divider()

                if tie:
                    st.markdown("""
                    <div class="card card-warning" style="text-align:center; padding:24px;">
                        <div style="font-size:2.5rem;">⚖️</div>
                        <div class="banner-title banner-gold" style="margin-top:8px;">TIE — NO EJECTION</div>
                        <p style="color:#8892b0; margin-top:6px;">The vote was split. Nobody leaves the airlock today.</p>
                    </div>
                    """, unsafe_allow_html=True)

                elif eliminated:
                    st.markdown(f"""
                    <div class="card card-danger" style="text-align:center; padding:24px;">
                        <div style="font-size:2.5rem;">🚀</div>
                        <div class="banner-title banner-red" style="margin-top:8px;">{eliminated} EJECTED</div>
                        <p style="color:#8892b0; margin-top:6px;">The crew has spoken. They have been launched into the void.</p>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.info("No one was eliminated.")


# ===================================================
# GAME STATUS
# ===================================================

elif menu == "📊  Game Status":

    st.markdown("# 📊 MISSION STATUS")

    if not st.session_state.game_started:
        st.markdown("""
        <div class="card card-warning">
            <span class="tag tag-gold">⚠️ NOT STARTED</span>
            <p style="color:#8892b0; margin-top:8px;">Launch the mission from Game Setup first.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        alive_players = gm.get_alive_players()
        dead_players  = gm.get_dead_players()
        roles         = gm.get_roles()

        alive_impostors  = [p for p in alive_players if roles[p] == "Impostor"]
        alive_crewmates  = [p for p in alive_players if roles[p] == "Crewmate"]

        # ── Metrics ──
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🟢 Crew Alive",     len(alive_crewmates))
        m2.metric("🔴 Impostors Alive", len(alive_impostors))
        m3.metric("☠️  Eliminated",      len(dead_players))
        m4.metric("👥 Total Players",   len(alive_players) + len(dead_players))

        st.divider()

        # ── Player lists ──
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🟢 Alive Crew")
            if alive_players:
                for p in alive_players:
                    st.markdown(f'<div class="player-chip">🧑‍🚀 {p}</div>', unsafe_allow_html=True)
            else:
                st.info("No survivors.")

        with col2:
            st.markdown("### ☠️ Eliminated")
            if dead_players:
                for p in dead_players:
                    st.markdown(f'<div class="player-chip player-chip-dead">💀 {p}</div>', unsafe_allow_html=True)
            else:
                st.info("No eliminations yet.")

        st.divider()

        # ── Win condition ──
        winner = gm.winner()

        if winner == "Crewmates":
            st.markdown("""
            <div class="card card-success glow-pulse" style="text-align:center; padding:36px;">
                <div style="font-size:4rem; margin-bottom:10px;">🏆</div>
                <div class="banner-title banner-green">CREWMATES WIN!</div>
                <p style="color:#8892b0; margin-top:10px;">
                    The impostors have been rooted out. The ship is safe.
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()

        elif winner == "Impostors":
            st.markdown("""
            <div class="alarm-card" style="text-align:center; padding:36px;">
                <div style="font-size:4rem; margin-bottom:10px;">🔴</div>
                <div class="banner-title banner-red">IMPOSTORS WIN!</div>
                <p style="color:#8892b0; margin-top:10px;">
                    The crew has been sabotaged. There's no one left to stop them.
                </p>
            </div>
            """, unsafe_allow_html=True)

        else:
            # Live threat-o-meter
            total = len(alive_players)
            imp_ratio = len(alive_impostors) / total if total else 0
            threat_pct = imp_ratio * 100

            color = "#00ff88" if threat_pct < 30 else ("#ffd700" if threat_pct < 50 else "#ff3860")
            label = "LOW THREAT" if threat_pct < 30 else ("ELEVATED" if threat_pct < 50 else "CRITICAL")

            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span style="font-family:'Exo 2',sans-serif; font-weight:700; color:#ccd6f6;">⚠️ Threat Level</span>
                    <span class="tag" style="background:rgba(255,255,255,.05); color:{color}; border-color:{color}40;">{label}</span>
                </div>
                <div class="vote-bar-bg">
                    <div class="vote-bar-fill" style="width:{threat_pct:.0f}%; background:linear-gradient(90deg,#00ff88,{color});"></div>
                </div>
                <div style="color:#8892b0; font-size:.78rem; margin-top:6px;">
                    {len(alive_impostors)} impostor{'s' if len(alive_impostors) != 1 else ''} among {total} remaining crew members
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.info("🎮 Mission in progress — keep playing!")

        st.divider()

        if st.button("🔄 START NEW MISSION", use_container_width=True, key="new_game_btn", type="primary"):
            pm.clear_players()
            gm.reset()

            st.session_state.game_started = False
            st.session_state.mediator = ""
            st.session_state.use_mediator = False
            st.session_state.use_custom_tasks = False
            st.session_state.custom_crewmate_tasks = []
            st.session_state.custom_impostor_tasks = []

            st.success("🚀 Mission reset. Ready for a new game!")
            st.rerun()
