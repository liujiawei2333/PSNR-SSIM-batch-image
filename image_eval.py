import argparse
import os
import cv2
import pandas as pd
from skimage.measure import compare_ssim
from skimage.measure import compare_psnr

parser = argparse.ArgumentParser(description='image_eval')
parser.add_argument('--orig_path',help='path to orig image dataset', default='orig/')
parser.add_argument('--recon_path',help='path to recon image dataset', default='recon/')
parser.add_argument('--image_format',help='format of the image', default='bmp')
opt = parser.parse_args()

num_files = 0
for fn in os.listdir(opt.orig_path):
    num_files += 1

image_number = []
psnr_number = []
ssim_number = []
for idx in range(num_files):
    locals()['orig_'+str(idx)+''] = cv2.imread('%s/orig_%d.%s' %(opt.orig_path,idx,opt.image_format))
    locals()['recon_'+str(idx)+''] = cv2.imread('%s/recon_%d.%s' %(opt.recon_path,idx,opt.image_format))
    locals()['psnr_'+str(idx)+''] = compare_psnr(locals()['orig_'+str(idx)+''],locals()['recon_'+str(idx)+''])
    locals()['ssim_'+str(idx)+''] = compare_ssim(locals()['orig_'+str(idx)+''],locals()['recon_'+str(idx)+''],multichannel=True)


    image_number.append(str(idx))
    psnr_number.append(locals()['psnr_'+str(idx)+''])
    ssim_number.append(locals()['ssim_'+str(idx)+''])

dit = {'image_number':image_number, 'psnr':psnr_number,'ssim':ssim_number}
df = pd.DataFrame(dit)
df.to_csv(r'./result.csv',columns=['image_number','psnr','ssim'],index=False,sep=',')
