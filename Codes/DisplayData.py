def displayData():
    '''
    This Program Only Display's the co-cd mapped data
    and total marks of each co-cd 


    '''


    from DataAnalyizer import cognitiveDomainCourseOutcomeAnalysis as c
    import pandas as pd
    question_paper_dataframe = pd.read_excel(r'../Data/marks_sheet.xlsx')
    mark_sheet_dataframe = pd.read_excel(r'../Data/qp.xlsx')

    cd_result,co_result,cd_ttl,co_ttl = c(question_paper_dataframe,mark_sheet_dataframe)


    co_result['total_marks'] = co_result[['CO1_marks', 'CO2_marks', 'CO3_marks', 'CO4_marks', 'CO5_marks']].sum(axis=1)
    cd_result['total_marks'] = cd_result[['CD1_marks', 'CD2_marks', 'CD3_marks', 'CD4_marks', 'CD5_marks']].sum(axis=1)



    print('\n\tCourseOutcome Result Analysis data \n',co_result.to_numpy())
    print('\n\tCognitiveDomain Result Analysis data \n',cd_result.to_numpy())
    print('\n\tCourseOutcome Total Marks \n',co_ttl)
    print('\n\tCognitiveDomain Total Marks \n',cd_ttl)
    return co_result,cd_result,co_ttl,cd_ttl

