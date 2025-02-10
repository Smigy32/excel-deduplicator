import io
from flask import Flask, render_template, request, redirect, send_file, url_for
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/handle_file", methods=["POST"])
def handle_file():
    file = request.files["xls_file"]
    if not file:
        return "No file uploaded", 400
    columns = []
    for key in request.form:
        if key.startswith("column-"):
            columns.append(request.form[key])
    df = pd.read_excel(file)
    df_cleaned = df.drop_duplicates(subset=columns, keep="first")
    output = io.BytesIO()
    df_cleaned.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)  # Move to the beginning of the file-like object

    # Send the file as a response
    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="result.xlsx"
    )


if __name__ == "__main__":
    app.run(debug=True)
