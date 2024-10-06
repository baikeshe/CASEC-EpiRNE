# CASEC-EpiRNE
# This file serves as supporting information for the work "A Framework for Counterfactual Analysis, Strategy Evaluation, and Control of Epidemics Using Reproduction Number Estimates."

# The file illinois_shield_covid_data_Updated.csv includes the COVID-19 data collected by the SHIELD: Target, Test, Tell committee at the University of Illinois Urbana-Champaign during the early stages of the COVID-19 pandemic.

# The file functions.py includes all functions created to implement the methods in this work.

# The file UIUC_Main.ipynb presents the data and estimates the effective reproduction number for the outbreak at UIUC. It includes an illustration of the three methods presented in the paper:

# 1. Quantifying the isolation rate on the infection profile.
# 2. Reverse engineering the estimated effective reproduction number of the real-world outbreak at UIUC to match the effective # reproduction number of a hypothetical spread with an alternative isolation rate.
# 3. A closed-loop feedback control algorithm to adjust the isolation rate based on the estimated effective reproduction number.
# The file generates all the figures related to UIUC's outbreak in the manuscript.


# The file UIUC_Sensitivity_Analysis.ipynb performs sensitivity analysis on:
# 1. Estimating the effective reproduction number by leveraging the infection data from UIUC.
# 2. Counterfactual analysis of what would have happened in the hypothetical spread without the implemented testing-for-isolation process, assuming the data collected from the real-world outbreak were under different isolation rates.
# The results are shown in the Supporting Information of the main manuscript.
