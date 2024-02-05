import matplotlib.pyplot as plt
import numpy as np

# Chargement du filtre prototype

h = np.loadtxt('prototypeFilter2.txt')
h = h.reshape(-1, 1)  # Transposition du filtre
L = len(h)

# Tracé du filtre prototype

plt.figure()
plt.subplot(2, 1, 1)
plt.stem(np.arange(0, L), h.flatten())
plt.title('Réponse impulsionnelle du filtre passe-bas prototype')

# Tracé de la réponse en fréquence

plt.subplot(2, 1, 2)
magnitude = np.abs(np.fft.fftshift(np.fft.fft(h.flatten(), 4 * L)))
magnitude_log = 20 * np.log10(np.maximum(magnitude, 1e-10))
freq_axis = np.linspace(-0.5, 0.5, len(magnitude_log))
plt.plot(freq_axis, magnitude_log)
plt.title('Réponse en fréquence du filtre passe-bas prototype')
plt.xlabel('Fréquence normalisée')

plt.tight_layout()
plt.show()

# Création de la banque de filtres d'analyse
numbands = 32
def analysis_filter(k, R):
    return R * np.cos(((2 * k + 1) * np.pi * (np.arange(L) - 16)) / (2 * numbands))
plt.figure()
for k in range(numbands):
    plt.plot(
        np.linspace(-1, 1, 4 * L),
        20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(analysis_filter(k, h.flatten()), 4 * L))))
    )
plt.title('BANQUE DE FILTRES D ANALYSE')
plt.show()

# Création de la banque de filtres de synthèse
hhs = np.zeros((numbands, L))
for k in range(1, numbands):
    hhs[k, :] = h.flatten() * np.cos(((2 * k + 1) * np.pi * (np.arange(L) + 16)) / (2 * numbands))

# Génération du signal d'entrée
N = 2 * 1024
wav_in = np.sin(0.05 * np.pi * np.arange(0, N))

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(wav_in)
plt.title('Signal d entrée')
plt.subplot(2, 1, 2)
plt.plot(np.linspace(-1, 1, 4 * N), 20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(wav_in, 4 * N)))))
plt.show()
yyd = np.zeros((numbands, int(np.floor(N / numbands))))
yyu = np.zeros((numbands, N))

for k in range(0, numbands):
    temp = np.convolve(wav_in, analysis_filter(k, h.flatten()))
    yyu[k, :] = temp[L // 2:L // 2 + N]
    yyd[k, :] = yyu[k, 1:N + 1:numbands]

ys = np.zeros(N)
yi = np.zeros(N)

for k in range(0, numbands):
    yi[1:N + 1:numbands] = yyd[k, :]
    temp = np.convolve(yi, hhs[k, :], mode='same')
    print(f"Intermediate result for band {k}: {temp}")
    ys = ys + temp

ys = numbands * ys

# Tracé du signal synthétisé
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(ys)
plt.title('Signal synthétisé')
plt.subplot(2, 1, 2)
plt.plot(np.linspace(-1, 1, 4 * N), 20 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(ys, 4 * N)))))
plt.show()
