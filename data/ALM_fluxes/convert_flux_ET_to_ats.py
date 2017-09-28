import numpy as np
import h5py
df = np.loadtxt("flux_output_w_fluxtowerR.txt",skiprows=1)
dv = np.loadtxt("vsfm_flux_output_w_fluxtowerR.txt",skiprows=1)

times = np.array(range(len(df)))
times = times * 86400.

hf = h5py.File("asu_pet_clm_forcing.h5",'w')
hf.create_dataset("time [s]", data=times)
hf.create_dataset("precipitation - ET [m s^-1]", data=(1.e-3 * (df[:,0] - df[:,5] - df[:,6] - df[:,7])))
hf.close()

hf = h5py.File("asu_pe_t_clm_forcing.h5",'w')
hf.create_dataset("time [s]", data=times)
hf.create_dataset("precipitation - E [m s^-1]", data=(1.e-3 * (df[:,0] - df[:,5] - df[:,6])))
hf.create_dataset("transpiration [-m s^-1]", data=(-1.e-3 * df[:,7]))
hf.close()

vf = h5py.File("asu_pet_vsfm_forcing.h5",'w')
vf.create_dataset("time [s]", data=times)
vf.create_dataset("precipitation - ET [m s^-1]", data=(1.e-3 * (dv[:,0] - dv[:,5] - dv[:,6] - dv[:,7])))
vf.close()

vf = h5py.File("asu_pe_t_vsfm_forcing.h5",'w')
vf.create_dataset("time [s]", data=times)
vf.create_dataset("precipitation - ET [m s^-1]", data=(1.e-3 * (dv[:,0] - dv[:,5] - dv[:,6])))
vf.create_dataset("transpiration [-m s^-1]", data=(-1.e-3 * dv[:,7]))
vf.close()


