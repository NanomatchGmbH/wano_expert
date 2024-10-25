#!/usr/bin/env python3

"""
Script that uses WaNo input to write QuantumPatch input.
"""

from os import environ
import yaml

# Reads rendered WaNo file
with open("rendered_wano.yml", "r") as ymlin:
    wano = yaml.safe_load(ymlin)

wano["Molecule Settings"]["Parameter File"] = 'default'
wano["DFT Engine"]["Threads"] = environ["UC_TOTAL_PROCESSORS"]
wano["DFT Engine"]["Memory (MB)"] = float(environ["UC_MEMORY_PER_NODE"]) * 0.85


if wano["Molecule Settings"]["Excited State of Interest"] == 0:
    del wano["DFT Engine"]["Turbomole Settings"]["excited_state_multiplicity"] 


if wano["DFT Engine"]["Turbomole Settings"]["Partial Charge Method"] == "No Charges":
    wano["DFT Engine"]["Turbomole Settings"]["Partial Charge Method"] = "ESP"
    wano["DFT Engine"]["Turbomole Settings"]["partial_charges"] =  False

if wano["DFT Engine"]["Turbomole Settings"]["cosmo"] == True:
    wano["DFT Engine"]["Turbomole Settings"]["cosmo"] = wano["DFT Engine"]["Turbomole Settings"]["Epsilon"]
    del wano["DFT Engine"]["Turbomole Settings"]["Epsilon"]
else:
    del wano["DFT Engine"]["Turbomole Settings"]["Epsilon"]
    del wano["DFT Engine"]["Turbomole Settings"]["cosmo"]

if wano["DFT Engine"]["Turbomole Settings"]["Analysis options"] == "Generate orbital plots":
    wano["DFT Engine"]["Turbomole Settings"]["plot_orb"] = {"homo" :True,"lumo":True}
elif wano["DFT Engine"]["Turbomole Settings"]["Analysis options"] == "Estimate electrostatic disorder":
    wano["DFT Engine"]["Turbomole Settings"]["ESP_surface"] = {'enabled':True, 'mode': "by element", 'vdw_scale': [1.0,2.0,3.5],'points': 30}
elif  wano["DFT Engine"]["Turbomole Settings"]["Analysis options"]  == "Generate ESP surface plot":
    wano["DFT Engine"]["Turbomole Settings"]["ESP_surface"] = {'enabled':True, 'mode': "by element", 'vdw_scale': 1.0,'points': 50,'plot_grid': True}

del wano["DFT Engine"]["Turbomole Settings"]["Analysis options"]


if  wano["DFT Engine"]["Turbomole Settings"]['TD-DFT with TAMM-Dancoff Approximation'] == True:
    del wano["DFT Engine"]["Turbomole Settings"]['TD-DFT with TAMM-Dancoff Approximation']
    wano["DFT Engine"]["Turbomole Settings"]['tda'] = True
else:
    del wano["DFT Engine"]["Turbomole Settings"]['TD-DFT with TAMM-Dancoff Approximation']


if  wano["DFT Engine"]["Turbomole Settings"]['use default range sep values'] == True:
    del wano["DFT Engine"]["Turbomole Settings"]['use default range sep values']
    del wano["DFT Engine"]["Turbomole Settings"]['rangesep']

else:
    del wano["DFT Engine"]["Turbomole Settings"]['use default range sep values']

#if wano["DFT Engine"]["Turbomole Settings"]["Functional"] not in ['wPBE_own','wPBEH_own','CAM-B3LYP_own']:

wano['DFT Engine']['w_fit'] = wano['DFT Engine']["Turbomole Settings"]['w_fit']
wano['DFT Engine']['w_fit']['guess_w']='normal'
del  wano["DFT Engine"]["Turbomole Settings"]['w_fit']

    
report_dict = {}
engine = wano["DFT Engine"]["Engine"] + " Settings"
#method = engine + " Settings"
report_dict["DFT Method"] = wano["DFT Engine"]["Engine"]
#report_dict["Simulation settings"] = wano["DFT Engine"][method]
report_dict["Simulation settings"] = wano["DFT Engine"][engine]
report_dict["Molecule Info"] = wano["Molecule Settings"]



#print(wano["DFT Engine"][wano["DFT Engine"]["Engine"]" Settings"])
with open("parametrizer_settings.yml", "w") as ymlout:
    yaml.safe_dump(wano, ymlout)

#if wano['DFT Engine']['w_fit']["do_w_fit"]:
 #   report_dict["Simulation settings"]["w-tuning"]= True

with open("output_dict.yml", "w") as reportout:
    yaml.safe_dump(report_dict,  reportout)

