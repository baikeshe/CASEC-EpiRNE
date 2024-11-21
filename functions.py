#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import numpy as np
import pandas as pd
import epyestim
import epyestim.covid19 as covid19
import epyestim.deconvolution as deconvolution
import epyestim.bootstrap as bootstrap
import epyestim.smoothen as smoothen
import os
from scipy.stats import gamma, poisson


def _synthetic_infections(seed, r_ts, serial_UIUC_New_U):
    assert len(seed) == len(serial_UIUC_New_U)
    generated_incidence = seed[:]
    for r in r_ts:
        mu = r * sum(p * i for i, p in zip(serial_UIUC_New_U[1:], generated_incidence[::-1]))
        generated_incidence.append(
            poisson(mu=mu).rvs()
        )
    return pd.Series(generated_incidence[len(seed):], index=r_ts.index)


# Construct the serial interval under the impact of control signal inputs (base_test = 1-base_t/window_t=1-1/7)
def _infection_update(testing_rate, serial_interval):                             
    serial_interval_New = serial_interval-serial_interval
    serial_interval_New[0]= serial_interval[0]
    serial_interval_New[1]= serial_interval[1]
    for x in range(2,len(serial_interval_New)):
        serial_interval_New [x] = testing_rate**(x-1)*serial_interval[x]
    return serial_interval_New


def _synthetic_infections_Rt(seed, r_ts,serial_UIUC_U,total_I_No_T,total_I_now,Total_pop, Multiplier):
    assert len(seed) == len(serial_UIUC_U)
    generated_incidence = seed[:]
    total_I_No_T_U=total_I_No_T-sum(generated_incidence)
    for r in r_ts:
        r_scale = r/Multiplier*(Total_pop-(total_I_No_T_U+sum(generated_incidence)))/(Total_pop-total_I_now)
        #r= r/Multiplier*(Total_pop-(total_I_No_T+sum(generated_incidence)))/(Total_pop-total_I_now)
        mu =r_scale * sum(p * i for i, p in zip(serial_UIUC_U[1:], generated_incidence[::-1]))
        #print(r_scale)
        #print(total_I_No_T_U+sum(generated_incidence))
        generated_incidence.append(
            poisson(mu=mu).rvs()
        )
    return pd.Series(generated_incidence[len(seed):], index=r_ts.index)

# Explain inputs:
    #1) seed: initial conditions for infectioned population; needs to be updated iteratively in a loop
    #2) r_ts: a list of estimated reproduction number from UIUC/Purdue testing data
    #3) serial_UIUC_U: serial distriubtion under UIUC's testing strategy (we should use the original serial distribtuion here)
    #4) total_I_No_T: total number of the cumulated infected population for the simulated environment
    #5) total_I_now: total number of the cumulated infected population for the UIUC testing process
    #6) Total_pop: total population (students + staff)
    #7) reproduction number scalor
    
    
def _synthetic_infections_U(seed, r_ts, SI_interval):           #seed is the initial condition; r_ts is Rt, which needs to be updated through esitmation and scaling; SI_interval is the serial interval which needs to be updated through control.
    assert len(seed) == len(SI_interval)                        #assert if the sizes are the same

    generated_incidence = seed[:]                               #pass the initial condition to generated_incidence
    for r in r_ts:
        mu = r * sum(p * i for i, p in zip(SI_interval[1:], generated_incidence[::-1])) #generating infection profile 
        generated_incidence.append(
            poisson(mu=mu).rvs()
        )

    return pd.Series(generated_incidence[len(seed):], index=r_ts.index)


# Construct a function to compute new R_t 
def _Rt_update(R_Test, Daily_infection_1, Daily_infection_2, Scaling_factor, Population):
    R_Ori = []
    for x in range(len(Daily_infection_1)):
        const = R_Test[x]/Scaling_factor*(Population-sum(Daily_infection_1[0:x]))/(Population-sum(Daily_infection_2[0:x])) #change scaling factor into scaling factor[x]
        R_Ori.append(const)
    return R_Ori

def _synthetic_infections_Adaptive(seed, r_ts,serial_UIUC_U,total_I_No_T,total_I_now,Total_pop, Multiplier,Rt_updated):
    assert len(seed) == len(serial_UIUC_U)
    generated_incidence = seed[:]
    total_I_No_T_U=total_I_No_T-sum(generated_incidence)
    for r in r_ts:
        r_scale = r/Multiplier*(Total_pop-(total_I_No_T_U+sum(generated_incidence)))/(Total_pop-total_I_now)
        Rt_updated = np.append (Rt_updated,r_scale)
        #print(Rt_updated)
        #r= r/Multiplier*(Total_pop-(total_I_No_T+sum(generated_incidence)))/(Total_pop-total_I_now)
        mu =r_scale * sum(p * i for i, p in zip(serial_UIUC_U[1:], generated_incidence[::-1]))
        #print(r_scale)
        #print(total_I_No_T_U+sum(generated_incidence))
        generated_incidence.append(
            poisson(mu=mu).rvs()
        )
    return pd.Series(generated_incidence[len(seed):], index=r_ts.index),Rt_updated[:]
