import requests as rq

firebase_url = 'https://sc-rct-default-rtdb.firebaseio.com/courses/'


class Course():
    def __init__(self, id_param, name_param, program_param, instruc_set, unit_param, semester_param,
                 prereq_param, descript_param, other_param):
        # description: initialize the data for courses
        # parameters:
        # id_param: the course id
        # depart_param: the parameter for course's department (string)
        # unit_param : number of units of the course
        # instruc_param: parameter for instructor (name, rmp score) (dictionary)
        # semester_param: which semesters that the course are given
            # Sp for spring, Sm for summer, Fa for fall
        # prereq_param: the pre-requisite for the course
        # descript_param: the description for the course
        self.id = id_param
        self.name = name_param
        self.program = program_param
        self.instruc = list(instruc_set)
        self.units = unit_param
        self.semester = semester_param
        self.prereq = prereq_param
        self.descript = descript_param
        self.other = other_param

    def upload_course_data(self):
        # description: upload the user data to the firebase
        # call the function using the crawler
        course_dict = {"program": self.program, "name": self.name, "instruc": self.instruc, "units": self.units, "semester": self.semester, "prereq": self.prereq,
                       "descript": self.descript, "other": self.other}
        composite_url = firebase_url + self.id + '.json'
        rq.patch(composite_url, json=course_dict)


if __name__ == '__main__':
    course1 = Course('DSCI551', 'Foundations of Data Management', 'Viterbi', {'Wu wensheng': 2.4}, '4.0 units', 'FaSp', 'None',
                     'Function and design of modern storage systems, including cloud; '
                     'data management techniques; data modeling; network attached storage, '
                     'clusters and data centers; relational databases; the map-reduce paradigm.')
    course1.upload_course_data()

