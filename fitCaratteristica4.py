import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData

# -----------------------------------------------------------
# 1) Definizione della funzione modello
# -----------------------------------------------------------

def diode_eq(beta, V):
    iconzero, etavuti = beta
    return iconzero * (np.exp(V / etavuti) - 1.0)

model = Model(diode_eq)

# -----------------------------------------------------------
# 2) Dati
# -----------------------------------------------------------

V = np.array([20,40,60,80,100,112,124,132,140,150,160,170,180,190,200,
              210,220,230,250,270,290,310], dtype=float)

errV = np.array([4,4,4,4,4,4,4,4,4,10,10,10,10,10,10,10,10,10,10,10,10,10], dtype=float)

I = np.array([0,0,1,2,3,4,5,6,7,8,10,13,16,19,23,28,33,39,55,78,108,148], dtype=float)

errI = np.array([3,3,3.015,3.03,3.045,3.06,3.075,3.09,3.105,3.12,3.15,
                 3.195,3.24,3.285,3.345,3.42,3.495,3.585,3.825,4.17,4.62,5.22],
                dtype=float)

# -----------------------------------------------------------
# 3) Setup dei dati per ODR (x e y entrambi con errori)
# -----------------------------------------------------------

data = RealData(V, I, sx=errV, sy=errI)

# -----------------------------------------------------------
# 4) Fit ODR
# -----------------------------------------------------------

beta0 = [1e-3, 30]  # guess iniziale

odr = ODR(data, model, beta0=beta0)
output = odr.run()

iconzero_fit, etavuti_fit = output.beta
err_iconzero, err_etavuti = output.sd_beta

print("\nRisultati del fit ODR con errori su V e I:")
print(f"iconzero  = {iconzero_fit:.6g} ± {err_iconzero:.6g}")
print(f"etavuti   = {etavuti_fit:.6g} ± {err_etavuti:.6g}")

# -----------------------------------------------------------
# 5) Grafico
# -----------------------------------------------------------

Vfit = np.linspace(min(V), max(V), 500)
Ifit = diode_eq([iconzero_fit, etavuti_fit], Vfit)

plt.errorbar(V, I, xerr=errV, yerr=errI, fmt='o', capsize=4, label="Dati")
plt.plot(Vfit, Ifit, label="Fit ODR")
plt.xlabel("V")
plt.ylabel("I")
plt.legend()
plt.grid(True)
plt.show()
