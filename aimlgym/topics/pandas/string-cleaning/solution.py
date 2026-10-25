r"""Reference solution for PD-11 Cleaning Text Columns.

Each column is cleaned with a chain of vectorised `.str` operations. The domain is the second
element after splitting on '@'; `.where(len > 1)` keeps it missing when there was no '@'. Missing
inputs propagate as missing through every `.str` call.
"""
import pandas as pd


def clean_contacts(df):
    name = df["name"].str.strip().str.replace(r"\s+", " ", regex=True).str.title()
    phone = df["phone"].str.replace(r"\D", "", regex=True)
    email = df["email"].str.strip().str.lower()
    parts = email.str.split("@")
    domain = parts.str[1].where(parts.str.len() > 1)
    return df.assign(name=name, phone=phone, email=email, domain=domain)
