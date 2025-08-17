import pandas as pd
import numpy as np
from sqlite3 import connect
import os
from db_wrangler import get_folder_uuids_run_id_range, get_folder_uuids_run_id_list

def get_time_series_data(folder_path, file_name):

    """
    Get time series data from a file in a specified folder.
    
    Args:
        folder_path (str): Path to the folder containing the file.
        file_name (str): Name of the file to read.
    
    Returns:
        pd.DataFrame: DataFrame containing the time series data.
    """
    file_path = os.path.join(folder_path, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_name} not found in {folder_path}")
    
    data = np.loadtxt(file_path)
    return data


dn = os.path.dirname(os.path.realpath(__file__))
db_name = "spring_2025_AxisymmLinStab"

conn = connect(os.path.dirname(dn)+"/{:s}/{:s}.db".format(db_name,db_name))  # Replace with your database connection
start = 85
stop = 87

df = get_folder_uuids_run_id_range(start, stop, conn)
#df = get_folder_uuids_run_id_list([34,35,36,37,38,39],conn)

reynolds = 41

time_step = 0.05
ekman = 0.000023669
query = f"""
    SELECT folder_uuid, run_id
    FROM run_info
    WHERE (ekman = {ekman})
    """


df = pd.read_sql(query, con=conn)  # Replace with your database connection

working_dir = os.path.join(os.path.dirname(dn), "db_wrangler", "working_dir")
if os.path.exists(working_dir):
    for filename in os.listdir(working_dir):
        file_path = os.path.join(working_dir, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            for root, dirs, files in os.walk(file_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(file_path)

for file_uuid in df['folder_uuid']:

    folder_path = os.path.dirname(dn)+"/{:s}/{:s}".format(db_name,file_uuid)

    ts_data = get_time_series_data(folder_path,"KE_array.txt")
    
    time_step = pd.read_sql(f"SELECT time_step FROM run_info WHERE folder_uuid = '{file_uuid}'", con=conn).iloc[0, 0]
    time_array = np.linspace(time_step,time_step*len(ts_data),len(ts_data))
    print(len(ts_data))
    ts_data = np.column_stack((time_array, ts_data))  # Add time as the first column
    # Create a DataFrame with time as the first column and KE values as subsequent columns
    ts_df = pd.DataFrame(ts_data,columns=['time','KE'])
    
    ts_df.to_csv(os.path.dirname(dn)+"/db_wrangler/working_dir/{:s}_KE_array.csv".format(file_uuid), index=False)


# Close the database connection
conn.close()
