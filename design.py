# design.py
from generate import generate_novel_smiles
from predict import predict_props

def inverse_design(target_props={'density': 1.5, 'shielding_eff': 60}):
    candidates = []
    mutations = [['add_H'], ['add_C'], ['add_H', 'add_C']]  # Try different mutations
    for mut in mutations:
        sm = generate_novel_smiles(base_smiles='C=C', mutations=mut)
        if sm:
            p = predict_props(sm)
            score = abs(p['density'] - target_props['density']) + abs(p['shielding_eff'] - target_props['shielding_eff'])
            candidates.append((sm, p, score))
    return sorted(candidates, key=lambda x: x[2])[0] if candidates else (None, None, float('inf'))

if __name__ == "__main__":
    best_sm, best_p, _ = inverse_design()
    if best_sm:
        print("Best SMILES:", best_sm, "Props:", best_p)
        from rdkit import Chem
        from rdkit.Chem import Draw
        mol = Chem.MolFromSmiles(best_sm)
        if mol:
            Draw.MolToFile(mol, 'novel_structure.png', size=(300, 300))
            print("Structure saved: novel_structure.png")
        else:
            print("Invalid SMILES for visualization")
    else:
        print("No valid designs generated")
