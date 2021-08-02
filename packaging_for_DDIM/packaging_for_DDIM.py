import pandas as pd
import os
import sys
from distutils.dir_util import copy_tree
import shutil
import zipfile
import warnings
warnings.filterwarnings("ignore")
import dicom
import glob
from pathlib import Path

def createDataframe(ds, own, job_id, mol):
    owner = own
    molecule = mol
    exceptions = []
    technique = ds.Modality.upper()
    if technique == 'CT':
        try:
            if job_id is None:
                job_id_n = ds.CommentsOnThePerformedProcedureStep
                job_id = job_id_n
                assert '' != str(job_id_n)
                assert 'none' != str(job_id_n).lower()

        except Exception as e:
            print("(0040|0280) --> Job_ID cannot be empty or 'none'")
            print()
                
            exceptions.append("(0040|0280) --> Job_ID cannot be empty")
            return None    
 
        try:
            if molecule is None:
                molecule = ds.OtherPatientIDs
                assert '' != str(molecule)
        except Exception as e:
            molecule = "None"

            
        experiment_id = ds.StudyID
        if ('' == str(experiment_id) or 'none' == str(experiment_id).lower()):
            experiment_id = input("(0020|0010) --> Experiment_ID cannot be empty, enter a new one: ")
            print("Experiment_ID: " + str(experiment_id))


        institute = str(ds.ReferringPhysicianName)
        if '' == str(institute) or 'none' == str(institute).lower():
            institute = input("(0008|0090) --> Institute cannot be empty, enter a new one: ")
            print("Institute: " + str(institute))

            
        subject_id = str(ds.PatientID)
        if '' == str(subject_id) or 'none' == str(subject_id).lower():
            subject_id = input("(0010|0020) --> Subject_ID cannot be empty, enter a new one: ")
            print("Subject_ID: " + str(subject_id))


        date = ds.StudyDate[0:4] + '-' + ds.StudyDate[4:6] + '-' + ds.StudyDate[6:8]
        if '' == str(date) or 'none' == str(date).lower():
            date = input("(0008|0020) --> Date cannot be empty, enter a new one: ")
            print("Date (YYYY-MM-DD): " + str(date))

 
        time = ds.StudyTime[0:2] + ':' + ds.StudyTime[2:4] + ':' + ds.StudyTime[4:6]
        if '' == str(time) or 'none' == str(time).lower():
            time = input("(0008|0030) --> Time cannot be empty, enter a new one: ")
            print("Time (HH:MM:SS): " + str(time))

        linked_experiment_id = ""
        
        if exceptions:
            for e in exceptions:
                print("- " + e)
            print()
        return CT_DataFrame(job_id, molecule, technique, experiment_id, institute, 
                            owner, date, time, subject_id, linked_experiment_id)
    
    
    elif technique == 'HISTOLOGY':
        return Hist_DataFrame()
    elif template == 'INVIVO':
        return IV_DataFrame()
    elif template == 'MALDI':
        return MALDI_DataFrame()
    elif template == 'POSTMORTEN':
        return PM_DataFrame()

    
def CT_DataFrame(job_id, molecule, technique, experiment_id, institute, 
                owner, date, time, subject_id, linked_experiment_id):
    
    df = pd.DataFrame({'Job_ID'               : [job_id],
                       'Molecule'             : [molecule],
                       'Technique'            : [technique],
                       'Experiment_ID'        : [experiment_id],
                       'Institute'            : [institute],
                       'Owner'                : [owner],
                       'Date'                 : [date],
                       'Time'                 : [time],
                       'Subject_ID'           : [subject_id],
                       'Linked_Experiment_ID' : [linked_experiment_id]})
    return df



def askForJob_ID():
    print()
    own_job_id = input("Do you want to enter your own Job_ID? (Yes or No): ")
    if own_job_id.lower() in ["y","ye","yes"]:
        job_id = input("Enter Job_ID: ")
        print("Job_ID: " + str(job_id))
    elif own_job_id.lower() in ["n","no"]:
        job_id = None    
    else:    
        print("Error")
        print("You must say 'Yes' or 'No'")
        print()
        job_id = askForJob_ID()
    return job_id


