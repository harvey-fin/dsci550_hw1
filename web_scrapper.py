from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import os


def course_info(course_id):
    PATH = '/Users/harveyfu/Desktop/pythonProject/DSCI551/Group_Project/chromedriver'
    driver = webdriver.Chrome(PATH)
    course_dic = {}
    course_new_id = str()
    for item in course_id:
        if item.isalpha():
            course_new_id += item.lower()
    course_new_id += '-'
    for num in course_id:
        if num.isnumeric():
            course_new_id += str(num)

    term = '20221'
    while True:
        url = 'https://classes.usc.edu/term-'+term+'/course/' + course_new_id
        driver.get(url)
        title = driver.find_element(by=By.XPATH, value='//h2[contains(@class, \'single\')]')

        if 'This course isn\'t available' in title.text and term != '20223':
            term = '20223'
            continue
        elif 'This course isn\'t available' in title.text and term == '20223':
            return 'This course is not available.'
        else:
            course_dic['name'] = re.sub(r'\([^)]*\)', '', title.text)
            description = driver.find_element(by=By.CLASS_NAME, value="catalogue")
            course_dic['description'] = description.text
            instructors = driver.find_elements(by=By.XPATH, value="//td[contains(@class, \"instructor\")]")
            instructor_set = set()
            for item in instructors:
                instructor_origin = item.text
                instructor_new = instructor_origin.replace('\n', ' ')
                instructor_set.add(instructor_new)
            course_dic['instructor'] = instructor_set
            program = driver.find_element(by=By.XPATH, value='//span')
            course_dic['program'] = program.text
            break
    driver.get('https://catalogue.usc.edu/')
    search = driver.find_element(by=By.NAME, value='filter[keyword]')
    search.clear()
    search.send_keys(course_id)
    search.send_keys(Keys.RETURN)
    time.sleep(0.2)

    link = driver.find_element(by=By.XPATH, value='//a[contains(.,\'Best Match\')]')
    link.click()
    time.sleep(0.5)

    title = driver.find_element(by=By.XPATH, value='//td[contains(@class,\'coursepadding\')]')
    title_text = title.text
    if title_text:
        driver.quit()

    # return title_text
    course_text = f'{course_id}.txt'
    with open(course_text, 'w') as f_in:
        f_in.write(title_text)
    with open(course_text, 'r') as f_out:
        lines = f_out.readlines()
    for line in lines:
        if 'Terms Offered' in line:
            course_dic['semester'] = line.strip()
        elif 'Prerequisite:' in line:
            course_dic['prerequisite'] = line.strip()
        elif 'Units:' in line:
            course_dic['units'] = line.strip()
        elif 'Satisfies New General' in line:
            if 'Other' in course_dic.keys():
                course_dic['Other'] += '\n'
                course_dic['Other'] += line.strip()
            else:
                course_dic['Other'] = line.strip()
        elif 'Recommended Preparation' in line:
            if 'Other' in course_dic.keys():
                course_dic['Other'] += '\n'
                course_dic['Other'] += line.strip()
            else:
                course_dic['Other'] = line.strip()
        elif 'Duplicate credit' in line:
            if 'Other' in course_dic.keys():
                course_dic['Other'] += '\n'
                course_dic['Other'] += line.strip()
            else:
                course_dic['Other'] = line.strip()
        elif 'Instruction Mode' in line:
            if 'Other' in course_dic.keys():
                course_dic['Other'] += '\n'
                course_dic['Other'] += line.strip()
            else:
                course_dic['Other'] = line.strip()
        elif 'Grading Option' in line:
            if 'Other' in course_dic.keys():
                course_dic['Other'] += '\n'
                course_dic['Other'] += line.strip()
            else:
                course_dic['Other'] = line.strip()
    os.remove(course_text)
    return course_dic


def instructor_info(instructor_name):
    PATH = '/Users/harveyfu/Desktop/pythonProject/DSCI551/Group_Project/chromedriver'
    driver = webdriver.Chrome(PATH)
    url = 'https://uscdirectory.usc.edu/web/directory/faculty-staff/'
    driver.get(url)
    search = driver.find_element(by=By.NAME, value='q')
    search.clear()
    search.send_keys(instructor_name)
    search.send_keys(Keys.RETURN)
    time.sleep(3)

    instructor_dic = {}
    name = driver.find_element(by=By.XPATH, value='//span[contains(@class, \'match\')]')
    title = driver.find_element(by=By.XPATH, value='//td[contains(@class, \'title\')]')
    department = driver.find_element(by=By.XPATH, value='//td[contains(@class, \'dept\')]')
    division = driver.find_element(by=By.XPATH, value='//td[contains(@class, \'div\')]')
    email = driver.find_element(by=By.XPATH, value='//td[contains(@class, \'email\')]')

    instructor_dic['name'] = name.text
    instructor_dic['title'] = title.text
    instructor_dic['department'] = department.text
    instructor_dic['division'] = division.text
    instructor_dic['email'] = email.text
    return instructor_dic


if __name__ == '__main__':
    # print(course_info('DSCI 551'))
    # test_string = 'Data Science at Scale (4.0 units)'
    instructor_info('Kristof Aldenderfer')
    # print(re.sub(r'\([^)]*\)', '', test_string))
    # print(re.findall('\(.*?\)', test_string)[0][1:-1])





