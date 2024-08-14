import streamlit as st
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import time

TIME_STEP = 3

if not os.path.exists("uploads"):
    os.makedirs("uploads")

if 'data' not in st.session_state:
    st.session_state.data = defaultdict(list)
if 'count' not in st.session_state:
    st.session_state.count = defaultdict(int)
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'time_step' not in st.session_state:
    st.session_state.time_step = []

class FakeModel:
    def predict(self):
        return np.random.randint(0, 4)


model = FakeModel()


st.title("Charts with File Upload")


uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)

btn_upload = st.button("Upload")

if btn_upload:
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        uploaded_files = None

        st.write("Files uploaded successfully")
    else:
        st.write("No files to upload")


if st.button("Start/Stop"):
    st.session_state.is_running = not st.session_state.is_running


placeholder = st.empty()


while st.session_state.is_running:

    pred = model.predict()

    if len(st.session_state.time_step) == 0:
        st.session_state.time_step.append(0)
    else:
        st.session_state.time_step.append(st.session_state.time_step[-1] + TIME_STEP) 

    st.session_state.count[pred] += 1
    for i in range(4):
        st.session_state.data[i].append(st.session_state.count[i])

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    for i in range(4):
        row = i // 2
        col = i % 2
        axs[row, col].plot(st.session_state.time_step, st.session_state.data[i])
        axs[row, col].set_title(f"Số lượng số {i}", fontsize=14)
        axs[row, col].set_xlabel('Thời gian', fontsize=12)
        axs[row, col].set_ylabel('Số lượng', fontsize=12)

    plt.subplots_adjust(wspace=0.3, hspace=0.4)

    placeholder.pyplot(fig)

    time.sleep(TIME_STEP)
else:
    st.write("Chưa chạy. Bấm nút Start để bắt đầu.")
