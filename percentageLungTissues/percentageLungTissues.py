import SimpleITK as sitk
import pandas as pd
import os
import numpy as np
import glob

## Original code
# def getPercentageLungTissues(images_path,results_path: str, lower_threshold = None , upper_threshold = None):
    
#lower_threshold = -965
#upper_threshold = -925
#    measures = []
#    min_max = sitk.MinimumMaximumImageFilter()
#    similarityFilter = sitk.SimilarityIndexImageFilter()

#    if os.path.isdir(images_path):
#        images_path = glob.glob(images_path + "/**/*.mhd", recursive=True)
#    else:
#        images_path = [images_path]
        
#    for image_path in images_path:

#        if len(os.path.split(image_path)[1]) > 0:    #Do not end with "/"
#                image_name = os.path.split(image_path)[1]
#        else:
#                image_name = os.path.split(os.path.split(image_path)[0])[1] + "/" + os.path.split(image_path)[1]
#        
#        image_name = os.path.splitext(image_name)[0]

#        image = sitk.ReadImage(image_path)

        
#        if lower_threshold is None:
#            lower_threshold = -400
    
#        if upper_threshold is None:
#            min_max.Execute(image)
#            upper_threshold = min_max.GetMaximum()

        
 #       seg = sitk.BinaryThreshold(image, lower_threshold, upper_threshold, 
 #                                  insideValue = 0, outsideValue = 1)
######################################################################################################################


def getPercentageLungTissues(seg, image_name, lower_threshold = None , upper_threshold = None):
    results_path = "/app/Results"

    
    measures = []
    min_max = sitk.MinimumMaximumImageFilter()
    similarityFilter = sitk.SimilarityIndexImageFilter()
        
        
    if lower_threshold is None:
        lower_threshold = -400

    if upper_threshold is None:
        min_max.Execute(image)
        upper_threshold = min_max.GetMaximum()

    
    seg[seg == 2] = 1  #Only one label for both lungs lobes
    seg = sitk.GetImageFromArray(seg)


    min_max.Execute(seg)

    connected = sitk.ConnectedComponent(seg)
    connected = connected > 1

    #Remove background's noise pixels
    openingFilter = sitk.BinaryMorphologicalOpeningImageFilter()
    openingFilter.SetKernelRadius(1)
    opened = openingFilter.Execute(connected)

    #
    closingFilter = sitk.BinaryMorphologicalClosingImageFilter()
    closingFilter.SetKernelRadius(5)
    closed = closingFilter.Execute(opened)
    
    old_closed = sitk.Image(closed.GetSize(), sitk.sitkUInt8)
    old_closed.CopyInformation(closed)
    similarityFilter.Execute(closed,old_closed)
    similarity = similarityFilter.GetSimilarityIndex()
    
    while similarity != 1:
        old_closed = closed
        closed = closingFilter.Execute(closed)
        similarityFilter.Execute(closed,old_closed)
        similarity = similarityFilter.GetSimilarityIndex()


    seg = sitk.GetArrayFromImage(seg)
    closed = sitk.GetArrayFromImage(closed)



    num_pixels_closed = np.count_nonzero(seg == 1)
    num_pixels_output = np.count_nonzero(output == 1)
    
    unhealthy_tissue = round(100 - (num_pixels_output/num_pixels_closed)*100,1)
    
    measures = {"Image":[image_name], "Unhealthy Lung Tissue(%)": [unhealthy_tissue], 
                "Lower Threshold (HU)": [lower_threshold], "Upper Threshold (HU)": [upper_threshold]}
    
    results_df = pd.DataFrame.from_dict(measures)
    results_df.to_csv(r'' + results_path + "/" + image_name +  '_PercentageLungTissues.csv', index = False, header=True)
