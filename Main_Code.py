# -*- coding: utf-8 -*-

!pip install rasterio
!pip install geopandas
!pip install earthpy
!pip install hdf5storage
import h5py
import hdf5storage
from tensorflow.keras.utils import to_categorical
!pip install osgeo
from osgeo import gdal
import rasterio
from rasterio.plot import show
import geopandas as gpd
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import numpy as np
from numpy import matlib as mb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import os
import pandas as pd
import matplotlib.pyplot as pltr

from sklearn.metrics import *
import xgboost

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, cohen_kappa_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import numpy as np
import cv2
!pip install spectral
import spectral
from sklearn import model_selection

import pandas as pd
import seaborn as sns
from xgboost import XGBClassifier
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np
from sklearn.metrics import accuracy_score
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe

import shap

def LoadMatFile(ModelFile,RegionName,Name):
    Data=hdf5storage.loadmat('/content/drive/MyDrive/Dataset/'+RegionName+'/'+Name+'.mat')['Subset']
    [F1,F2,F3]=Data.shape
    Data2D=np.reshape(Data,(F1*F2,F3))
    Data2D=np.nan_to_num(Data2D)
    predicted = ModelFile.predict(Data2D)
    predicted=np.reshape(predicted,(F1,F2))+1
    return predicted

def Writtt(MaskData,RegionName,Name,PhaseName,Classsfierr):

    file =fp = r''RegionName+'/'+Name+'-Trn+.tif'
    print(file)
    (fileRoot, fileExt) = os.path.splitext(file)
    outFileName = fileRoot + "_mod" + fileExt
    format='GTiff'
    (fileRoot, fileExt) = os.path.splitext(file)
    outFileName = fileRoot + "_mod" + fileExt
    format='GTiff'
    ds = gdal.Open(file)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    destination = PhaseName+'/'+PhaseName+'-'+Classsfierr+'/Result-'+Classsfierr+PhaseName+RegionName+'-'+Name+'.tif'
    print(destination)
    [cols, rows] = arr.shape
    dtype = gdal.GDT_Float32
    driver = gdal.GetDriverByName(format)
    outdata = driver.Create(destination, rows, cols, 1, dtype)
    outdata.SetGeoTransform(ds.GetGeoTransform())
    outdata.SetProjection(ds.GetProjection())
    outdata.GetRasterBand(1).WriteArray(np.squeeze(np.float64(MaskData)))
    outdata.GetRasterBand(1).SetNoDataValue(0)
    outdata.FlushCache()
    outdata = None
    band=None
    print('Complete')


def EvaluationResult(Label,PredictLabel):
    accuracy = accuracy_score(Label, PredictLabel)
    print('Accuracy: %f' % accuracy)
    kappa = cohen_kappa_score(Label, PredictLabel)
    print('Cohens kappa: %f' % kappa)# kappa


    matrix = confusion_matrix(Label, PredictLabel)# confusion matrix
    cmn = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]
    cmn = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]
    fig, ax = plt.subplots(figsize=(7,5))
    sns.set(font_scale=1.4)
    plt.rcParams["font.family"] = "Times New Roman"
    sns.heatmap(cmn, annot=True, fmt='.3f', xticklabels= ['Low', 'Moderate','High','Very High'], yticklabels= ['Low', 'Moderate','High','Very High'],cmap='Blues',annot_kws={'fontsize': 18,'fontfamily': 'Times New Roman'})
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show(block=False)

"""# **Define Global Pramters**"""

Phase='Phase-1'
ModelName='XGboost'

"""# **Concate Dataset**"""

Xtrain = pd.read_csv('Xtrain.csv')
ytrain = pd.read_csv('ytrain.csv')
Xtest = pd.read_csv('Xtest.csv')
Xvalidation = pd.read_csv('Xvalidation.csv')
ytest = pd.read_csv('ytest.csv')
yvalidation = pd.read_csv('yvalidation.csv')

Xtest.shape, Xvalidation.shape, ytest.shape, yvalidation.shape

