# Importing dependencies
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def plotQuestionPaperAnalysis(question_paper):
    '''
    questionPaperAnalyser(QP_df): Plots a graph for Course outCome and Cognative domain of marks 
    Input:Takes a pandas dataframe of the question paper 
    Output:Returns the a matplot lib plt as a image
    '''
    # Extracting the info nd storing 
    course_output=np.unique(question_paper['CO'].to_numpy(),return_counts=True)
    cogonative_domain = np.unique([int(item) for sublist in [str(x).split(',') for x in question_paper["CD"]] for item in sublist],return_counts=True)
    
    # Ploting the graphs for COs & CDs
    fig,axs=plt.subplots(1,2,figsize=(15, 5))
    axs[0].bar(course_output[0],course_output[1])
    axs[0].set_title("Course outcome analysis")
    axs[0].set_xlabel("Course outcome")
    axs[0].set_ylabel("Number of questions")

    axs[1].bar(cogonative_domain[0],cogonative_domain[1])
    axs[1].set_title("CogonativeDomain analysis")
    axs[1].set_xlabel("Cogonative Domain")
    axs[1].set_ylabel("Number of questions")
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64

