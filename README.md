Invalid Sensor Generator
Author: Ankit Garg (email: ankitgarg@arizona.edu or ankit195300@gmail.com)
Date created: 08/16/2024


Purpose:
This python program uses the export check from a newly generated configuration file of the SDI12 sensors (see Config Parser) to find which sensors are reporting invalid (-9999) values. This program detects dead 5TM and MPS2 sensors which have not been physically removed, and reports these sensors into a csv file organized by group. This script is currently set up to work with SDI12 export checks, but can be modified and adjusted to work with similar data exports. To do this, edit the export_checker.py file.


Required Libraries:
-Pandas (https://pandas.pydata.org)

The easiest way to install pandas is through pip. Open a terminal application and type "pip install pandas" to install.


How to use:
1. Ensure that export_check.py, csv_cration_removed_sensors.py, and invalid_sensor_generator.py are in the same folder as the export check csv file and the excel file of the removed sensors masterlist of the bay you want to generate an invalid sensor list for. 

2. Open this directory or folder in a code editor such as VSCode. This can be ran from the terminal as well, although it will be more difficult to edit the correct variable and path names.

3. In the invalid_sensor_generator.py file at the top of the main function, edit the strings f_name_excel and f_name_export to be the name of the excel masterlist file and the export check file, respectively. 

4. Run invalid_sensor_generator.py. Running this will generate 2 files. The first file generated will be a csv file which is equivalent to the excel masterlist file of the physically removed sensors, organized by sensor zone. The other file will be a csv file list of the invalid sensors in the given bay.
