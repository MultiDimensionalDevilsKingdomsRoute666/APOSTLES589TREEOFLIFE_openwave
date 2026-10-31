"""Row 25 check: the WKB action a neutron lifetime of 878 s implies, Gamma = nu exp(-2 S/hbar), S/hbar = ln(nu tau)/2,
for attempt frequencies from 1e21 /s to the hadronic scale (1 GeV/hbar). The chart's note says 27 to 31 hbar."""
import numpy as np
tau = 878.4; hbar_MeVs = 6.582119569e-22
for nu, lab in ((1e21, '1e21 /s'), (1e22, '1e22 /s'), (139.57/hbar_MeVs, 'm_pi c^2/hbar'), (939.57/hbar_MeVs, 'm_n c^2/hbar'), (1000/hbar_MeVs, '1 GeV/hbar')):
    print(f"nu = {nu:9.3g} /s ({lab:14s}): S/hbar = ln(nu tau)/2 = {np.log(nu*tau)/2:5.1f}")
