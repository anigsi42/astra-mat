import streamlit as st
import pandas as pd
from design import inverse_design
from rdkit import Chem
from rdkit.Chem import Draw

st.title("AstraMat: AI Material Designer")
st.markdown("**NASA Space Apps Challenge 2025 - Open Innovation**")
st.write("Design novel regolith-based composites for Mars radiation shielding using AI inverse design.")

col1, col2 = st.columns(2)
with col1:
    density = st.slider("Target Density (g/cm³)", 1.0, 3.0, 1.5)
with col2:
    shielding = st.slider("Target Shielding (%)", 30, 80, 60)
if st.button("Design Novel Composite"):
    with st.spinner("Generating novel composite..."):
        sm, props, _ = inverse_design({'density': density, 'shielding_eff': shielding})
        if sm:
            st.write(f"**Novel SMILES**: {sm}")
            st.table(pd.DataFrame([props]))
            mol = Chem.MolFromSmiles(sm)
            if mol:
                Draw.MolToImageFile(mol, 'temp.png')
                st.image('temp.png', caption="Structure Visualization")
            else:
                st.error("Invalid SMILES for visualization")
        else:
            st.error("No valid design found; adjust targets.")
st.markdown("---\n**Built solo with AI**: Uses NASA-inspired regolith data (NTRS) and RDKit for material discovery.")
