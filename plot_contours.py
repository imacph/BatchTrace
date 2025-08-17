import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.interpolate import interp1d


s_func = np.loadtxt("s_func_real.txt")
ss = np.loadtxt("ss.txt")
zz = np.loadtxt("zz.txt")


n_rad_max = 140
n_leg_max = 150

rad_ratio = 0.35


fig,ax = plt.subplots(1,1,figsize=(8, 6))

vmax = np.max(s_func)
vmin = np.min(s_func)

norm = colors.SymLogNorm(vmin=vmin,vmax=vmax,linthresh = (vmax-vmin)/20)

levels = -np.logspace(np.log10(-vmin),np.log10(-vmin)-6,100)
levels = np.concatenate((levels,np.logspace(np.log10(vmax)-6,np.log10(vmax),100)))

tt = np.arctan(zz/ss)
rr = np.sqrt(ss*ss+zz*zz)




#ax.contourf(tt, rr, s_func,cmap='seismic',norm=norm,levels=levels)


ax.contourf(ss, zz, s_func,cmap='seismic',norm=norm,levels=levels)
ax.set_aspect('equal')
#plt.show()


fig,ax = plt.subplots(1,1,figsize=(5,5),dpi=200)

r = 1.5232
i = np.argmin(np.abs(r-rr[:,0]))



# Example: Discrete Fourier Transform of a signal vs angular frequency

theta_lim = 15

min_idx = np.argmin(np.abs(tt[0,:]-theta_lim/100*np.pi/2))
max_idx = np.argmin(np.abs(tt[0,:]+theta_lim/100*np.pi/2))

theta = tt[0,min_idx:max_idx+1]  # angular positions

signal = s_func[i, min_idx:max_idx+1]  # example signal, last row, adjust as needed


# Interpolate onto a high resolution uniform grid
N_uniform = 4096  # Increase number of points for higher frequency resolution
theta_uniform = np.linspace(np.min(theta), np.max(theta), N_uniform)
interp_func = interp1d(theta, signal, kind='cubic', fill_value="extrapolate")
signal_uniform = interp_func(theta_uniform)

# Optional: Zero-padding to further increase frequency resolution
pad_width = 2*N_uniform
signal_padded = np.pad(signal_uniform, pad_width, mode='constant')
theta_padded = np.linspace(np.min(theta), np.max(theta), N_uniform + 2 * pad_width)

ax.plot(theta_padded, signal_padded)

# Compute DFT frequencies for uniform grid
dt_uniform = theta_uniform[1] - theta_uniform[0]
freqs = np.fft.fftfreq(len(theta_padded), d=dt_uniform)
omega = 2 * np.pi * freqs

fft_vals = np.fft.fft(signal_padded)
fft_shifted = np.fft.fftshift(fft_vals)
omega_shifted = np.fft.fftshift(omega)

plt.figure(figsize=(6,4))
plt.plot(omega_shifted, np.abs(fft_shifted)**2)
plt.xlabel(r'latitudinal wave number ($\ell$)')
plt.xlim(0,)

plt.show()