feature_names =[
'dnbr',#1

'Elevation',#2
'Slope 2',#3
'Aspect',#4

'clay 0-5',#5
'cfvo 0-5',#6
'sand 0-5',#7
'silt 0-5',#8
'soc 0-5',#9

'LCLU',#10

'DVAR',#11
'SHADE',#12
'SAVG',  #13

'VS',#14
'ERC',#15
'VPD',#16
'PPT',#17
'TMMX1']

"""# **XGB Classifier load**"""

import pickle
file_name = Phase+'/Model-'+Phase+'/'+Phase+'-'+ModelName+'.pkl'
modelXgboost = pickle.load(open(file_name, "rb"))

"""# **Model Validation**"""

yvalidation, predicted = yvalidation,modelXgboost.predict(Xvalidation)

from sklearn.metrics import *
# calculate errors
accuracy = accuracy_score(yvalidation, predicted)
print('Accuracy: %f' % accuracy)
kappa = cohen_kappa_score(yvalidation, predicted)
print('Cohens kappa: %f' % kappa)# kappa
matthews_corr_coef= matthews_corrcoef(yvalidation, predicted)# matthews_corr_coef
print('matthews_corr_coef: %f' % matthews_corr_coef)
balanced_acc_s= balanced_accuracy_score(yvalidation, predicted)# balanced_accuracy_score
print('balanced_accuracy_score: %f' % balanced_acc_s)
matrix = confusion_matrix(yvalidation, predicted)# confusion matrix
print(matrix)
import seaborn as sns
sns.heatmap(matrix, annot=True, fmt='d')

cmn = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]
cmn = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]
fig, ax = plt.subplots(figsize=(14,10))
sns.set(font_scale=3.4)
plt.rcParams["font.family"] = "Times New Roman"
sns.heatmap(cmn, annot=True, fmt='.3f', xticklabels= ['Low', 'Moderate','High','Very High'], yticklabels= ['Low', 'Moderate','High','Very High'],cmap='Blues',annot_kws={'fontsize': 45,'fontfamily': 'Times New Roman'})
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize =45)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize = 45)
plt.ylabel('Actual', fontsize = 55, fontweight="bold")
plt.xlabel('Predicted', fontsize = 55, fontweight="bold")
ax.set_title('XGBoost', loc='center', wrap=True,fontsize = 55, fontweight="bold")
plt.show(block=False)

"""# **Next-Code**"""

import shap
explainer = shap.TreeExplainer(modelXgboost)
shap.initjs()

shap_values = explainer.shap_values(Xvalidation, approximate=True)

shap.summary_plot(shap_values, Xvalidation, plot_type="bar",feature_names=feature_names,max_display = 19, show = True)

"""# **Prediction Region 1**"""

RegionNumber='Region-1'

Name='Alice-Creek'
ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

Name='Hanover'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

Name='Lolo-Peak'
RegionNumber='Region-1'
ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

"""# **Prediction Region 2**"""

RegionNumber='Region-2'
Name='Williams-Fork'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

"""# **Prediction Region  3**"""

RegionNumber='Region-3'
Name='Bonita'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

RegionNumber='Region-3'
Name='Griffin'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

RegionNumber='Region-3'
Name='Johnson'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

"""# **Prediction Region  4**"""

RegionNumber='Region-4'
Name='Dollar-Ridge'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

Name='Rabbit-Foot'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

Name='Ross-Fork'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)



"""# **Prediction Region  5**"""

RegionNumber='Region-5'
Name='Delta'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

Name='Detwiler'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

Name='River-Complex'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

"""# **Prediction Region  6**"""

RegionNumber='Region-6'
Name='Cougar-Peak'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

Name='Devils-Knob-Complex'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)

Name='Rough-Patch-Complex'

ClssData=LoadMatFile(modelXgboost,RegionName=RegionNumber,Name=Name)
Writtt(MaskData=ClssData,RegionName=RegionNumber,Name=Name,PhaseName=Phase,Classsfierr=ModelName)
