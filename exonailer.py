# -*- coding: utf-8 -*-
import sys
sys.path.append('utilities')
import transit_utils
import general_utils
import numpy as np

################# OPTIONS ######################

# Define the target name, detrending method and parameters of it:
target = 'CL005-04'
phot_noise_model = 'white'
phot_detrend = 'mfilter'
window = 21#41

# Define if you want to perform automatic outlier removal (sigma-clipping):
phot_get_outliers = True

# Define which transits you want to ommit (counted from first transit):
n_ommit = [3,9]

# Limb-darkening law to be used:
ld_law = 'quadratic'

# Define the mode to be used:
mode = 'full' 

# Define noise properties:
rv_jitter = False

################################################

# ---------- DATA PRE-PROCESSING ------------- #

# First, get the transit and RV data:
t,f,f_err,t_rv,rv,rv_err = general_utils.read_data(target,mode)

# Initialize the parameters:
parameters = general_utils.read_priors(target)

# Pre-process the transit data if available:
if mode != 'rvs':
    t,phases,f, f_err = transit_utils.pre_process(t,f,f_err,phot_detrend,\
                                                  phot_get_outliers,n_ommit,\
                                                  window,parameters,ld_law)

# Run the MCMC:
import time
tic = time.time()
transit_utils.exonailer_mcmc_fit(t, f, f_err, t_rv, rv, rv_err, \
                                 parameters, ld_law, mode, rv_jitter = rv_jitter, \
                                 njumps=5000, nburnin = 5000, \
                                 nwalkers = 100,  noise_model = phot_noise_model)
toc = time.time()
print 'Took',toc-tic,' seconds to do 5000 jumps, 5000 burnins with 100 walkers.'
# Get plot of the transit-fit:
if mode == 'transit':
    transit_utils.plot_transit(t,f,parameters,ld_law)
elif mode == 'full':
    transit_utils.plot_transit_and_rv(t,f,t_rv,rv,rv_err,parameters,ld_law,rv_jitter)