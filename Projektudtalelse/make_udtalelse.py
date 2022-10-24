# write_messages.py

from jinja2 import Environment, FileSystemLoader
from datetime import date
import json, makejson, os

today = date.today()

date = today.strftime("%d.%m.%Y")

# Brug Jinja til at genere fælles skabelon
common_environment = Environment(loader=FileSystemLoader("templates/"))
template_ok = common_environment.get_template("message_ok.txt") # Bliver ikke brugt
template_bedømmelse = common_environment.get_template("bedømmelse.txt") # Karakter, dato, lærere
template_info = common_environment.get_template("info.txt") # Elev, Overemne, Underemne, Problemformulering



students = makejson.create_student_dict('students.xlsx')

students = json.loads(students)
print(students)


if __name__ == "__main__":
    for student in students:

        # Brug Jinja til at generere skabeloner 
        if student.get("gruppe") == "ja":
            environment = Environment(loader=FileSystemLoader("templates/gruppe/"))
        
        else:
            environment = Environment(loader=FileSystemLoader("templates/single/"))

        content = ""
        # genererer filnavn på baggrund af den studerendes navn
        filename = f"Udtalelse_{student['name'].lower()}.txt"

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

        try:
            print("Checking for file")
            if os.path.exists(f"udtalelser/{filename}"):
                print("File already exists. File not written!")
                print("To create the file, delete existing file first and run the script again.")
                continue
            else:
                with open(f"udtalelser/{filename}", mode="w", encoding="utf-8") as message:
                    message.write(content)
                    print(f".... wrote {filename}")
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            print("Creating directory")
            os.mkdir("udtalelser")
            with open(f"udtalelser/{filename}", mode="w", encoding="utf-8") as message:
                message.write(content)
                print(f".... wrote {filename}")

        


