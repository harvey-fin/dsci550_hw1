import streamlit as st
from rest_api import get_data as gt
import web_scrapper as ws
from rest_api.courses import Course
import requests as rq

firebase_url = 'https://sc-rct-default-rtdb.firebaseio.com/users/'


def course_selection(user_name):
    course_list = gt.get_user_course(user_name)
    course = st.sidebar.selectbox('Select Course from below:', course_list)
    # let the user choose to add or remove a course from the list
    # after manipulation, update the firebase info
    course_mani = st.sidebar.selectbox('Add or Delete a course:', ('', 'ADD', 'DELETE'))
    if course_mani == 'ADD':
        course_add = st.sidebar.text_input('Enter the course ID to add:')
        add = st.sidebar.button('Add')
        for j in range(len(course_add)):
            if course_add[j].islower():
                course_add = course_add[:j]+course_add[j].upper()+course_add[j+1:]
        if course_add not in course_list and course_add and add:
            course_list.append(course_add)
            st.sidebar.success('Add Success! Refresh the page and login to see.')
        elif course_add in course_list and add and course_add:
            st.sidebar.error('Text already in the course list.')
        composite_url = firebase_url + user_name + '/course.json'
        course_json = {}
        for i in range(len(course_list)):
            course_json[i] = course_list[i]
        rq.put(composite_url, json=course_json)
    if course_mani == 'DELETE':
        course_delete = st.sidebar.text_input('Enter the course ID to delete:')
        delete = st.sidebar.button('Delete')
        for j in range(len(course_delete)):
            if course_delete[j].islower():
                course_delete = course_delete[:j]+course_delete[j].upper()+course_delete[j+1:]
        if course_delete in course_list and course_delete and delete:
            course_list.remove(course_delete)
            st.sidebar.success('Delete Success! Refresh the page and login to see')
        elif course_delete not in course_list and course_delete and delete:
            st.sidebar.error('Course not in the list.')
        composite_url = firebase_url + user_name +'/course.json'
        course_json = {}
        for i in range(len(course_list)):
            course_json[i] = course_list[i]
        rq.put(composite_url, json=course_json)

    # description: print the course_info for each course
    # program, semester, course description, prerequisite, instructor, other info
    for i in range(len(course_list)):
        if course == course_list[i]:
            st.title(f'Course Info for {course}:')
            course_data = gt.get_course_info(course)
            if gt.get_course_name(course_data):
                st.subheader(gt.get_course_name(course_data))
            if gt.get_course_program(course_data):
                st.subheader(f'Program: ')
                st.markdown(gt.get_course_program(course_data))
            if gt.get_course_semester(course_data) != 'None':
                course_string= str()
                st.subheader(f'Semester: ')
                for item in gt.get_course_semester(course_data):
                    course_string += ' '+item
                st.markdown(course_string)
            if gt.get_course_units(course_data):
                st.subheader(f'{gt.get_course_units(course_data)}')
            if gt.get_course_descript(course_data):
                st.subheader(f'Course Description: ')
                st.markdown(f'{gt.get_course_descript(course_data)}')
            if gt.get_course_prereq(course_data):
                st.subheader(f'Prerequisite:')
                course_pre = gt.get_course_prereq(course_data)
                course_pre_new = course_pre.replace('Prerequisite', '')
                st.markdown(f'{course_pre_new}')
            if not gt.get_course_prereq(course_data):
                st.subheader(f'Prerequisite:')
                st.markdown(f'None')
            if gt.get_course_instruc(course_data):
                st.subheader(f'Instructors:')
                for item in gt.get_course_instruc(course_data):
                    if item:
                        st.markdown(f'{item}')
            if gt.get_course_other(course_data):
                st.subheader(f'Other information:')
                course_other = gt.get_course_other(course_data)
                course_other_list = course_other.split('\n')
                for other in course_other_list:
                    st.markdown(f'{other}')

    # if course == course_list[1]:
    #     st.title(f'Here is the course info for {course}:')
    # if course == course_list[2]:
    #     st.title(f'Here is the course info for {course}:')

    # should print out the course info, currently using user_input, could use crawler in the future
    # create a direcory in firebase called courses to store course info
    # if the course info is not in the firebase, ask user to update the info
