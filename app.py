# Importing libraries 
from flask import Flask, render_template, request, redirect, flash
import pandas as pd

# Importing Modules
from Codes.StudentAnalysis import plotStudentAnalysis
from Codes.ClassAnalysis import plotClassAnalysis,plotClassAnalysisPieChart
from Codes.QuestionPaperAnalyser import plotQuestionPaperAnalysis
from Codes.FileValidator import validate

app = Flask(__name__)
app.secret_key = 'Shinota'

@app.route('/')
def home():
    return render_template('home.html')

# Route to handle file upload and plotting
@app.route('/plot', methods=['POST'])
def plot():
    marks_sheet,question_paper = validate(request.files,request.url)
    # Read the Excel files into DataFrames
    try:
        question_paper = pd.read_excel(question_paper)
        marks_sheet = pd.read_excel(marks_sheet)
    except Exception as e:
        flash(f'Error reading Excel files: {e}', 'error')
        return redirect(request.url)

    # Get the student USN from the form
    student_usn = request.form.get('student_usn')
    
    # Check which button was clicked
    action = request.form.get('action')

    images = []  # Initialize an empty list for images

    # If the "Plot Student Analysis" button was clicked
    if action == 'plot_student':
        if not student_usn:
            flash('Student USN is required for Student Analysis', 'error')
            return redirect(request.url)
        
        # Plot student analysis
        plot_image = plotStudentAnalysis(student_usn, marks_sheet,question_paper)
        images.append(plot_image)  # Add the plot to the images list
        return render_template('plot_student.html', images=images)



    # If the "Plot Class Result" button was clicked
    elif action == 'plot_class':
        # Plot class analysis
        plot_image = plotClassAnalysis(marks_sheet,question_paper)
        question_paper_plot = plotQuestionPaperAnalysis(question_paper)
        qp_pie_chart = plotClassAnalysisPieChart(marks_sheet, question_paper)
        
        # Add the class analysis plot and question paper plot to the images list
        images.extend([plot_image, question_paper_plot, qp_pie_chart])

    # Return the plots as base64 images to the HTML template
    return render_template('plot_class.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
