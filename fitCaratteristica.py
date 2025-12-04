from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("datiCaratteristicaSilicio.csv", delimiter=",", names=True)

x = data["V"]
y = data["I"]
sx = data["errV"]
sy = data["errI"]   # qui sono tutti 0: NON usarli come sigma

def pippo(x, iconzero, etavuti):
    return iconzero * (np.exp(x / etavuti) - 1)

# stima iniziale decente per l'esponenziale
p0 = (1.0, 60.0)  # iconzero ~ 1, etavuti ~ 60 V (ordine di grandezza)

popt, pcov = curve_fit(pippo, x, y, p0=p0, maxfev=10000)

iconzero_fit, etavuti_fit = popt
perr = np.sqrt(np.diag(pcov))

print("iconzero =", iconzero_fit, "+/-", perr[0])
print("etavuti  =", etavuti_fit,  "+/-", perr[1])

# plot
x_fit = np.linspace(min(x), max(x), 500)
y_fit = pippo(x_fit, *popt)

plt.errorbar(x, y, xerr=sx, yerr=None, fmt='o', label="dati")
plt.plot(x_fit, y_fit, label="fit")
plt.xlabel("V")
plt.ylabel("I")
plt.legend()
plt.grid(True)
plt.show()
