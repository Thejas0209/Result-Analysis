# Importing libraries 
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64


from Codes.Student_Analisis import plot_student_analysis


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

    # Process the data and generate the plot
    plot_image = plot_student_analysis('01JCE21PMC006',qp_df, co_mapping_df)

    # Return the plot as a base64 image to the HTML template
    return render_template('plot.html', image_base64=plot_image)

# def questionPaperAnalyser(qp_df, co_mapping_df):
#     # Example processing - replace with your actual logic
#     plt.figure(figsize=(6,4))
#     plt.plot([1, 2, 3], [4, 5, 6])  # Example plot

#     # Convert the plot to PNG image and base64 encode it
#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plot_url = base64.b64encode(img.getvalue()).decode('utf8')
#     return plot_url

if __name__ == '__main__':
    app.run(debug=True)
