import requests as rq
import json
firebase_url = 'https://sc-rct-default-rtdb.firebaseio.com/users/'


class User():
    def __init__(self, uname_param, fname_param, lname_param,
                 email_param, major_param, standing_param, course_list_param, password_param):
        # description: initialize user data
        # parameters:
        # a. uname_param: username (string)
        # b. fname_param: user's firstname (string)
        # c. lname_param: user's lastname (string)
        # d. email_param: user's email (string)
        # e. major_param: user's major (string)
        # f. standing_param: user's class standing (string)
        # g. course_list_param: user's enrolled course list (string)
        # h. user's password (string)
        # i. user's login status (boolean), default to be false
        # j. user's discussion board course list, default set to be the enrolled course list

        self.uname = uname_param
        self.fname = fname_param
        self.lname = lname_param
        self.email = email_param
        self.major = major_param
        self.standing = standing_param
        self.course = course_list_param
        self.password = password_param
        self.login = 'False'
        self.discussion = course_list_param

    def course_format(self):
        # description: adjust the course_list input into the AAAA000 format.
        # Always call this function once user input course data
        self.course = self.course.split(',')
        for i in range(len(self.course)):
            self.course[i] = self.course[i].strip(' ')
            for j in range(len(self.course[i])):
                if self.course[i][j].islower():
                    self.course[i] = self.course[i][:j]+self.course[i][j].upper()+self.course[i][j+1:]

    def discussion_format(self):
        # description: adjust the course_list input into the AAAA000 format.
        # Always call this function once user input course data
        self.discussion = self.discussion.split(',')
        for i in range(len(self.discussion)):
            self.discussion[i] = self.discussion[i].strip(' ')
            for j in range(len(self.discussion[i])):
                if self.discussion[i][j].islower():
                    self.discussion[i] = self.discussion[i][:j]+self.discussion[i][j].upper()+self.discussion[i][j+1:]

    def upload_user_data(self):
        # description: upload the user data to the firebase.
        # only call this function for users' FIRST register
        course_json = {}
        discussion_json = {}
        User.course_format(self)
        User.discussion_format(self)
        for i in range(len(self.course)):
            course_json[i] = self.course[i]
        for i in range(len(self.discussion)):
            discussion_json[i] = self.discussion[i]
        user_dict = {"fname": self.fname, "lname": self.lname, "email": self.email, "major": self.major,
                     "standing": self.standing, "course": course_json, 'password': self.password, 'login': self.login,
                     "discussion": discussion_json}
        composite_url = firebase_url + self.uname + '.json'
        rq.patch(composite_url, json=user_dict)

    # retrieve user data using REST API
    def get_user_data(self):
        composite_url = firebase_url + self.uname + '.json'
        response = rq.get(composite_url)
        data = response.json()
        return data

    # get functions for all user data
    def get_user_name(self):
        data = User.get_user_data(self)
        return data['fname'] + data['lname']

    def get_user_uname(self):
        data = User.get_user_data(self)
        return data['uname']

    def get_user_email(self):
        data = User.get_user_data(self)
        return data['email']

    def get_user_major(self):
        data = User.get_user_data(self)
        return data['major']

    def get_user_standing(self):
        data = User.get_user_data(self)
        return data['standing']

    def get_user_course(self):
        data = User.get_user_data(self)
        return data['course']

    def get_user_password(self):
        data = User.get_user_data(self)
        return data['password']

    # set function for appending or deleting course from the course list
    def set_user_course(self, org_course, add):
        # description: manipulate user courses
        # parameter:
        # course: the course that user want to add/drop (string)
        # add: whether user want to add(True) or remove(False) (bool)
        course = str('')
        composite_url = firebase_url + self.uname + '/course.json'
        for i in range(len(org_course)):
            if org_course[i].isalnum():
                course += org_course[i]
        for j in range(len(course)):
                if course[j].islower():
                    course = course[:j]+course[j].upper()+course[j+1:]

        if add:
            self.course.append(course)
        else:
            if course in self.course:
                self.course.remove(course)
            else:
                return 'Error. Not in the course list.'

        course_json = {}
        for i in range(len(self.course)):
            course_json[i] = self.course[i]
        rq.patch(composite_url, json=course_json)


if __name__ == '__main__':
    user1 = User('harveyfin', 'Fu', 'Harvey', 'harveyfu@usc.edu', 'ECMA', 'junior', 'DScI551, DSCI552', 'password')
    user1.upload_user_data()
    user1.set_user_course('MATH*&466', True)

