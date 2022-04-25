import streamlit as st
from rest_api.user import User
import rest_api.get_data as gt

login_info = []


def login_function():
    # description: collect username and password information and then compare with the data in the database
    # return True if user successfully logged in.
    user_name = st.text_input('Please enter your username')
    user_pass = st.text_input('Please enter your password:', type='password')
    login_confirm = st.button('Login')
    user_list = gt.get_user_list()

    if login_confirm and user_name and user_name not in user_list:
        st.error('Not registered yet, please create your account.')
    elif user_name and user_pass and login_confirm and user_name in user_list:
        user_info = gt.get_user_info(user_name)
        if user_name and user_pass and login_confirm and user_pass != gt.get_user_password(user_info):
            st.error('Incorrect password')
        elif user_name and user_pass and login_confirm and user_pass == gt.get_user_password(user_info):
            st.success('Login Success!')
            gt.update_login_status(user_name, 'True')
            login_info.append(user_name)
            return user_name


def login_return():
    if login_info:
        return True
    else:
        return False


def get_login():
    return login_info[0]


def logout():
    gt.update_login_status(login_info[0], 'False')
    login_info.pop(0)
