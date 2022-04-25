import streamlit as st
from rest_api import get_data as gt
import requests as rq
firebase_url = 'https://sc-rct-default-rtdb.firebaseio.com/users/'


def add_rating(user_name, course_name, instructor_name):
    score = st.slider('Rate for this session:', 1, 5, 3)
    grade_received = st.selectbox('Grade Received: ', ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C- or below'))
    semester = st.text_input('In which semester did you take the course?')
    comment = st.text_area('write a review')
    composite_url = 'https://sc-rct-default-rtdb.firebaseio.com/courses/' + course_name + '/ratings/' + \
                        instructor_name + '/' + user_name + '.json'

    confirm = st.button('ADD')
    if confirm:
        rating_dict = {"username": user_name, "score": score, "grade": grade_received,
                       "semester": semester, "comment": comment}
        rq.patch(composite_url, json=rating_dict)


def course_selection(user_name):
    # description: get the user's discussion course list
    discussion_list = gt.get_user_discussion(user_name)
    course = st.sidebar.selectbox('Select Course from below:', discussion_list)

    # let the user choose to add or remove a course from the list
    # after manipulation, update the firebase info
    course_mani = st.sidebar.selectbox('Add or Delete a course:', ('', 'ADD', 'DELETE'))
    if course_mani == 'ADD':
        course_add = st.sidebar.text_input('Enter the course ID to add:')
        add = st.sidebar.button('Add')
        for j in range(len(course_add)):
            if course_add[j].islower():
                course_add = course_add[:j]+course_add[j].upper()+course_add[j+1:]
        if course_add not in discussion_list and course_add and add:
            discussion_list.append(course_add)
            st.sidebar.success('Add Success! Refresh the page and login to see.')
        elif course_add in discussion_list and add and course_add:
            st.sidebar.error('Text already in the course list.')
        composite_url = firebase_url + user_name + '/discussion.json'
        course_json = {}
        for i in range(len(discussion_list)):
            course_json[i] = discussion_list[i]
        rq.put(composite_url, json=course_json)

    if course_mani == 'DELETE':
        course_delete = st.sidebar.text_input('Enter the course ID to delete:')
        delete = st.sidebar.button('Delete')
        for j in range(len(course_delete)):
            if course_delete[j].islower():
                course_delete = course_delete[:j]+course_delete[j].upper()+course_delete[j+1:]
        if course_delete in discussion_list and course_delete and delete:
            discussion_list.remove(course_delete)
            st.sidebar.success('Delete Success! Refresh the page and login to see')
        elif course_delete not in discussion_list and course_delete and delete:
            st.sidebar.error('Course not in the list.')
        composite_url = firebase_url + user_name +'/discussion.json'
        course_json = {}
        for i in range(len(discussion_list)):
            course_json[i] = discussion_list[i]
        rq.put(composite_url, json=course_json)

    rate_or_not = st.sidebar.radio('', ('View Ratings', 'Add Rating'))
    if rate_or_not == 'View Ratings':
        st.session_state['add_rating'] = False
    elif rate_or_not == 'Add Rating':
        st.session_state['add_rating'] = True

    for i in range(len(discussion_list)):
        if course == discussion_list[i]:
            st.title(f'Course Ratings for {course}:')
            instructor = gt.get_course_instruc(gt.get_course_info(course))
            instructor_chosen = st.radio('Choose instructor', tuple(instructor))
            for instruc in instructor:
                if instructor_chosen == instruc:
                    info = gt.get_rating_info(course, instructor_chosen)
                    if info:
                        users = list(info.keys())
                        for user in users:
                            rating_info = info[user]
                            rating = rating_info['score']
                            semester = rating_info['semester']
                            grade = rating_info['grade']
                            comment = rating_info['comment']
                            st.markdown(user)
                            code = f'Rating: {rating}\nGrade Received: {grade}\nSemester: {semester}\n\n{comment}'
                            st.code(code)
                    else:
                        st.markdown(f'No ratings for {instructor_chosen} yet.')
                    if st.session_state['add_rating']:
                        add_rating(user_name, course, instructor_chosen)