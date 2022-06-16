import os
import streamlit as st
from PIL import Image
import pandas as pd

from modules.conector import interface_datastore




base_url = 'http://loaas-is-a-good-solution'


st.set_page_config(
                    page_title='This is our beloved page tittle and will change',
                    page_icon='💘',
                    layout='centered',
                    menu_items={
                        'Get Help': 'https://github.com/chironcodes/loaas_on_paas',
                        'Report a bug': "https://cantos42.com",
                        'About': "# This is only a *placeholder* text so far!"
                    }
                    )

@st.cache
def load_image(image_file):
	img = Image.open(image_file)
	return img

@st.cache
def get_con():
    return interface_datastore()    


col1, col2, col3 = st.columns(3)

st.markdown('------------')
with col1:
    st.write('')
with col2:
    st.write('## 💘 LOaaS')

ds = interface_datastore()

# st.markdown("<h1 style='text-align: center; color: red;'> 💘 LOaaS</h1>", unsafe_allow_html=True)



with st.form(key='my_form'):
    
    from_who = st.text_input('From who',
        value="",
        max_chars=20,
        help=None,
        autocomplete='name',
        on_change=None,
        args=None,
        kwargs=None,
        placeholder="your name",
        disabled=False
        )

    to_you = st.text_input('To who',
        value="",
        max_chars=20,
        help=None,
        autocomplete='name',
        on_change=None,
        args=None,
        kwargs=None,
        placeholder="your lover's name",
        disabled=False
        )
    
    uploaded_files = st.file_uploader('Upload your pictures here (optional)',
        type=["png","jpg","jpeg"],
        accept_multiple_files=True,
        key=None,
        help=None,
        on_change=None,
        args=None,
        disabled=False)

    if uploaded_files is not None:
        for image_file in uploaded_files:
            file_details = {"filename":image_file.name,"filetype":image_file.type,
                            "filesize":image_file.size}
            st.write(file_details)
            st.image(load_image(image_file), width=250)

    submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        try:
            unique_id = ds.insertEntity(from_who, to_you)
            unique_url = f"{base_url}/from_who={from_who}&to_you={to_you}&key={unique_id}"
            st.write(unique_url)
        except Exception as e:
            print(str(e))


        
