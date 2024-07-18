import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def symmetric_gaussian(x, amplitude, center, sigma):
    return amplitude * np.exp(-(x - center) ** 2 / (2 * sigma ** 2))


def asymmetric_gaussian(x, amplitude, center, sigma_left, sigma_right):
    y = np.zeros_like(x)
    mask = x <= center
    y[mask] = amplitude * np.exp(-(x[mask] - center) ** 2 / (2 * sigma_left ** 2))
    y[~mask] = amplitude * np.exp(-(x[~mask] - center) ** 2 / (2 * sigma_right ** 2))
    return y


def generate_spectrum(wave_nm, peaks, peak_function):
    spectrum = np.zeros_like(wave_nm)
    for peak in peaks:
        spectrum += peak_function(wave_nm, *peak)
    return spectrum


def save_spectrum(wave_nm, spectrum, filename):
    df = pd.DataFrame({'wave_nm': wave_nm, 'int': spectrum})
    df.to_csv(filename, index=False, sep=" ")
    print(f"Data has been saved to '{filename}'")


def plot_spectrum(wave_nm, spectrum, title):
    plt.figure(figsize=(10, 6))
    plt.plot(wave_nm, spectrum)
    plt.xlabel('wave_nm')
    plt.ylabel('int')
    plt.title(title)
    plt.grid(True)
    plt.show()


# Set up the wavelength range
wave_nm = np.linspace(200, 800, 1000)

# Define symmetric peak parameters: (amplitude, center, sigma)
symmetric_peaks = [
    (1.0, 300, 5),
    (0.8, 450, 8),
    (1.2, 550, 6),
    (0.6, 700, 10)
]

# Define asymmetric peak parameters: (amplitude, center, sigma_left, sigma_right)
asymmetric_peaks = [
    (1.0, 300, 5, 10),
    (0.8, 450, 8, 15),
    (1.2, 550, 6, 12),
    (0.6, 700, 10, 5)
]

# Generate symmetric spectrum
symmetric_spectrum = generate_spectrum(wave_nm, symmetric_peaks, symmetric_gaussian)
save_spectrum(wave_nm, symmetric_spectrum, 'symmetric_data.csv')
plot_spectrum(wave_nm, symmetric_spectrum, 'Spectrum with Symmetric Gaussian Peaks')

# Generate asymmetric spectrum
asymmetric_spectrum = generate_spectrum(wave_nm, asymmetric_peaks, asymmetric_gaussian)
save_spectrum(wave_nm, asymmetric_spectrum, 'asymmetric_data.csv')
plot_spectrum(wave_nm, asymmetric_spectrum, 'Spectrum with Asymmetric Gaussian Peaks')
