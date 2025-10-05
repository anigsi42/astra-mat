import pubchempy as pcp
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

data = {
    'smiles': ['[Si](=O)=O', 'C=C', '[B]', 'O', 'C=C', 'C1CO1', 'S', 'C', 'CC', 'c1ccccc1'],
    'density': [2.65, 0.92, 2.34, 1.0, 1.8, 1.9, 2.0, 1.7, 1.6, 1.4],
    'shielding_eff': [30, 60, 50, 70, 55, 50, 40, 65, 62, 58],
    'tensile_strength': [50, 20, 100, 0, 30, 40, 60, 100, 30, 200]
}
df = pd.DataFrame(data)

try:
    c = pcp.get_compounds('SiO2', 'formula')[0]
    print(f"SiO2 Mol Weight: {c.molecular_weight}")
except Exception as e:
    print(f"PubChem failed: {e}")
df.to_csv('regolith_data.csv')
print(df.head(10))
