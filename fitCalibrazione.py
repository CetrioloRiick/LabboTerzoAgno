# Assicurati di avere scipy installato:
# pip install scipy

import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData

# -------------------------
# 1) METTI QUI I TUOI DATI
# -------------------------
# x, y: liste/array delle misure
# sx, sy: errori (incertezze) corrispondenti ad ogni misura

# Legge le colonne dal CSV
data = np.genfromtxt("datiCalibrazione.csv", delimiter=",", names=True)

x  = data["Vo"]
y  = data["Vm"]
sx = data["VoErr"]
sy = data["VmErr"]

# -------------------------
# 2) DEFINISCI IL MODELLO
# SciPy ODR vuole una funzione f(B, x) dove B = [m, q]
# -------------------------
def linear_model(B, x):
    m, q = B
    return m * x + q

model = Model(linear_model)

# -------------------------
# 3) CREA RealData con errori
# -------------------------
data = RealData(x, y, sx=sx, sy=sy)

# -------------------------
# 4) COSTRUISCI ESEGUI L'ODR
# beta0 = stima iniziale [m0, q0] (scegli qualcosa di sensato)
# -------------------------
beta0 = [1.0, 0.0]        # stima iniziale: m=1, q=0
odr = ODR(data, model, beta0=beta0)
out = odr.run()           # esegue il fit

# -------------------------
# 5) PARAMETRI DI FIT E INCOCERTEZZA
# out.beta: [m, q]
# out.sd_beta: errori standard dei parametri (sigma_m, sigma_q)
# out.cov_beta: matrice di covarianza dei parametri
# out.res_var: residual variance (utile come chi^2 ridotto approx)
# -------------------------
m, q = out.beta
sigma_m, sigma_q = out.sd_beta
cov_beta = out.cov_beta
res_var = out.res_var

print(f"m = {m:.6f} ± {sigma_m:.6f}")
print(f"q = {q:.6f} ± {sigma_q:.6f}")
print("Matrice di covarianza dei parametri:\n", cov_beta)
print(f"res_var (residual variance, approx reduced chi2) = {res_var:.6f}")

# -------------------------
# 6) CALCOLO DI CHI^2 RIDOTTO (esplicito, usando distanza ortogonale)
# Per controllo: calcolo la distanza ortogonale di ciascun punto dalla retta
# e valuto il chi^2 usando la varianza proiettata lungo la direzione perpendicolare.
# -------------------------
# distanza ortogonale (algebrica) del punto (x_i,y_i) dalla retta m x + q
dist_perp = (m * x + q - y) / np.sqrt(m**2 + 1)

# varianza della componente ortogonale (propagazione degli errori)
sigma_perp2 = (m*2 * sx + sy) / (m*2 + 1)

chi2 = np.sum(dist_perp**2 / sigma_perp2)
dof = len(x) - 2
chi2_red = chi2 / dof
print(f"chi2 = {chi2:.4f}, dof = {dof}, chi2_red = {chi2_red:.4f}")

# -------------------------
# 7) PLOT (punti + barre d'errore + retta di fit)
# -------------------------
xx = np.linspace(np.min(x) - 0.2, np.max(x) + 0.2, 200)
yy = m * xx + q

plt.figure()
plt.errorbar(x, y, xerr=sx, yerr=sy, fmt='o', capsize=3, label='dati ± errori')
plt.plot(xx, yy, '-', label=f'ODR fit: y={m:.3f}x + {q:.3f}')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Fit lineare con errori in x e y (scipy.odr)')
plt.show()