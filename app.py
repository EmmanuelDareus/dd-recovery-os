import streamlit as st

# Page Config
st.set_page_config(page_title="ToonFit Tracker", page_icon="💥", layout="centered")

# Custom Styling for a Fun, Comic Vibe
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fc;
    }
    h1 {
        color: #ff4757;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 2px 2px #ff6b81;
    }
    .stButton>button {
        background-color: #2ed573;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        border: 2px solid #26af5f;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("💥 ToonFit: The Comic Workout Tracker!")
st.write("Level up your real-life stats just like an anime or cartoon hero. No boring spreadsheets allowed.")

# Sidebar for Hero Profile
st.sidebar.header("🦸‍♂️ Hero Profile")
hero_name = st.sidebar.text_input("Hero Name", "Saitama Junior")
hero_class = st.sidebar.selectbox("Hero Class", ["Brawler", "Speedster", "Tank", "Wizard"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏆 Unlock Pro Sidekick")
st.sidebar.markdown("[Upgrade for $3 (Unlock Boss Fights)](https://buy.stripe.com/your_link_here)")

# Main Workout Logging Section
st.subheader("⚡ Log Today's Hero Training")

col1, col2 = st.columns(2)

with col1:
    pushups = st.number_input("Push-ups completed", min_value=0, value=0, step=5)
    squats = st.number_input("Squats completed", min_value=0, value=0, step=5)

with col2:
    running = st.number_input("Running (Minutes)", min_value=0, value=0, step=5)
    water = st.number_input("Water intake (Glasses)", min_value=0, value=0, step=1)

# Calculate "XP" (Experience Points)
total_xp = (pushups * 2) + (squats * 2) + (running * 5) + (water * 10)

if st.button("🚀 Submit Training & Gain XP!"):
    st.success(f"Awesome job, Hero {hero_name}! You earned **{total_xp} XP** today!")
    
    # Dynamic Cartoon Badges based on XP
    st.markdown("### 🏅 Daily Achievement Badges Unlocked:")
    if total_xp >= 100:
        st.balloons()
        st.markdown("🌟 **Super Saiyan Status:** Absolute workout beast!")
    elif total_xp >= 50:
        st.markdown("🔥 **On Fire:** Consistency is building your power level!")
    elif total_xp > 0:
        st.markdown("🌱 **Level 1 Novice:** The journey of a thousand miles begins with one rep.")
    else:
        st.markdown("💤 **Couch Potato Mode:** Zero XP. Time to drop and give me ten!")

# Progress Tracker visualization
st.markdown("---")
st.subheader("📊 Daily Power Meter")
progress_val = min(total_xp / 200.0, 1.0) # 200 XP maxes out the daily bar
st.progress(progress_val)
st.caption(f"Power Capacity: {total_xp} / 200 XP Daily Goal")