def askMolecule():
    print()
    own_molecule = input("Do you want to enter your own molecule? (Yes or No): ")
    if own_molecule.lower() in ["y","ye","yes"]:
        molecule = input("Enter molecule: ")
        print("Molecule: " + str(molecule))
    elif own_molecule.lower() in ["n","no"]:
        molecule = None    
    else:    
        print("Error")
        print("You must say 'Yes' or 'No'")
        print()
        molecule = askMolecule()
    return molecule

#---------------------------------------------------------------------------#

if len(sys.argv) != 2 :
    print("Error")
    print("Usage: python3 packaging_for_DDIM.py <path_to_images_folder>")
    print()
    sys.exit (1)

print()
owner = input("Type Job's owner name: ")

directories_path = sys.argv[1] + "/"

experiments = glob.glob(os.path.join(directories_path, "*", ""))

df = pd.DataFrame({'Job_ID'               : [],
                   'Molecule'             : [],
                   'Technique'            : [],
                   'Experiment_ID'        : [],
                   'Institute'            : [],
                   'Owner'                : [],
                   'Date'                 : [],
                   'Time'                 : [],
                   'Subject_ID'           : [],
                   'Linked_Experiment_ID' : []})

#Creation of Zip object
path = Path(directories_path)
zipobj = zipfile.ZipFile(str(path.parent.absolute()) + '/Archive.zip', 'w', zipfile.ZIP_DEFLATED)

job_id = askForJob_ID()

molecule = askMolecule()

for exp in experiments:
    
    if not os.path.isdir(exp):
        print("Ignoring " + exp + " because it is not a directory")
        print("It must follow:")
        print("Images Folder")
        print("--> Experiment Folder 0")
        print("           .")
        print("           .")
        print("           .")
        print("--> Experiment Folder N")
        print()
    else:
        if not glob.glob(exp + "*"):
            print()
            print(os.path.basename(exp[:-1]))
            print("Is empty. Ignoring...")
            
        else:
            print()
            print(os.path.basename(exp[:-1]))
            file = glob.glob(exp + "*")[0]
            try:
                ds = dicom.read_file(file)
                
                # Create and append Dataframe
                df_new = createDataframe(ds,owner, job_id, molecule)
                
                if df_new is None:
                    break
                df = pd.concat([df,df_new], axis=0, ignore_index=False) 

                # Get folder's structure   
                folder_job_id = df_new['Job_ID'].values[0]
                experiment_id = df_new['Experiment_ID'].values[0]
                subject_id = df_new['Subject_ID'].values[0]


                # Path where the results will be saved
                results_folder = directories_path + folder_job_id + "/" + experiment_id + "/" + subject_id
                #Create results folder
                old_mask = os.umask(0) # Saving the old umask value and setting umask to 0   
                if not os.path.exists(results_folder):
                    os.makedirs(results_folder,exist_ok=True)
                os.umask(old_mask) # Reverting umask value
                    #Copy files to results folder
                for file_path in glob.glob(exp + "*.*"):
                    shutil.copy(file_path,results_folder)


                files = glob.glob(directories_path + folder_job_id + "/" + experiment_id + "/*/*")

                for file in files:
                    file_name = os.path.split(file)[1]
                    zipobj.write(file, arcname = folder_job_id + "/" + experiment_id + "/" + subject_id + "/" + file_name)
                
                
            except Exception as e:
                print(e)
            else:
                print("Everything was okay!")
                print()
        
    
        
        
shutil.rmtree(directories_path + folder_job_id)

df.to_csv(r'' + directories_path + 'Metadata.csv', index = False, header=True)

zipobj.write(directories_path + 'Metadata.csv', arcname = 'Metadata.csv')
os.remove(directories_path + 'Metadata.csv') 

zipobj.close()

print()
print(str(len(df.index)) + " of " + str(len(experiments)) + " experiments were compressed")
print()
