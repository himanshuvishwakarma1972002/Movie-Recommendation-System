import streamlit as st
import os
import requests
import json
from streamlit_lottie import st_lottie

# 🔄 Load Lottie animation
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Could not load animation {filepath}: {e}")
        return None

# 🔑 TMDB API Key
api_key = os.getenv("TMDB_API_KEY", "")
API_BASE = "http://localhost:3000"

# --------------------------- Helpers ---------------------------

def parse_response_json(response):
    try:
        return response.json(), True
    except:
        return {"message": "Invalid server response.", "status": False}, False

# --------------------------- API Calls ---------------------------

def signup_user(name, email, password, confirm_password):
    return requests.post(f"{API_BASE}/save", json={
        "Name": name, "Email": email, "Password": password, "Confirm_password": confirm_password
    })

def verify_otp(user_id, otp, endpoint="/otp_verify"):
    return requests.post(f"{API_BASE}{endpoint}", json={"User_id": user_id, "Otp": otp})

def resend_otp(user_id, endpoint="/resendotp"):
    return requests.post(f"{API_BASE}{endpoint}", json={"User_id": user_id})


# 📝 Signup Page
def signup():
    st.markdown("<h1 style='text-align: center;'>📝 Create Your Account</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])

    with col1:
        animation = load_lottiefile("signup.json")  # Make sure file exists in same dir
        if animation:
            st_lottie(animation, height=300, loop=True)
        else:
            st.info("Signup animation not found.")

    with col2:
        st.subheader("🚀 Sign Up")
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Send OTP"):
            res = signup_user(name, email, password, confirm)
            data, success = parse_response_json(res)
            if success and data.get("status"):
                st.success("✅ OTP sent.")
                st.session_state.pending_user_id = data.get("User_id")
            else:
                  message = data.get("message") or data.get("error") or "Signup failed"
                  st.error(message)

        if "pending_user_id" in st.session_state:
            otp = st.text_input("Enter OTP")
            if st.button("Verify OTP"):
                res = verify_otp(st.session_state.pending_user_id, otp)
                data, success = parse_response_json(res)
                if success and data.get("status"):
                    st.success("🎉 Signup complete")
                    del st.session_state.pending_user_id
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    message = data.get("message") or data.get("error") or "Signup failed"
                    st.error(message)

            if st.button("Resend OTP"):
                res = resend_otp(st.session_state.pending_user_id)
                _, success = parse_response_json(res)
                if success:
                    st.info("🔁 OTP resent")
                else:
                    st.error("❌ Failed to resend OTP")

    if st.button("🔐 Already have an account? Login"):
        st.session_state.page = "login"
        










# import streamlit as st
# import sqlite3
# import json
# from streamlit_lottie import st_lottie

# # 🔄 Load Lottie animation
# def load_lottiefile(filepath: str):
#     try:
#         with open(filepath, "r") as f:
#             return json.load(f)
#     except Exception as e:
#         st.warning(f"⚠️ Could not load animation {filepath}: {e}")
#         return None

# # 🔒 Check if user exists
# def user_exists(username):
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM users WHERE username = ?', (username,))
#     user = c.fetchone()
#     conn.close()
#     return user is not None

# # ➕ Add new user
# def add_user(username, password):
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     try:
#         c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
#         conn.commit()
#         return True
#     except sqlite3.IntegrityError:
#         return False
#     finally:
#         conn.close()

# # 📝 Signup Page
# def signup():
#     st.markdown("<h1 style='text-align: center;'>📝 Create Your Account</h1>", unsafe_allow_html=True)
#     col1, col2 = st.columns([1, 2])

#     with col1:
#         animation = load_lottiefile("signup.json")  # Make sure file exists in same dir
#         if animation:
#             st_lottie(animation, height=300, loop=True)
#         else:
#             st.info("Signup animation not found.")

#     with col2:
#         st.subheader("🚀 Sign Up")
#         username = st.text_input("👤 Choose a username")
#         password = st.text_input("🔒 Choose a password", type="password")
#         confirm_password = st.text_input("🔒 Confirm password", type="password")

#         if st.button("✅ Create Account"):
#             if not username or not password or not confirm_password:
#                 st.warning("⚠️ Please fill out all fields.")
#             elif password != confirm_password:
#                 st.error("❌ Passwords do not match.")
#             elif user_exists(username):
#                 st.error("❌ Username already exists.")
#             else:
#                 success = add_user(username, password)
#                 if success:
#                     st.success("✅ Account created! Please login.")
#                     st.session_state.page = "login"
#                 else:
#                     st.error("❌ Error creating account.")

#         if st.button("🔐 Already have an account? Login"):
#             st.session_state.page = "login"
