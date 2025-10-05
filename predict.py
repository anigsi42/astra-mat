# predict.py
from rdkit import Chem
from rdkit.Chem import Descriptors
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv('regolith_data.csv')
def get_descriptors(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return [0, 0, 0]
    return [Descriptors.MolWt(mol), Descriptors.TPSA(mol), Descriptors.NumHDonors(mol)]

# Train
valid_smiles = [s for s in df['smiles'] if Chem.MolFromSmiles(s)]
X = np.array([get_descriptors(s) for s in valid_smiles])
y_density = df['density'].iloc[:len(X)].values
y_shielding = df['shielding_eff'].iloc[:len(X)].values
model_density = LinearRegression().fit(X, y_density)
model_shielding = LinearRegression().fit(X, y_shielding)

def predict_props(smiles):
    desc = get_descriptors(smiles)
    density = max(0.5, model_density.predict([desc])[0])
    shielding = min(80, max(20, model_shielding.predict([desc])[0] + 10 * desc[2]))  # NASA H-boost
    return {'density': round(density, 2), 'shielding_eff': round(shielding, 2)}

if __name__ == "__main__":
    from generate import generate_novel_smiles
    novel = generate_novel_smiles(base_smiles='C=C')  # Use PE base
    if novel:
        props = predict_props(novel)
        print("Novel:", novel, "Props:", props)
    else:
        print("Failed to generate SMILES")
