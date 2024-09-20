from DataAnalyizer import cognitiveDomainCourseOutcomeAnalysis as c
import pandas as pd
qp = pd.read_excel(r'../Data/qp_list.xlsx')
ms = pd.read_excel(r'../Data/inpu.xlsx')

cd_result,co_result,cd_ttl,co_ttl = c(qp,ms)


co_result['total_marks'] = co_result[['CO1_marks', 'CO2_marks', 'CO3_marks', 'CO4_marks', 'CO5_marks']].sum(axis=1)
cd_result['total_marks'] = cd_result[['CD1_marks', 'CD2_marks', 'CD3_marks', 'CD4_marks', 'CD5_marks']].sum(axis=1)



print('\n\tCourseOutcome Result Analysis data \n',co_result)
print('\n\tCognitiveDomain Result Analysis data \n',cd_result)
print('\n\tCourseOutcome Total Marks \n',co_ttl)
print('\n\tCognitiveDomain Total Marks \n',cd_ttl)

