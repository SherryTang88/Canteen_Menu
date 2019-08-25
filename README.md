# Canteen_Menu

 <p>This application allows users to:

  1. Sign in as admin -> For canteen store owners to set or delete menu
  2. Sign in as user -> For Customer to view available menu</p><br>
  
  
To start the application, please save the py file and csv file (severs as local database) to the same directory. 
Then use terminal cd to the directory and run command line:

#### $ python3 canteen_menu.py -d menu_database.csv

<br>Notes for Admin:

  * The password for login as admin is __"admin"__
  * Please follow the input format while setting/deleting menu:
    * For dish Name use _ to replace space : eg. chicken_rice/french_fries...
    * Availble Day Format : eg. monday/tuesday/wedneday...
    * Timing use 24-hours Format : eg. 10:00/22:30...
