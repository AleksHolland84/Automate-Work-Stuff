#!/usr/bin/env python3

# write_messages.py

from jinja2 import Environment, FileSystemLoader
from datetime import date
import json, makejson, os

today = date.today()

date = today.strftime("%d.%m.%Y")



students = makejson.create_student_dict('students.xlsx')

students = json.loads(students)
print(students)


# Use Jinja to generate templates
environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("message.txt")
template12 = environment.get_template("bedømmelse_12.txt")
template_ok = environment.get_template("message_ok.txt")



if __name__ == "__main__":
    for student in students:

        # genererer filnavn på baggrund af den studerendes navn
        filename = f"Udtalelse_{student['name'].lower()}.txt"
        
        if student.get("grade") == "12":
            content = template12.render(
                name = student.get("name"),
                date = date,
                lærer1 = student.get("lærer1"),
                lærer2 = student.get("lærer2"),
                delemne = student.get("delemne"),
                overemne = student.get("overemne"),
                
            )

        elif student.get("grade") == "10":
            content = template.render(
                student,
        )
            content = content + template_ok.render(
                consultation1 = student.get("consultation1"),
                consultation2 = student.get("consultation2"),

            )

        elif student.get("grade") == "7":
            content = template.render(
                student,
        )
            content = content + template_ok.render(
                consultation1 = student.get("consultation1"),
                consultation2 = student.get("consultation2"),

            )

        elif student.get("grade") == "4":
            content = template.render(
                student,
        )
            content = content + template_ok.render(
                consultation1 = student.get("consultation1"),
                consultation2 = student.get("consultation2"),

            )

        else:
            content = template.render(
                student,
        )

        try:
            print("Checking for file")
            if os.path.exists(f"udtalelser/{filename}"):
                print("File allready exists!")
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

        


