# Docker for image pipeline

## Latest version 1.1
How to use it:
```bash
docker run -it -v /your/path/to/Images:/app/Images image_pipeline/call_apply -v /your/path/to/Results:/app/Results [image] [species*]
```
At this moment, this docker image returns three files for each CT image in the *Images* folder:

  - First of all, two of the three files are the resulting mask in *.mhd* and *.raw* format of segmenting the lungs 🫁 (left and right lobes). *MHD* file is an ITK MetaImage Header. Insight Segmentation and Registration Toolkit (ITK).
  
  - Last but not least, a comma-separated values file (*.csv*) with the value of volume of healthy and unhealthy lung.
  
![structure](https://user-images.githubusercontent.com/72487236/127621083-6584a5f1-3af5-4758-8784-8b64d225f9ac.png)

Input images can be in *.mhd/.raw* or DICOM format.

It is also advisable to run the docker typing which model (*species*) is going to be used to get the masks. Otherwise, default model is *human's model*. There are two additional models: *mice* and *macaques*.   

-----------------------------------------------------------
-----------------------------------------------------------

# Packaging for DDIM

Usage: 
``` python3
python3 packaging_for_DDIM.py <path_to_images_folder>
```

When uploading an experiment to DDIM, it is necessary to upload a .zip file with with the following structure:

<img width="1578" alt="folders" src="https://user-images.githubusercontent.com/72487236/127639010-36f32487-eb7f-4ae3-9428-6b21367cf794.png">

Furthermore, it is mandatory to create a .csv or .xls (*Excel*) file with some *metadata* about the images. 

| Job_ID  | Molecule |	Technique |	Experiment_ID |	Institute |	Owner |	Date |	Time |	Subject_ID |	Linked_Experiment_ID |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |

To ease this process, *packaging_for_DDIM.py* can be used.

In order to so, in <path_to_images_folder> there must be one folder for each subject and its images inside that.

For example:

<img width="492" alt="example" src="https://user-images.githubusercontent.com/72487236/127641163-a750734a-5470-40e0-bf93-4c457c7e1129.png">

## DICOM Tags
A DICOM data element, or attribute, is composed of a tag that identifies the attribute, usually in the format (XXXX,XXXX). To provide all necessary fields to create *metadata* file, the following DICOM tags are used:

        (0040,0280)  # User-defined comments on the Performed Procedure Step. Used for Job_ID
        (0010,1000)  # Other Patient IDs. Used for Molecule
        (0008,0060)  # Modality
        (0020,0010)  # Study ID, for human consumption
        (0008,0090)  # Referring Physician's Name. Used for Institute
        (0008,0020)  # Date in format YYYYMMDD
        (0008,0030)  # Time in format HHMMSS
        (0010,0020)  # Patient ID
        (0010,4000)  # User-defined additional information about the Patient. Used for TB strain.

If images have got these tags, *packaging_for_DDIM.py* will use them (asked previously if user wants to use these fields). If one of them is missing, it will be asked to the user to type them. 

As a result, the .zip file will be produced and ready to upload it to DDIM. 
