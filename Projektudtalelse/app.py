from jinja2 import Environment, FileSystemLoader
from datetime import date
import json, make_jsonObj
import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module

#To run the app, use a terminal: streamlit run .\app.py
#Inspiration til denne app er fundet i videoen: https://www.youtube.com/watch?v=IolyDeV0wmo.
#Jinja guide er fundet på https://realpython.com/primer-on-jinja-templating/
whole_content = ""

# Create date variables
today = date.today()
date = today.strftime("%d.%m.%Y")

# Use Jinja to generate common templates
common_environment = Environment(loader=FileSystemLoader("templates/"))
template_ok = common_environment.get_template("message_ok.txt") # Bliver ikke brugt
template_bedømmelse = common_environment.get_template("bedømmelse.txt") # Karakter, dato, lærere
template_info = common_environment.get_template("info.txt") # Elev, Overemne, Underemne, Problemformulering

# Function to generate downloadable excel file
def generate_excel_download_link(df):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    buffer = BytesIO()
    df.to_json(buffer, orient="records",)  # write to BytesIO buffer
    buffer.seek(0)  # reset pointer
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Student_data.json">Download Json data</a>'
    return st.markdown(href, unsafe_allow_html=True)

# Setup config - to configure title of webpage
st.set_page_config(page_title='Projekttalelser')

if __name__ == "__main__":
    st.title('Projektudtalelser')

    # Download student.elsx DataFrame
    st.markdown('''Download skabelonen, udfyld den og upload den efterfølgende til siden.
    Dette vil generere elevudtalelser på baggrund af den data skabelonen indeholder''')
    with open('template_v1.xlsx', 'rb') as my_file:
        st.download_button(label = 'Download skabelon', data = my_file, file_name = 'Template.xlsx', mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') 

    


    st.subheader('Træk os slip excelfilen herunder')
    uploaded_file = st.file_uploader('Upload dit Excelark herunder', type='xlsx')
    if uploaded_file:
        st.markdown('---')
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        st.markdown('Nedenfor er et datasæt, som du kan bruge til at kontrollere dit uploaded data')
        st.dataframe(df)

        st.subheader('Downloads:')
        generate_excel_download_link(df)
        students = make_jsonObj.create_student_dict(uploaded_file)
        students = json.loads(students)

        for student in students:

            # Brug Jinja til at generere skabeloner 
            if student.get("gruppe") == "ja":
                environment = Environment(loader=FileSystemLoader("templates/gruppe/"))
            
            else:
                environment = Environment(loader=FileSystemLoader("templates/single/"))

            content = ""
            # genererer filnavn på baggrund af den studerendes navn
            navn = student['name'].lower()

            # Tildeler de 4 karakter til de 4 variabler
            fag_grade = student.get("fagligtindhold")
            arb_grade = student.get("arbejdsprocessen")
            pro_grade = student.get("produkt")
            frem_grade = student.get("fremlæggelse")

            content = template_info.render(
                name = student.get("name"),
                delemne = student.get("delemne"),
                overemne = student.get("overemne"),
                problemformulering = student.get("problemformulering"),
            ) + "\n\n"


            template_fagligtindhold = environment.get_template(f"fagligtindhold{fag_grade}.txt")
            content = content + template_fagligtindhold.render() + "\n\n"

            template_arbejdsprocessen = environment.get_template(f"arbejdsprocessen{arb_grade}.txt")
            content = content + template_arbejdsprocessen.render() + "\n\n"

            template_produkt = environment.get_template(f"produkt{pro_grade}.txt")
            content = content + template_produkt.render() + "\n\n"

            template_fremlæggelse = environment.get_template(f"fremlæggelse{frem_grade}.txt")
            content = content + template_fremlæggelse.render() + "\n"

            

            content = content + template_bedømmelse.render(
                date = date,
                grade = student.get("grade"),
                lærer1 = student.get("lærer1"),
                lærer2 = student.get("lærer2"),
            )



            #df_student = pd.read_csv(StringIO(content))
            #generate_student_link(content, name=navn)

            st.markdown(content)
            st.markdown('-'*17)
            whole_content += content + "\r\n" + '-'*80 + "\n\n\n"


        st.download_button('Download file', whole_content)
