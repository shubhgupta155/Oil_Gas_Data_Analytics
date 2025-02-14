import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dynamic pressure profile")

st.sidebar.title("Inputs")

k = st.sidebar.slider("Permeability(mD)", min_value= 10, max_value=200, value = 100)
mu = st.sidebar.slider("Viscosity(cP)", min_value= 1, max_value=50, value = 10)
q = st.sidebar.slider("Flowrate(stbpd)", min_value= 100, max_value=500, value = 200)

re = st.sidebar.number_input("Outer radius of reservoir (ft)", min_value = 1000, max_value = 10000, value= 2500)
rw = st.sidebar.number_input("Outer radius of Well (ft)", min_value = 0.1, max_value = 0.5, value=0.1, step=0.01, format="%.2f")
pe = st.sidebar.number_input("Reservoir pressure", min_value = 1000, max_value = 10000, value= 2000)
B = st.sidebar.number_input("Formation volume factor", min_value = 1.0, max_value = 2.0, step=0.01, format="%.2f", value= 1.1)
h = st.sidebar.number_input("Pay thickness (ft)", min_value = 10, max_value = 100, value= 25)

r= np.linspace(rw,re,1000)
P = pe -((141.2*q*B*mu)*(np.log(re/r))/k/h)

y_min = P[np.where(r==rw)]

b = st.button("Show pressure profile")

if b:

    plt.figure(figsize=(8,6))

    fig,ax = plt.subplots()

    ax.plot(r,P, linewidth=4)
    ax.grid(True)
    ax.axhline(y_min, linewidth = 4, color = "red")

    ax.set_title("Steady state pressure profile")
    ax.set_xlabel("Radius (feet)")
    ax.set_ylabel("Pressure at radius r, (psi)")
    ax.set_ylim(0,5000)
    ax.set_xlim(0,re)

    st.pyplot(fig)

    
df = pd.DataFrame({"Radius (ft)": r, "Pressure (psi)": P})
        
csv = df.to_csv(index=False).encode('utf-8')  # Convert to CSV format

st.download_button(
    label="Download Pressure Profile CSV",
    data=csv,
    file_name="pressure_profile.csv",
    mime="text/csv"
)

