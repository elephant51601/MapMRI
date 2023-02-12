# -*- coding: utf-8 -*-


import MapMRI
import SimpleITK as sitk
import os

import saveNii

niiPath = r"D:\Pycharm\Project\patient_data\source\20220731_091656qspace2mmDSIs017a001.nii"
bvalsPath = r"D:\Pycharm\Project\patient_data\source\20220731_091656qspace2mmDSIs017a001.bval"
bvecsPath = r"D:\Pycharm\Project\patient_data\source\20220731_091656qspace2mmDSIs017a001.bvec"
# 数据路径

data, affine = MapMRI.get_data(niiPath)
# 获取数据和数据的放射变换(affine)
bvals, bvecs = MapMRI.get_bvals_bvecs(bvalsPath, bvecsPath)
# 获取b值

big_delta = 0.0304
small_delta = 0.0207
# 这两个是指定的梯度参数，为了让Q空间的指标有实际意义
# 不可修改

gtab = MapMRI.get_gtab(bvals, bvecs, big_delta, small_delta)
# 获取梯度信息

data_small = data[40:65, 40:51]
# 数据中的片选，用于测试


print('data.shape (%d, %d, %d, %d)' % data.shape)

radial_order = 4
# 决定基的展开顺序，即用多少个基函数来近似信号

# map_model_laplacian_aniso = MapMRI.Laplacian(gtab, radial_order)

map_model_positivity_aniso = MapMRI.Positivity(gtab, radial_order)

# map_model_both_aniso = MapMRI.BothMethod(gtab, radial_order)
# 分别为用拉普拉斯正则化，正定约束和两种方法都使用建立的各向异性(aniso)模型

# map_model_both_ng = MapMRI.BothMethod_NG(gtab, radial_order)
# map_model_both_iso = MapMRI.BothMethod_ODF(gtab, radial_order)
# NG和ODF两种方法都使用

# mapfit_laplacian_aniso = map_model_laplacian_aniso.fit(data)
mapfit_positivity_aniso = map_model_positivity_aniso.fit(data)
# mapfit_both_aniso = map_model_both_aniso.fit(data_small)
# mapfit_both_ng = map_model_both_ng.fit(data)
# mapfit_both_iso = map_model_both_iso.fit(data_small)
# 信号的拟合


# Save nii files

# odf = MapMRI.getODF(mapfit_both_iso)
# 得到ODF
path_save_RTOP = os.path.abspath(os.path.join(niiPath,"..")) + "\\" + os.path.split(niiPath)[1] + "RTOP_new.nii"
path_save_RTAP = os.path.abspath(os.path.join(niiPath,"..")) + "\\" + os.path.split(niiPath)[1] + "RTAP_new.nii"
path_save_RTPP = os.path.abspath(os.path.join(niiPath,"..")) + "\\" + os.path.split(niiPath)[1] + "RTPP_new.nii"

saveNii.saveNii(mapfit_positivity_aniso.rtop(), niiPath, path_save_RTOP)
saveNii.saveNii(mapfit_positivity_aniso.rtap(), niiPath, path_save_RTAP)
saveNii.saveNii(mapfit_positivity_aniso.rtpp(), niiPath, path_save_RTPP)


# MapMRI.showRTOP(mapfit_laplacian_aniso, mapfit_positivity_aniso, mapfit_both_aniso)
# MapMRI.showlpNorm(mapfit_laplacian_aniso, mapfit_positivity_aniso, mapfit_both_aniso)
# MapMRI.showAll(mapfit_laplacian_aniso, mapfit_positivity_aniso, mapfit_both_aniso)
# MapMRI.showNG(mapfit_both_ng)
# MapMRI.showODF(mapfit_both_iso)
# 以PNG格式展示处理结果