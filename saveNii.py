## using simpleITK to load and save data.
import SimpleITK as sitk
import os
import nibabel as nb

def saveNii(img, reference_file_path, new_name):
    # 读取nii文件
    nii_img = nb.load(reference_file_path)
    nii_data = nii_img.get_fdata()
    new_data = nii_data.copy()

    # 把仿射矩阵和头文件都存下来
    affine = nii_img.affine.copy()
    hdr = nii_img.header.copy()

    scale = img.shape[0] / new_data.shape[0]  # when img is resampled from the img in reference file, the starting center of image maybe changed

    # 获取单个像素的信息并按照scale进行修改
    hdr['pixdim'][1] = hdr['pixdim'][1] / (img.shape[0] / new_data.shape[0])
    hdr['pixdim'][2] = hdr['pixdim'][2] / (img.shape[1] / new_data.shape[1])
    hdr['pixdim'][3] = hdr['pixdim'][3] / (img.shape[2] / new_data.shape[2])



    # if img.shape[3] == 1:
    if len(img.shape) == 3:
        hdr['dim'][0] = 3
        hdr['dim'][1] = img.shape[0]
        hdr['dim'][2] = img.shape[1]
        hdr['dim'][3] = img.shape[2]
        hdr['dim'][4] = 1

    # elif img.shape[3] > 1:
    elif len(img.shape) == 4:
        hdr['dim'][0] = 4
        hdr['dim'][1] = img.shape[0]
        hdr['dim'][2] = img.shape[1]
        hdr['dim'][3] = img.shape[2]
        hdr['dim'][4] = img.shape[3]

    if isinstance(img, float):
        hdr['datatype'] = 16
        hdr['bitpix'] = 32

    elif isinstance(img, int):

        hdr['datatype'] = 4
        hdr['bitpix'] = 16

    hdr['srow_x'][3] = hdr['srow_x'][3] * scale
    hdr['srow_y'][3] = hdr['srow_y'][3] * scale
    hdr['srow_z'][3] = hdr['srow_z'][3] * scale

    print(hdr)

    new_nii = nb.Nifti1Image(img, affine, hdr)

    # 保存nii文件，后面的参数是保存的文件名
    nb.save(new_nii, new_name)


if __name__ == "__main__":

    # reference_file_path = r'C:\Users\Gerald\Desktop\TestCases\q_Space\4Dsrf2022081301-0018-00001-000001-01.nii'
    # path_save = Path = os.path.abspath(os.path.join(reference_file_path, "..")) + "\\" + os.path.splitext(os.path.split(reference_file_path)[1])[0] + "_new.nii"

    # 读取img文件
    nii_img = nb.load(r'C:\Users\Gerald\Desktop\TestCases\img\AS_01_swdti_FA.nii')
    nii_data = nii_img.get_fdata()
    new_data = nii_data.copy()

    hdr = nii_img.header.copy()
    print(hdr)

    # 读取referenc 文件
    reference_file_path = r'C:\Users\Gerald\Desktop\TestCases\q_Space\4Dsrf2022081301-0018-00001-000001-01.nii'
    path_save = os.path.abspath(os.path.join(reference_file_path, "..")) + "\\" + os.path.splitext(os.path.split(reference_file_path)[1])[0] + "_new.nii"

    nii_img = nb.load(reference_file_path)



    saveNii(new_data, reference_file_path, path_save)



    # print(new_data.shape)
    # print(new_data.shape[0])    #
    #
    # print(hdr)

    # # 形成新的nii文件
    # new_nii = nb.Nifti1Image(new_data, affine, hdr)
    #
    # # 保存nii文件，后面的参数是保存的文件名
    # nb.save(new_nii, 'new_test.nii')
    #
    #
    #
    # itk_img = sitk.ReadImage(nii_path)



    # img = sitk.GetArrayFromImage(itk_img)
    # print("img shape:",img.shape)
    #
    # ## save
    # out = sitk.GetImageFromArray(img)
    # out.SetSpacing(itk_img.GetSpacing())
    # out.SetOrigin(itk_img.GetOrigin())
    #
    # path_save = Path=os.path.abspath(os.path.join(nii_path,"..")) + "\\" + os.path.split(nii_path)[1] + "_new.nii"
    #
    # sitk.WriteImage(out,path_save)




