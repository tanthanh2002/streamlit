import streamlit as st
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import time
import random

TIME_STEP = 1

st.set_page_config(layout='wide')

if not os.path.exists("static"):
    os.makedirs("static")

if 'data' not in st.session_state:
    st.session_state.data = defaultdict(list)
if 'count' not in st.session_state:
    st.session_state.count = defaultdict(int)
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'time_step' not in st.session_state:
    st.session_state.time_step = []
if 'index' not in st.session_state:
    st.session_state.index = 0

def reset():
    st.session_state.data = defaultdict(list)
    st.session_state.count = defaultdict(int)
    st.session_state.is_running = False
    st.session_state.time_step = []
    st.session_state.index = 0

class FakeModel:
    def predict(self, frame):
        val = np.random.randint(0, 5)
        accuracy = random.uniform(0.95, 1.0)

        if val == 5:
            raise ValueError("Model error")
        
        return (val, accuracy)

model = FakeModel()


# col1, col2 = st.columns([1, 2])

# col1
st.title("Sample Data")

# get all folder in uploads
folders_name = os.listdir("static")

col1_1,col1_2 = st.columns(2)

# btn_prev = col1_1.button("previous")
# btn_next = col1_2.button("next")

option = st.selectbox(
    label="Choose folder",
    options=folders_name,
    key='folder_option'  # Use a key to store the selected option
)

if option:
    reset()
    def processing_folder():
        selected_option = st.session_state['folder_option']
        # Do something with selected_option
        st.write(f"Processing folder: {selected_option}")

        images = os.listdir(f"static/{selected_option}")
        
        sorted_images = sorted(images)

        dict_frame = defaultdict(list)

        for file in sorted_images:
            time_str = file.split("_")[0]
            day = time_str[:-6]
            hour = time_str[-6:-4]
            minute = time_str[-4:-2]
            second = time_str[-2:]

            dict_frame[f'{hour}:{minute}:{second}'].append(f'static/{selected_option}/{file}')

        # sort dict_frame by key
        dict_frame = dict(sorted(dict_frame.items()))

        placeholder = st.empty()

        for k, v in dict_frame.items():

            (pred, accuracy) = model.predict(v)
            # st.session_state.index += 11
            # show_images(col1)

            st.session_state.time_step.append(k)
            st.session_state.count[pred] += 1
            for i in range(4):
                st.session_state.data[i].append(accuracy if i == pred else 0)

            fig, axs = plt.subplots(4, 1, figsize=(10, 16))  # 4 rows, 1 column
            for i in range(4):
                time_step = st.session_state.time_step

                y_values = st.session_state.data[i]
                x_values = range(len(y_values))
                for j in range(1, len(y_values)):
                    if y_values[j] == 0:
                        axs[i].axvspan(j-1, j, facecolor='red', alpha=0.0)

                for j in range(1, len(y_values)):
                    color = 'red' if y_values[j] == 0 else 'blue'
                    axs[i].plot(x_values[j-1:j+1], y_values[j-1:j+1], color=color)

                # for j in range(1, len(y_values)):
                #     if y_values[j] != 0:  # Only plot if the value is not 0
                #         axs[i].bar(x_values[j-1:j+1], y_values[j-1:j+1], color='blue')
                
                axs[i].set_xticks(range(len(time_step)))
                axs[i].set_xticklabels(time_step, rotation=45, ha='right', fontsize=5) 
                axs[i].set_title(f"Số {i}", fontsize=14)
                axs[i].set_xlabel('Thời điểm', fontsize=12)
                axs[i].set_ylabel('Độ chính xác', fontsize=12)
                axs[i].set_ylim(0, 1)  # Fix y-axis from 0 to 1

            plt.subplots_adjust(hspace=0.5) 

            placeholder.pyplot(fig)

            plt.close(fig)

    processing_folder()



# show images 3x3 grid layout

st.title("Charts")

# uploaded_files = col2.file_uploader("Upload files", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

# btn_upload = col2.button("Upload")

# if btn_upload:
#     if uploaded_files:
#         for uploaded_file in uploaded_files:
#             with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
#                 f.write(uploaded_file.getbuffer())
        
#         uploaded_files = None

#         col2.write("Files uploaded successfully")
#     else:
#         col2.write("No files to upload")


# if st.button("Start/Stop"):
#     st.session_state.is_running = not st.session_state.is_running


