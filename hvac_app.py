
import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Function to load data
def load_data(file_path):
    return pd.read_excel(file_path, engine='openpyxl')

# Function to display images
def display_images(image_paths):
    for image_path in image_paths:
        st.image(image_path, use_column_width=True)

# Function to plot airflow
def plot_airflow(min_airflow, max_airflow):
    plt.figure(figsize=(6, 4))
    plt.plot(['Min Airflow', 'Max Airflow'], [min_airflow, max_airflow], marker='o')
    plt.title('Airflow Performance')
    plt.xlabel('Airflow')
    plt.ylabel('Value')
    st.pyplot(plt)

# Function to plot rectangle
def plot_rectangle(coords):
    plt.figure(figsize=(6, 4))
    plt.plot([coords[0], coords[1]], [coords[2], coords[3]], marker='o')
    plt.title('Internal Section')
    plt.xlabel('X')
    plt.ylabel('Y')
    st.pyplot(plt)

# Function to plot duct connection
def plot_duct(coords, diameter):
    plt.figure(figsize=(6, 4))
    if diameter > 0:
        circle = plt.Circle((coords[0], coords[1]), diameter, color='blue', fill=False)
        plt.gca().add_patch(circle)
    else:
        plt.plot([coords[0], coords[1]], [coords[2], coords[3]], marker='o')
    plt.title('Duct Connection')
    plt.xlabel('X')
    plt.ylabel('Y')
    st.pyplot(plt)

# Main function
def main():
    st.title('HVAC Data Viewer')

    folder_path = st.text_input('Enter the folder path:')
    if folder_path:
        file_path = os.path.join(folder_path, 'Form_source_20250605.xlsx')
        if os.path.exists(file_path):
            data = load_data(file_path)
            quarter = st.selectbox('Select Quarter', ['Q1', 'Q2', 'Q3', 'Q4'])
            st.write(data[quarter])

            recovery_type = data['Recovery type'][0]
            if recovery_type == 'RRG':
                st.write('Unit size quantity:', data['Unit size quantity RRG'][0])
            else:
                st.write('Unit size quantity:', data['Unit size quantity HEX'][0])

            plot_airflow(data['Airflow min'][0], data['Airflow max'][0])
            plot_rectangle([data['Rect coord 1'][0], data['Rect coord 2'][0], data['Rect coord 3'][0], data['Rect coord 4'][0]])
            plot_duct([data['Duct coord 1'][0], data['Duct coord 2'][0], data['Duct coord 3'][0], data['Duct coord 4'][0]], data['Duct diameter'][0])

            image_paths = [os.path.join(folder_path, 'images', f'example_image_{i}.jpg') for i in range(1, 9)]
            display_images(image_paths)
        else:
            st.error('File not found. Please check the folder path.')

if __name__ == '__main__':
    main()
