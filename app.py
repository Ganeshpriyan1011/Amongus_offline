import streamlit as st

from players import PlayerManager
from game import GameManager


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Offline Among Us Manager",
    page_icon="🎮",
    layout="wide"
)

# Custom CSS for improved UI
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 12px;
        font-weight: bold;
    }
    .report-button {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
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
        "Cafeteria",
        "MedBay",
        "Electrical",
        "Upper Engine",
        "Lower Engine",
        "Security",
        "Reactor",
        "Navigation",
        "O2",
        "Weapons",
        "Shields",
        "Communications",
        "Storage",
        "Admin",
        "Laboratory"
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

st.sidebar.title("🎮 Offline Among Us")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Game Setup",
        "Role Reveal",
        "Dead Body Report",
        "Voting",
        "Game Status"
    ]
)


# ===================================================
# GAME SETUP
# ===================================================

if menu == "Game Setup":

    st.title("🎮 Offline Among Us Manager")
    
    st.markdown("""
    <div class='info-box'>
        <h3>📋 Game Setup</h3>
        <p>Add players and configure game settings. Impostors will be automatically assigned based on player count.</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.subheader("➕ Add Player")

    col1, col2 = st.columns([4, 1])

    with col1:
        player_name = st.text_input(
            "Player Name",
            placeholder="Enter player name",
            key="player_name_input"
        )

    with col2:

        st.write("")
        st.write("")

        if st.button("Add", key="add_player_btn"):

            success, message = pm.add_player(player_name)

            if success:
                st.success(message)
            else:
                st.error(message)

    st.divider()

    st.subheader("👥 Current Players")

    players = pm.get_players()

    if len(players) == 0:
        st.info("No players added.")

    else:

        for player in players:

            c1, c2 = st.columns([8, 1])

            c1.write("✅ " + player)

            if c2.button(
                "❌",
                key="remove_" + player
            ):
                pm.remove_player(player)
                st.rerun()

    st.divider()

    st.subheader("👨‍⚖️ Mediator (Optional)")

    use_mediator = st.checkbox("Use a Mediator", value=st.session_state.use_mediator)
    st.session_state.use_mediator = use_mediator

    if use_mediator:
        mediator = st.text_input(
            "Mediator Name",
            value=st.session_state.mediator,
            key="mediator_input"
        )
        st.session_state.mediator = mediator
        st.info("The mediator will not participate in the game but can help manage it.")
    else:
        st.session_state.mediator = ""
        st.info("No mediator - all players will participate in the game.")

    st.divider()

    st.subheader("🔴 Impostor Assignment")

    player_count = len(players)
    if player_count >= 4:
        if player_count <= 5:
            auto_impostors = 1
        elif player_count <= 8:
            auto_impostors = 2
        else:
            auto_impostors = 3
        
        st.markdown(f"""
        <div class='info-box'>
            <h4>🤖 Automatic Impostor Count</h4>
            <p>With <strong>{player_count}</strong> players, the game will assign <strong>{auto_impostors}</strong> impostor(s).</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Add at least 4 players to see impostor assignment.")

    st.divider()

    st.subheader("🗺 Game Locations")

    st.markdown("""
    <div class='info-box'>
        <h4>📍 Configure Game Locations</h4>
        <p>Add or remove locations where dead bodies can be found.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])

    with col1:
        new_location = st.text_input(
            "Add Location",
            placeholder="Enter location name",
            key="new_location_input"
        )

    with col2:
        st.write("")
        st.write("")
        if st.button("Add", key="add_location_btn"):
            if new_location.strip():
                if new_location not in st.session_state.locations:
                    st.session_state.locations.append(new_location.strip())
                    st.success(f"{new_location} added!")
                    st.rerun()
                else:
                    st.error("Location already exists.")
            else:
                st.error("Enter a location name.")

    st.subheader("Current Locations")
    if st.session_state.locations:
        for loc in st.session_state.locations:
            c1, c2 = st.columns([8, 1])
            c1.write("📍 " + loc)
            if c2.button("❌", key="remove_loc_" + loc):
                st.session_state.locations.remove(loc)
                st.rerun()
    else:
        st.warning("No locations added.")

    st.divider()

    st.subheader("📋 Game Tasks")

    use_custom_tasks = st.checkbox("Use Custom Tasks", value=st.session_state.use_custom_tasks)
    st.session_state.use_custom_tasks = use_custom_tasks

    if use_custom_tasks:
        st.markdown("""
        <div class='info-box'>
            <h4>📝 Configure Custom Tasks</h4>
            <p>Add custom tasks for crewmates and impostors.</p>
        </div>
        """, unsafe_allow_html=True)

        # Crewmate Tasks
        st.subheader("🟢 Crewmate Tasks")
        col1, col2 = st.columns([4, 1])
        with col1:
            new_crewmate_task = st.text_input(
                "Add Crewmate Task",
                placeholder="Enter task description",
                key="new_crewmate_task"
            )
        with col2:
            st.write("")
            st.write("")
            if st.button("Add", key="add_crewmate_task"):
                if new_crewmate_task.strip():
                    st.session_state.custom_crewmate_tasks.append(new_crewmate_task.strip())
                    st.success("Crewmate task added!")
                    st.rerun()
                else:
                    st.error("Enter a task description.")

        if st.session_state.custom_crewmate_tasks:
            st.write("Current Crewmate Tasks:")
            for i, task in enumerate(st.session_state.custom_crewmate_tasks):
                c1, c2 = st.columns([8, 1])
                c1.write(f"{i+1}. {task}")
                if c2.button("❌", key=f"remove_crew_{i}"):
                    st.session_state.custom_crewmate_tasks.pop(i)
                    st.rerun()
        else:
            st.warning("No crewmate tasks added.")

        st.divider()

        # Impostor Tasks
        st.subheader("🔴 Impostor Tasks")
        col1, col2 = st.columns([4, 1])
        with col1:
            new_impostor_task = st.text_input(
                "Add Impostor Task",
                placeholder="Enter task description",
                key="new_impostor_task"
            )
        with col2:
            st.write("")
            st.write("")
            if st.button("Add", key="add_impostor_task"):
                if new_impostor_task.strip():
                    st.session_state.custom_impostor_tasks.append(new_impostor_task.strip())
                    st.success("Impostor task added!")
                    st.rerun()
                else:
                    st.error("Enter a task description.")

        if st.session_state.custom_impostor_tasks:
            st.write("Current Impostor Tasks:")
            for i, task in enumerate(st.session_state.custom_impostor_tasks):
                c1, c2 = st.columns([8, 1])
                c1.write(f"{i+1}. {task}")
                if c2.button("❌", key=f"remove_imp_{i}"):
                    st.session_state.custom_impostor_tasks.pop(i)
                    st.rerun()
        else:
            st.warning("No impostor tasks added.")

        # Check for duplicate tasks between crewmate and impostor
        duplicate_tasks = set(st.session_state.custom_crewmate_tasks) & set(st.session_state.custom_impostor_tasks)
        if duplicate_tasks:
            st.warning(f"Warning: These tasks appear in both lists: {', '.join(duplicate_tasks)}. Crewmates and impostors should have different tasks.")
    else:
        st.markdown("""
        <div class='info-box'>
            <h4>📝 Default Tasks</h4>
            <p>Using default task list for crewmates and impostors.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    if st.button(
        "🎮 Start Game",
        use_container_width=True,
        key="start_game_btn"
    ):

        if len(players) < 4:

            st.error(
                "Minimum 4 players required."
            )

        elif use_mediator and mediator.strip() == "":

            st.error(
                "Enter mediator name."
            )

        elif use_custom_tasks and (len(st.session_state.custom_crewmate_tasks) == 0 or len(st.session_state.custom_impostor_tasks) == 0):

            st.error(
                "Add at least one crewmate and one impostor task when using custom tasks."
            )

        elif use_custom_tasks:
            # Check for duplicate tasks
            duplicate_tasks = set(st.session_state.custom_crewmate_tasks) & set(st.session_state.custom_impostor_tasks)
            if duplicate_tasks:
                st.error(
                    f"Remove duplicate tasks: {', '.join(duplicate_tasks)}. Crewmates and impostors must have different tasks."
                )
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
                        mediator if use_mediator else None,
                        custom_tasks
                    )

                    st.session_state.game_started = True

                    st.success(
                        "🎮 Game Started Successfully!"
                    )

                    st.balloons()

                except Exception as e:

                    st.error(str(e))
        else:

            try:

                gm.start_game(
                    players,
                    mediator if use_mediator else None
                )

                st.session_state.game_started = True

                st.success(
                    "🎮 Game Started Successfully!"
                )

                st.balloons()

            except Exception as e:

                st.error(str(e))


# ===================================================
# ROLE REVEAL
# ===================================================

elif menu == "Role Reveal":

    st.title("🕵 Secret Role Reveal")

    if not st.session_state.game_started:

        st.warning("Start the game first.")

    else:

        st.markdown("""
        <div class='warning-box'>
            <h4>⚠️ Secret Role Reveal</h4>
            <p>Select a player to reveal their role privately. Make sure only that player can see the screen!</p>
        </div>
        """, unsafe_allow_html=True)

        reveal_players = gm.get_roles().keys()

        player = st.selectbox(
            "Select Player",
            reveal_players,
            key="role_reveal_select"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "👁 Reveal Role",
                use_container_width=True,
                key="reveal_role_btn"
            ):

                info = gm.reveal_player(player)

                st.divider()

                if info["role"] == "Impostor":

                    st.markdown("""
                    <div class='danger-box'>
                        <h2>🔴 IMPOSTOR</h2>
                    </div>
                    """, unsafe_allow_html=True)

                else:

                    st.markdown("""
                    <div class='success-box'>
                        <h2>🟢 CREWMATE</h2>
                    </div>
                    """, unsafe_allow_html=True)

                st.subheader("📋 Task")

                st.info(info["task"])

                st.warning(
                    "After the player finishes reading, click Hide."
                )

        with col2:
            if st.button(
                "🙈 Hide",
                use_container_width=True,
                key="hide_role_btn"
            ):

                st.success("Ready for next player.")
                st.rerun()


# ===================================================
# DEAD BODY REPORT
# ===================================================

elif menu == "Dead Body Report":

    st.title("☠ Dead Body Report")

    if not st.session_state.game_started:

        st.warning("Start the game first.")

    else:

        if gm.is_body_reported():
            
            st.markdown(f"""
            <div class='danger-box'>
                <h2>🚨 EMERGENCY MEETING CALLED!</h2>
                <p><strong>{gm.get_reporter()}</strong> reported <strong>{gm.get_victim()}</strong>'s body at <strong>{gm.get_location()}</strong>!</p>
                <p>Proceed to the Voting section to discuss and vote.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Reset Report", key="reset_report_btn"):
                gm.dead_body_reported = False
                gm.reported_by = None
                gm.victim = None
                gm.location = None
                st.success("Report reset.")
                st.rerun()

        else:

            st.markdown("""
            <div class='info-box'>
                <h4>📢 Report a Dead Body</h4>
                <p>When a player finds a dead body, they can report it to call an emergency meeting. The victim will be automatically marked as dead.</p>
            </div>
            """, unsafe_allow_html=True)

            alive_players = gm.get_alive_players()

            if len(alive_players) == 0:
                st.warning("No alive players to report.")
            else:

                col1, col2, col3 = st.columns(3)

                with col1:
                    reporter = st.selectbox(
                        "Who found the body?",
                        alive_players,
                        key="dead_body_reporter"
                    )

                with col2:
                    # Exclude reporter from victim selection
                    potential_victims = [p for p in alive_players if p != reporter]
                    victim = st.selectbox(
                        "Who died?",
                        potential_victims,
                        key="dead_body_victim"
                    )

                with col3:
                    location = st.selectbox(
                        "Location",
                        st.session_state.locations,
                        key="dead_body_location"
                    )

                if st.button(
                    "🚨 Report Dead Body",
                    use_container_width=True,
                    key="report_body_btn"
                ):

                    # First kill the victim
                    kill_success, kill_message = gm.kill_player(victim)
                    
                    if not kill_success:
                        st.error(kill_message)
                    else:
                        # Then report the body
                        success, message = gm.report_dead_body(reporter, victim, location)

                        if success:
                            st.markdown(f"""
                            <div class='danger-box'>
                                <h2>🚨 {message}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                            st.balloons()
                        else:
                            st.error(message)


# ===================================================
# VOTING
# ===================================================

elif menu == "Voting":

    st.title("🗳 Emergency Meeting")

    if not st.session_state.game_started:

        st.warning("Start the game first.")

    else:

        if gm.is_body_reported():
            st.markdown(f"""
            <div class='danger-box'>
                <h4>🚨 Emergency Meeting</h4>
                <p>Called by: <strong>{gm.get_reporter()}</strong></p>
                <p>Victim: <strong>{gm.get_victim()}</strong></p>
                <p>Location: <strong>{gm.get_location()}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='info-box'>
                <h4>📢 Emergency Meeting</h4>
                <p>Discuss and vote to eliminate a suspected impostor.</p>
            </div>
            """, unsafe_allow_html=True)

        alive = gm.get_alive_players()

        if len(alive) <= 2:

            st.info("Not enough players alive for voting.")

        else:

            col1, col2 = st.columns(2)

            with col1:

                voter = st.selectbox(
                    "Voter",
                    alive,
                    key="voter_select"
                )

            with col2:

                options = [
                    p for p in alive
                    if p != voter
                ]

                voted = st.selectbox(
                    "Vote Against",
                    options,
                    key="vote_against_select"
                )

            if st.button(
                "Submit Vote",
                use_container_width=True,
                key="submit_vote_btn"
            ):

                success, msg = gm.vote(
                    voter,
                    voted
                )

                if success:
                    st.success(msg)

                else:
                    st.error(msg)

            st.divider()

            if st.button(
                "End Meeting",
                use_container_width=True,
                key="end_meeting_btn"
            ):

                eliminated, tie, votes = gm.end_meeting()

                st.subheader("Vote Results")

                if len(votes) == 0:

                    st.info("No votes cast.")

                else:

                    for player, count in votes.items():

                        st.write(
                            f"**{player}** : {count}"
                        )

                st.divider()

                if tie:

                    st.markdown("""
                    <div class='warning-box'>
                        <h3>⚠️ Tie! Nobody was eliminated.</h3>
                    </div>
                    """, unsafe_allow_html=True)

                elif eliminated:

                    st.markdown(f"""
                    <div class='danger-box'>
                        <h3>☠ {eliminated} has been eliminated.</h3>
                    </div>
                    """, unsafe_allow_html=True)

                else:

                    st.info(
                        "Nobody eliminated."
                    )


# ===================================================
# GAME STATUS
# ===================================================

elif menu == "Game Status":

    st.title("📊 Game Status")

    if not st.session_state.game_started:

        st.warning("Start the game first.")

    else:

        alive_players = gm.get_alive_players()
        dead_players = gm.get_dead_players()

        roles = gm.get_roles()

        alive_impostors = [
            p for p in alive_players
            if roles[p] == "Impostor"
        ]

        alive_crewmates = [
            p for p in alive_players
            if roles[p] == "Crewmate"
        ]

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("🟢 Alive Players")

            if alive_players:
                for player in alive_players:
                    st.success(player)
            else:
                st.info("None")

        with col2:

            st.subheader("☠ Dead Players")

            if dead_players:
                for player in dead_players:
                    st.error(player)
            else:
                st.info("None")

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Crewmates Alive",
                len(alive_crewmates),
                delta_color="normal"
            )

        with c2:
            st.metric(
                "Impostors Alive",
                len(alive_impostors),
                delta_color="inverse"
            )

        st.divider()

        winner = gm.winner()

        if winner == "Crewmates":

            st.markdown("""
            <div class='success-box'>
                <h2>🏆 CREWMATES WIN!</h2>
            </div>
            """, unsafe_allow_html=True)

        elif winner == "Impostors":

            st.markdown("""
            <div class='danger-box'>
                <h2>🔴 IMPOSTORS WIN!</h2>
            </div>
            """, unsafe_allow_html=True)

        else:

            st.info("Game is still in progress.")

        st.divider()

        if st.button(
            "🔄 New Game",
            use_container_width=True,
            key="new_game_btn"
        ):

            pm.clear_players()
            gm.reset()

            st.session_state.game_started = False
            st.session_state.mediator = ""
            st.session_state.use_mediator = False
            st.session_state.use_custom_tasks = False
            st.session_state.custom_crewmate_tasks = []
            st.session_state.custom_impostor_tasks = []

            st.success("Game Reset Successfully!")

            st.rerun()


# ===================================================
# FOOTER
# ===================================================

st.sidebar.divider()

st.sidebar.info(
    "🎮 Offline Among Us Manager\n\n"
    "Developed using Streamlit\n\n"
    "Version 2.0"
)
