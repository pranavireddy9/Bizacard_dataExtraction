import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import mysql.connector as sql
import io

mydb=sql.connect(host="localhost",
                   user="root",
                   password='Yerram@123',
                   database= "bizcard",
                   port = "3306")
my_cursor = mydb.cursor(buffered=True)

selected = option_menu(None, ["Home", "Upload", "Delete"],
                       icons=["house", "cloud-upload", "trash"],
                       default_index=2,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "5px",
                                            "--hover-color": "#545454"},
                               "icon": {"font-size": "25px"},
                               "container": {"max-width": "2000px"},
                               "nav-link-selected": {"background-color": "#fe7f9c"}})

def setting_bg():
    st.markdown(f""" <style>.stApp {{
                        background:url("https://i.pinimg.com/originals/4a/7c/2e/4a7c2e2749f974a7daa2e96bed7224d4.jpg");
                        background-size: cover}}
                     </style>""", unsafe_allow_html=True)


setting_bg()


def extract_data(result):
    ext_data={'Name': [], 'Designation': [], 'Company name': [], 'Contact': [], 'Email': [], 'Website': [],
               'Address': [], 'Pincode': []}
    ext_data['Name'].append(result[0])
    ext_data['Designation'].append(result[1])

    for i in range(2, len(result)):

        if (result[i].startswith('+')) or (result[i].replace('-', '').isdigit() and '-' in result[i]):
            ext_data['Contact'].append(result[i])
        elif '@' in result[i] and '.com' in result[i]:
            small = result[i].lower()
            ext_data['Email'].append(small)
        elif 'www' in result[i] or 'WWW' in result[i] or 'wwW' in result[i] or '.com' in result[i] and '@' not in result[i]:
            small = result[i]
            if 'WWW' in small:
                small=small.replace('WWW','www.')
            if '.com' not in small:
                small=(small.lower()).replace('com','.com')
            ext_data['Website'].append(small)
        
        elif  (re.search(r'[A-Za-z]',result[i]) or re.search(r'\d',result[i])) and ',' not in result[i] and ';' not in result[i] and (re.search(r'\b\d{6}\b', result[i]) or re.search(r'\b\d{7}\b',result[i])):
            data=result[i].split(' ')
            if len(data)>1:
                ext_data['Pincode'].append(data[1])
            else:
                ext_data['Pincode'].append(data[0])

        elif (re.search(r'[a-zA-Z]', result[i]) and re.search(r',', result[i])) or (re.search(r'[a-zA-Z]', result[i]) and re.search(r'\d',result[i]) or (re.search(r';',result[i]))):
            
            ext_data['Address'].append(result[i])

            
        else:

            ext_data['Company name'].append(result[i])
    for key, value in ext_data.items():
        if len(value) > 0:
            concatenated_string = ' '.join(value)
            ext_data[key] = [concatenated_string]
        else:
            value = 'NA'
            ext_data[key] = [value]
    return ext_data
    

if selected=="Home":
    
    st.write("-------------------")  
    st.header(":red[BizCardX: Extracting Business Card Data with OCR]")
    col1,col2=st.columns(2)
    with col1:   
        st.image("https://tse4.mm.bing.net/th?id=OIP.W1ns45b_yKshHN5k8M2tnQHaEK&pid=Api&P=0&h=180")
        st.markdown("## :red[Technologies used] : OCR, Streamlit GUI, SQL,Pandas,Numpy,re,Data Extraction")
    with col2:
        st.markdown("## :red[Overview] : The purpose of the project is to automate the process of extracting data from the bizzcard The extracted information should be displayed in a clean and organized manner, and users should be able to easily add it to the database with the click of a button and Allow the user to Read the data,Update the data and Allow the user to delete the data through the streamlit UI")

