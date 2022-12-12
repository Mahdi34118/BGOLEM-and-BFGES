#! /bin/bash
#						  ____________________________________
#_____________________________________|            needed files          |________________________________
#_________________________________________________________________________________________________________| 
# Download 3T diffusion images from https://connectomeDB.com

#						  ____________________________________
#_____________________________________|             run code              |________________________________
#__________________________________________________________________________________________________________| 
#
#


#directories of data and codes
data_dir=/home/abagheri/HCP
code_dir=/home/abagheri/codes

#data directory variables
struct_folder=T1w
diff_folder=T1w/Diffusion



# source freesurfer
export FREESURFER_HOME=/usr/local/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh



#touch ${code_dir}/subjects_list.txt
#make subject list for loop over subjects
ls ${data_dir} | cat > ${code_dir}/subjects_list.txt



for subj in `cat ${code_dir}/subjects_list.txt`; do

	mkdir -p ${data_dir}/${subj}/MRtrix #make output dir

	cd ${data_dir}/${subj}/${struct_folder} #chenge diretctory to data file


	#run 5ttgen function to make tissue classifivation for 5 tissue csd
	5ttgen fsl ${data_dir}/${subj}/${struct_folder}/T1w_acpc_dc_restore_brain.nii.gz ${data_dir}/${subj}/MRtrix/5TT.mif -premasked -nthreads 40 -force
	
	#convert native space Desiakn2009 atlas to nodes.mif file
	labelconvert ${data_dir}/${subj}/${struct_folder}/aparc.a2009s+aseg.nii.gz /usr/local/freesurfer/FreeSurferColorLUT.txt /usr/local/mrtrix3/share/mrtrix3/labelconvert/fs_a2009s.txt ${data_dir}/${subj}/MRtrix/nodes.mif -force
	#change labes nubmer from number in freesurfer FreeSurferColorLUT.txt to fs_a2009s.txt label numbers
	labelsgmfix ${data_dir}/${subj}/MRtrix/nodes.mif ${data_dir}/${subj}/${struct_folder}/T1w_acpc_dc_restore_brain.nii.gz /usr/local/mrtrix3/share/mrtrix3/labelconvert/fs_a2009s.txt ${data_dir}/${subj}/MRtrix/nodes_fixSGM.mif -premasked -nthreads 40 -force
	# convert diffusion data to from nii.gz to .mif file
	mrconvert ${data_dir}/${subj}/${diff_folder}/data.nii.gz ${data_dir}/${subj}/MRtrix/DWI.mif -fslgrad ${data_dir}/${subj}/${diff_folder}/bvecs ${data_dir}/${subj}/${diff_folder}/bvals -datatype float32 -strides 0,0,0,1 -force
	
	#change directory do output folder
	cd ${data_dir}/${subj}/MRtrix
	#extract zero beta images from diffusion file and mean zero imgaes 
	dwiextract DWI.mif - -bzero | mrmath - mean meanb0.mif -axis 3 -force
	# use multi-shell multi to make reponse function for dti images (Perform Multi-Shell, Multi-Tissue Constrained Spherical Deconvolution)
	dwi2response msmt_5tt DWI.mif 5TT.mif RF_WM.txt RF_GM.txt RF_CSF.txt -voxels RF_voxels.mif -nthreads 80 -force
	# make fiber orientation density image from response function
	dwi2fod msmt_csd DWI.mif RF_WM.txt WM_FODs.mif RF_GM.txt GM.mif RF_CSF.txt CSF.mif -mask ${data_dir}/${subj}/${diff_folder}/nodif_brain_mask.nii.gz -nthreads 80 -force
	# This generates a 4D image with 3 volumes, corresponding to the tissue densities of CSF, GM and WM, which will then be displayed in mrview as an RGB image with CSF as red, GM as green and WM as blue (as was presented in the MSMT CSD manuscript).
	mrconvert WM_FODs.mif - -coord 3 0 | mrcat CSF.mif GM.mif - tissueRGB.mif -axis 3 -force
	# Generate the initial tractogram with maximum tract length of 250 mm and without  
	tckgen WM_FODs.mif 50M.tck -act 5TT.mif -backtrack -crop_at_gmwmi -seed_dynamic WM_FODs.mif -maxlength 250 -select 50M -cutoff 0.06 -nthreads 80 -force
	# make connectome matrix from generated tracks (with zero values at diagonal)
	tck2connectome -symmetric -zero_diagonal 50M.tck nodes_fixSGM.mif connectome_50M.csv -nthreads 80 -force
	# make connectome matrix from generated tracks (with zero values at diagonal) and also nomalized with nodes volume
	tck2connectome -symmetric -scale_invnodevol -zero_diagonal 50M.tck nodes_fixSGM.mif connectome_invnodevol_50M.csv -nthreads 80 -force



done
