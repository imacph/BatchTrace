import numpy as np
import pandas as pd

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


def get_folder_uuids_run_id_list(run_ids,conn):
    """
    Get file UUIDs for a given run_id range.
    
    Args:
        start (int): Start of the run_id range.
        stop (int): End of the run_id range.
    
    Returns:
        pd.DataFrame: DataFrame containing file UUIDs and their corresponding run_ids.
    """
    # Assume 'start' is now a list of run_ids to match
    run_ids_str = ','.join(str(run_id) for run_id in run_ids)
    
    query = f"""
    SELECT folder_uuid, run_id
    FROM run_info
    WHERE run_id IN ({run_ids_str})
    """

    df = pd.read_sql(query, con=conn)  # Replace with your database connection
    return df

def get_ekman_report(conn):

    query = """SELECT ekman,
    count(*) as n_runs,
    count(distinct reynolds) as distinct_reynolds
    FROM run_info
    GROUP BY ekman;"""

    df = pd.read_sql(query,con=conn)

    return df