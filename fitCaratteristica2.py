from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("datiCaratteristicaSilicio1.csv", delimiter=",", names=True)

x  = data["V"]
y  = data["I"]
sx = data["errV"]
sy = data["errI"]


def pippo(x, iconzero, etavuti):
    return iconzero * (np.exp(x / etavuti) - 1.0)

p0 = (1.0, 60.0)


popt, pcov = curve_fit(pippo, x, y, p0=p0, maxfev=10000)

iconzero_fit, etavuti_fit = popt
perr = np.sqrt(np.diag(pcov))

print("Risultati del fit:")
print(f"iconzero = {iconzero_fit:.6g} +/- {perr[0]:.6g}")
print(f"etavuti  = {etavuti_fit:.6g} +/- {perr[1]:.6g}")


y_fit     = pippo(x, *popt)
residuals = y - y_fit

chi2 = np.sum(residuals**2)
ndof = len(y) - len(popt)
chi2_red = chi2 / ndof

print(f"chi^2        = {chi2:.6g}")
print(f"chi^2 ridotto = {chi2_red:.6g} (con sigma_I = 1 in unità di I)")


x_fit = np.linspace(np.min(x), np.max(x), 500)
y_fit_smooth = pippo(x_fit, *popt)


plt.figure(figsize=(8, 5))
plt.errorbar(x, y, xerr=sx, yerr=sy, fmt='o', label="Dati")
plt.plot(x_fit, y_fit_smooth, label="Fit")
plt.xlabel("V [V]")
plt.ylabel("I [A]")
plt.legend()
plt.grid(True)
plt.title("Caratteristica I-V del diodo (scala lineare)")


mask_pos = y > 0
x_pos  = x[mask_pos]
y_pos  = y[mask_pos]
sx_pos = sx[mask_pos]
sy_pos = sy[mask_pos]

y_fit_pos = pippo(x_fit, *popt)
mask_fit_pos = y_fit_pos > 0
x_fit_pos  = x_fit[mask_fit_pos]
y_fit_pos  = y_fit_pos[mask_fit_pos]

plt.figure(figsize=(8, 5))
plt.errorbar(x_pos, y_pos, xerr=sx_pos, yerr=sy_pos, fmt='o', label="Dati (I>0)")
plt.plot(x_fit_pos, y_fit_pos, label="Fit")
plt.yscale("log")
plt.xlabel("V [V]")
plt.ylabel("I [A] (scala log)")
plt.legend()
plt.grid(True, which="both", ls=":")
plt.title("Caratteristica I-V del diodo (scala semi-log)")

plt.show()
