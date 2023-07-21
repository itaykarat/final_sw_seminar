import pandas as pd
import plotly.express as px



def read_data_as_datafrane(table_path = r'C:\Users\97252\PycharmProjects\final_sw_seminar\GitHub archive tables\pushes__in_all_2023.csv',complexity_score=None,project_id = 27567171398):
    # Read CSV file into a DataFrame
    data_frame = pd.read_csv(table_path)

    # Find the row with 'id' equal to complexity score
    mask = data_frame['id'] == project_id

    # Update the complexity score to 2 for the matching row
    data_frame.loc[mask, 'complexity_score'] = complexity_score
    # Assuming your DataFrame is called 'df'

    # correlation_matrix = data_frame.corr()
    # fig = px.imshow(correlation_matrix)
    # fig.show()

    # Display the DataFrame
    # print(data_frame['id'],'\n\n',data_frame['complexity_score'])
    # print('')
    # values = data_frame['repo'].values
    repo_vector = data_frame['repo']
    for r_entry in repo_vector:
        # print(type(r_entry))
        print(r_entry.find('url'))
    cols = data_frame.columns
    # for col in cols:
    #     print(f'-------------------------------- {col} --------------------------------')
    #     print(data_frame[col])
    #     print('\n\n\n')

    # print(data_frame.corr())
    # for index, row in data_frame.iterrows():
    #     print(row)
    # for value in values:
    #     print('printing a value')
    #     print(value)



if __name__ == '__main__':
    read_data_as_datafrane()
