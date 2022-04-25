import requests as rq

firebase_url = 'https://sc-rct-default-rtdb.firebaseio.com/'


def get_user_list():
    composite_url = firebase_url+'users/.json'
    response = rq.get(composite_url)
    data = response.json()
    return dict(data).keys()


def get_user_info(username):
    composite_url = firebase_url + 'users/' + username + '.json'
    response = rq.get(composite_url)
    data = response.json()
    return data


def get_user_password(user_data):
    return user_data['password']


def get_user_fname(user_data):
    return user_data['fname']


def get_user_major(user_data):
    return user_data['major']


def get_user_standing(user_data):
    return user_data['standing']


def get_user_lname(user_data):
    return user_data['lname']


def get_user_course(user_name):
    composite_url = firebase_url + 'users/' + user_name + '/course.json'
    response = rq.get(composite_url)
    course_list = response.json()
    return list(course_list)


def get_user_discussion(user_name):
    composite_url = firebase_url + 'users/' + user_name + '/discussion.json'
    response = rq.get(composite_url)
    discussion_list = response.json()
    return list(discussion_list)


def update_login_status(username, status):
    # description: update user_login info, if login --> status = 'True'(string)
    # if logout --> status = 'False' (string)
    composite_url = firebase_url + 'users/' + username + '/login.json'
    rq.patch(composite_url, status)


def get_user_login(user_data):
    return user_data['login']


def get_course_list():
    # description: get the list of courses
    # param: N/A
    # return: course list (list)
    composite_url = firebase_url+'courses/.json'
    response = rq.get(composite_url)
    data = response.json()
    return dict(data).keys()


def get_course_info(course_name):
    # description: get the information of course with course_name as the key
    # param: course_name
    # return: course data as a (dictionary)

    composite_url = firebase_url + 'courses/' + course_name + '.json'
    response = rq.get(composite_url)
    data = response.json()
    return data


def get_course_instruc(course_data):
    # description: get the information of instructors for the course
    # param: dictionary for the course
    # return: the set of instructors (dictionary)
    return course_data['instruc']


def get_course_semester(course_data):
    # description: get the information of semester taught for the course
    # param: dictionary for the course
    # return: the semester of the course taught (list)
    course_semester = []
    if 'Sp' in course_data['semester']:
        course_semester.append('Spring')
    if 'Sm' in course_data['semester']:
        course_semester.append('Summer')
    if 'Fa' in course_data['semester']:
        course_semester.append('Fall')
    return course_semester


def get_course_prereq(course_data):
    # description: get the information of pre-requisite for the course
    # param: dictionary for the course
    # return: name of the pre-req courses (string)
    return course_data['prereq']


def get_course_units(course_data):
    # description: get the information of units for the course
    # param: dictionary for the course
    # return: number of units (as a string)
    return course_data['units']


def get_course_other(course_data):
    # description: get other description for the course
    # param: dictionary for the course
    # return: other description (as a string)
    return course_data['other']


def get_course_descript(course_data):
    # description: get the description of the course
    # param: dictionary for the course
    # return: description of the course (string)
    return course_data['descript']


def get_course_program(course_data):
    # description: get the department of the course
    # param: dictionary for the course
    # return: department of the course (string)
    return course_data['program']


def get_course_name(course_data):
    # description: get the name of the course
    # param: dictionary for the course
    # return: name of the course (string)
    return course_data['name']


def get_courses_list():
    composite_url = firebase_url+'courses/.json'
    response = rq.get(composite_url)
    data = response.json()
    return dict(data).keys()


def get_instructor_list():
    composite_url = firebase_url+'instructors/.json'
    response = rq.get(composite_url)
    data = response.json()
    return list(dict(data).keys())


def get_instructor_info(instructor_name):
    composite_url = firebase_url + 'instructors/' + instructor_name + '.json'
    response = rq.get(composite_url)
    data = response.json()
    return data


def get_rating_info(course_name, instructor_name):
    composite_url = firebase_url + 'courses/' + course_name + '/ratings/' + instructor_name + '.json'
    response = rq.get(composite_url)
    data = response.json()
    return data


def get_chat_list(user_name):
    composite_url = firebase_url + 'users/' + user_name + '/chat.json'
    response = rq.get(composite_url)
    data = response.json()
    return dict(data).keys()


def get_dialogue(user_name, target_name):
    composite_url = firebase_url + 'users/' + user_name + '/chat/' + target_name + '.json'
    response = rq.get(composite_url)
    data = response.json()
    return data


if __name__ == '__main__':
    # get_user_list()
    # print(get_instructor_info('Harvey Fu'))
    # print(get_instructor_list())
    # print(get_course_instruc(get_course_info('DSCI550')))
    print(get_dialogue('harveyfin', 'tigo'))