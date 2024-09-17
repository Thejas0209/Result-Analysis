# plot_student_analysis(usn_no, qp_mark_sheet_df, marks_schema):
# input : usn_number , qp marks sheet dataframe , marks schema
# output : buffer image containing 4 subplots 2 bar graph and 2 pie charts

from Codes import DataAnalizer
import io
import base64
import matplotlib.pyplot as plt



def plot_student_analysis(usn_no, qp_mark_sheet_df, marks_schema):

    # Get CO and CD data for the student
    cognitive_domain, course_outcome, cognitive_domain_total_marks, course_outcome_total_marks = DataAnalizer.CognitiveDomain_CourseCoutcome_Analysis(qp_mark_sheet_df, marks_schema)

    # Extract Scores from the main CO, CD Dataframe
    course_outcome_scores = course_outcome[course_outcome['student_usno'] == usn_no].drop(columns=['student_usno']).values.flatten()
    cognitive_domain_scores = cognitive_domain[cognitive_domain['student_usno'] == usn_no].drop(columns=['student_usno']).values.flatten()
    
    # Bar Plot for CO and CD
    plt.figure(figsize=(14, 7))

    plt.subplot(2, 2, 1)
    course_outcome_labels = [f'CourseOutcome{idx+1}' for idx in range(len(course_outcome_scores))]
    plt.bar(course_outcome_labels, course_outcome_scores, label='Student Scores', alpha=0.7, color='b')
    plt.bar(course_outcome_labels, course_outcome_total_marks['Total Marks'], label='Total Marks', alpha=0.3, color='g')
    plt.xlabel('Course Outcomes (CO)')
    plt.ylabel('Marks')
    plt.title(f'Student {usn_no} CO Performance')
    plt.legend()

    plt.subplot(2, 2, 2)
    cognitive_domain_labels = [f'CourseDomain{idx+1}' for idx in range(len(cognitive_domain_scores))]
    plt.bar(cognitive_domain_labels, cognitive_domain_scores, label='Student Scores', alpha=0.7, color='b')
    plt.bar(cognitive_domain_labels, cognitive_domain_total_marks['Total Marks'], label='Total Marks', alpha=0.3, color='g')
    plt.xlabel('Course Domains (CD)')
    plt.ylabel('Marks')
    plt.title(f'Student {usn_no} CD Performance')
    plt.legend()

    # Pie Charts for CO and CD
    plt.subplot(2, 2, 3)
    plt.pie(course_outcome_scores, labels=course_outcome_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title(f'Student {usn_no} CO Score Distribution')

    plt.subplot(2, 2, 4)
    plt.pie(cognitive_domain_scores, labels=cognitive_domain_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title(f'Student {usn_no} CD Score Distribution')

    plt.tight_layout()

    # Convert the plot to PNG image and base64 encode it
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url
