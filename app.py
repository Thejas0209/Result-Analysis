# Importing libraries 
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd

# Importing Modules
from Codes.StudentAnalysis import plot_student_analysis
from Codes.ClassAnalysis import plot_class_analysis
from Codes.QuestionPaperAnalyser import question_paper_analyser

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

    images = []  # Initialize an empty list for images

    # If the "Plot Student Analysis" button was clicked
    if action == 'plot_student':
        if not student_usn:
            flash('Student USN is required for Student Analysis', 'error')
            return redirect(request.url)
        
        # Plot student analysis
        plot_image = plot_student_analysis(student_usn, qp_df, co_mapping_df)
        images.append(plot_image)  # Add the plot to the images list

    # If the "Plot Class Result" button was clicked
    elif action == 'plot_class':
        # Plot class analysis
        plot_image = plot_class_analysis(qp_df, co_mapping_df)
        question_paper_plot = question_paper_analyser(co_mapping_df)
        
        # Add the class analysis plot and question paper plot to the images list
        images.extend([plot_image, question_paper_plot])

    # Return the plots as base64 images to the HTML template
    return render_template('plot.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
