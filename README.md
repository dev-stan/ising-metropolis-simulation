# ising-metropolis-simulation

[Live Demo](https://dev-stan.github.io/ising-metropolis-simulation/)

An interactive ( and high performance! ) 2D physics simulation of the **Ising Model** using the **Metropolis-Hastings Algorithm**. Built with Python and Pygame. The Ising Model is used to describe **ferromagnetism** (the strongest, most common form of magnetism). 

It consists of variables called **spins**. Each "atom" has a spin value arranged in a grid:
* **Red (+1)**
* **Blue (-1)**

This project simulates how local "peer pressure" between atoms leads to the emergence of large scale magnetic domains.

https://github.com/user-attachments/assets/2ec22536-8919-4608-9926-ba524707185b

Pretty cool right? It's red atoms basically "fighting" the blue ones in a tug of war.

## The Science & Math

The simulation is governed by two main concepts: **Energy** and **Probability**.

### The Energy Formula (Hamiltonian)
Each atom ($s$) calculates its "comfort level" or energy based on its neighbors and an optional external magnetic field ($H$):

$$E = -s \left( \sum_{i=1}^{n} \text{neighbors}_i + H \right)$$

* **Stable State (Low Energy):** When an atom matches its neighbors, the product is positive, making the energy **negative** (e.g., $-4$). Nature prefers this. Every atom wants to be "lazy", it wants to use as little energy as possible!
* **Unstable State (High Energy):** When an atom disagrees with its neighbors (e.g., atom is positive, neighbors are negative), the product is negative, making the energy **positive**

---
### "Peer Pressure" Example

To understand the logic, imagine a **Red atom ($s = +1$)** surrounded by **4 Blue neighbors ($s = -1$)** with no external magnetic field ($H = 0$):

1. **Calculate Neighbors Sum**
    The neighbors (always 4 of them!) are Up, Down, Left, and Right:
    $$\text{neighbors} = (-1) + (-1) + (-1) + (-1) = -4$$

2. **Calculate Energy Change ($\Delta E$)**
    Using the formula from the code: `dE = 2 * spin * (neighbors + field)`
    $$\Delta E = 2 \times (+1) \times (-4 + 0)$$
    $$\Delta E = -8$$

3. **The Decision**
    Since **$\Delta E = -8$** (which is $\leq 0$), the "Peer Pressure" is so high that the atom will **always** flip to Blue to reach a more stable state.

<img width="566" height="391" alt="image" src="https://github.com/user-attachments/assets/0d463875-84b6-470d-96a1-0a64e5b485f2" />

---

### Fighting the Crowd (High Temperature)

Now, imagine a **Blue atom ($s = -1$)** that is already stable, surrounded by **4 Blue neighbors**:
$$\Delta E = 2 \times (-1) \times (-4 + 0) = +8$$

Normally, this atom would never flip because $\Delta E$ is positive. However, if the **Temperature ($T$)** is high (e.g., $T = 4.0$):

1.  The code calculates the probability: $e^{-\Delta E / T} \rightarrow e^{-8 / 4.0} = e^{-2} \approx 0.135$.
2.  There is now a **13.5% chance** the atom will flip to Red anyway, simply because of the "Thermal Heat."

<img width="515" height="349" alt="image" src="https://github.com/user-attachments/assets/ef49b254-50c0-49d5-998c-05483ecb1759" />

---

### The Metropolis Algorithm
To decide whether an atom should flip its spin, we calculate the change in energy ($\Delta E$) that a flip would cause. This is the **Metropolis Criterion**:

1.  **If $\Delta E \leq 0$**: The flip makes the system more stable (going "downhill"). **Always flip.**
2.  **If $\Delta E > 0$**: The flip makes the system less stable ("uphill"). We only flip if the "Thermal Jitter" allows it:
    $$P < e^{-\frac{\Delta E}{T}}$$
    *(Where $P$ is a random number between 0 and 1, and $T$ is the Temperature.)*
```python
if dE <= 0 or random.random() < math.exp(-dE / temp):
    grid[r][c] *= -1 # This flips the spin of the atom
```
---

## Controls

Run the simulation and use your keyboard to act as a "God" over the atoms:

| Key | Action | Effect |
| :--- | :--- | :--- |
| **Up Arrow** | Increase **Temperature** | Adds chaos/heat |
| **Down Arrow** | Decrease **Temperature** | Freezes system into order |
| **Right Arrow** | Increase **Magnetic Field** | Biases system towards **Red** |
| **Left Arrow** | Decrease **Magnetic Field** | Biases system towards **Blue** |
| **Space** | Reset Field | Sets Magnetic Field to zero |

---
