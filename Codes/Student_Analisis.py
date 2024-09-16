import CD
import io
import base64


import matplotlib.pyplot as plt

def plot_student_analysis(usno, co, cd, co_ttl, cd_ttl):
    # Extract data for the given student
    student_co_scores = co[co['student_usno'] == usno].drop(columns=['student_usno']).values.flatten()
    student_cd_scores = cd[cd['student_usno'] == usno].drop(columns=['student_usno']).values.flatten()
    
    # CO Plot
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    co_labels = [f'CO{idx+1}' for idx in range(len(student_co_scores))]
    plt.bar(co_labels, student_co_scores, label='Student Scores', alpha=0.7, color='b')
    plt.bar(co_labels, co_ttl['Total Marks'], label='Total Marks', alpha=0.3, color='g')
    plt.xlabel('Course Outcomes (CO)')
    plt.ylabel('Marks')
    plt.title(f'Student {usno} CO Performance')
    plt.legend()

    # CD Plot
    plt.subplot(1, 2, 2)
    cd_labels = [f'CD{idx+1}' for idx in range(len(student_cd_scores))]
    plt.bar(cd_labels, student_cd_scores, label='Student Scores', alpha=0.7, color='b')
    plt.bar(cd_labels, cd_ttl['Total Marks'], label='Total Marks', alpha=0.3, color='g')
    plt.xlabel('Course Domains (CD)')
    plt.ylabel('Marks')
    plt.title(f'Student {usno} CD Performance')
    plt.legend()

    plt.tight_layout()
    plt.show()
    # buf = io.BytesIO()
    # plt.savefig(buf, format='png')
    # buf.seek(0)
    
    # image_base64 = base64.b64encode(buf.read()).decode('utf-8')

# Example usage
usno = '01JCE21PMC006'  # Provide the student usno here

co, cd, co_ttl, cd_ttl = CD.CD_df()


def p(usno):
    plot_student_analysis(usno, co, cd, co_ttl, cd_ttl)

p(usno)


