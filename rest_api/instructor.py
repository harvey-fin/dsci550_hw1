import requests as rq
import json
firebase_url = 'https://sc-rct-default-rtdb.firebaseio.com/instructors/'


class Instructor():
    def __init__(self, name_param, title_param, depart_param, division_param, email_param):
        # description:
        # name_param, title_param, depart_param, division_param, email_param are all strings

        self.name = name_param
        self.title = title_param
        self.depart = depart_param
        self.division = division_param
        self.email = email_param

    def upload_instructor_data(self):
        instructor_dict = {'name': self.name, 'title': self.title, 'department': self.depart, 'division': self.division,
                           'email': self.email}
        composite_url = firebase_url + self.name + '.json'
        rq.patch(composite_url, json=instructor_dict)


if __name__ == '__main__':
    instructor1 = Instructor('Harvey Fu', 'president of 3578', '3578 Basketball', 'Fu School of 3pt shooting',
                             'lol@123.com')
    instructor1.upload_instructor_data()