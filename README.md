# 🔬 Series LCR Frequency Response Analyzer

A **professional Python-based virtual instrument** to analyze the **frequency response of a Series LCR circuit**.  
This tool is designed for **physics laboratories, teaching, and experimental analysis**, featuring real-time plotting, parameter extraction, and CRO-like interaction.

---

## 🚀 Features

- 📊 Frequency response plotting (I vs f)
- 🔁 Multiple curves on same graph for comparison
- 📈 Logarithmic & Linear scale options
- 🎯 Automatic extraction of:
  - Resonant frequency (f₀)
  - Bandwidth (Δf)
  - Quality factor (Q)
- 🖱️ Cursor readout (f, I) like CRO
- 🔍 Zoom & Pan (embedded toolbar)
- ⚙️ Manual & Auto axis scaling
- 📜 Scrollable control panel

---

## 🧠 Theory

A **Series LCR circuit** consists of:
- Inductor (L)
- Capacitor (C)
- Resistor (R)

When driven by an AC source, the circuit exhibits **resonance**.

### 🔹 Impedance of Series LCR Circuit

$$
Z = \sqrt{R^2 + (\omega L - \frac{1}{\omega C})^2}
$$

Where: $\omega = 2\pi f $

---

### 🔹 Current in the Circuit

$$
I = \frac{V}{Z}
$$

---

### 🔹 Resonant Frequency

At resonance:

$$
\omega_0 L = \frac{1}{\omega_0 C}
$$

$$
f_0 = \frac{1}{2\pi\sqrt{LC}}
$$

---

### 🔹 Bandwidth & Quality Factor

- Half-power condition:
  
$$
I = \frac{I_{max}}{\sqrt{2}}
$$

- Bandwidth:
  
$$
\Delta f = f_H - f_L
$$

- Quality Factor:
  
$$
Q = \frac{f_0}{\Delta f}
$$

---

## ⚡ Experimental Consideration (Important)

In practical setups, a **small test resistor (e.g., 56 Ω)** is added in series to measure voltage/current electronically.

So, total resistance becomes:

$$
R_{total} = R + R_{test}
$$

This affects:
- Peak current
- Bandwidth
- Q-factor

---

## 🔌 Circuit Diagram


## 🖥️ Software Interface

The software acts like a **virtual CRO / network analyzer**:

- Add multiple frequency response curves
- Observe resonance shift with resistance
- Measure bandwidth visually
- Extract Q automatically

---

## 📦 Requirements

Install dependencies:

```bash
pip install numpy matplotlib

