import radiomics
from radiomics import featureextractor as FEE

# file name
main_path = '.'
ori_name = r'\brain1_image.nrrd'
lab_name = r'\brain1_label.nrrd'
para_name = r'\Params.yaml'

# file path
ori_path = main_path + ori_name
lab_path = main_path + lab_name
para_path = main_path + para_name
print("originl path: " + ori_path)
print("label path: " + lab_path)
print("parameter path: " + para_path)

# Initialising the feature extractor using a configuration file
extractor = FEE.RadiomicsFeaturesExtractor(para_path)
print("Extraction parameters:\n\t", extractor.settings)
print("Enabled filters:\n\t", extractor.enabledImagetypes)
print("Enabled features:\n\t", extractor.enabledFeatures)

# run
result = extractor.execute(ori_path, lab_path)  # Extraction features
print("Result type:", type(result))  # result is returned in a Python ordered dictionary
print("")
print("Calculated features")
for key, value in result.items():  # output
    print("\t", key, ":", value)
