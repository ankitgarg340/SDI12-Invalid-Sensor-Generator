import pandas as pd

#creates a csv that is equivalent to the removed sensors masterlist

def load_sheet(f_excel, sheet, csv_list):
    '''
    Loads an excel sheet from a workbook into a pandas dataframe

    Inputs:
    f_excel: a string containing the filepath extension to the excel workbook

    sheet: a string denoting the sheet name to be loaded into the dataframe

    Output:
    A pandas dataframe of the excel sheet
    '''
    df = pd.read_excel(f_excel, sheet_name=sheet, usecols = [0,1,2,3])
    df_csv = df.to_csv(header=False, index=False)
    df_csv = df_csv.split("\n")

    #loads items from csv of execl sheet into csv_list
    #adds height and group to each item
    for item in df_csv:
        if len(item) > 3:
            item_as_list = item.strip("\r").split(",")
            item_as_list.append(sheet)
            try:
                height = int(item_as_list[0].split("_")[2])
            except:
                print(item_as_list)
            item_as_list.append(height)
            csv_list.append(item_as_list)

def main_create_csv(f_name_excel):
    list_items = []
    sheets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]

    #loads each sheet, adds to list_itmes
    for sheet in sheets:
        load_sheet(f_name_excel, sheet, list_items)
    
    #sorts list by group
    list_items.sort(key= lambda item:item[4])

    csv_file_name = f_name_excel.strip(".xlsx") + "(by group).csv"
    csv_file = open(csv_file_name, "w")

    csv_file.write("Sensor Code,Sensor Address,Sensor Group,MPS2 Failed,5TM Failed\n")
    for item in list_items:
        line = item[0] + "," + item[1] + "," + item[4] + "," + item[2] + "," + item[3] + "\n"
        csv_file.write(line)
    
    return csv_file_name



