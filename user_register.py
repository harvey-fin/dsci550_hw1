from rest_api.user import User
import streamlit as st
import rest_api.get_data as gt


def create_account():
    # description: ask for user input
    # parameters:
    # a. uname_param: username (string)
    # b. fname_param: user's firstname (string)
    # c. lname_param: user's lastname (string)
    # d. email_param: user's email (string)
    # e. major_param: user's major (string)
    # f. standing_param: user's class standing (string)
    # g. course_list_param: user's course list (list of strings)
    # h. password: user's password

    username_input = st.text_input("Username:")
    password_input = st.text_input('Please enter your password', type='password')
    fname_input = st.text_input("First name:")
    lname_input = st.text_input("Last name:")
    email_input = st.text_input("USC Email:")
    major_input = st.text_input("What is your Major:")
    standing_input = st.selectbox('What is your current school year:', ('freshman', 'sophomore', 'junior', 'senior', 'graduate'))
    course_input = st.text_input("Please enter your currently enrolled courses (separate by commas):")

    submit = st.button('Submit')
    if username_input and fname_input and lname_input and email_input and major_input and standing_input and course_input and submit:
        new_user = User(username_input, fname_input, lname_input, email_input, major_input, standing_input, course_input, password_input)
        new_user.upload_user_data()
        if username_input in gt.get_user_list():
            st.error('User already exist, please login using your credentials')
        else:
            st.success('Account Created.')
    else:
        st.error('Please fill in all the information.')


if __name__ == '__main__':
    create_account()