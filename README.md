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
