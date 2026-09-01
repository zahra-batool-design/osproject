import streamlit as st

# --- INITIALIZE SYSTEM STATE (OS RAM) ---
if "gate_queue" not in st.session_state:
    st.session_state.gate_queue = []
if "TOTAL_SPOTS" not in st.session_state:
    st.session_state.TOTAL_SPOTS = 50
if "available_spots" not in st.session_state:
    st.session_state.available_spots = 50
if "waiting_outside" not in st.session_state:
    st.session_state.waiting_outside = 0
if "spot_12_locked" not in st.session_state:
    st.session_state.spot_12_locked = False
if "spot_12_owner" not in st.session_state:
    st.session_state.spot_12_owner = None
if "ramp_car_up" not in st.session_state:
    st.session_state.ramp_car_up = None
if "ramp_car_down" not in st.session_state:
    st.session_state.ramp_car_down = None
if "deadlock_detected" not in st.session_state:
    st.session_state.deadlock_detected = False

# APP SETTINGS
st.set_page_config(page_title="Smart Campus Parking OS Simulator", layout="wide")
st.title("🚗 Smart Campus Parking OS Simulator")
st.markdown("---")

# SIDEBAR FOR LIVE METRICS
with st.sidebar:
    st.header("📊 Live OS Status")
    st.metric(label="Available Spots (Semaphore)", value=st.session_state.available_spots)
    st.metric(label="Blocked Cars (Waiting)", value=st.session_state.waiting_outside)
    st.markdown("---")
    if st.button("🔄 Reset System"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# 4 MODULES TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Gate Scheduling", 
    "🚦 Semaphores", 
    "🔒 Mutex Sync", 
    "🚨 Deadlock Detection"
])

# --- MODULE 1: GATE SCHEDULING ---
with tab1:
    st.header("📋 Module 1: Entrance Gate Scheduling")
    col1, col2 = st.columns(2)
    with col1:
        car_name = st.text_input("Car Name:", value="Student Car A", key="g1")
        priority = st.selectbox("Priority Level:", ["1 - Faculty", "2 - Student"])
        
        if st.button("Add Car to Queue"):
            p_level = 1 if "Faculty" in priority else 2
            # Sobia's exact logic: Append and sort
            st.session_state.gate_queue.append({"car_name": car_name, "priority": p_level})
            st.session_state.gate_queue.sort(key=lambda x: x["priority"])
            st.success(f"🚗 Arrived: {car_name}")
            
    with col2:
        st.subheader("Current Line (Queue)")
        if st.session_state.gate_queue:
            for idx, car in enumerate(st.session_state.gate_queue):
                icon = "👑 Faculty" if car['priority'] == 1 else "🎓 Student"
                st.write(f"**{idx+1}.** {car['car_name']} ({icon})")
        else:
            st.info("Gate is idle. No cars waiting.")
            
        if st.button("Process Gate (Open Gate)"):
            if len(st.session_state.gate_queue) > 0:
                entering_car = st.session_state.gate_queue.pop(0)
                st.success(f"✅ Gate Opened: {entering_car['car_name']} has entered the garage.")
            else:
                st.warning("Gate is idle. No cars waiting.")

# --- MODULE 2: SEMAPHORES ---
with tab2:
    st.header("🚦 Module 2: Counting Semaphores")
    col1, col2 = st.columns(2)
    with col1:
        sem_car = st.text_input("Car Name to Park:", value="Student Car X", key="s1")
        if st.button("Attempt to Park"):
            if st.session_state.available_spots > 0:
                st.session_state.available_spots -= 1
                st.success(f"🟢 {sem_car} parked! Spots left: {st.session_state.available_spots}")
            else:
                st.session_state.waiting_outside += 1
                st.error(f"🔴 SEMAPHORE BLOCKED: {sem_car} must wait outside. Garage is FULL.")
                
    with col2:
        leave_car = st.text_input("Car Name to Leave:", value="Student Car X", key="s2")
        if st.button("Car Leaves"):
            if st.session_state.available_spots < st.session_state.TOTAL_SPOTS:
                st.session_state.available_spots += 1
                st.info(f"👋 {leave_car} left.")
                if st.session_state.waiting_outside > 0:
                    st.session_state.waiting_outside -= 1
                    st.session_state.available_spots -= 1
                    st.warning("➡️ A waiting car was allowed in by the semaphore.")

# --- MODULE 3: MUTEX ---
with tab3:
    st.header("🔒 Module 3: Process Synchronization (Mutex)")
    m_car = st.text_input("Car trying to claim Spot #12:", value="Student Car A", key="m1")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Claim Spot #12"):
            if not st.session_state.spot_12_locked:
                st.session_state.spot_12_locked = True
                st.session_state.spot_12_owner = m_car
                st.success(f"🔒 MUTEX ACQUIRED: {m_car} locked Spot #12.")
            else:
                st.error(f"❌ MUTEX DENIED: Held by {st.session_state.spot_12_owner}.")
    with c2:
        if st.button("Leave Spot #12"):
            if st.session_state.spot_12_owner == m_car:
                st.session_state.spot_12_locked = False
                st.session_state.spot_12_owner = None
                st.info(f"🔓 MUTEX RELEASED: Spot #12 is now unlocked.")

# --- MODULE 4: DEADLOCK ---
with tab4:
    st.header("🚨 Module 4: Deadlock Detection & Resolution")
    col1, col2 = st.columns(2)
    with col1:
        d_car = st.text_input("Car entering ramp:", value="Faculty Car", key="d1")
        direction = st.radio("Direction:", ["UP", "DOWN"])
        if st.button("Enter Ramp"):
            if direction == "UP":
                st.session_state.ramp_car_up = d_car
            else:
                st.session_state.ramp_car_down = d_car
            if st.session_value.ramp_car_up and st.session_state.ramp_car_down:
                st.session_state.deadlock_detected = True
        
        if st.session_state.deadlock_detected:
            st.error(f"🚨 DEADLOCK DETECTED! {st.session_state.ramp_car_up} and {st.session_state.ramp_car_down} are stuck!")
        else:
            st.info(f"Ramp Up: {st.session_state.ramp_car_up} | Ramp Down: {st.session_state.ramp_car_down}")
            
    with col2:
        if st.session_state.deadlock_detected:
            victim = st.selectbox("Force to reverse:", [st.session_state.ramp_car_up, st.session_state.ramp_car_down])
            if st.button("Resolve Deadlock"):
                if victim == st.session_state.ramp_car_up:
                    st.session_state.ramp_car_up = None
                else:
                    st.session_state.ramp_car_down = None
                st.session_state.deadlock_detected = False
                st.success("✅ Deadlock resolved.")