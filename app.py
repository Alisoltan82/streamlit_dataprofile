
import sys
import os

import pandas as pd
import pandas_profiling
import streamlit as st
from pandas_profiling import ProfileReport

from streamlit_pandas_profiling import st_profile_report

st.set_page_config(page_title= 'Data Profile Gen' , layout= 'wide')

def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024**2)
    return size_mb


def validate_file(file):
    filename = file.name
    name , ext = os.path.splitext(filename)
    if ext in ('.csv' , '.xlsx'):
        return ext
    else:
        return False






with st.sidebar:
    uploaded_file = st.file_uploader('upload .csv , .xlsx file not exceeding 10 MB')
    if uploaded_file is not None:
        st.write('Operations Mode')
        minimal = st.checkbox('Do you want minimal report ?')
        display_mode = st.radio('Display Mode' , 
                                options=('Primary' , 
                                         'Dark',
                                         'Orange'))
        
        if display_mode == 'Dark':
            dark_mode = True
            orange_mode = False
        elif display_mode == 'Orange':
            dark_mode = False
            orange_mode = True
        else:
            dark_mode = False
            orange_mode = False

if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:
        filesize = get_filesize(uploaded_file)
        if filesize <= 10:
            if ext == '.csv':
                df = pd.read_csv(uploaded_file)
            else:
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar._selectbox('Select the sheet' , sheet_tuple)
                df = xl_file.parse(sheet_name)


        

            st.dataframe(df.head())

            #generate report
            with st.spinner('Generating Report'):
                pr =  ProfileReport(
                    df = df ,
                    minimal = minimal , 
                    dark_mode = dark_mode,
                    orange_mode = orange_mode,
                    )

            st_profile_report(pr)

        else:
            st.error('Maximum allowed file size = 10 MB. but recieved {filesize} MB')
    else:
        st.error('only support .csv or xlsx file types')

else:
    st.title(':bar_chart: Data Profiler')
    st.sidebar.caption('[Feedback](phalisultan@gmail.com)')
    st.sidebar.caption('[Reach out](https://www.linkedin.com/in/alisultan1/git )')
    st.info('Upload your data in the left sidebar to start')
