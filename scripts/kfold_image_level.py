import numpy as np
from Orange.data import DiscreteVariable
from sklearn.model_selection import StratifiedKFold

SEED = 42
N_FOLDS = 5


def get_groups(table, name="lesion_id"):
    if name not in table.domain:
        raise ValueError(f"A coluna '{name}' não foi encontrada.")
    var = table.domain[name]
    col = table.get_column(var)
    groups = []
    for i, g in enumerate(col):
        if var.is_discrete:
            val = None if np.isnan(float(g)) else var.values[int(g)]
        else:
            if g is None or (isinstance(g, (float, np.floating)) and np.isnan(g)):
                val = None
            else:
                val = str(g).strip()
                if val.lower() in ("", "?", "nan", "none"):
                    val = None
        groups.append(val if val is not None else f"missing_{i}")
    return np.array(groups, dtype=object)


# 1. Entrada e alvo
if in_data is None:
    raise ValueError("Nenhuma tabela recebida.")

target = in_data.domain.class_var
if target is None:
    raise ValueError("Defina dx como Target.")

y = np.asarray(in_data.get_column(target), dtype=float).ravel()
if np.any(np.isnan(y)):
    raise ValueError("Existem diagnósticos ausentes.")
y = y.astype(int)

classes, counts = np.unique(y, return_counts=True)
if counts.min() < N_FOLDS:
    raise ValueError(f"Cada diagnóstico precisa ter pelo menos {N_FOLDS} imagens.")

# 2. Divisão estratificada por diagnóstico (ignora a lesão de propósito)
cv = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)

fold_ids = np.full(len(y), -1, dtype=int)
for fold, (_, test_idx) in enumerate(cv.split(np.zeros(len(y)), y)):
    fold_ids[test_idx] = fold

if np.any(fold_ids == -1):
    raise ValueError("Existem imagens sem fold atribuído.")

# 3. Variável de fold (meta, não entra como atributo do modelo)
fold_var = DiscreteVariable(
    "fold_dx", values=[f"Fold_{i}" for i in range(N_FOLDS)]
)
out_data = in_data.add_column(fold_var, fold_ids, to_metas=True)

# 4. Relatório
print("\n========== K-FOLD INTRA (por imagem) ==========")
print(f"Semente: {SEED} | Folds: {N_FOLDS} | Total de imagens: {len(y)}")

for fold in range(N_FOLDS):
    idx = np.where(fold_ids == fold)[0]
    print(f"\nFold {fold}: {len(idx)} imagens")
    for cls in classes:
        c = np.sum(y[idx] == cls)
        print(f"  {target.values[int(cls)]}: {c} ({c / len(idx) * 100:.2f}%)")

# 5. Diagnóstico de vazamento (apenas informativo)
if "lesion_id" in in_data.domain:
    groups = get_groups(in_data)
    lesion_folds = {}
    for g, f in zip(groups, fold_ids):
        lesion_folds.setdefault(g, set()).add(f)

    n_lesions = len(lesion_folds)
    n_split = sum(1 for s in lesion_folds.values() if len(s) > 1)

    leaked = 0
    for g, f in zip(groups, fold_ids):
        # a imagem tem "irmã" da mesma lesão em outro fold (portanto no treino)?
        if len(lesion_folds[g]) > 1:
            leaked += 1

    print("\n--- Diagnóstico de vazamento (intra) ---")
    print(f"Lesões distintas: {n_lesions}")
    print(f"Lesões espalhadas em mais de um fold: {n_split} "
          f"({n_split / n_lesions * 100:.2f}%)")
    print(f"Imagens cuja lesão aparece em outro fold: {leaked} "
          f"({leaked / len(y) * 100:.2f}%)")

print("\nDIVISÃO CONCLUÍDA COM SUCESSO!")