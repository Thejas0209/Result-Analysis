from Codes import DataAnalyizer
import pandas as pd

def displayData(mark_sheet_df ,question_paper_df):
    '''
    This Program Only Display's the co-cd mapped data
    and total marks of each co-cd 

    '''
    # question_paper_dataframe = pd.read_excel(r'../Data/marks_sheet.xlsx')
    # marks_sheet_dataframe = pd.read_excel(r'../Data/qp.xlsx')

    cd_result,co_result,cd_ttl,co_ttl = DataAnalyizer.cognitiveDomainCourseOutcomeAnalysis(mark_sheet_df, question_paper_df)


    co_result['total_marks'] = co_result[['CO1_marks', 'CO2_marks', 'CO3_marks', 'CO4_marks', 'CO5_marks']].sum(axis=1)
    cd_result['total_marks'] = cd_result[['CD1_marks', 'CD2_marks', 'CD3_marks', 'CD4_marks', 'CD5_marks']].sum(axis=1)
    co_result=co_result.to_html()
    cd_result=cd_result.to_html()
    return co_result,cd_result