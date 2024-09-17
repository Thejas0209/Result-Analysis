# Importing libraries 
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

from Codes.Student_Analysis import plot_student_analysis
from Codes.Class_Analisis import plot_c
from Codes.QuestionPaperAnalyser import questionPaperAnalyser

app = Flask(__name__)
app.secret_key = 'Shinota'

@app.route('/')
def home():
    return render_template('home.html')

# Route to handle file upload and plotting
@app.route('/plot', methods=['POST'])
def plot():
    # Check if both files are uploaded
    if 'Question_paper' not in request.files or 'CO_mapping' not in request.files:
        flash('Both files are required', 'error')
        return redirect(request.url)
    
    qp_file = request.files['Question_paper']
    co_mapping_file = request.files['CO_mapping']

    # Check if files are selected and have content
    if qp_file.filename == '' or co_mapping_file.filename == '':
        flash('Both files must be selected', 'error')
        return redirect(request.url)

    # Check if the uploaded files are Excel files
    if not qp_file.filename.endswith('.xlsx') or not co_mapping_file.filename.endswith('.xlsx'):
        flash('Files must be Excel (.xlsx)', 'error')
        return redirect(request.url)

    # Read the Excel files into DataFrames
    try:
        qp_df = pd.read_excel(qp_file)
        co_mapping_df = pd.read_excel(co_mapping_file)
    except Exception as e:
        flash(f'Error reading Excel files: {e}', 'error')
        return redirect(request.url)

    # Get the student USN from the form
    student_usn = request.form.get('student_usn')

    # Check which button was clicked
    action = request.form.get('action')

    # If the "Plot Student Analysis" button was clicked
    if action == 'plot_student':
        if not student_usn:
            flash('Student USN is required for Student Analysis', 'error')
            return redirect(request.url)
        
        # Plot student analysis
        plot_image = plot_student_analysis(student_usn, qp_df, co_mapping_df)

    # If the "Plot Class Result" button was clicked
    elif action == 'plot_class':
        # Plot class analysis
        plot_image = plot_c(qp_df, co_mapping_df)
        Question_paper_plot=questionPaperAnalyser(co_mapping_df)
        images=[plot_image,Question_paper_plot]

    # Return the plot as a base64 image to the HTML template
    return render_template('plot.html', image_base64=images)

if __name__ == '__main__':
    app.run(debug=True)
