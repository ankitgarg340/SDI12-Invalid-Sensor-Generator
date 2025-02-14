import pandas as pd
def value_invalid(value_list):
    #function to test all values to see if all are -9999
    for item in value_list:
        if item != item:
            return True
        if item != -9999:
            return False
    return True

def find_sensor_name(sensor_str):
    list_sensor = sensor_str.split("\\")
    return list_sensor[6] + "_" + list_sensor[7]

def find_sensor_id_wheader(sensor_str):
    list_sensor = sensor_str.split("_")
    return list_sensor[0] + "_" + list_sensor[1] + "_" + list_sensor[2] + "_" + list_sensor[3] + "_" + list_sensor[4]

def find_sensor_id(sensor_str):
    list_sensor = sensor_str.split("_")
    return list_sensor[1] + "_" + list_sensor[2] + "_" + list_sensor[3]

def find_bay(src_csv, src_csv_master):
    '''
    Ensures that the excel workbook and config file are about sensors in the same bay

    Inputs:
    f_excel: a string containing the filepath extension to the excel workbook

    f_ini: a string containing the filepath extension to the config file 

    Output:
    A string denoting the LEO bay the excel and config file are about
    '''

    if "center" in src_csv and "CENTER" in src_csv_master:
        return "C"
    
    if "east" in src_csv and "EAST" in src_csv_master:
        return "E"
    
    if "west" in src_csv and "WEST" in src_csv_master:
        return "W"
    
    return "Error"

def create_hash_mastercsv(src_csv_masterlist):
    sensor_dict = {}

    #converts masterlist of removed sensors into dict
    f = open(src_csv_masterlist, "r")
    for line in f:
        clean_line = line.strip("\n")
        list_line = clean_line.split(",")
        sensor_dict[list_line[0]] = [list_line[1], list_line[2]] 
    
    return sensor_dict


def load_sheet(f_excel, sheet):
    '''
    Loads an excel sheet from a workbook into a pandas dataframe

    Inputs:
    f_excel: a string containing the filepath extension to the excel workbook

    sheet: a string denoting the sheet name to be loaded into the dataframe

    Output:
    A pandas dataframe of the excel sheet
    '''
    df = pd.read_excel(f_excel, sheet_name=sheet, usecols=[0, 2, 3])
    df_csv = df.to_csv(header=False, index=False)
    df_csv = df_csv.split("\n")

    csv_list = []
    for item in df_csv:
        if len(item) > 3:
            csv_list.append(item.strip("\r").split(","))

    return csv_list

def create_removal_list_mps2(csv_list, removal_list, bay):
    '''
    Appends to a running python list all the mps2 sensors to remove.

    Inputs:
    df: a pandas dataframe of an excel sheet

    col_name: a string containing the name of the column in excel with the log of the MPS2 failure

    removal_list: the removal python list to be appended to

    bay: a string containing the name of the LEO bay the excel and config file are about

    Output:
    None (appends to a running list)
    '''

    for item in csv_list:
        if len(item[1]) > 0:
            removal_list.append("[LEO-" + bay + "_" + item[0] + "_MPS-2_soilTemp]")
            removal_list.append("[LEO-" + bay + "_" + item[0] + "_MPS-2_MWP]")
    

def create_removal_list_5tm(csv_list, removal_list, bay):
    '''
    Appends to a running python list all the 5TM sensors to remove.

    Inputs:
    df: a pandas dataframe of an excel sheet

    col_name: a string containing the name of the column in excel with the log of the MPS2 failure

    removal_list: the removal python list to be appended to

    bay: a string containing the name of the LEO bay the excel and config file are about

    Output:
    None (appends to a running list)
    '''
    for item in csv_list:
        if len(item[2]) > 0:
            removal_list.append("[LEO-" + bay + "_" + item[0] +"_5TM_VWC]")
            removal_list.append("[LEO-" + bay + "_" + item[0] + "_5TM_bulkPerm]")
            removal_list.append("[LEO-" + bay + "_" + item[0] +"_5TM_soilTemp]")

def read_csv(csv_src):
    df = pd.read_csv(csv_src)
    csv_dict = {}

    #only copies non-header values from csv
    for column in df:
        if "YYYY" not in column and "CS451" not in column:
            csv_dict[find_sensor_name(column)] = df[column].tolist()
    
    #finds invalid sensors
    invalid_sensors = []
    for k,v in csv_dict.items():
        if value_invalid(v):
            invalid_sensors.append(k)

    return invalid_sensors


def main_export(src_csv, src_csv_master):

    invalid_sensors = read_csv(src_csv)
    invalid_ids = []

    bay = find_bay(src_csv, src_csv_master)

    #deletes duplicates from invalid sensor list
    for sensor in invalid_sensors:
        sensor_id = find_sensor_id_wheader(sensor)
        if sensor_id not in invalid_ids:
            invalid_ids.append(sensor_id)

    sensor_groups = create_hash_mastercsv(src_csv_master)

    #writes all file lines to list
    f_out = open("invalid sensors in " + bay + " bay.csv", "w")
    file_lines = []
    for sensor in invalid_ids:
        file_lines.append([sensor, sensor_groups[find_sensor_id(sensor)][1], sensor_groups[find_sensor_id(sensor)][0]])
    
    #sorts list by group
    file_lines.sort(key=lambda line:line[1])
    f_out.write("sensor id,sensor group,serial ID\n")

    #writes to file
    for line in file_lines:
        f_out.write(line[0] + "," + line[1]+ "," + line[2] + "\n")
    
    print(str(len(invalid_ids)) + " invalid sensors in " + bay + " bay")