import streamlit as st
from typing import List

def browse_file(file_types = ['xlsx']):
    return st.file_uploader('Choisis ton fichier excel',
                            type = file_types)


def select_box(label: str, choices: List[str]):
    return st.selectbox(label,
                        choices)

def multiselect(label: str, options: List[str]):
    return st.multiselect(label,
                          options)