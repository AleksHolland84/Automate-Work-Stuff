from jinja2 import Environment, FileSystemLoader, BaseLoader
from datetime import date
import streamlit as st # pip install streamlit
from streamlit_extras.buy_me_a_coffee import button as coffee_button # import streamlit extras
import pandas as pd # pip install pandas

import json
with open("templates.json", encoding="utf-8") as templates:
    data_strings = json.load(templates)
grades = ('-3','00','02','4', '7', '10', '12')

#To run the app, use a terminal: streamlit run .\app.py
#Jinja guide er fundet på https://realpython.com/primer-on-jinja-templating/
whole_content = ""

# Create date variables
today = date.today()
download_date = today.strftime("%d.%m.%Y")

# Use Jinja to generate common templates
common_environment = Environment(loader=FileSystemLoader("templates/"))
template_bedømmelse = common_environment.get_template("bedømmelse.txt") # Karakter, dato, lærere
template_info = common_environment.get_template("info.txt") # Elev, Overemne, Underemne, Problemformulering

students = {}

def gradeSelect(grade, check_grade):
    if  grade == check_grade:
        return True
    else:
        return False
    
from session import *
get_session()
get_template_session()


if __name__ == "__main__":
    # Setup config - to configure title of webpage
    st.set_page_config(page_title='Projekttalelser')

    st.title('Projektudtalelser')
    st.markdown('''Dette er en simpel udtalelsesgenerator, der generer elevudtalelser på baggrund af bedømmelsen på de 4 områder. 
                    Træk i slideren for at genere "templates" til det antal elever der skal bedømmes. Udfyld derefter datafelterne med det ønskede input.''')
    #class_size = st.slider('Hvor mange elever', 0, 36, 0)
    class_size = 1

    overemne = st.text_input('Overemne', 
                        key="_overemne")


    LA1, LA2 = st.columns(2)
    with LA1:
        teacher1 = st.text_input(
            "Lærer 1",
            key="_teacher1",
        )
    with LA2:
        teacher2 = st.text_input(
            "Lærer 2",
            key="_teacher2",
        )

    date = st.date_input ("Dato", date(2023, 5, 2))
    date = date.strftime("%d.%m.%Y")
        
    if class_size > 0:
        st.markdown('---')

        st.markdown('''Nedenfor kan du se et datafelt for det antal elever du har valgt.
        Udtalelsen bliver genereret ud fra karakterene du vælger under Arbejdsprocessen, Fagligtindhold, 
        Produktet og Fremlæggelsen og genereres løbende imens du bruger appen''')

        #st.subheader('Downloads:')
        st.subheader("Elevudtalelse")


        # Create input text for student name
        navn = st.text_input('Navn', key="_name")
        navn = ' '.join(elem.capitalize() for elem in navn.split())

        underemne = st.text_input('Underemne', key=f"_underemne")
        problemformulering = st.text_area('Problemformulering', key=f"_problem")
        gruppe_checkbox = st.checkbox(f'{"Eleven"} har arbejdet i gruppe', key="_gruppe_checkbox")

        # Create columns with student's grade for the 4 areas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            arb_grade = st.selectbox("Arbejdsprocessen", ('-3','00','02','4', '7', '10', '12'), key=f"_arb")
        with col2:
            fag_grade = st.selectbox("Fagligtindhold", ('-3','00','02','4', '7', '10', '12'), key=f"_fag")
        with col3:
            pro_grade = st.selectbox("Produktet", ('-3','00','02','4', '7', '10', '12'), key=f"_pro")
        with col4:
            frem_grade = st.selectbox("Fremlæggelsen", ('-3','00','02','4', '7', '10', '12'), key=f"_frem")

        # Create selectbox for the student's grade
        karakter = st.selectbox("Samlet karakter", ('-3','00','02','4', '7', '10', '12'), key=f"_grade")

            

        with st.expander("Arbejdssprocessen"):
            arbejdsprocessen = []
            for _grade in grades:
                st.caption(f"Anbefalet til karakteren {_grade}:")
                # check all checkboxes associated with the given grade using gradeSelect() function
                for line in data_strings["arbejdsprocessen"][_grade]:
                    add_arb_line = st.checkbox(line, value=gradeSelect(arb_grade, _grade), key=f"_arb_{_grade}_{line}")
                    if add_arb_line:
                        arbejdsprocessen.append(line)
                            
        with st.expander("Fagligtindhold"):
            fagligtindhold = []
            for _grade in grades:
                st.caption(f"Anbefalet til karakteren {_grade}:")
                for line in data_strings["fagligtindhold"][_grade]:
                    add_fag_line = st.checkbox(line, value=gradeSelect(fag_grade, _grade), key=f"_fag_{_grade}_{line}")
                    if add_fag_line:
                        fagligtindhold.append(line)

        with st.expander("Produktet"):
            produkt = []
            for _grade in grades:
                st.caption(f"Anbefalet til karakteren {_grade}:")
                for line in data_strings["produktet"][_grade]:
                    add_pro_line = st.checkbox(line, value=gradeSelect(pro_grade, _grade), key=f"_pro_{_grade}_{line}")
                    if add_pro_line:
                        produkt.append(line)

        with st.expander("Fremlæggelsen"):
            fremlæggelsen = []
            for _grade in grades:
                st.caption(f"Anbefalet til karakteren {_grade}:")
                for line in data_strings["fremlæggelsen"][_grade]:
                    add_frem_line = st.checkbox(line, value=gradeSelect(frem_grade, _grade), key=f"_frem_{_grade}_{line}")
                    if add_frem_line:
                        fremlæggelsen.append(line)
                
        content = ""

        content = template_info.render(
            name = navn,
            delemne = underemne,
            overemne = overemne,
            problemformulering = problemformulering,
        ) + "\n\n"

        if gruppe_checkbox == True:
            gruppe_string = data_strings["gruppe"]["true"]
            template_gruppe = Environment(loader=BaseLoader()).from_string(f'{navn} {gruppe_string}')
            content = content + template_gruppe.render(
                elev = navn,
            )+ "\n\n"

        arbejdsprocessen_text = " ".join(arbejdsprocessen)
        template_arbejdsprocessen = Environment(loader=BaseLoader()).from_string("ARBEJDSPROCES: " + arbejdsprocessen_text)
        content = content + template_arbejdsprocessen.render() + "\n\n"
            
        fagligtindhold_text = " ".join(fagligtindhold)
        template_fagligtindhold = Environment(loader=BaseLoader()).from_string("FAGLIGT INDHOLD: " + fagligtindhold_text)
        content = content + template_fagligtindhold.render() + "\n\n"

        produkt_text = " ".join(produkt)
        template_produkt = Environment(loader=BaseLoader()).from_string("PRODUKT: " + produkt_text)
        content = content + template_produkt.render() + "\n\n"

        fremlæggelsen_text = " ".join(fremlæggelsen)
        template_fremlæggelse = Environment(loader=BaseLoader()).from_string("FREMLÆGGELSE: " + fremlæggelsen_text)
        content = content + template_fremlæggelse.render() + "\n"

            

        content = content + template_bedømmelse.render(
            date = date,
            grade = karakter,
            lærer1 = teacher1,
            lærer2 = teacher2,
        )

        # Display content to web app
        st.markdown(content)

        down_button, spacer, rest_button = st.columns(3)
        with down_button:
            st.download_button(f'Download udtalelse', content, file_name=f"projektudtalelse_{navn}_{download_date}.txt", help=f"Downloader projektudtalelse for {navn}")
        
        with rest_button:
            st.button("Ny elevuudtalelse", on_click=set_template_session, help="Fjerner alt input under 'Elevudtalelse'. Overemne, lærernavne og dato slettes ikke,")
            
        st.markdown('-'*17)
        whole_content += content + "\r\n" + '-'*80 + "\n\n\n"
            


    coffee, spacer1, spacer2, mail = st.columns(4)
    with coffee:
                coffee_button(username="fake-username", floating=False, width=221)

    with mail:
        st.markdown('<a href="mailto:hello@streamlit.io">Kontakt mig</a>', unsafe_allow_html=True)


