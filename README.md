# Bizacard_dataExtraction
BizCardX-Extracting Business Card Data with OCR
Bizcard Extraction is a Python application built with Streamlit, EasyOCR, OpenCV, regex function, and MySQL database. It allows users to extract information from business cards and store it in a MySQL database for further analysis. The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.

Project Overview
BizCardX is a user-friendly tool for extracting information from business cards. The tool uses OCR technology to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. Users can access the extracted information using a GUI built using streamlit. The BizCardX application is a simple and intuitive user interface that guides users through the process of uploading the business card image and extracting its information. The extracted information would be displayed in a clean and organized manner, and users would be able to easily add it to the database with the click of a button. Further the data stored in database can be easily Read, updated and deleted by user as per the requirement.

Libraries/Modules used for the project!
Pandas - (To Create a DataFrame with the scraped data)
mysql.connector - (To store and retrieve the data)
Streamlit - (To Create Graphical user Interface)
EasyOCR - (To extract text from images)


Features
Extracts text information from business card images using EasyOCR.
Utilizes OpenCV for image preprocessing, such as resizing, cropping, and enhancing.
Uses regular expressions (RegEx) to parse and extract specific fields like name, designation, company, contact details, etc.
Stores the extracted information in a MySQL database for easy retrieval and analysis.
Provides a user-friendly interface built with Streamlit to upload images, extract information, and view/update the database.
