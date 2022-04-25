import streamlit as st
import rest_api.get_data as gt
import user_register
import course_interface as ci
import discussion_interface as di
import web_scrapper as ws
from rest_api.courses import Course
import requests as rq
import chat_interface as chi


def interface_page():
    user_name = st.session_state['user_name']
    st.sidebar.title(f'Logged in as {user_name}')
    log_out = st.sidebar.button('Log out')
    if log_out:
        st.session_state.runpage = main_page
        gt.update_login_status(user_name, 'False')
        del st.session_state['login']
        del st.session_state['user_name']
        st.experimental_rerun()
    choice2 = st.sidebar.selectbox('Menu', ('Personal Information', 'Course', 'Course Ratings',
                                            'Search For Professors', 'Search For User', 'Chats'))
    if choice2 == 'Personal Information':
        user_info = gt.get_user_info(user_name)
        st.subheader(f'Welcome, {user_name}!')
        st.subheader('Your courses are: ')
        course_str = str()
        for item in user_info['course']:
            course_str += item + '  '
        st.markdown(course_str)
        st.subheader('Your major is: ')
        st.markdown(str(user_info['major']))
        st.subheader('Your current standing is: ')
        st.markdown(user_info['standing'])

    if choice2 == 'Course':
        ci.course_selection(user_name)
    if choice2 == 'Discussion Board':
        di.course_selection(user_name)
    if choice2 == 'Search For Professors':
        instructor_name = st.sidebar.text_input('Please enter the name of the professor: ')
        search = st.sidebar.button('Search')
        if search:
            if instructor_name not in gt.get_instructor_list():
                instructor_dict = ws.instructor_info(instructor_name)
                composite_url = 'https://sc-rct-default-rtdb.firebaseio.com/instructors/' + instructor_name + '.json'
                rq.patch(composite_url, json=instructor_dict)
            elif instructor_name in gt.get_instructor_list():
                instructor_dict = gt.get_instructor_info(instructor_name)
            st.title(f'Instructor Info for:')
            st.subheader(instructor_dict['name'])
            st.subheader(f'TITLE:')
            st.markdown(instructor_dict['title'])
            st.subheader(f'DEPARTMENT:')
            st.markdown(instructor_dict['department'])
            st.subheader('DIVISION:')
            st.markdown(instructor_dict['division'])
            st.subheader('EMAIL')
            st.markdown(instructor_dict['email'])
    if choice2 == 'Search For User':
        search_name = st.sidebar.text_input('Please enter the Username you want to search: ')
        search = st.sidebar.button('Search')
        if search:
            if search_name in gt.get_user_list():
                user_info = gt.get_user_info(search_name)
                st.title(f'User Information for: {search_name}')
                user_full_name = user_info['fname'] + " " + user_info['lname']
                st.subheader(f'NAME')
                st.markdown(user_full_name)
                st.subheader(f'MAJOR')
                st.markdown(user_info['major'])
                st.subheader(f'CURRENT STANDING')
                st.markdown(user_info['standing'])
                st.subheader(f'ENROLLED COURSES')
                course_str = str()
                for item in user_info['course']:
                    course_str += item + '  '
                st.markdown(course_str)
                st.subheader(f'EMAIL')
                st.markdown(user_info['email'])
            else:
                st.subheader(f'\"{search_name}\" does not exist!')
    if choice2 == 'Chats':
        user_info = gt.get_user_info(user_name)
        if 'chat' not in user_info.keys():
            chi.start_chat_function(user_name)
        chat_list = gt.get_chat_list(user_name)
        if 'initial' in chat_list:
            st.subheader('You have no chats yet, start chatting with other users!')
        elif 'initial' not in chat_list:
            target_chat = st.sidebar.selectbox('Select chat window', tuple(chat_list))
            for target in chat_list:
                if target_chat == target:
                    chi.display_chat_window(user_name, target)
                    text_input = st.text_input('Enter new text:')
                    enter = st.button('Enter')
                    if enter:
                        chi.add_chat(user_name, target, text_input)
                    st.button('Refresh')
        target_user = st.sidebar.text_input('Enter the user that you want to chat with:')
        find = st.sidebar.button('FIND')
        if find:
            if target_user not in gt.get_user_list():
                st.sidebar.subheader(f'\"{target_user}\" does not exist!')
            else:
                if target_user in chat_list:
                    st.sidebar.subheader(f'You already started the chat with {target_user}')
                elif target_user not in chat_list:
                    chi.start_chat_with(user_name, target_user)


def main_page():
    st.sidebar.title('Menu')
    choice1 = st.sidebar.selectbox('Login/Signup', ('Login', 'Signup'))

    if choice1 == 'Login':
        # description: collect username and password information and then compare with the data in the database
        # then update the sessionstate.runpage to interface_page
        # update the user_name to session state
        # update the login variable in the session state
        # call the rerun function
        st.title('Welcome to the USC course helper!')
        st.subheader('Login with your credentials')
        user_name = st.text_input('Please enter your username')
        user_pass = st.text_input('Please enter your password:', type='password')
        login_confirm = st.button('Login')
        forgot_password = st.button('Forgot my password')
        if forgot_password:
            st.markdown('Please email harveyfu@usc.edu to retrieve your password.')

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
                st.session_state.runpage = interface_page
                st.session_state['login'] = True
                st.session_state['user_name'] = user_name
                course_list = gt.get_user_course(user_name)
                for course_to_choose in course_list:
                    if course_to_choose not in gt.get_course_list():
                        course_dict = ws.course_info(course_to_choose)
                        if course_dict == 'This course is not available.':
                            continue
                        if 'prerequisite' not in course_dict.keys():
                            course_dict['prerequisite'] = 'None'
                        if 'semester' not in course_dict.keys():
                            course_dict['semester'] = 'None'
                        course_to_create = Course(course_to_choose, course_dict['name'], course_dict['program'],
                                                  course_dict['instructor'], course_dict['units'],
                                                  course_dict['semester'], course_dict['prerequisite'],
                                                  course_dict['description'], course_dict['Other'])
                        course_to_create.upload_course_data()
                st.experimental_rerun()

    if choice1 == 'Signup':
        st.subheader('Create New Account')
        if user_register.create_account():
            st.experimental_rerun()

    if choice1 == 'Login Confirm':
        st.experimental_rerun()


if 'login' not in st.session_state:
    st.session_state.runpage = main_page

st.session_state.runpage()

if __name__ == '__main__':
    # streamlit run /Users/harveyfu/Desktop/pythonProject/DSCI551/Group_Project/main.py
    print('run the code above in terminal')