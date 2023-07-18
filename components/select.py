import streamlit as st

def browse_file(file_types = ['xlsx']):
    return st.file_uploader('Choisis ton fichier excel',
                            type = file_types)


def select_box(label: str, choices: list[str]):
    return st.selectbox(label,
                        choices)

def multiselect(label: str, options: list[str]):
    return st.multiselect(label,
                          options)