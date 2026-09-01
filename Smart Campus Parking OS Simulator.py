# --- MODULE 1: ENTRANCE GATE SCHEDULING ---

# This list represents the cars waiting outside the LCWU gate
gate_queue = []

def add_car_to_queue(car_name, priority_level):
    # Add the car to our list with its priority (1 = Faculty, 2 = Student)
    gate_queue.append({"car_name": car_name, "priority": priority_level})
    
    # OS LOGIC: Sort the queue based on priority (Shortest Job / Highest Priority First)
    gate_queue.sort(key=lambda x: x["priority"])
    
    print(f"🚗 Arrived: {car_name}. Current Line: {[car['car_name'] for car in gate_queue]}")

def process_gate():
    # If there are cars in line, let the first one in
    if len(gate_queue) > 0:
        entering_car = gate_queue.pop(0) # Removes the car at the front of the line
        print(f"✅ Gate Opened: {entering_car['car_name']} has entered the garage.")
    else:
        print("Gate is idle. No cars waiting.")

# --- TESTING THE LOGIC ---
print("--- Morning Traffic ---")
add_car_to_queue("Student Car A", 2)
add_car_to_queue("Student Car B", 2)

# Oh look, a teacher arrives! Watch them jump the queue.
add_car_to_queue("Faculty Car", 1) 

print("\n--- Processing the Queue ---")
process_gate() # The Faculty car should enter first!
process_gate() # Then Student A
process_gate() # Then Student B
# --- MODULE 2: SEMAPHORES (CAPACITY CONTROL) ---

# We use a variable to act as our Counting Semaphore
TOTAL_SPOTS = 50
available_spots = TOTAL_SPOTS 
waiting_outside = 0

def attempt_to_park(car_name):
    global available_spots, waiting_outside
    
    # OS LOGIC: Check the semaphore value
    if available_spots > 0:
        # If > 0, the car takes a spot and the semaphore decreases by 1
        available_spots -= 1
        print(f"🟢 {car_name} passed the semaphore and parked! (Spots left: {available_spots})")
    else:
        # If = 0, the semaphore BLOCKS the car
        waiting_outside += 1
        print(f"🔴 SEMAPHORE BLOCKED: {car_name} must wait outside. Garage is FULL.")

def car_leaves(car_name):
    global available_spots, waiting_outside
    
    # When a car leaves, the semaphore increases by 1
    if available_spots < TOTAL_SPOTS:
        available_spots += 1
        print(f"👋 {car_name} left. A spot opened up! (Spots left: {available_spots})")
        
        # If cars are waiting, let one in immediately
        if waiting_outside > 0:
            waiting_outside -= 1
            available_spots -= 1
            print(f"➡️ A waiting car was allowed in by the semaphore. (Spots left: {available_spots})")

# --- TESTING THE LOGIC ---
print("\n--- Testing the Semaphore ---")
attempt_to_park("Faculty Car")
attempt_to_park("Student Car A")
attempt_to_park("Student Car B")
attempt_to_park("Student Car C")
attempt_to_park("Student Car D") # Semaphore hits 0 here!

# This 6th car should be blocked by our semaphore
attempt_to_park("Student Car E") 

# A car leaves, freeing up a resource
car_leaves("Faculty Car")
# --- MODULE 3: PROCESS SYNCHRONIZATION (MUTEX) ---

# The Mutex Lock ensures only ONE process can use a specific resource at a time.
# Here, 'Spot #12' is our critical shared resource.
spot_12_locked = False 
spot_12_owner = None

def claim_specific_spot(car_name):
    global spot_12_locked, spot_12_owner
    
    print(f"👀 {car_name} spots empty Spot #12 and tries to pull in...")
    
    # OS LOGIC: Check the Mutex Lock state
    if not spot_12_locked:
        # If unlocked, Car A claims it and instantly engages the lock
        spot_12_locked = True
        spot_12_owner = car_name
        print(f"🔒 MUTEX ACQUIRED: {car_name} successfully parked and locked Spot #12.")
    else:
        # If already locked, Car B is safely rejected (preventing a data crash!)
        print(f"❌ MUTEX DENIED: {car_name} almost crashed! Spot #12 is currently locked by {spot_12_owner}.")

def leave_specific_spot(car_name):
    global spot_12_locked, spot_12_owner
    
    if spot_12_owner == car_name:
        # The car releases the lock when it backs out of the space
        spot_12_locked = False
        spot_12_owner = None
        print(f"🔓 MUTEX RELEASED: {car_name} left. Spot #12 is now unlocked and available.")

# --- TESTING THE LOGIC ---
print("\n--- Testing Synchronization (Mutex Lock) ---")

# Both cars attempt to claim the exact same spot at the same time
claim_specific_spot("Student Car A")
claim_specific_spot("Faculty Car") # This one will be safely rejected!

# The first car finishes using the resource and leaves
leave_specific_spot("Student Car A")

# Now the spot is open again for someone else
claim_specific_spot("Faculty Car")
# --- MODULE 4: DEADLOCK DETECTION & RESOLUTION ---

# Variables tracking who is currently on the single-lane ramp
ramp_car_up = None
ramp_car_down = None
deadlock_detected = False

def enter_ramp(car_name, direction):
    global ramp_car_up, ramp_car_down, deadlock_detected
    
    print(f"🚙 {car_name} enters the ramp heading {direction}.")
    
    if direction == "UP":
        ramp_car_up = car_name
    elif direction == "DOWN":
        ramp_car_down = car_name
        
    # OS LOGIC: Check for a Circular Wait (Deadlock)
    if ramp_car_up is not None and ramp_car_down is not None:
        deadlock_detected = True
        print(f"🚨 DEADLOCK DETECTED! {ramp_car_up} and {ramp_car_down} are stuck nose-to-nose!")
        print("   System frozen. Manual override required.")

def resolve_deadlock(override_car):
    global ramp_car_up, ramp_car_down, deadlock_detected
    
    # OS LOGIC: Force a process to yield its resource
    if deadlock_detected:
        print(f"👮 TRAFFIC WARDEN OVERRIDE: Forcing {override_car} to reverse and yield the ramp.")
        
        if override_car == ramp_car_up:
            ramp_car_up = None
        elif override_car == ramp_car_down:
            ramp_car_down = None
            
        deadlock_detected = False
        print("✅ Deadlock resolved. Traffic is flowing again.")
    else:
        print("System clear. No deadlock to resolve.")

# --- TESTING THE LOGIC ---
print("\n--- Testing Deadlock ---")

# We simulate two cars entering the ramp from opposite directions at the same time
enter_ramp("Student Car A", "UP")
enter_ramp("Faculty Car", "DOWN") # This triggers the deadlock alert!

# The system is frozen. We must use our override function to clear it.
resolve_deadlock("Student Car A")