if selected =='Upload':
    st.write("-------------------")
    image=st.file_uploader(label="upload image",type=['png', 'jpg', 'jpeg'], label_visibility="hidden")
    @st.cache_data
    def load_image():
        reader=easyocr.Reader(['en'],model_storage_directory='.')
        return reader

    reader1=load_image()
    if image is not None:
        input_image=Image.open(image)
        st.image(input_image,width=350,caption="your image")
        
        with st.spinner("image is processing"):
            result=reader1.readtext(np.array(input_image),detail=0)
            ext_text = extract_data(result)
            df = pd.DataFrame(ext_text)
            st.dataframe(df)
            image_bytes = io.BytesIO()
            input_image.save(image_bytes, format='PNG')
            image_data = image_bytes.getvalue()
            data = {"Image": [image_data]}
            df_1 = pd.DataFrame(data)
            concat_df = pd.concat([df, df_1], axis=1)
            col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            selected = option_menu(
                    menu_title=None,
                    options=["Preview"],
                    icons=['file-earmark'],
                    default_index=0,
                    orientation="horizontal"
                )

            ext_text = extract_data(result)
            df = pd.DataFrame(ext_text)
        if selected == "Preview":
            col_1, col_2 = st.columns([4, 4])
            with col_1:
                modified_n = st.text_input('Name', ext_text["Name"][0])
                modified_d = st.text_input('Designation', ext_text["Designation"][0])
                modified_c = st.text_input('Company name', ext_text["Company name"][0])
                modified_con = st.text_input('Mobile', ext_text["Contact"][0])
                concat_df["Name"], concat_df["Designation"], concat_df["Company name"], concat_df[
                    "Contact"] = modified_n, modified_d, modified_c, modified_con
            with col_2:
                modified_m = st.text_input('Email', ext_text["Email"][0])
                modified_w = st.text_input('Website', ext_text["Website"][0])
                modified_a = st.text_input('Address', ext_text["Address"][0])
                modified_p = st.text_input('Pincode', ext_text["Pincode"][0])
                concat_df["Email"], concat_df["Website"], concat_df["Address"], concat_df[
                    "Pincode"] = modified_m, modified_w, modified_a, modified_p
            col3, col4 = st.columns([4, 4])
            with col3:
                Preview = st.button("Preview modified text")
            with col4:
                Upload = st.button("Upload")
            if Preview:
                filtered_df = concat_df[
                    ['Name', 'Designation', 'Company name', 'Contact', 'Email', 'Website', 'Address', 'Pincode']]
                st.dataframe(filtered_df)
            else:
                pass
            if Upload:
                with st.spinner("In progress"):
                    my_cursor.execute(
                        "CREATE TABLE IF NOT EXISTS BUSINESS_CARD(NAME VARCHAR(50), DESIGNATION VARCHAR(100), "
                        "COMPANY_NAME VARCHAR(100), CONTACT VARCHAR(35), EMAIL VARCHAR(100), WEBSITE VARCHAR("
                        "100), ADDRESS TEXT, PINCODE VARCHAR(100))")
                    mydb.commit()
                    A = "INSERT INTO BUSINESS_CARD(NAME, DESIGNATION, COMPANY_NAME, CONTACT, EMAIL, WEBSITE, ADDRESS, " \
                        "PINCODE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    for index, i in concat_df.iterrows():
                        result_table = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
                        my_cursor.execute(A, result_table)
                        mydb.commit()
                        st.success('SUCCESSFULLY UPLOADED', icon="✅")
    else:
        st.write("Upload an image")

if selected=="Delete":
    st.write("-------------------")
    col1, col2 = st.columns([4, 4])
    with col1:
        my_cursor.execute("SELECT NAME FROM BUSINESS_CARD")
        Y = my_cursor.fetchall()
        names = ["Select"]
        for i in Y:
            names.append(i[0])
        name_selected = st.selectbox("Select the name to delete", options=names)
    with col2:
        my_cursor.execute(f"SELECT DESIGNATION FROM BUSINESS_CARD WHERE NAME = '{name_selected}'")
        Z = my_cursor.fetchall()
        designation = ["Select"]
        for j in Z:
            designation.append(j[0])
        designation_selected = st.selectbox("Select the designation of the chosen name", options=designation)
    st.markdown(" ")
    col_a, col_b, col_c = st.columns([5, 3, 3])
    with col_b:
        remove = st.button("Clik here to delete")
    if name_selected and designation_selected and remove:
        my_cursor.execute(
            f"DELETE FROM BUSINESS_CARD WHERE NAME = '{name_selected}' AND DESIGNATION = '{designation_selected}'")
        mydb.commit()
        if remove:
            st.warning('DELETED', icon="⚠️")

