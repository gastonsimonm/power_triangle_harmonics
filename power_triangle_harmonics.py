import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import TextBox

def update_plot(P1_mag, cos_fi, D_mag, ax):
    # We only clear the previous lines, but keep the chart and legend.
    for line in ax.collections + ax.lines:
        line.remove()

    # We check that the entered values are valid.
    if P1_mag <= 0 or D_mag < 0 or not (0 < cos_fi < 1):
        raise ValueError("Values out of range. P1 must be greater than 0, D must be greater than or equal to 0, and cos(fi) between 0 and 1.")
    
    # Necessary calculations.
    fi = np.arccos(cos_fi)
    Q1_mag = P1_mag * np.tan(fi)
    S1_mag = np.sqrt(P1_mag**2 + Q1_mag**2)
    
    if D_mag == 0:
        S2_mag = 0
        Q2_mag = 0
        theta = 0
    else:
        S2_mag = np.sqrt(S1_mag**2 + D_mag**2)
        Q2_mag = np.sqrt(Q1_mag**2 + D_mag**2)
        theta = np.arccos(P1_mag / S2_mag)
    
    # Coordinates for the vectors.
    P = np.array([P1_mag, 0, 0])
    Q1 = np.array([0, Q1_mag, 0])
    S1 = P + Q1
    D = np.array([0, 0, D_mag])
    S2 = S1 + D
    Q2 = S2 - P
    
    # Add the vectors to the chart.
    ax.quiver(0, 0, 0, P[0], P[1], P[2], color='r', label='P', arrow_length_ratio=0.12)
    ax.quiver(P[0], P[1], P[2], Q1[0], Q1[1], Q1[2], color='maroon', label='Q1', arrow_length_ratio=0.12)
    ax.quiver(0, 0, 0, S1[0], S1[1], S1[2], color='g', label='S1', arrow_length_ratio=0.12)
    
    if D_mag > 0:
        ax.quiver(S1[0], S1[1], S1[2], D[0], D[1], D[2], color='orange', label='D', arrow_length_ratio=0.12)
        ax.quiver(P[0], P[1], P[2], Q2[0], Q2[1], Q2[2], color='purple', label='Q2', arrow_length_ratio=0.12)
        ax.quiver(0, 0, 0, S2[0], S2[1], S2[2], color='b', label='S2', arrow_length_ratio=0.12)
    
    # Axis adjustments.
    max_lim = max(P1_mag, D_mag) * 2
    ax.set_xlim([0, max_lim])
    ax.set_ylim([0, max_lim])
    ax.set_zlim([0, max_lim])
    
    ax.set_xlabel('Active Power (kW)')
    ax.set_ylabel('Reactive Power (kVAr)')
    ax.set_zlabel('Harmonic Distortion')
    
    ax.set_title("Power Triangle With Harmonics")
    
    # We ensure the legend remains present.
    if not ax.get_legend():
        ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

    # We update the text box with the calculated values.
    update_text_box(P1_mag, cos_fi, D_mag, S1_mag, Q1_mag, S2_mag, Q2_mag, fi, theta)

def update_text_box(P1_mag, cos_fi, D_mag, S1_mag, Q1_mag, S2_mag, Q2_mag, fi, theta):
    if D_mag == 0:
        text_box.set_val(f" • Apparent Power (S1): {S1_mag:.2f} kVA\n\n"
                         f" • Reactive Power (Q1): {Q1_mag:.2f} kVAr\n\n"
                         f" • Active Power (P): {P1_mag:.2f} kW\n\n"
                         f" • Cos(φ): {cos_fi:.2f}\n\n"
                         f" • Angle φ: {np.degrees(fi):.2f}°\n\n"
                         f" • Harmonic Distortion (D): {D_mag:.2f} kVAr\n\n"
                         f" • Apparent Power (S2): 0 kVA\n\n"
                         f" • Reactive Power (Q2): 0 kVAr\n\n"
                         f" • Power Factor: 0\n\n"
                         f" • Angle θ: 0°")
    else:
        text_box.set_val(f" • Apparent Power (S1): {S1_mag:.2f} kVA\n\n"
                         f" • Reactive Power (Q1): {Q1_mag:.2f} kVAr\n\n"
                         f" • Active Power (P): {P1_mag:.2f} kW\n\n"
                         f" • Cos(φ): {cos_fi:.2f}\n\n"
                         f" • Angle φ: {np.degrees(fi):.2f}°\n\n"
                         f" • Harmonic Distortion (D): {D_mag:.2f} kVAr\n\n"
                         f" • Apparent Power (S2): {S2_mag:.2f} kVA\n\n"
                         f" • Reactive Power (Q2): {Q2_mag:.2f} kVAr\n\n"
                         f" • Power Factor: {P1_mag/S2_mag:.2f}\n\n"
                         f" • Angle θ: {np.degrees(theta):.2f}°")

# The rest of the code remains the same.
def submit(text, ax, fig, input_type):
    try:
        value = float(text)
        if input_type == 'P1':
            P1_mag = value
            cos_fi = float(textboxes[1].text)
            D_mag = float(textboxes[2].text)
        elif input_type == 'cos_fi':
            cos_fi = value
            P1_mag = float(textboxes[0].text)
            D_mag = float(textboxes[2].text)
        elif input_type == 'D':
            D_mag = value
            P1_mag = float(textboxes[0].text)
            cos_fi = float(textboxes[1].text)
        
        # We update the chart with the new values.
        update_plot(P1_mag, cos_fi, D_mag, ax)
        fig.canvas.draw()
        
    except ValueError as e:
        print(f"Error: {e}")

# Create the figure and set up the subplot layout.
fig = plt.figure(figsize=(12, 7))
fig.canvas.manager.set_window_title('POWER TRIANGLE SIMULATION WITH HARMONICS - GSM')
plt.subplots_adjust(left=0.3, right=0.9, bottom=0, top=0.925)
ax = fig.add_subplot(111, projection='3d')

# Create text boxes for the input values.
axbox1 = plt.axes([0.13, 0.85, 0.23, 0.05])
text_box_P1 = TextBox(axbox1, 'Active Power (P):', initial="1")
text_box_P1.on_submit(lambda text: submit(text, ax, fig, 'P1'))

axbox2 = plt.axes([0.13, 0.75, 0.23, 0.05])
text_box_cos_fi = TextBox(axbox2, 'Cos(φ):', initial="0.8")
text_box_cos_fi.on_submit(lambda text: submit(text, ax, fig, 'cos_fi'))

axbox3 = plt.axes([0.13, 0.65, 0.23, 0.05])
text_box_D = TextBox(axbox3, 'Harmonic Distortion (D):', initial="1")
text_box_D.on_submit(lambda text: submit(text, ax, fig, 'D'))

# Create a text box to display the calculated values.
axbox4 = plt.axes([0.13, 0.05, 0.23, 0.55])
text_box = TextBox(axbox4, '', initial='')
text_box.set_active(False)

# Save the text boxes for reuse.
textboxes = [text_box_P1, text_box_cos_fi, text_box_D]

# Initialize the chart with default values.
update_plot(1, 0.8, 1, ax)

plt.show()