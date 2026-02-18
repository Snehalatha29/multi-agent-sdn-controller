import streamlit as st
import sqlite3
import pandas as pd
import os

from database.auth_db import init_user_db, create_user, validate_user

# Init user DB
init_user_db()

st.set_page_config(page_title="Multi-Agent SDN", layout="wide")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------- LOGIN PAGE ----------------
def login_page():
    st.title(" Login Page")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # LOGIN
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if validate_user(username, password):
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # SIGNUP
    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if create_user(new_user, new_pass):
                st.success("Account created! Login now.")
            else:
                st.error("Username already exists")


# ---------------- DASHBOARD ----------------
def dashboard():
    st.title(" Multi-Agent SDN Controller Dashboard")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    db_path = "database/traffic_logs.db"

    if not os.path.exists(db_path):
        st.error("Database not found. Run controller first.")
        return

    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM traffic_logs ORDER BY id DESC LIMIT 50", conn)
    conn.close()

    if df.empty:
        st.warning("No data yet. Generate traffic.")
        return

    st.subheader("📊 Recent Network Data")
    st.dataframe(df)

    st.subheader("📈 Performance Graph")
    st.line_chart(df[["latency", "bandwidth"]])


# ---------------- MAIN ----------------
if st.session_state.logged_in:
    dashboard()
else:
    login_page()
