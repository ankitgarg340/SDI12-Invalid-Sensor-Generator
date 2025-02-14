from export_checker import *
from csv_creation_removed_sensors import *
'''
***Requires Pandas library***

Things to change:
f_name_excel: file name or path to file of the excel masterlist of physically removed sensors
f_name_export: file name or path to file of the export check generated from a new config file
'''
def main():
    f_name_excel = "subsoil SDI12 Sensor Status WEST.xlsx"
    f_name_export = "leo_west_sdi12-export-check-6 1.csv"

    csv_file_master = main_create_csv(f_name_excel)

    main_export(f_name_export, csv_file_master)
    print("done :)")

main()


