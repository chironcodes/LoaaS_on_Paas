import os
import streamlit as st
import pandas as pd


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './key.json'

st.set_page_config(
                    page_title='This is our beloved page tittle and will chance',
                    page_icon=':bar_chart:',
                    layout='centered',
                    menu_items={
                        'Get Help': 'https://github.com/chironcodes/loaas_on_paas',
                        'Report a bug': "https://cantos42.com",
                        'About': "# This is only a *placeholder* text so far!"
                    }
                    )


@st.cache
def get_csv_as_df(file_name:str):
    df = pd.read_csv(f"./data/{file_name}.csv")
    return df



st.title('LOaaS')







st.markdown('------------')
st.write('## 📊 LOaaS')

with st.form(key='my_form'):
    your_name = st.text_input('Tell me your name',
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

    lovers_name = st.text_input('Tell me your name',
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
    
    pics = st.file_uploader('Upload your pictures here (optional)',
        type=None,
        accept_multiple_files=True,
        key=None,
        help=None,
        on_change=None,
        args=None,
        disabled=False)

    submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        st.text('submitted')
