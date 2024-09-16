#Importing libraries 
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import pandas as pd
import matplotlib.pyplot as plt

# Importing files
from QuestionPaperAnalyser import questionPaperAnalyser
app = Flask(__name__)
app.secret_key = 'Shinota'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/plot', methods=['POST'])
def plot():
    # Check if a file is uploaded
    if 'Question_paper' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    file = request.files['Question_paper']

    # Check if the file is selected and has content
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)

    # Check if the uploaded file is a CSV file
    if not file.filename.endswith('.csv'):
        flash('File must be a CSV', 'error')
        return redirect(request.url)

    # Read the CSV file into a DataFrame
    try:
        df = pd.read_csv(file)
    except Exception as e:
        flash(f'Error reading CSV file: {e}', 'error')
        return redirect(request.url)

    plot=questionPaperAnalyser(df)

    # Return the image as a file to the browser
    return render_template('plot.html',image_base64=plot)

if __name__ == '__main__':
    app.run(debug=True)
