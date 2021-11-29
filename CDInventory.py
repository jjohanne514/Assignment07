#------------------------------------------#
# Title: CD_Invetory.py
# Desc: Working with classes and functions.
# Change Log: (who, when, what)
# Jason Johanneck, 2021-Nov-28, Created File
#------------------------------------------#

import os
import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def add_inventory(intID,strTitle,strArtist,lstTable):
        """Add a CD to the inventory table in memory

        Args:
            cd id (int)
            cd title (string)
            cd artist (string)
            current inventory in memmory (2D List of dictionary rows)
        Returns:
            current inventory in memory (2D List of dictionary rows)
        """
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        lstTable.append(dicRow)
        return lstTable
    
    @staticmethod
    def del_inventory(del_cd_id,table,confirm):
        """Remove a CD from 2D table in memory

        Args:i
            cd id to delete (int)
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
            confirm delete flag (boolean) - variable to check if cd id was found and deleted.
        Returns:
            table (list) - cd inventory in memory after the delete
            confirm (boolean) - delete flag to confirm the CD was removed.
        """
        intRowNr = -1
        print(del_cd_id)
        print(confirm)
        for row in table:
            intRowNr += 1
            if row['ID'] == del_cd_id:
                del lstTbl[intRowNr]
                confirm = True
                break
        print(confirm)
        return table ,confirm   

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()
        with open(strFileName, 'rb') as objFile:
            # was not sure how to check for end of file so used a While Loop
            # with try/except block instead.
            while True:
                try:
                    pdata = pickle.load(objFile)
                    data = pdata.strip().split(',')
                    dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                    table.append(dicRow)
                except:
                    break

    @staticmethod
    def write_file(file_name, table):
        """Function to write cd inventory to text file

        Args:
            file_name (string): name of the output file
            table (list of dict): 2D data structure to unpack and output to file
        Returns:
            None.
        """
        with open(strFileName, 'wb') as objFile:
            for row in table:
                lstValues = list(row.values())
                lstValues[0] = str(lstValues[0])
                pickle.dump((','.join(lstValues) + '\n'),objFile)

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        

# Check for empty file before attempting to load.
try:
    if os.path.getsize(strFileName) > 0:
        FileProcessor.read_file(strFileName, lstTbl)
    else:
        print("Input file is empty - proceeding to main menu")
        print()
except FileNotFoundError as e:
    print(type(e),e,e.__doc__, sep = '\n')
    print('File Not Found - proceeding to main menu')
    print()
    

# main loop
while True:
    # Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    if strChoice == 'x':
        break
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top
    elif strChoice == 'a':
        try:
            strID = input('Enter ID: ').strip()
            intID = int(strID)
        except ValueError as e:
            print('Not an integer')
            print(type(e),e,e.__doc__, sep = '\n')
            continue # re-display main menu if error on CD ID input
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        lstTbl = DataProcessor.add_inventory(strID,strTitle,strArtist,lstTbl)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        print('You added: ',dicRow)
        print()
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.i
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    elif strChoice == 'd':
        IO.show_inventory(lstTbl)
        strIDDel = input('Which ID would you like to delete? ').strip()
        try:
            intIDDel = int(strIDDel)
        except ValueError as e:
            print('CD ID is not an integer')
            print(type(e),e,e.__doc__, sep = '\n')
            continue # re-display main menu if error on CD ID input
        CDRemoved = False
        lstTbl, CDRemoved = DataProcessor.del_inventory(intIDDel,lstTbl, CDRemoved)
        if CDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    elif strChoice == 's':
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        if strYesNo == 'y':
            #save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    else:
        print('General Error')




