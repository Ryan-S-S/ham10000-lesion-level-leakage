import numpy as np
from Orange.data import DiscreteVariable
from sklearn.model_selection import StratifiedGroupKFold

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


# 1. Entrada, alvo e grupos
if in_data is None:
    raise ValueError("Nenhuma tabela recebida.")

target = in_data.domain.class_var
if target is None:
    raise ValueError("Defina dx como Target.")

y = np.asarray(in_data.get_column(target), dtype=float).ravel()
if np.any(np.isnan(y)):
    raise ValueError("Existem diagnósticos ausentes.")
y = y.astype(int)

groups = get_groups(in_data, "lesion_id")
if len(np.unique(groups)) < N_FOLDS:
    raise ValueError(f"São necessários pelo menos {N_FOLDS} grupos.")

classes = np.unique(y)

# 2. Divisão agrupada por lesão e estratificada por diagnóstico
cv = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)

fold_ids = np.full(len(y), -1, dtype=int)
for fold, (_, test_idx) in enumerate(cv.split(np.zeros(len(y)), y, groups)):
    fold_ids[test_idx] = fold

if np.any(fold_ids == -1):
    raise ValueError("Existem imagens sem fold atribuído.")

# 3. Verificação de vazamento: cada lesão deve estar em exatamente 1 fold
lesion_folds = {}
for g, f in zip(groups, fold_ids):
    lesion_folds.setdefault(g, set()).add(f)

violations = [g for g, s in lesion_folds.items() if len(s) != 1]
if violations:
    raise ValueError(
        f"ERRO: {len(violations)} lesões aparecem em mais de um fold!"
    )

# 4. Variável de fold (meta)
fold_var = DiscreteVariable(
    "fold_lesion", values=[f"Fold_{i}" for i in range(N_FOLDS)]
)
out_data = in_data.add_column(fold_var, fold_ids, to_metas=True)

# 5. Relatório
print("\n========== K-FOLD INTER (por lesão) ==========")
print(f"Semente: {SEED} | Folds: {N_FOLDS} | Total de imagens: {len(y)}")
print(f"Lesões distintas: {len(lesion_folds)}")
print(f"Lesões compartilhadas entre folds: {len(violations)}")

global_prop = {cls: np.mean(y == cls) * 100 for cls in classes}

for fold in range(N_FOLDS):
    idx = np.where(fold_ids == fold)[0]
    print(f"\nFold {fold}: {len(idx)} imagens | "
          f"{len(np.unique(groups[idx]))} lesões")
    for cls in classes:
        c = np.sum(y[idx] == cls)
        print(f"  {target.values[int(cls)]}: {c} "
              f"({c / len(idx) * 100:.2f}% | global {global_prop[cls]:.2f}%)")

print("\nDIVISÃO CONCLUÍDA COM SUCESSO!")