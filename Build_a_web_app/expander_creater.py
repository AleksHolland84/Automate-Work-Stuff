def template_returner(grades: tuple = ('-3','00','02','4', '7', '10', '12'), template: str = "", template_selecter: str = "", key_string="") -> list:
    return_list = []
    for _grade in grades:
        st.caption(f"Anbefalet til karakteren {_grade}:")
        for line in template_selecter[template][_grade]:
            add_frem_line = st.checkbox(line, key=f"_{key_string}_{_grade}_{line}")
            if add_frem_line:
                return_list.append(line)
    user_input = st.text_area(f'Tilføj dine egne linjer her', key=f"_{key_string}_user_input")
    if user_input:
        return_list.append(user_input.capitalize())
    return return_list

# Example of use:
#with st.expander("tester"):
#    list_of_strings = template_returner(template="arbejdsprocessen", template_selecter=template_selecter, key_string="list")
