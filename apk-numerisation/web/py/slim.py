"""Charge finish.py tel quel, en libérant la mémoire plus tôt.

Le calcul de reprint_clean n'est pas modifié : on ajoute seulement « nom = None » juste après
la dernière ligne qui utilise chaque grand tableau, pour que le navigateur du téléphone n'ait
pas à garder toute la page en double. Le résultat est le même pixel pour pixel."""
import ast
import types


def _names(node):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _overwrites(st, name):
    """st est une affectation simple qui remplace « name » sans lire son ancienne valeur."""
    if not isinstance(st, ast.Assign) or name in _names(st.value):
        return False
    stores, loads = set(), set()
    for t in st.targets:
        for n in ast.walk(t):
            if isinstance(n, ast.Name):
                (stores if isinstance(n.ctx, ast.Store) else loads).add(n.id)
    return name in stores and name not in loads


def _slim_function(f):
    inner = set()  # noms vus par les fonctions internes : gardés jusqu'au bout
    for n in ast.walk(f):
        if n is not f and isinstance(n, (ast.FunctionDef, ast.Lambda)):
            inner |= _names(n)
            if isinstance(n, ast.FunctionDef):
                inner.add(n.name)
    local = {a.arg for a in f.args.args} | {
        n.id for n in ast.walk(f) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
    uses = {}
    for i, st in enumerate(f.body):
        for name in _names(st) & local:
            uses.setdefault(name, []).append(i)
    # Une valeur est morte après l'instruction i si le nom n'est plus jamais utilisé, ou si la
    # prochaine instruction qui le cite le remplace sans le lire (« nom = ... » sans condition).
    dead = {}
    for name, idx in uses.items():
        if name in inner:
            continue
        for i, j in zip(idx, idx[1:] + [None]):
            if j is None or _overwrites(f.body[j], name):
                dead.setdefault(i, []).append(name)
    body = []
    for i, st in enumerate(f.body):
        body.append(st)
        if isinstance(st, ast.Return) or i == len(f.body) - 1:
            continue
        free = sorted(dead.get(i, ()))
        for n in free:
            body.append(ast.Assign(targets=[ast.Name(n, ast.Store())], value=ast.Constant(None)))
    f.body = body


def load(path, name="finish", funcs=("reprint_clean",)):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in funcs:
            _slim_function(node)
    ast.fix_missing_locations(tree)
    mod = types.ModuleType(name)
    mod.__file__ = path
    exec(compile(tree, path, "exec"), mod.__dict__)
    return mod
