import pandas as pd
import time
import errno
import gc
import logging
import os


def update_csv(hab, usuario, situacion):
    year = time.gmtime().tm_year
    mes = time.gmtime().tm_mon
    path = "../src/informes/" + f"Año - {year}/mes_{mes}.csv"

    try:
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    logging.error(
                        "specified path is not possible to be created")
                    raise
        df = pd.read_csv(path, sep='|')
    except:
        df = pd.DataFrame(columns=['hora', 'habitacion', 'usuario', 'situacion'])

    df_row = pd.DataFrame([[time.asctime(), hab, usuario, situacion]],
                          columns=['hora', 'habitacion', 'usuario', 'situacion'])
    df = df.append(df_row, ignore_index=True)

    df.to_csv(path, sep='|', index=False, header=True)
