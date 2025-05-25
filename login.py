import streamlit as st
import os
import json
import requests
from streamlit_lottie import st_lottie

# 🔄 Load Lottie animation (supports URL or local file)
def load_lottiefile(filepath_or_url: str):
    try:
        if filepath_or_url.startswith("http"):
            r = requests.get(filepath_or_url)
            if r.status_code != 200:
                raise Exception("Request failed")
            return r.json()
        else:
            with open(filepath_or_url, "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Could not load animation {filepath_or_url}: {e}")
        return None
#--------API KEYS
api_key = os.getenv("TMDB_API_KEY", "")
API_BASE = "http://localhost:3000"

#-----------KEYSS
def login_user(email, password):
    return requests.post(f"{API_BASE}/check", json={"Email": email, "Password": password})
def forgot_password_request(email):
    return requests.post(f"{API_BASE}/forgotp", json={"Email": email})
def verify_otp(user_id, otp, endpoint="/otp_verify"):
    return requests.post(f"{API_BASE}{endpoint}", json={"User_id": user_id, "Otp": otp})
def resend_otp(user_id, endpoint="/resendotp"):
    return requests.post(f"{API_BASE}{endpoint}", json={"User_id": user_id})
def reset_pass(User_id, Password, Confirm_password):
    return requests.patch(f"{API_BASE}/updatepass", json={
        "User_id": User_id, "Password": Password, "Confirm_password": Confirm_password
    })


# --------------------------- Helpers ---------------------------

def parse_response_json(response):
    try:
        return response.json(), True
    except:
        return {"message": "Invalid server response.", "status": False}, False

# 🔐 Login Page
def login():
    st.markdown("<h1 style='text-align: center;'>🔐 Login to Your Account</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        # ✅ Load animation from LottieFiles URL
        lottie_url = "https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json"  # You can replace this with any Lottie URL
        lottie_login = load_lottiefile(lottie_url)
        if lottie_login:
            st_lottie(lottie_login, height=300, loop=True)

    with col2:
        st.subheader("🔑 Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
               res = login_user(email, password)
               data, success = parse_response_json(res)
               st.write(data)
               if success and isinstance(data, dict) and data.get("status"):
                   st.success("✅ Logged in")
                   st.session_state.authenticated = True
                   st.session_state.page = "app"
                   st.rerun()
               else:
                   message = data.get("message") if isinstance(data, dict) else str(data)
                   st.error(f"❌ Login failed: {message}")

        if st.button("📝 Don't have an account? Sign up"):
          st.session_state.page = "signup"
        if st.button("Forgot Password?"):
            st.session_state.page = "forgot_pass_page"

def forgot_pass_page():
    st.title("🔐 Forgot Password")
    email = st.text_input("Email")

    if st.button("Send OTP"):
        res = forgot_password_request(email)
        data, success = parse_response_json(res)
        st.write("Parsed response:", data)
        st.write("Success:", success)
        if success and isinstance(data, dict) and data.get("status"):
            st.session_state.pending_user_id = data.get("User_id")
            st.session_state.otp_verified = False
            st.success("✅ OTP sent to your email.")
        else:
            message = data.get("message") if isinstance(data, dict) else str(data)
            st.error(f"❌ failed: {message}")

    if "pending_user_id" in st.session_state and not st.session_state.get("otp_verified"):
        otp = st.text_input("Enter OTP")
        if st.button("Verify OTP"):
            res = verify_otp(st.session_state.pending_user_id, otp, endpoint="/forgotpverify")
            data, success = parse_response_json(res)
            if success and data.get("status"):
                st.session_state.otp_verified = True
                st.success("✅ OTP verified. You can now reset your password.")
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

    if st.session_state.get("otp_verified"):
        Password = st.text_input("New Password", type="password")
        Confirm_password = st.text_input("Confirm New Password", type="password")

        if st.button("Reset Password"):
            if Password != Confirm_password:
                st.error("❌ Passwords do not match.")
            elif len(Password) < 6:
                st.warning("⚠️ Password should be at least 6 characters.")
            else:
                User_id = st.session_state.pending_user_id
                res = reset_pass(User_id, Password, Confirm_password)
                st.write("reset debug",res)
                data, success = parse_response_json(res)
                if success and data.get("status"):
                    st.success("🎉 Password reset successful. You can now log in.")
                    del st.session_state.pending_user_id
                    del st.session_state.otp_verified
                    st.session_state.page = "login"
                    st.rerun()
                else:
                   message = data.get("message") or data.get("error") or "Signup failed"
                   st.error(message)







#----------------------first code 








# import streamlit as st
# import sqlite3
# import json
# import requests
# from streamlit_lottie import st_lottie

# # 🔄 Load Lottie animation (supports URL or local file)
# def load_lottiefile(filepath_or_url: str):
#     try:
#         if filepath_or_url.startswith("http"):
#             r = requests.get(filepath_or_url)
#             if r.status_code != 200:
#                 raise Exception("Request failed")
#             return r.json()
#         else:
#             with open(filepath_or_url, "r") as f:
#                 return json.load(f)
#     except Exception as e:
#         st.warning(f"⚠️ Could not load animation {filepath_or_url}: {e}")
#         return None

# # 🔐 Verify credentials
# def check_credentials(username, password):
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
#     data = c.fetchone()
#     conn.close()
#     return data

# # 🔐 Login Page
# def login():
#     st.markdown("<h1 style='text-align: center;'>🔐 Login to Your Account</h1>", unsafe_allow_html=True)
#     col1, col2 = st.columns([1, 2])
#     with col1:
#         # ✅ Load animation from LottieFiles URL
#         lottie_url = "https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json"  # You can replace this with any Lottie URL
#         lottie_login = load_lottiefile(lottie_url)
#         if lottie_login:
#             st_lottie(lottie_login, height=300, loop=True)

#     with col2:
#         st.subheader("🔑 Login")
#         username = st.text_input("👤 Username")
#         password = st.text_input("🔒 Password", type="password")

#         if st.button("🔓 Login"):
#             user = check_credentials(username, password)
#             if user:
#                 st.success(f"✅ Welcome back, {username}!")
#                 st.session_state.authenticated = True
#                 st.session_state.page = "app"
#             else:
#                 st.error("❌ Invalid username or password.")

#         if st.button("📝 Don't have an account? Sign up"):
#             st.session_state.page = "signup"
