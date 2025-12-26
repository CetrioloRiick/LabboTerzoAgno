import matplotlib.pyplot as plt
import numpy as np
from scipy import odr

data = np.genfromtxt("2/data1.csv", delimiter=",", names=True)

all_x = data["V"]
all_y = data["I"]
all_sx = data["errV"]
all_sy = data["errI"]

x =  all_x[1:-10]
y =  all_y[1:-10]
sx =  all_sx[1:-10]
sy = all_sy[1:-10]

def retta(B, x):
    return B[0] * x + B[1]   # B[0]=m, B[1]=q

model = odr.Model(retta)
data = odr.RealData(x, y, sx=sx, sy=sy)

odr_fit = odr.ODR(data, model, beta0=[1.0, 0.0])
output = odr_fit.run()

m, q = output.beta
dm, dq = output.sd_beta


chi2 = output.sum_square
ndof = len(x) - len(output.beta)
chi2_red = chi2 / ndof

print(f"m = {m} ± {dm}")
print(f"q = {q} ± {dq}")
print(f"chi^2 = {chi2}")
print(f"gradi di libertà = {ndof}")
print(f"chi^2 ridotto = {chi2_red}")

x_fit = np.linspace(min(x), max(x), 200)
y_fit = m * x_fit + q

plt.errorbar(all_x, all_y, xerr=all_sx, yerr=all_sy, fmt='o', label='Dati')
plt.plot(x_fit, y_fit, label='York fit')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
