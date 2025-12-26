import matplotlib.pyplot as plt
import numpy as np
from scipy import odr

# =========================
# Lettura dati
# =========================
data = np.genfromtxt("2/data3.csv", delimiter=",", names=True)

all_x = data["V"]          # V_CE [V]
all_y = data["I"]          # I_C [A]
all_sx = data["errV"]      # errore su V [V]
all_sy = data["errI"]      # errore su I [A]

# Selezione regione lineare
x = all_x[:-10]
y = all_y[:-10]
sx = all_sx[:-10]
sy = all_sy[:-10]

# =========================
# Modello lineare
# =========================
def retta(B, x):
    return B[0] * x + B[1]   # B[0]=m, B[1]=q

model = odr.Model(retta)
data_odr = odr.RealData(x, y, sx=sx, sy=sy)

odr_fit = odr.ODR(data_odr, model, beta0=[1.0, 0.0])
output = odr_fit.run()

m, q = output.beta
dm, dq = output.sd_beta

chi2 = output.sum_square
ndof = len(x) - len(output.beta)
chi2_red = chi2 / ndof

print(f"m = {m:.3e} ± {dm:.3e} A/V")
print(f"q = {q:.3e} ± {dq:.3e} A")
print(f"chi^2 ridotto = {chi2_red:.2f}")

# =========================
# Fit
# =========================
x_fit = np.linspace(min(x), max(x), 300)
y_fit = m * x_fit + q

# =========================
# Grafico
# =========================
plt.figure(figsize=(8, 6), dpi=120)

# Conversione corrente in mA
plt.errorbar(
    all_x,
    all_y * 1e3,
    xerr=all_sx,
    yerr=all_sy * 1e3,
    fmt='o',
    markersize=4,
    capsize=3,
    label='Dati sperimentali'
)

plt.plot(
    x_fit,
    y_fit * 1e3,
    color='red',
    linewidth=2,
    label=(
        f'Fit lineare\n'
        f'm = ({m*1e3:.3f} ± {dm*1e3:.3f}) mA/V\n'
        f'q = ({q*1e3:.3f} ± {dq*1e3:.3f}) mA'
    )
)

plt.xlabel(r'$V_{CE}$ [V]', fontsize=12)
plt.ylabel(r'$I_C$ [$\times 10^{-3}$ A]', fontsize=12)

plt.title(
    'Caratteristica di uscita BJT PNP\n'
    'Configurazione a emettitore comune',
    fontsize=13
)

plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()
