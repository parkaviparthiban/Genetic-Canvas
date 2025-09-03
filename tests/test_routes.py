from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with env var in production

# Allowed file extensions
ALLOWED_EXTENSIONS = {'fasta', 'fa'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "fasta_files" not in request.files:
            flash("No file part")
            return redirect(request.url)

        files = request.files.getlist("fasta_files")
        if not files or files[0].filename == "":
            flash("No files selected")
            return redirect(request.url)

        saved_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join("uploads", filename)
                os.makedirs("uploads", exist_ok=True)
                file.save(filepath)
                saved_files.append(filename)
            else:
                flash(f"Invalid file type: {file.filename}")
                return redirect(request.url)

        # Placeholder: You can add prediction logic here
        flash(f"Successfully uploaded: {', '.join(saved_files)}")
        return render_template("results.html", files=saved_files)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)