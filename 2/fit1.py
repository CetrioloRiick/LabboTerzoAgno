import matplotlib.pyplot as plt
import numpy as np
from scipy import odr

# =========================
# Lettura dati
# =========================
data = np.genfromtxt("2/data1.csv", delimiter=",", names=True)

all_V = data["V"]          # V_CE [V]
all_I = data["I"]          # I_C [A]
all_sV = data["errV"]      # errore su V [V]
all_sI = data["errI"]      # errore su I [A]

# Selezione regione lineare
V = all_V[1:-10]
I = all_I[1:-10]
sV = all_sV[1:-10]
sI = all_sI[1:-10]

# =========================
# Modello lineare INVERSO: V(I)
# =========================
def retta_inversa(B, I):
    return B[0] * I + B[1]   # B[0]=a, B[1]=b

model = odr.Model(retta_inversa)

# Ora:
# x = I
# y = V
# sx = errore su I
# sy = errore su V
data_odr = odr.RealData(I, V, sx=sI, sy=sV)

odr_fit = odr.ODR(data_odr, model, beta0=[1.0, 0.0])
output = odr_fit.run()

a, b = output.beta
da, db = output.sd_beta

chi2 = output.sum_square
ndof = len(V) - len(output.beta)
chi2_red = chi2 / ndof

print(f"b = {a:.3e} ± {da:.3e} V/A")
print(f"a = {b:.3e} ± {db:.3e} V")
print(f"chi^2 ridotto = {chi2_red:.2f}")

# =========================
# Inversione analitica per il grafico: I(V)
# =========================
V_fit = np.linspace(min(V), max(V), 300)
I_fit = (V_fit - b) / a

# =========================
# Grafico (INVARIATO)
# =========================
plt.figure(figsize=(8, 6), dpi=120)

plt.errorbar(
    all_V,
    all_I * 1e3,
    xerr=all_sV,
    yerr=all_sI * 1e3,
    fmt='o',
    markersize=4,
    capsize=3,
    label='Dati sperimentali'
)

plt.plot(
    V_fit,
    I_fit * 1e3,
    color='red',
    linewidth=2,
    label=(
        f'Fit lineare (da V(I))\n'
        f'b = ({a:.3e} ± {da:.3e}) V/A\n'
        f'a = ({b:.3e} ± {db:.3e}) V'
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
#plt.show()
plt.savefig("2/Grafico1.pdf")
