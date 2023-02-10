import pandas as pd
import io
from flask import Flask, make_response, send_file

app = Flask(__name__)

@app.route("/download")
def download():
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel("students_v2.xlsx")

    # Number of times to insert the first row
    n = 5

    # Get the first row as a DataFrame
    first_row = df.iloc[0, :].to_frame().T

    # Concatenate the first row with itself `n` times
    new_df = pd.concat([first_row] * n, ignore_index=True)

    # Change the value of the name column for each row
    for i in range(n):
        new_df.at[i, 'name'] = f"new_name_{i+1}"

    # Concatenate the new DataFrame and the original DataFrame
    df = pd.concat([df, new_df], ignore_index=True)

    # Save the DataFrame to a memory buffer
    buffer = io.BytesIO()
    df.to_excel(buffer, index=True)

    # Create a Flask response object and set the headers
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=modified_file.xlsx"
    response.headers["Content-type"] = "application/vnd.ms-excel"

    return response

if __name__ == "__main__":
    app.run()
