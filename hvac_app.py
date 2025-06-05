
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the Excel file
file_path = 'Form_source_20250605.xlsx'
df = pd.read_excel(file_path, header=5)

# Sidebar for selecting the quarter
quarter = st.sidebar.selectbox('Select Quarter', df['Quarter'].unique())

# Filter data based on selected quarter
filtered_df = df[df['Quarter'] == quarter]

# Display the parameters and their meanings
st.write("### Parameters and their meanings")
st.write("""
- **Column 4**: Image 1
- **Column 6**: Image 2
- **Column 10**: Unit size quantity (RRG)
- **Column 11**: Unit size quantity (HEX)
- **Column 35**: Min air performance
- **Column 37**: Max air performance
- **Column 44-63**: Internal cross-section coordinates
- **Column 67-76**: Duct connection coordinates
- **Column 77**: Diameter (if numeric value present)
""")

# Display the data
st.write("### Data for selected quarter")
st.dataframe(filtered_df)

# Display images from columns 4 and 6
st.write("### Images")
for index, row in filtered_df.iterrows():
    image1 = row[3]  # Column 4
    image2 = row[5]  # Column 6
    if os.path.exists(f'images/{image1}'):
        st.image(f'images/{image1}', caption=image1)
    if os.path.exists(f'images/{image2}'):
        st.image(f'images/{image2}', caption=image2)

# Display Unit size quantity based on Recovery type
st.write("### Unit size quantity")
for index, row in filtered_df.iterrows():
    recovery_type = row[8]  # Column 'Recovery type'
    if recovery_type == 'RRG':
        st.write(f"Unit size quantity (RRG): {row[9]}")  # Column 10
    elif recovery_type == 'HEX':
        st.write(f"Unit size quantity (HEX): {row[10]}")  # Column 11

# Generate air performance plot
st.write("### Air performance plot")
for index, row in filtered_df.iterrows():
    min_air_performance = row[34]  # Column 35
    max_air_performance = row[36]  # Column 37
    plt.plot([min_air_performance, max_air_performance], [1, 1], marker='o')
plt.xlabel('Air Performance')
plt.ylabel('Value')
st.pyplot(plt)

# Generate internal cross-section plot
st.write("### Internal cross-section plot")
for index, row in filtered_df.iterrows():
    x_coords = row[43:63:2]  # Columns 44, 46, 48, ..., 62
    y_coords = row[44:64:2]  # Columns 45, 47, 49, ..., 63
    plt.plot(x_coords, y_coords, marker='o')
plt.xlabel('X Coordinates')
plt.ylabel('Y Coordinates')
st.pyplot(plt)

# Generate duct connection plot
st.write("### Duct connection plot")
for index, row in filtered_df.iterrows():
    if pd.notna(row[76]):  # Column 77
        diameter = row[76]
        circle = plt.Circle((0, 0), diameter / 2, color='blue', fill=False)
        plt.gca().add_patch(circle)
    else:
        x_coords = row[66:76:2]  # Columns 67, 69, 71, ..., 75
        y_coords = row[67:77:2]  # Columns 68, 70, 72, ..., 76
        plt.plot(x_coords, y_coords, marker='o')
plt.xlabel('X Coordinates')
plt.ylabel('Y Coordinates')
st.pyplot(plt)
