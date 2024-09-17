from Codes import CD
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Load the CSV files
def plot_c(df, co_mapping_df):

    marks_df_cd, marks_df_co, cd_total_df, co_total_df = CD.CD_df(df, co_mapping_df)

    # Compute the average marks per CD
    mrkt_cd = round(marks_df_cd.drop(columns='student_usno').sum() / marks_df_cd.shape[0])

    # Extract total marks for each CD
    ttl_mrk_cd = [int(cd_total_df.iloc[i]['Total Marks']) for i in range(len(mrkt_cd))]

    # Define categories for CDs
    categories_cd = [f'CD{i + 1}' for i in range(len(mrkt_cd))]

    # Compute the average marks per CO
    mrkt_co = round(marks_df_co.drop(columns='student_usno').sum() / marks_df_co.shape[0])

    # Extract total marks for each CO
    ttl_mrk_co = [int(co_total_df.iloc[i]['Total Marks']) for i in range(len(mrkt_co))]

    # Define categories for COs
    categories_co = [f'CO{i + 1}' for i in range(len(mrkt_co))]

    # Set bar width and positions
    bar_width = 0.4
    index_cd = range(len(categories_cd))
    index_co = range(len(categories_co))

    # Create the subplots for bar charts and pie charts
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    # Plot for CDs (Bar Chart)
    bars1_cd = axs[0, 0].bar(index_cd, mrkt_cd, bar_width, color='blue', alpha=0.7, label='Average Marks')
    bars2_cd = axs[0, 0].bar(index_cd, ttl_mrk_cd, bar_width, color='green', alpha=0.7, label='Total Marks')

    # Add labels, title, and legend for CD Bar Chart
    axs[0, 0].set_xlabel('Category')
    axs[0, 0].set_ylabel('Values')
    axs[0, 0].set_title('Comparison of Average and Total Marks per CD')
    axs[0, 0].set_xticks(index_cd)
    axs[0, 0].set_xticklabels(categories_cd)
    axs[0, 0].legend()

    # Plot for COs (Bar Chart)
    bars1_co = axs[0, 1].bar(index_co, mrkt_co, bar_width, color='blue', alpha=0.7, label='Average Marks')
    bars2_co = axs[0, 1].bar(index_co, ttl_mrk_co, bar_width, color='green', alpha=0.7, label='Total Marks')

    # Add labels, title, and legend for CO Bar Chart
    axs[0, 1].set_xlabel('Category')
    axs[0, 1].set_ylabel('Values')
    axs[0, 1].set_title('Comparison of Average and Total Marks per CO')
    axs[0, 1].set_xticks(index_co)
    axs[0, 1].set_xticklabels(categories_co)
    axs[0, 1].legend()

    # Plot for CDs (Pie Chart)
    axs[1, 0].pie(mrkt_cd, labels=categories_cd, autopct='%1.1f%%', colors=['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightpink'], startangle=140)
    axs[1, 0].set_title('Distribution of Average Marks per CD')

    # Plot for COs (Pie Chart)
    axs[1, 1].pie(mrkt_co, labels=categories_co, autopct='%1.1f%%', colors=['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightpink'], startangle=140)
    axs[1, 1].set_title('Distribution of Average Marks per CO')

    # Adjust layout and display the plot
    plt.tight_layout()

    # Convert the plot to PNG image and base64 encode it
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url
