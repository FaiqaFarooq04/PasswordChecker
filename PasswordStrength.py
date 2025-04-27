import streamlit as st 
import re
import random
import string
import time
import io

if "password_history" not in st.session_state:
    st.session_state.password_history = []

if "last_password" not in st.session_state:
    st.session_state.last_password = None


def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))


def check_password_strength(password):
    blacklist = {"password", "123456", "qwerty", "password123", "letmein", "admin", "welcome"}
    score = 0
    feedback = []

    if password.lower() in blacklist:
        return 0, ["❌ This password is too common. Please choose another."]

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    return score, feedback


def animated_strength_meter(score):
    percent_target = int((score / 4) * 100)
    progress_placeholder = st.empty()
    text_placeholder = st.empty()

    for percent in range(0, percent_target + 1, 5):
        if percent == 100:
            color = "#4CAF50"
        elif percent >= 70:
            color = "#FF9800"
        else:
            color = "#f44336"

        progress_bar_html = f"""
        <div style="margin-top: 10px;">
            <div style="background-color: #ddd; width: 100%; height: 25px; border-radius: 5px;">
                <div style="width: {percent}%; height: 25px; background-color: {color}; border-radius: 5px;"></div>
            </div>
        </div>
        """
        progress_placeholder.markdown(progress_bar_html, unsafe_allow_html=True)
        text_placeholder.markdown(f"*Strength: {percent}%*")
        time.sleep(0.02)


st.set_page_config(page_title="Password Strength",page_icon="🔐")
st.title("🔐 Password Strength Checker")

password = st.text_input("Enter a password to check", type="password")

if password:
    score, messages = check_password_strength(password)
    animated_strength_meter(score)

    if score == 4:
        st.success("✅ Strong Password!")
        st.session_state.last_password = password  # store it temporarily
        if st.button("💾 Save This Password"):
            if password not in st.session_state.password_history:
                st.session_state.password_history.append(password)
                st.success("Password saved.")
    elif score >= 3:
        st.warning("⚠ Moderate Password")
    else:
        st.error("❌ Weak Password")

    for msg in messages:
        st.write(msg)


if "generated_password" not in st.session_state:
    st.session_state.generated_password = ""

# Generate and store the password when button is clicked
if st.button("🎲 Generate a Strong Password"):
    st.session_state.generated_password = generate_strong_password()

# Display the generated password and save button if it exists
if st.session_state.generated_password:
    st.code(st.session_state.generated_password)

    if st.button("💾 Save Generated Password"):
        pwd = st.session_state.generated_password
        if pwd not in st.session_state.password_history:
            st.session_state.password_history.append(pwd)
            st.success("Generated password saved.")
        else:
            st.info("Password already saved.")


if st.button("Clear History"):
    st.session_state.password_history.clear()

with st.expander("📂 View Saved Passwords (Click to Show)", expanded=False):    
    if st.session_state.password_history:
        for i, pwd in enumerate(st.session_state.password_history, 1):
            st.write(f"{i}.** {pwd}")
    else:
            st.info("No passwords saved yet.")

if st.session_state.password_history:
    buffer = io.StringIO("\n".join(st.session_state.password_history))
    st.download_button(
        label="Download Saved Passwords",
        data=buffer.getvalue(),
        file_name="saved_passwords.txt",
        mime="text/plain",
        icon=":material/download:"
    )