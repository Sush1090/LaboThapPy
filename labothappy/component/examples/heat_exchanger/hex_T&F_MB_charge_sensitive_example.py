"""
Supplemental code for paper:
I. Bell et al., "A Generalized Moving-Boundary Algorithm to Predict the Heat Transfer Rate of 
Counterflow Heat Exchangers for any Phase Configuration", Applied Thermal Engineering, 2014
"""

"""
Modification w/r to previous version:
    - Putting some order in the Objective Function "for" loops. Sparing some
    lines of code.
    - x_di_c correct calculation.
"""

# from __future__ import division, print_function
import __init__
from component.heat_exchanger.hex_MB_charge_sensitive import HeatExchangerMB
from toolbox.geometries.heat_exchanger.geometry_tube_and_fins_hx import TubeAndFinsGeom

#%%

import time
start_time = time.time()   

"--------- Tube and Fins HTX ------------------------------------------------------------------------------------------"

"HTX Instanciation"

HX = HeatExchangerMB('Tube&Fins')

# "Setting inputs"

# -------------------------------------------------------------------------------------------------------------

# # DECAGONE Recuperator HTX case

HX.set_inputs(
    # First fluid
    Hsu_fluid = 'Cyclopentane',
    Hsu_T = 133.8 + 273.15, # K
    Hsu_p = 0.9*1e5, # Pa
    Hsu_m_dot = 13.8, # kg/s

    # Second fluid
    Csu_fluid = 'Cyclopentane',
    Csu_T = 35.1 + 273.15, # K
    Csu_p = 31.5*1e5, # Pa
    Csu_m_dot = 13.8, # kg/s  # Make sure to include fluid information
)

"Geometry Loading"

HX_geom = TubeAndFinsGeom()
HX_geom.set_parameters("DECAGONE_RECUP") 

Fin_Side = 'H'

"Correlation Loading"

# Corr_H = {"1P" : "Tube_And_Fins", "2P" : "ext_tube_film_condens"}
Corr_H = {"1P" : "Tube_And_Fins", "2P" : "Tube_And_Fins"}
Corr_C = {"1P" : "Gnielinski", "2P" : "Boiling_curve"}

# -------------------------------------------------------------------------------------------------------------

# # DECAGONE ACC HTX case

# HX.set_inputs(
#     # First fluid
#     Hsu_fluid = 'Cyclopentane',
#     Hsu_T = 53.6 + 273.15, # K
#     Hsu_p = 0.7*1e5, # Pa
#     Hsu_m_dot = 13.8/2, # kg/s

#     # Second fluid
#     Csu_fluid = 'Air',
#     Csu_T = 12 + 273.15, # K
#     Csu_p = 1.05*1e5, # Pa
#     Csu_m_dot = 158.5, # kg/s  # Make sure to include fluid information
# )

# "Geometry Loading"

# HX_geom = TubeAndFinsGeom()
# HX_geom.set_parameters("DECAGONE_ACC") 

# Fin_Side = 'C'

# "Correlation Loading"

# Corr_H = {"1P" : "Gnielinski", "2P" : "Horizontal_Tube_Internal_Condensation"}
# Corr_C = {"1P" : "Tube_And_Fins", "2P" : "Boiling_curve"}

# -------------------------------------------------------------------------------------------------------------

"Parameters Setting"

HX.set_parameters(
    A_finned = HX_geom.A_finned, A_flow = HX_geom.A_flow, A_in_tot = HX_geom.A_in_tot, A_out_tot = HX_geom.A_out_tot, A_unfinned = HX_geom.A_unfinned, # 5
    B_V_tot = HX_geom.B_V_tot, Fin_OD = HX_geom.Fin_OD, Fin_per_m = HX_geom.Fin_per_m, Fin_t = HX_geom.Fin_t, Fin_type = HX_geom.Fin_type, # 10
    Finned_tube_flag = HX_geom.Tube_t, L = HX_geom.L, T_V_tot = HX_geom.T_V_tot, Tube_L = HX_geom.Tube_L, Tube_OD = HX_geom.Tube_OD, # 15
    Tube_cond = HX_geom.Tube_cond, Tube_t = HX_geom.Tube_t, fouling = HX_geom.fouling, h = HX_geom.h, k_fin = HX_geom.k_fin, # 20
    Tube_pass = HX_geom.Tube_pass, n_rows = HX_geom.n_rows, n_series = HX_geom.n_series, n_tubes = HX_geom.n_tubes, pitch = HX_geom.pitch, # 25
    pitch_H = HX_geom.pitch, pitch_V = HX_geom.pitch, pitch_ratio = HX_geom.pitch_ratio, tube_arrang = HX_geom.tube_arrang, w = HX_geom.w, # 30

    Fin_Side = Fin_Side, # 28

    Flow_Type = 'CrossFlow', H_DP_ON = True, C_DP_ON = True, n_disc = 50) # 32

# Shell&Tube

# UD_H_HTC = {'Liquid':100,
#             'Vapor' : 100,
#             'Two-Phase' : 1000,
#             'Vapor-wet' : 100,
#             'Dryout' : 1000,
#             'Transcritical' : 200}

# UD_C_HTC = {'Liquid':100,
#             'Vapor' : 100,
#             'Two-Phase' : 1000,
#             'Vapor-wet' : 100,
#             'Dryout' : 10000,
#             'Transcritical' : 200}

# HX.set_HTC(htc_type = 'User-Defined', UD_H_HTC = UD_H_HTC, UD_C_HTC = UD_C_HTC) # 'User-Defined' or 'Correlation'
HX.set_htc(htc_type = 'Correlation', Corr_H = Corr_H, Corr_C = Corr_C) # 'User-Defined' or 'Correlation' # 33
HX.set_DP(DP_type="User-Defined", UD_H_DP = 5*1e3, UD_C_DP = 10*1e3)
# HX.set_DP()

"Solve the component"
HX.solve()
