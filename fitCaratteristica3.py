from scipy.odr import ODR, Model, RealData
import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("datiCaratteristicaSilicio1.csv", delimiter=",", names=True)

x  = data["V"]
y  = data["I"]
sx = data["errV"]
sy = data["errI"]

# Modello (stesso del fit originale)
def pippo(B, x):
    iconzero, etavuti = B
    return iconzero * (np.exp(x / etavuti) - 1.0)

model = Model(pippo)

# Dati con errori su x e y
data_odr = RealData(x, y, sx=sx, sy=sy)

# Valori iniziali
beta0 = [1.0, 60.0]

# Impostazione ODR
odr = ODR(data_odr, model, beta0=beta0)
output = odr.run()

iconzero_fit, etavuti_fit = output.beta
perr = output.sd_beta  # incertezze sui parametri

print("Risultati del fit (ODR):")
print(f"iconzero = {iconzero_fit:.6g} +/- {perr[0]:.6g}")
print(f"etavuti  = {etavuti_fit:.6g} +/- {perr[1]:.6g}")

# Calcolo chi2 “effettivo” ODR
chi2 = output.sum_square
ndof = len(x) - len(output.beta)
chi2_red = chi2 / ndof

print(f"chi^2        = {chi2:.6g}")
print(f"chi^2 ridotto = {chi2_red:.6g}")

# Curve smooth
x_fit = np.linspace(np.min(x), np.max(x), 500)
y_fit = pippo(output.beta, x_fit)

# Grafico scala lineare
plt.figure(figsize=(8,5))
plt.errorbar(x, y, xerr=sx, yerr=sy, fmt='o', label="Dati")
plt.plot(x_fit, y_fit, label="Fit ODR")
plt.xlabel("V [V]")
plt.ylabel("I [A]")
plt.legend()
plt.grid(True)
plt.title("Caratteristica I-V con fit ODR (errori su x e y)")

# Grafico semilog
mask_pos = y > 0
x_pos, y_pos = x[mask_pos], y[mask_pos]
sx_pos, sy_pos = sx[mask_pos], sy[mask_pos]

y_fit_all = pippo(output.beta, x_fit)
mask_fit_pos = y_fit_all > 0
x_fit_pos, y_fit_pos = x_fit[mask_fit_pos], y_fit_all[mask_fit_pos]

plt.figure(figsize=(8,5))
plt.errorbar(x_pos, y_pos, xerr=sx_pos, yerr=sy_pos, fmt='o', label="Dati (I>0)")
plt.plot(x_fit_pos, y_fit_pos, label="Fit ODR")
plt.yscale("log")
plt.xlabel("V [V]")
plt.ylabel("I [A] (scala log)")
plt.legend()
plt.grid(True, which="both", ls=":")
plt.title("Caratteristica I-V con ODR (errori su x e y)")

plt.show()
