import pandas as pd

def cognitiveDomainCourseOutcomeAnalysis(qp_marks_dataFrame,Marks_Schema_dataFrame):
    '''
    CognitiveDomain_CourseCoutcome_Analysis(qp_marks_dataFrame,Marks_Schema_dataFrame):
    input : qp_marks_dataFrame,Marks_Schema_dataFrame
    output : returns dataFrame of CognitiveDomain_results,CourseOutcome_results,total_marks_CourseDomain,total_marks_CourseOutcome
    '''
    # Create a CO and CD mapping dictionary from the CO mapping file
    CourseOutcome_Mapping = {}
    CognitiveDomain_Mapping = {}

    for index, row in Marks_Schema_dataFrame.iterrows():
        question_no = row['QNo']
        CourseOutcome = row['CO']
        
        # Ensure the 'CD' column value is treated as a string before splitting
        CognitiveDomain_list = map(int, str(row['CD']).split(','))  # Split and convert CDs to integers
        Marks = row['Marks']
        
        # Mapping questions to CO
        if CourseOutcome not in CourseOutcome_Mapping:
            CourseOutcome_Mapping[CourseOutcome] = []
        CourseOutcome_Mapping[CourseOutcome].append(question_no)
        
        # Mapping questions to each CD
        for cd in CognitiveDomain_list:
            if cd not in CognitiveDomain_Mapping:
                CognitiveDomain_Mapping[cd] = []
            CognitiveDomain_Mapping[cd].append(question_no)

    # Define marks based on question columns
    def get_question_marks(df):
        question_marks = {}
        for col in df.columns[2:]:
            question_marks[col] = df[col].dropna().iloc[0]  # Assuming marks are in the first non-NaN value
        return question_marks

    question_marks = get_question_marks(qp_marks_dataFrame)

    # Calculate total marks for each CO and CD
    def calculate_total_marks(row, questions, marks):
        total_marks = 0
        for question in questions:
            if pd.notna(row[question]):
                total_marks += row[question]  # Use the actual marks from the DataFrame
        return total_marks

    # Create results DataFrame for CO
    CourseOutcome_results = pd.DataFrame()

    for CourseOutcome, questions in CourseOutcome_Mapping.items():
        CourseOutcome_results[f'CO{CourseOutcome}_marks'] = qp_marks_dataFrame.apply(lambda row: calculate_total_marks(row, questions, question_marks), axis=1)

    CourseOutcome_results['student_usno'] = qp_marks_dataFrame['student_usno']


    # Create results DataFrame for CD
    CognitiveDomain_results = pd.DataFrame()

    for cd, questions in CognitiveDomain_Mapping.items():
        CognitiveDomain_results[f'CD{cd}_marks'] = qp_marks_dataFrame.apply(lambda row: calculate_total_marks(row, questions, question_marks), axis=1)

    CognitiveDomain_results['student_usno'] = qp_marks_dataFrame['student_usno']


    # Calculate and store total marks for each CO and CD
    total_marks_CourseOutcome = {co: Marks_Schema_dataFrame[Marks_Schema_dataFrame['CO'] == co]['Marks'].sum() for co in CourseOutcome_Mapping}
    total_marks_CourseDomain = {cd: Marks_Schema_dataFrame[Marks_Schema_dataFrame['CD'].apply(lambda x: str(cd) in str(x))]['Marks'].sum() for cd in CognitiveDomain_Mapping}

  
    # Optionally, save the total marks to a CSV file or a separate data structure for future use
    total_marks_CourseOutcome = pd.DataFrame(list(total_marks_CourseOutcome.items()), columns=['CO', 'Total Marks'])
    total_marks_CourseDomain = pd.DataFrame(list(total_marks_CourseDomain.items()), columns=['CD', 'Total Marks'])


    return CognitiveDomain_results,CourseOutcome_results,total_marks_CourseDomain,total_marks_CourseOutcome

