from Codes import CD
import io
import base64
import matplotlib.pyplot as plt

def plot_student_analysis(usno, df, co_mapping_df):

    # Get CO and CD data for the student
    cd, co, cd_ttl, co_ttl = CD.CD_df(df, co_mapping_df)

    # Extract data for the given student
    student_co_scores = co[co['student_usno'] == usno].drop(columns=['student_usno']).values.flatten()
    student_cd_scores = cd[cd['student_usno'] == usno].drop(columns=['student_usno']).values.flatten()
    
    # Bar Plot for CO and CD
    plt.figure(figsize=(14, 7))

    plt.subplot(2, 2, 1)
    co_labels = [f'CO{idx+1}' for idx in range(len(student_co_scores))]
    plt.bar(co_labels, student_co_scores, label='Student Scores', alpha=0.7, color='b')
    plt.bar(co_labels, co_ttl['Total Marks'], label='Total Marks', alpha=0.3, color='g')
    plt.xlabel('Course Outcomes (CO)')
    plt.ylabel('Marks')
    plt.title(f'Student {usno} CO Performance')
    plt.legend()

    plt.subplot(2, 2, 2)
    cd_labels = [f'CD{idx+1}' for idx in range(len(student_cd_scores))]
    plt.bar(cd_labels, student_cd_scores, label='Student Scores', alpha=0.7, color='b')
    plt.bar(cd_labels, cd_ttl['Total Marks'], label='Total Marks', alpha=0.3, color='g')
    plt.xlabel('Course Domains (CD)')
    plt.ylabel('Marks')
    plt.title(f'Student {usno} CD Performance')
    plt.legend()

    # Pie Charts for CO and CD
    plt.subplot(2, 2, 3)
    plt.pie(student_co_scores, labels=co_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title(f'Student {usno} CO Score Distribution')

    plt.subplot(2, 2, 4)
    plt.pie(student_cd_scores, labels=cd_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title(f'Student {usno} CD Score Distribution')

    plt.tight_layout()

    # Convert the plot to PNG image and base64 encode it
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url
