import base64
from io import BytesIO
from PIL import Image
from urllib.parse import quote, unquote
import streamlit as st
import streamlit.components.v1 as components
from modules.conector import interface_datastore




base_url = 'http://localhost:8501'

@st.cache
def load_image(image_file):
	img = Image.open(image_file)
	return img

@st.cache
def get_decoded_img(image_file):
        img_in_memory = BytesIO()
        byte_img = BytesIO(image_file)
        foto = Image.open(byte_img)
        foto.save(img_in_memory, format="png") # save the image in memory using BytesIO
        img_in_memory.seek(0) # rewind to beginning of file
        image = base64.b64encode(img_in_memory.getvalue()) # load the bytes in the context as base64
        return image.decode('utf8')

@st.cache
def get_con():
    return interface_datastore()    

st.set_page_config(
                    page_title='This is our beloved page tittle and will change',
                    page_icon='💘',
                    layout='wide',
                    menu_items={
                        'Get Help': 'https://github.com/chironcodes/loaas_on_paas',
                        'Report a bug': "https://cantos42.com",
                        'About': "# This is only a *placeholder* text so far!"
                    }
                    )

    



ds = interface_datastore()
st.markdown('------------')


# If streamlit receives query params, we get to see a whole different page
if(st.experimental_get_query_params()):
    query_data = st.experimental_get_query_params()
    from_who = unquote(query_data['from_who'][0])
    to_you = unquote(query_data['to_you'][0])
    unique_key = query_data['unique_key'][0]

    try:
        content = ds.getEntity(from_who, to_you, unique_key)
    except Exception as e:
        print(str(e))
        st.exception(f'{str(e)}')

    if content:
        try:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write('')
            with col2:
                st.write(f'## {from_who} 💘 {to_you} ')

            caroussel=[]

            if content['pictures']:
                for image_file in content['pictures']:
                    image = get_decoded_img(image_file)
                    caroussel.append(image)


        except Exception as e:
            print(str(e))
            st.exception(f'{str(e)}')


        divs=''
        if (len(caroussel)>1):
            for i in range(1,(len(caroussel))):
                divs=divs+(f"""
                <div class="carousel-item">
                    <img class="d-block w-100" src="data:image/jpg;base64,{caroussel[i]}" alt="First slide">
                </div>
                """)
    
        components.html(
        f"""
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div id="carouselExampleControls" class="carousel slide" data-ride="carousel">
        <div class="carousel-inner">
                <div class="carousel-item active">
                <img class="d-block w-100" src="data:image/jpg;base64,{caroussel[0]}" alt="First slide">
                </div>
                """
        f"""{divs}
        """
                    
                
        f"""</div>
            <a class="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="sr-only">Previous</span>
            </a>
            <a class="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="sr-only">Next</span>
            </a>
        </div>
        """,
        height=800,
    )
    else:
        
        st.error("Couldn't find the album you request. Does that album exist?")

                

else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        st.write('## 💘 LOaaS')

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

        # if uploaded_files is not None:
        #     for image_file in uploaded_files:
        #         file_details = {"filename":image_file.name,"filetype":image_file.type,
        #                         "filesize":image_file.size}
        #         st.write(file_details)
        #         st.image(load_image(image_file), width=250)

        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            pictures = []
            try:
                for uploaded_file in uploaded_files:
                    bytes_data = uploaded_file.read()
                    st.write("filename:", uploaded_file.name)
                    st.write(type(bytes_data))
                    picture = BytesIO(bytes_data)
                    st.write(picture)
                    pictures.append(picture.getvalue())
                    st.image(load_image(picture), width=250)
                
                unique_key = ds.insertEntity(from_who, to_you, pictures)
                unique_url = f"{base_url}/?from_who={quote(from_who)}&to_you={quote(to_you)}&unique_key={unique_key}"
                st.write(unique_url)
            
            except Exception as e:
                print(str(e))


