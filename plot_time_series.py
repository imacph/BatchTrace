import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
from sqlite3 import connect


dn = os.path.dirname(os.path.realpath(__file__))


db_name = "spring_2025_AxisymmLinStab"

conn = connect(os.path.dirname(dn)+"/{:s}/{:s}.db".format(db_name,db_name))  # Replace with your database connection

working_dir = os.path.join(dn, 'working_dir/')

file_names = glob.glob(working_dir+'*')


fig,ax = plt.subplots(1, 1, figsize=(8, 6))
for file in file_names:

    df = pd.read_csv(file)
    f_uuid = file.split('\\')[-1].split('_')[0]

    ekman,reynolds,n_rad_max,n_leg_max = pd.read_sql(f"SELECT ekman, reynolds, n_rad_max, n_leg_max FROM run_info WHERE folder_uuid = '{f_uuid}'", con=conn).iloc[0]
    
    
    label_str = "{:.2f} {:.2f} {:d} {:d}".format(np.log10(ekman), reynolds, int(n_rad_max), int(n_leg_max))
    ax.plot(df['time']/2/np.pi, df['KE'], label=label_str)

ax.set_yscale('log')
ax.set_xlabel('Time', fontsize=14)
ax.set_ylabel('Kinetic Energy', fontsize=14)
ax.legend(loc='upper right', fontsize=12, ncol=2)
fig.savefig("KE_plot.png", dpi=300, bbox_inches='tight')

