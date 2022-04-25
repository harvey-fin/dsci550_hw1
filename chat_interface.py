import streamlit as st
from rest_api import get_data as gt
import requests as rq

firebase_url = 'https://sc-rct-default-rtdb.firebaseio.com/users/'
from datetime import datetime
from datetime import date

todays_date = date.today()
now = datetime.now()
current_time = now.strftime("%H*%M")


def start_chat_function(user_name):
    composite_url = firebase_url + user_name + '/chat.json'
    intial_dict = {"initial": "started"}
    rq.patch(composite_url, json=intial_dict)


def start_chat_with(user_name, target_name):
    composite_url = firebase_url + user_name + '/chat' + '.json'
    initial_url = firebase_url + user_name + '/chat/initial.json'
    welcome_message = f'Start chatting with {target_name}'
    chat_list = {"welcome message": welcome_message}
    chat_dict = {target_name: chat_list}
    rq.patch(composite_url, json=chat_dict)
    if 'initial' in gt.get_chat_list(user_name):
        rq.delete(initial_url)

    composite_url_target = firebase_url + target_name + '/chat' + '.json'
    initial_url_target = firebase_url + target_name + '/chat/initial.json'
    welcome_message_target = f'Start chatting with {user_name}'
    chat_list_target = {"welcome message": welcome_message_target}
    chat_dict_target = {user_name: chat_list_target}
    rq.patch(composite_url_target, json=chat_dict_target)
    if 'initial' in gt.get_chat_list(target_name):
        rq.delete(initial_url_target)


def display_chat_window(user_name, target_name):
    st.title(f'Dialogue with {target_name}')
    user_info = gt.get_user_info(target_name)
    user_full_name = user_info['fname'] + " " + user_info['lname']
    target_major = user_info['major']
    target_standing = user_info['standing']
    target_email = user_info['email']
    info_code = f'NAME: {user_full_name}\nMAJOR: {target_major}\nSTANDING: {target_standing}'
    st.markdown(f'EMAIL: {target_email}')
    st.code(info_code)

    dialogue = gt.get_dialogue(user_name, target_name)
    item_code_str = str()
    for item in dialogue.items():
        chat_name = str(item[0])
        chat_sentence = str(item[1])
        if chat_name == 'welcome message':
            item_code = chat_name + ': ' + chat_sentence
            st.code(item_code)
        if chat_name != 'welcome message':
            chat_split = chat_name.split(' ')
            date = chat_split[1]
            time = chat_split[2]
            chat_new = chat_split[0] + ' ' + date.replace('*', '/') + ' ' +time.replace('*', ":")
            item_code = chat_new + ': ' + chat_sentence + '\n'
            item_code_str += item_code
    st.code(item_code_str)


def add_chat(user_name, target_name, input_text):
    chat_dict = gt.get_dialogue(user_name, target_name)
    new_key = user_name + f' {todays_date.month}*{todays_date.day} {current_time}'
    chat_dict[new_key] = input_text
    print(chat_dict)
    composite_url = firebase_url + user_name + '/chat' + '.json'
    chat_dict_upload = {target_name: chat_dict}
    rq.patch(composite_url, json=chat_dict_upload)

    composite_url_target = firebase_url + target_name + '/chat' + '.json'
    chat_dict_upload_target = {user_name: chat_dict}
    rq.patch(composite_url_target, json=chat_dict_upload_target)


if __name__ == '__main__':
    # start_chat_function('tigo')
    start_chat_with('harveyfin', 'tigo')
