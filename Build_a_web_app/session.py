import streamlit as st
import json

with open("templates.json", encoding="utf-8") as templates:
    session_data = json.load(templates)


def get_session():
    session_items = session_data["session"]
    for key, value in session_items.items():
        if key not in st.session_state:
            #print("Key not set", key)
            #print(f"Setting session: {key}:{value}")
            st.session_state[key] = value
        else:
            #print(f"Session key found: {key}: {st.session_state[key]}")
            pass

def get_template_session():
    session_items = session_data["template_session"]
    for key, value in session_items.items():
        if key not in st.session_state:
            #print("Key not set", key)
            #print(f"Setting session: {key}:{value}")
            st.session_state[key] = value
        else:
            #print(f"Session key found: {key}: {st.session_state[key]}")
            pass

def set_session():
    session_items = session_data["session"]
    for key, value in session_items.items():
        if key  in st.session_state:
            #print("Key set", key)
            #print(f"Setting session: {key}:{value}")
            st.session_state[key] = ""

def set_template_session():
    session_items = session_data["template_session"]
    for key, value in session_items.items():
        if key in st.session_state:
            #print("Key set", key)
            #print(f"Setting session: {key}:{value}")
            if isinstance(st.session_state[key], str): 
                st.session_state[key] = ""
            elif isinstance(st.session_state[key], bool):
                st.session_state[key] = False

    # Reset checked checkboxes for 
    uncheck_checkbox()
    
def uncheck_checkbox():
    areas = {
            "arbejdsprocessen": "_arb", 
            "fagligtindhold": "_fag", 
            "produktet": "_pro", 
            "fremlæggelsen": "_frem"
            }
    for area, _key in areas.items():
        area_items = session_data[area]
        for grade, lines in area_items.items():
            for line in lines:
                key = f"{_key}_{grade}_{line}"
                if key in st.session_state:
                    if isinstance(st.session_state[key], bool):
                        st.session_state[key] = False


def debug_session():
    for key in st.session_state:
        print(key, st.session_state[key])

    