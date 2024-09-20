# Importing libraries 
from flask import redirect, flash

def validate(files,url):
    # Check if both files are uploaded
    if 'question_paper' not in files or 'marks_sheet' not in files:
        flash('Both files are required', 'error')
        return redirect(url)
    
    marks_sheet = files['marks_sheet']
    question_paper = files['question_paper']

    # Check if files are selected and have content
    if question_paper.filename == '' or marks_sheet.filename == '':
        flash('Both files must be selected', 'error')
        return redirect(url)

    # Check if the uploaded files are Excel files
    if not question_paper.filename.endswith('.xlsx') or not marks_sheet.filename.endswith('.xlsx'):
        flash('Files must be Excel (.xlsx)', 'error')
        return redirect(url)
    print("File validate sucessfull")
    return [marks_sheet,question_paper]
    