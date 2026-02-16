# ising-metropolis-simulation

A high-performance, interactive 2D physics simulation of the **Ising Model** using the **Metropolis-Hastings Algorithm**. Built with Python and Pygame.

## Overview

The Ising Model is a pillar of statistical mechanics used to describe ferromagnetism ( strongest, most common form of magnetism). It consists of variables called **spins**. Each "atom" has a spin value ($+1$ is red in my visualization, Blue is for $-1$) arranged in a grid. This project simulates how local "peer pressure" between atoms leads to the emergence of large-scale magnetic domains.

## The Science & Math

The simulation is governed by two main concepts: **Energy** and **Probability**.

### 1. The Energy Formula (Hamiltonian)
Each atom ($s$) calculates its "comfort level" or energy based on its neighbors and an optional external magnetic field ($H$):

$$E = -s \left( \sum_{i=1}^{n} \text{neighbors}_i + H \right)$$

* **Stable State (Low Energy):** When an atom matches its neighbors, the product is positive, making the energy **negative** (e.g., $-4$). Nature prefers this. Every atom wants to be lazy, so it wants to use as little energy ( a negative value ), always!
* **Unstable State (High Energy):** When an atom disagrees with its neighbors ( atom has a spin of a positive value, and neighbors have a negative one), the product is negative, making the energy **positive**

- I think the simplest way of thinking about this is with this example. We have an atom that has a positive spin, but is surrounded by 8 negative atoms ( left, right, top, bottom, top right, top left... you get it). 

### What made me understand the logic ( and maths )

Take a look at the equation above, we're now subsituting the values.


We have a **Red atom ($s = +1$)** surrounded by **4 Blue neighbors ($s = -1$)** with no external magnetic field ($H = 0$):

#### 1. Calculate Neighbors Sum
The neighbors are Up, Down, Left, and Right:
$$\text{neighbors} = (-1) + (-1) + (-1) + (-1) = -4$$

#### 2. Calculate Energy Change ($\Delta E$)
Using the formula from the code: `dE = 2 * spin * (neighbors + field)`
$$\Delta E = 2 \times (+1) \times (-4 + 0)$$
$$\Delta E = 2 \times (-4)$$
$$\Delta E = -8$$

#### 3. The Decision
Since **$\Delta E = -8$** (which is $\leq 0$), the "Peer Pressure" is so high that the atom will **always** flip to Blue to reach a more stable state.

---

### Example: Fighting the Crowd (High Temperature)

Now, imagine a **Blue atom ($s = -1$)** that is already stable, surrounded by **4 Blue neighbors**:
$$\Delta E = 2 \times (-1) \times (-4 + 0) = +8$$

Normally, this atom would never flip because $\Delta E$ is positive. However, if the **Temperature** is high (e.g., $T = 4.0$):
1. The code calculates $e^{-\Delta E / T} \rightarrow e^{-8 / 4.0} = e^{-2} \approx 0.135$.
2. There is now a **13.5% chance** the atom will flip to Red anyway, simply because of the "Heat."




### 2. The Metropolis Algorithm
To decide whether an atom should flip its spin, we calculate the change in energy ($\Delta E$) that a flip would cause. This is the **Metropolis Criterion**:

1.  **If $\Delta E \leq 0$**: The flip makes the system more stable (going "downhill"). **Always flip.**
2.  **If $\Delta E > 0$**: The flip makes the system less stable ("uphill"). We only flip if the "Thermal Jitter" allows it:
    $$P < e^{-\frac{\Delta E}{T}}$$
    *(Where $P$ is a random number between 0 and 1, and $T$ is the Temperature.)*



## Controls

Run the simulation and use your keyboard to act as a "God" over the atoms:

| Key | Action |
| :--- | :--- |
| **Up Arrow** | Increase **Temperature** (Add chaos/heat) |
| **Down Arrow** | Decrease **Temperature** (Freeze into order) |
| **Right Arrow** | Increase **Magnetic Field** (Bias towards Red) |
| **Left Arrow** | Decrease **Magnetic Field** (Bias towards Blue) |
| **Space** | Reset Magnetic Field to zero |