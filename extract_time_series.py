import pandas as pd
import numpy as np
from sqlite3 import connect
import os
def get_folder_uuids_run_id_range(start,stop,conn):
    """
    Get file UUIDs for a given run_id range.
    
    Args:
        start (int): Start of the run_id range.
        stop (int): End of the run_id range.
    
    Returns:
        pd.DataFrame: DataFrame containing file UUIDs and their corresponding run_ids.
    """
    query = f"""
    SELECT folder_uuid, run_id
    FROM run_info
    WHERE run_id >= {start} AND run_id <= {stop}
    """

    df = pd.read_sql(query, con=conn)  # Replace with your database connection
    return df


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
start = 1
stop = 6

df = get_folder_uuids_run_id_range(start, stop, conn)

for file_uuid in df['folder_uuid']:

    folder_path = os.path.dirname(dn)+"/{:s}/{:s}".format(db_name,file_uuid)

    ts_data = get_time_series_data(folder_path,"KE_array.txt")

    time_step = pd.read_sql(f"SELECT time_step FROM run_info WHERE folder_uuid = '{file_uuid}'", con=conn).iloc[0, 0]
    time_array = np.linspace(time_step,time_step*len(ts_data),len(ts_data))

    ts_data = np.column_stack((time_array, ts_data))  # Add time as the first column
    # Create a DataFrame with time as the first column and KE values as subsequent columns
    ts_df = pd.DataFrame(ts_data,columns=['time','KE'])
    
    ts_df.to_csv(os.path.dirname(dn)+"/db_wrangler/working_dir/{:s}_KE_array.csv".format(file_uuid), index=False)


# Close the database connection
conn.close()
