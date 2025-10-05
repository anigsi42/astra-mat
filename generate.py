# generate.py
from rdkit import Chem

def generate_novel_smiles(base_smiles='C=C', mutations=['add_H']):  # Switch to PE base
    mol = Chem.MolFromSmiles(base_smiles)
    if not mol:
        return None
    if 'add_H' in mutations:
        # Add CH3 group to carbon
        editable = Chem.EditableMol(mol)
        new_atom = Chem.Atom('C')
        idx = mol.GetNumAtoms()
        editable.AddAtom(new_atom)
        # Find a carbon with available valence
        for atom in mol.GetAtoms():
            if atom.GetSymbol() == 'C' and atom.GetExplicitValence() < 4:
                editable.AddBond(idx, atom.GetIdx(), Chem.BondType.SINGLE)
                break
        mol = editable.GetMol()
    try:
        Chem.SanitizeMol(mol)
        return Chem.MolToSmiles(mol)
    except:
        return None

if __name__ == "__main__":
    novel = generate_novel_smiles()
    print("Novel SMILES:", novel)
