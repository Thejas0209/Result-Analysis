from Codes import DataAnalyizer
import matplotlib.pyplot as plt
import io
import base64

def plotClassAnalysis(mark_sheet_df, question_paper):
    '''
    plot_Class_Analisis(mark_sheet_df, qp): plots bar and pie chart for overall class course out come and analysis
    input : give two DataFrame - > mark_sheet DataFrame, qp
      DataFrame
    output : return's image of bar graph and pie chart as -> plot_url
    '''

    Cognitive_Domain_marks, Course_Outcome_marks, CognitiveDomain_TotalMarks, CourseOutcome_TotalMarks = DataAnalyizer.cognitiveDomainCourseOutcomeAnalysis(mark_sheet_df, question_paper)

    # Compute the average marks per CD
    CognitiveDomain_AverageMarks = round(Cognitive_Domain_marks.drop(columns='student_usno').sum() / Cognitive_Domain_marks.shape[0])

    # Extract total marks for each CD
    Total_marks_CogntivDomain = [int(CognitiveDomain_TotalMarks.iloc[i]['Total Marks']) for i in range(len(CognitiveDomain_AverageMarks))]

    # Define categories for CDs
    Cognitive_Domain_Lables = [f'CognitiveDomain{i + 1}' for i in range(len(CognitiveDomain_AverageMarks))]

    # Compute the average marks per CO
    CourseOutcome_AverageMarks = round(Course_Outcome_marks.drop(columns='student_usno').sum() / Course_Outcome_marks.shape[0])

    # Extract total marks for each CO
    Total_marks_CourseOutcome = [int(CourseOutcome_TotalMarks.iloc[i]['Total Marks']) for i in range(len(CourseOutcome_AverageMarks))]

    # Define categories for COs
    Cognitive_Outcome_Lables = [f'CO{i + 1}' for i in range(len(CourseOutcome_AverageMarks))]



    df = Course_Outcome_marks
    df2 = Cognitive_Domain_marks

    # Sum the marks across all COs for each student
    df['total_marks'] = df[['CO1_marks', 'CO2_marks', 'CO3_marks', 'CO4_marks', 'CO5_marks']].sum(axis=1)

    # Define the ranges
    ranges = {
        '0-35%': 0,
        '35-60%': 0,
        '60-80%': 0,
        '80-100%': 0
    }

    # Calculate the percentage for each student
    for marks in df['total_marks']:
        percentage = (marks / 100) * 100  # Assuming the total max marks for all CDs is 100
        if percentage <= 35:
            ranges['0-35%'] += 1
        elif percentage <= 60:
            ranges['35-60%'] += 1
        elif percentage <= 80:
            ranges['60-80%'] += 1
        else:
            ranges['80-100%'] += 1


    # Set bar width and positions
    bar_width = 0.4
    CognitiveDomain_Index = range(len(Cognitive_Domain_Lables))
    CourseOutcome_Index = range(len(Cognitive_Outcome_Lables))

    # Create the subplots for bar charts and pie charts
    fig, axs = plt.subplots(3, 2, figsize=(15, 15))

    # Plot for CDs (Bar Chart)
    bars1_cd = axs[0, 0].bar(CognitiveDomain_Index, CognitiveDomain_AverageMarks, bar_width, color='blue', alpha=0.7, label='Average Marks')
    bars2_cd = axs[0, 0].bar(CognitiveDomain_Index, Total_marks_CogntivDomain, bar_width, color='green', alpha=0.7, label='Total Marks')

    # Add labels, title, and legend for CD Bar Chart
    axs[0, 0].set_xlabel('Category')
    axs[0, 0].set_ylabel('Values')
    axs[0, 0].set_title('Comparison of Average and Total Marks per CD')
    axs[0, 0].set_xticks(CognitiveDomain_Index)
    axs[0, 0].set_xticklabels(Cognitive_Domain_Lables, rotation=45, ha='right')
    axs[0, 0].legend()

    # Plot for COs (Bar Chart)
    bars1_co = axs[0, 1].bar(CourseOutcome_Index, CourseOutcome_AverageMarks, bar_width, color='blue', alpha=0.7, label='Average Marks')
    bars2_co = axs[0, 1].bar(CourseOutcome_Index, Total_marks_CourseOutcome, bar_width, color='green', alpha=0.7, label='Total Marks')

    # Add labels, title, and legend for CO Bar Chart
    axs[0, 1].set_xlabel('Category')
    axs[0, 1].set_ylabel('Values')
    axs[0, 1].set_title('Comparison of Average and Total Marks per CO')
    axs[0, 1].set_xticks(CourseOutcome_Index)
    axs[0, 1].set_xticklabels(Cognitive_Outcome_Lables, rotation=45, ha='right')
    axs[0, 1].legend()

    # Plot for CDs (Pie Chart)
    axs[1, 0].pie(CognitiveDomain_AverageMarks, labels=Cognitive_Domain_Lables, autopct='%1.1f%%', colors=['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightpink'], startangle=140)
    axs[1, 0].set_title('Distribution of Average Marks per CD')

    # Plot for COs (Pie Chart)
    axs[1, 1].pie(CourseOutcome_AverageMarks, labels=Cognitive_Outcome_Lables, autopct='%1.1f%%', colors=['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightpink'], startangle=140)
    axs[1, 1].set_title('Distribution of Average Marks per CO')


    axs[2,0].pie(ranges.values(), labels=ranges.keys(), autopct='%1.1f%%', colors=['lightcoral', 'lightyellow', 'lightblue', 'lightgreen'], startangle=140)
    axs[2, 0].set_title('Percentage of student scored marks in the range of 0-35 ,35-60, 60-80, 80-100')

    axs[2, 1].axis('off')



    # Adjust layout and display the plot
    plt.tight_layout()

    # Convert the plot to PNG image and base64 encode it
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url
