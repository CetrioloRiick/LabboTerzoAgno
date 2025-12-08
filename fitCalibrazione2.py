import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData


# --- Modello lineare per ODR ---
def linear_model(B, x):
    m, q = B
    return m * x + q


def odr_linear_fit(x, y, sx, sy, beta0=(1.0, 0.0)):
    """
    Esegue un fit lineare con ODR (errori in x e y).
    Ritorna un dizionario con parametri, incertezze, covarianza e statistiche.
    """
    data = RealData(x, y, sx=sx, sy=sy)
    model = Model(linear_model)
    odr = ODR(data, model, beta0=beta0)

    out = odr.run()

    # Parametri e incertezze
    m, q = out.beta
    sigma_m, sigma_q = out.sd_beta
    cov = out.cov_beta

    # gradi di libertà (N punti - N parametri)
    dof = len(x) - len(out.beta)

    # in scipy.odr: res_var ≈ chi2_red
    chi2_red = out.res_var
    chi2 = chi2_red * dof

    # correlazione m-q
    rho_mq = cov[0, 1] / (sigma_m * sigma_q)

    return {
        "m": m,
        "q": q,
        "sigma_m": sigma_m,
        "sigma_q": sigma_q,
        "cov": cov,
        "rho_mq": rho_mq,
        "chi2": chi2,
        "chi2_red": chi2_red,
        "dof": dof,
        "out": out,
    }


def main():
    # --- Lettura dati ---
    data = np.genfromtxt("datiCalibrazione.csv", delimiter=",", names=True)

    x = data["Vo"]
    y = data["Vm"]
    sx = data["VoErr"]
    sy = data["VmErr"]

    # --- Fit ODR ---
    res = odr_linear_fit(x, y, sx, sy, beta0=(1.0, 0.0))

    m = res["m"]
    q = res["q"]
    sigma_m = res["sigma_m"]
    sigma_q = res["sigma_q"]
    cov = res["cov"]
    rho_mq = res["rho_mq"]
    chi2 = res["chi2"]
    chi2_red = res["chi2_red"]
    dof = res["dof"]

    # --- Stampa risultati ---
    print(f"m = {m:.6f} ± {sigma_m:.6f}")
    print(f"q = {q:.6f} ± {sigma_q:.6f}")
    print("Matrice di covarianza dei parametri:\n", cov)
    print(f"Correlazione m-q: rho = {rho_mq:.4f}")
    print(f"chi2 = {chi2:.4f}, dof = {dof}, chi2_red (odr) = {chi2_red:.4f}")

    # --- Distanze perpendicolari e chi2 geometrico (opzionale) ---
    # distanza ortogonale dei punti dalla retta y = m x + q
    dist_perp = (m * x + q - y) / np.sqrt(m**2 + 1.0)

    # varianza della distanza perpendicolare (errori indipendenti)
    sigma_perp2 = (m**2 * sx**2 + sy**2) / (m**2 + 1.0)

    chi2_geom = np.sum(dist_perp**2 / sigma_perp2)
    chi2_geom_red = chi2_geom / dof
    print(f"chi2_geom (da distanze ⟂) = {chi2_geom:.4f}, chi2_geom_red = {chi2_geom_red:.4f}")

    # --- Retta di fit + banda a 1σ ---
    xx = np.linspace(np.min(x) - 0.2, np.max(x) + 0.2, 200)
    yy = m * xx + q

    # Propagazione errore su y(x) = m x + q
    # Var[y] = (x^2) Var[m] + Var[q] + 2 x Cov[m,q]
    sigma_y = np.sqrt(
        (xx**2) * sigma_m**2
        + sigma_q**2
        + 2 * xx * cov[0, 1]
    )

    # --- Grafico ---
    plt.figure(figsize=(7, 5))

    # dati con barre d'errore
    plt.errorbar(x, y, xerr=sx, yerr=sy, fmt='o', capsize=3, label='Dati ± errori')

    # retta di fit
    plt.plot(xx, yy, '-', label=f'Fit ODR: y = {m:.3f} x + {q:.3f}')

    # banda di confidenza a 1σ
    plt.fill_between(xx, yy - sigma_y, yy + sigma_y, alpha=0.2, label='Banda 1σ')

    plt.xlabel('Vo')
    plt.ylabel('Vm')
    plt.title('Fit lineare con errori in x e y (scipy.odr)')
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
