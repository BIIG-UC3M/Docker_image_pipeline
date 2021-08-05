import sys
import SimpleITK as sitk
import numpy as np
import torch
from caller import call
import os
import glob
from percentageLungTissues.percentageLungTissues import *

species_dict = {"human":"human_org",
				"mice":"mice_TL",
				"macaque":"mix_no_TL_a_mac"}


def ReadImage(path : str, image_extension =".mhd"):
    
    def read_dicom(path):
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(path)
        reader.SetFileNames(dicom_names)
        return reader.Execute()
    
    
    if image_extension == ".mhd":
        image = sitk.ReadImage(path)
    elif image_extension == ".dcm" or image_extension == "":
        image = read_dicom(path)
    
    return image


images_folder  = "/app/Images"
results_folder = "/app/Results"

biological_species=sys.argv[1].lower()

if len(sys.argv) <= 2:
	model = species_dict["human"]
else:
	if "human" in biological_species:
		model = species_dict["human"]

	elif ("mouse" or "mice") in biological_species:
		model = species_dict["mice"]

	elif "nhp" or "macaque" or "monkey" in biological_species:
		model = species_dict["macaque"]

	else:
		print("Unknown species:", biological_species)
		print("Species must be one of the following:")
		for k in species_dict.keys():
			print("  -",k)
		sys.exit("Choose a correct one!") 



images_path = glob.glob(images_folder + "/*.mhd")

for path in images_path:
	name = os.path.split(path)[1]
	image_extension = os.path.splitext(path)[1]

	image = ReadImage(path,image_extension)

	mask = call.apply(image,model)

	seg = sitk.GetImageFromArray(mask)

	sitk.WriteImage(seg, os.path.join(results_folder, 'Res_' + name))

getPercentageLungTissues(images_folder,results_folder)