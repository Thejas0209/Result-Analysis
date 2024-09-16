import pandas as pd

def CD_df(df,co_mapping_df):


    # Load the data from the Excel file
    # path = r"../Data/qp_list.xlsx"
    # df = pd.read_excel(path)

    # Load the CO mapping from the Excel file
    # co_mapping_path = r"../Data/inpu.xlsx"  # Path to your CO mapping Excel file
    # co_mapping_df = pd.read_excel(co_mapping_path)

    # Create a CO and CD mapping dictionary from the CO mapping file
    co_mapping = {}
    cd_mapping = {}

    for index, row in co_mapping_df.iterrows():
        q_no = row['QNo']
        co = row['CO']
        
        # Ensure the 'CD' column value is treated as a string before splitting
        cd_list = map(int, str(row['CD']).split(','))  # Split and convert CDs to integers
        marks = row['Marks']
        
        # Mapping questions to CO
        if co not in co_mapping:
            co_mapping[co] = []
        co_mapping[co].append(q_no)
        
        # Mapping questions to each CD
        for cd in cd_list:
            if cd not in cd_mapping:
                cd_mapping[cd] = []
            cd_mapping[cd].append(q_no)

    # Define marks based on question columns
    def get_question_marks(df):
        question_marks = {}
        for col in df.columns[2:]:
            question_marks[col] = df[col].dropna().iloc[0]  # Assuming marks are in the first non-NaN value
        return question_marks

    question_marks = get_question_marks(df)

    # Calculate total marks for each CO and CD
    def calculate_total_marks(row, questions, marks):
        total_marks = 0
        for question in questions:
            if pd.notna(row[question]):
                total_marks += row[question]  # Use the actual marks from the DataFrame
        return total_marks

    # Create results DataFrame for CO
    co_results = pd.DataFrame()

    for co, questions in co_mapping.items():
        co_results[f'CO{co}_marks'] = df.apply(lambda row: calculate_total_marks(row, questions, question_marks), axis=1)

    co_results['student_usno'] = df['student_usno']


    # Create results DataFrame for CD
    cd_results = pd.DataFrame()

    for cd, questions in cd_mapping.items():
        cd_results[f'CD{cd}_marks'] = df.apply(lambda row: calculate_total_marks(row, questions, question_marks), axis=1)

    cd_results['student_usno'] = df['student_usno']


    # Calculate and store total marks for each CO and CD
    total_marks_co = {co: co_mapping_df[co_mapping_df['CO'] == co]['Marks'].sum() for co in co_mapping}
    total_marks_cd = {cd: co_mapping_df[co_mapping_df['CD'].apply(lambda x: str(cd) in str(x))]['Marks'].sum() for cd in cd_mapping}

  
    # Optionally, save the total marks to a CSV file or a separate data structure for future use
    total_marks_co = pd.DataFrame(list(total_marks_co.items()), columns=['CO', 'Total Marks'])
    total_marks_cd = pd.DataFrame(list(total_marks_cd.items()), columns=['CD', 'Total Marks'])


    return cd_results,co_results,total_marks_cd,total_marks_co

