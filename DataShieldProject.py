# command line input

import sys
import os
import time
import schedule
import shutil
import hashlib
import zipfile

############################################################################
#
#   Function Name : Make_Zip
#   Description   : Return the Zip file of the current directory 
#   Author        : Shubham Shankarlal Kumawat
#   Date          : 09/02/2026
#
############################################################################

def Make_Zip(folder):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-c%S")
    zip_Name = folder+"_"+timestamp+".zip"

    # Open the Zip File 

    zobj = zipfile.ZipFile(zip_Name,'w',zipfile.ZIP_DEFLATED)

    for root ,dirs,files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root,file)
            relative = os.path.relpath(full_path,folder)
            zobj.write(full_path,relative)
    zobj.close()

    return zip_Name

############################################################################
#
#   Function Name : Calculate_hash
#   Description   : Return the MD5 hash of a file
#   Author        : Shubham Shankarlal Kumawat
#   Date          : 09/02/2026
#
############################################################################

def Calculate_hash(Path):
    hobj = hashlib.md5()
    fobj = open(Path,"rb")

    while True:
        data = fobj.read(1024)
        if not data:
            break
        else:
            hobj.update(data)

    fobj.close()
    return hobj.hexdigest()

############################################################################
#
#   Function Name : BackupFiles
#   Description   : Returns Backup files from source to destination
#   Author        : Shubham Shankarlal Kumawat
#   Date          : 09/02/2026
#
############################################################################

def BackupFiles(Source , Destination):
    Copied_Files = []

    print("Creating the backup folder for backup process")
    os.makedirs(Destination, exist_ok = True)

    for root ,dirs,files in os.walk(Source):
        for file in files:
            src_path = os.path.join(root,file)
            relative = os.path.relpath(src_path,Source)
            dest_path = os.path.join(Destination,relative)

            os.makedirs(os.path.dirname(dest_path),exist_ok= True)

            # Cpoy the files if its new
            if (not os.path.exists(dest_path)) or (Calculate_hash(src_path) != Calculate_hash(dest_path)):

                shutil.copy2(src_path,dest_path)
                Copied_Files.append(relative)
                
    return Copied_Files

############################################################################
#
#   Function Name : DataShieldStart
#   Description   : Returns the Backup files and Zip file name
#   Author        : Shubham Shankarlal Kumawat
#   Date          : 09/02/2026
#
############################################################################

def DataShieldStart(Source = "Data"):
    Border = "-" * 50
    BackupName = "Backuped_Files"

    print(Border)
    print("Backup Process Stated Sucessfully at : ",time.ctime())
    print(Border)

    files = BackupFiles(Source , BackupName)
    zip_file = Make_Zip(BackupName)

    print(Border)
    print("Backup Completed Sucessfully")
    print("Zip File gets created : ",zip_file)
    print(Border)
        
 ############################################################################
#
#   Function Name : main
#   Description   : Returns the command line arguments and apply the scheduler
#   Author        : Shubham Shankarlal Kumawat
#   Date          : 09/02/2026
#
############################################################################

def main():
    
    Border = "-" * 50
    print(Border)
    print("--------------- Data Shield System ---------------")
    print(Border)

    if len(sys.argv) == 2:
        if sys.argv[1] == "--h" or sys.argv[1] == "--H":
            print("This Script is used to :")
            print("1 : Takes auto backup at given time.")
            print("2 : Backup only new and updated files.")
            print("3 : Create an archive of the backup periodically.")

        elif sys.argv[1] == "--u" or sys.argv[1] == "--U":
            print("Use the automation script as")
            print("ScriptName.py TimeInterval  SourceDirectory")
            print("TimeInterval : The time in minutes for periodic sceduling")
            print("SourceDirectory : Name of directory to backup")

        else:
            print("Enable to proceed as there is no such option..")
            print("please use --u or --h for more details...")

    # python ProcessLogger.py 5 Data
    elif len(sys.argv) == 3:
        print("Inside Projects Logic")
        print("Time Interval :", sys.argv[1], " Minutes")
        print("Directory Name :", sys.argv[2])

        # Apply the Schedular

        schedule.every(int(sys.argv[1])).minutes.do(DataShieldStart, sys.argv[2])

        print(Border)
        print("Data Shield System Started Successfully...")
        print("Time Interval in Minutes: ", sys.argv[1])
        print("Press Ctrl + C  to stop the execution")
        print(Border)

        # Wait Till Abort
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print("Invalid Number of Command line arguments...")
        print("Enable to proceed as there is no such option..")
        print("please use --u or --h for more details...")

    print(Border)
    print("----------Thank You For Using Our Script----------")
    print(Border)

############################################################################
#
#  Call of main function to start the execution of the script
#
############################################################################

if __name__ == "__main__":
    main()

############################################################################
#
#   Input  : python DataShieldFinal.py 5 Data
#
#   Output : Program will take backup of the Data folder after every 5 min
#            and create a zip file of the backuped files.
#
############################################################################

