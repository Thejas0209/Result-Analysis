# Importing dependencies
import numpy as np
import matplotlib.pyplot as plt
import io
import base64


def question_paper_analyser(QP_df):
    '''
    questionPaperAnalyser(QP_df): Plots a graph for Course outCome and Cognative domain of marks 
    Input:Takes a pandas dataframe of the question paper 
    Output:Returns the a matplot lib plt as a image
    '''
    # Extracting the info nd storing 
    Course_Output=np.unique(QP_df['CO'].to_numpy(),return_counts=True)
    Cogonative_Domain = np.unique([int(item) for sublist in [str(x).split(',') for x in QP_df["CD"]] for item in sublist],return_counts=True)
    
    # Ploting the graphs for COs & CDs
    fig,axs=plt.subplots(1,2)
    axs[0].bar(Course_Output[0],Course_Output[1])
    axs[0].set_title("Course outcome analysis")
    axs[0].set_xlabel("Course outcome")
    axs[0].set_ylabel("Number of questions")

    axs[1].bar(Cogonative_Domain[0],Cogonative_Domain[1])
    axs[1].set_title("CogonativeDomain analysis")
    axs[1].set_xlabel("Cogonative Domain")
    axs[1].set_ylabel("Number of questions")
    plt.show()
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64

