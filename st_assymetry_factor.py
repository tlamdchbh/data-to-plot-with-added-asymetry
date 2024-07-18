import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from scipy.signal import find_peaks, peak_widths

def find_asymmetry(data, peak_prominence, filename, rel_height):
    fig = px.line(data, x="wave_nm", y="int", title=f'Spectra {filename}')
    peaks, properties = find_peaks(data["int"], prominence=peak_prominence)

    asymmetry_factor_list = []
    for i, peak in enumerate(peaks):
        widths, heights, left_ips, right_ips = peak_widths(data["int"], [peak], rel_height=rel_height)

        # Convert interpolated indices to x-axis values
        left_x = np.interp(left_ips[0], range(len(data)), data['wave_nm'])
        right_x = np.interp(right_ips[0], range(len(data)), data['wave_nm'])
        peak_x = data['wave_nm'].iloc[peak]

        # Calculate asymmetry factor
        asymmetry_factor = (right_x - peak_x) / (peak_x - left_x)

        asymmetry_factor_list.append(asymmetry_factor)
        # print(
        #     f"Peak {i + 1}: Left HW = {left_half_width:.2f}, Right HW = {right_half_width:.2f}, Asymmetry Factor = {asymmetry_factor:.3f}")

        # Add annotation to the plot
        fig.add_annotation(x=peak_x, y=data['int'].iloc[peak],
                           text=f'AF: {asymmetry_factor:.3f}',
                           showarrow=True,
                           arrowhead=2)

        # Add vertical lines for peak boundaries
        fig.add_vline(x=left_x, line_dash="dash", line_color="red")
        fig.add_vline(x=right_x, line_dash="dash", line_color="red")

    # fig.write_html(f'spectra_{peak_prominence}_{filename}.html')
    return fig, asymmetry_factor_list

if __name__ == "__main__": 

    st.header('Spectra symmetry factor calculator')
    
    with st.expander("Important", icon="🚨"):
        st.info("! column name: wave_nm and int")
        st.info("! separator is whitespace or tab")
        st.info("! file format txt or csv")
        st.write("https://www.shimadzu.com/an/service-support/technical-support/analysis-basics/basic/theoretical_plate.html")
        formula = r'''
        $$ 
        Symmetry factor =  \frac{right_x - peak_x}{peak_x - left_x} 
        $$ 
        '''
        st.write(formula)
        st.image("img_formula.jpg")
    
    with st.form("input data:"):
        filename = st.file_uploader("Choose a file")
    
        peak_prominence = st.number_input("approx intensity of peaks", value=10_000)
        rel_height = 1 - st.number_input("relative height for symmetry factor", value=0.05)
    
        submitted = st.form_submit_button("Submit")
    
    
    if submitted:
        data: str = pd.read_csv(filename, sep='\s+')
    fig, asymmetry_factor_list = find_asymmetry(data, peak_prominence, filename, rel_height)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("assymetry factors")
    st.dataframe(asymmetry_factor_list)
