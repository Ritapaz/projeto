from collections import defaultdict
from typing import Dict, Iterable, List, Sequence, Tuple

from pulp import LpMinimize, LpProblem, LpVariable, PULP_CBC_CMD, lpSum, LpStatus


Slot = Tuple[str, str]


def print_listagem_detalhada_por_professor(
    alocacoes: Iterable[Tuple[str, str, str, str]],
    dias: Sequence[str],
    periodos: Sequence[str],
) -> None:
    """Imprime a listagem detalhada agrupando por professor."""

    por_prof = defaultdict(list)
    for professor, disciplina, dia, periodo in alocacoes:
        por_prof[professor].append(
            {
                "disciplina": disciplina,
                "dia": dia,
                "periodo": periodo,
            }
        )

    ordem_dias = {d: i for i, d in enumerate(dias)}
    ordem_periodos = {p: i for i, p in enumerate(periodos)}

    print("\n=== Listagem Detalhada por Professor ===")
    for professor in sorted(por_prof.keys(), key=lambda x: str(x).lower()):
        print(f"\nProfessor: {professor}")
        itens = por_prof[professor]
        itens.sort(
            key=lambda it: (
                ordem_dias.get(it["dia"], 1_000_000),
                ordem_periodos.get(it["periodo"], 1_000_000),
                str(it["disciplina"]).lower(),
            )
        )

        dia_atual = object()
        for item in itens:
            if item["dia"] != dia_atual:
                dia_atual = item["dia"]
                print(f"- Dia: {item['dia']}")
            print(f"  • {item['periodo']}: {item['disciplina']}")


DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
PERIODOS = ["7-9", "9-11", "11-13", "14-16", "16-18"]
SLOTS: List[Slot] = [(dia, periodo) for dia in DIAS for periodo in PERIODOS]

prereq_pairs = [
    ("Mat I", "Micro I"),
    ("Micro I", "Micro II"),
    ("Micro II", "Micro III"),
    ("Mat I", "Mat II"),
    ("Mat II", "Mat Eco"),
    ("PEC I", "PEC II"),
    ("Intr. Eco", "Micro I"),
    ("Intr. Eco", "Macro I"),
    ("PEC II", "Eco Pol"),
    ("Mat II", "Estatística"),
    ("Estatística", "Econome I"),
    ("Econome I", "Econom II"),
    ("Macro I", "FEB"),
    ("Macro I", "Macro II"),
    ("Macro II", "Macro III"),
    ("Macro III", "Macro IV"),
    ("FEB", "EBC I"),
    ("EBC I", "EBC II"),
    ("Micro II", "OI"),
    ("Macro II", "Desenv I"),
    ("Desenv I", "Desenv II"),
]

course_demands: Dict[str, Dict[str, object]] = {
    "Mat I": {
        "professor": "Rita",
        "periodo": 1,
        "horarios": 3,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
        },
    },
    "Intr. Eco": {
        "professor": "Luiz Gustavo",
        "periodo": 1,
        "horarios": 2,
        "disponibilidade": {
            ("Quinta", "11-13"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
            ("Sexta", "11-13"),
        },
    },
    "PEC I": {
        "professor": "Vanuza",
        "periodo": 1,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
        },
    },
    "Teoria Sociológica": {
        "professor": "Subst 1",
        "periodo": 1,
        "horarios": 2,
        "disponibilidade": {
            ("Quinta", "14-16"),
            ("Quinta", "16-18"),
        },
    },
    "História Econ": {
        "professor": "Walter",
        "periodo": 1,
        "horarios": 2,
        "disponibilidade": {
            ("Sexta", "14-16"),
            ("Sexta", "16-18"),
        },
    },
    "Teoria Pol": {
        "professor": "Subst 2",
        "periodo": 1,
        "horarios": 2,
        "disponibilidade": {
            ("Sexta", "9-11"),
            ("Sexta", "11-13"),
        },
    },
    "Contabilidade": {
        "professor": "Patrick",
        "periodo": 2,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Segunda", "11-13"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
        },
    },
    "Direito": {
        "professor": "Patrick",
        "periodo": 2,
        "horarios": 1,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Segunda", "11-13"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
        },
    },
    "Optat 1": {
        "professor": "Patrick",
        "periodo": 7,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Segunda", "11-13"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
        },
    },
    "Mat II": {
        "professor": "Marcus",
        "periodo": 2,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Segunda", "11-13"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
            ("Sexta", "11-13"),
        },
    },
    "PEC II": {
        "professor": "Daniela",
        "periodo": 2,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
        },
    },
    "Macro I": {
        "professor": "Breno",
        "periodo": 2,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
        },
    },
    "Ética": {
        "professor": "Roney",
        "periodo": 2,
        "horarios": 1,
        "disponibilidade": {
            ("Quarta", "11-13"),
        },
    },
    "Micro I": {
        "professor": "Roni",
        "periodo": 2,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
        },
    },
    "Mat Eco": {
        "professor": "Samuel",
        "periodo": 3,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Segunda", "11-13"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
            ("Sexta", "11-13"),
        },
    },
    "FEB": {
        "professor": "Vanessa",
        "periodo": 3,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
        },
    },
    "Eco Pol": {
        "professor": "Maracajaro",
        "periodo": 3,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "9-11"),
            ("Segunda", "11-13"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Sexta", "9-11"),
            ("Sexta", "11-13"),
        },
    },
    "Estatística": {
        "professor": "Simone",
        "periodo": 3,
        "horarios": 3,
        "disponibilidade": {
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
            ("Sexta", "11-13"),
        },
    },
    "Macro II": {
        "professor": "Alan",
        "periodo": 3,
        "horarios": 2,
        "disponibilidade": {
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
        },
    },
    "Micro II": {
        "professor": "Patrícia",
        "periodo": 3,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
        },
    },
    "Optat Ext 1": {
        "professor": "Marcus",
        "periodo": 3,
        "horarios": 1,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Segunda", "11-13"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
        },
    },
    "Micro III": {
        "professor": "Roni",
        "periodo": 4,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
        },
    },
    "Desenv I": {
        "professor": "Marcos T.",
        "periodo": 4,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
        },
    },
    "Econom I": {
        "professor": "Vladimir",
        "periodo": 4,
        "horarios": 2,
        "disponibilidade": {
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
        },
    },
    "EBC I": {
        "professor": "Vanessa",
        "periodo": 4,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
        },
    },
    "Macro III": {
        "professor": "Felipe",
        "periodo": 4,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
        },
    },
    "TGA": {
        "professor": "Cristiano",
        "periodo": 4,
        "horarios": 2,
        "disponibilidade": {
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
        },
    },
    "Macro IV": {
        "professor": "Marcos T.",
        "periodo": 5,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
        },
    },
    "Mat Financ": {
        "professor": "José Eduardo",
        "periodo": 5,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
        },
    },
    "Desenv II": {
        "professor": "Rodrigo Delpupo",
        "periodo": 5,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
        },
    },
    "OI": {
        "professor": "Rosendo",
        "periodo": 5,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
        },
    },
    "EBC II": {
        "professor": "Álvaro",
        "periodo": 5,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "9-11"),
            ("Segunda", "11-13"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
            ("Sexta", "9-11"),
            ("Sexta", "11-13"),
        },
    },
    "Econom II": {
        "professor": "Simone",
        "periodo": 5,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
            ("Sexta", "11-13"),
        },
    },
    "Optat Ext 3": {
        "professor": "Cristiano",
        "periodo": 5,
        "horarios": 1,
        "disponibilidade": {
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
        },
    },
    "Projetos": {
        "professor": "José Eduardo",
        "periodo": 6,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
        },
    },
    "ESP": {
        "professor": "Alan",
        "periodo": 6,
        "horarios": 2,
        "disponibilidade": {
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
        },
    },
    "Optat Ext 4": {
        "professor": "Patrícia",
        "periodo": 6,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
        },
    },
    "ERU": {
        "professor": "Rosendo",
        "periodo": 6,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
        },
    },
    "Internac": {
        "professor": "Breno",
        "periodo": 6,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
        },
    },
    "Monetária": {
        "professor": "Felipe",
        "periodo": 6,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
        },
    },
    "TPE": {
        "professor": "Luiz Gustavo",
        "periodo": 6,
        "horarios": 2,
        "disponibilidade": {
            ("Quinta", "11-13"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
            ("Sexta", "11-13"),
        },
    },
    "Optat Ext 5": {
        "professor": "Vanuza",
        "periodo": 7,
        "horarios": 2,
        "disponibilidade": {
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
        },
    },
    "Optat 3": {
        "professor": "Vladimir",
        "periodo": 7,
        "horarios": 2,
        "disponibilidade": {
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
        },
    },
    "Optat 4": {
        "professor": "Marcus",
        "periodo": 8,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "7-9"),
            ("Segunda", "9-11"),
            ("Segunda", "11-13"),
            ("Terça", "7-9"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "7-9"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "7-9"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
            ("Sexta", "7-9"),
            ("Sexta", "9-11"),
            ("Sexta", "11-13"),
        },
    },
    "Optat 6": {
        "professor": "Álvaro",
        "periodo": 8,
        "horarios": 2,
        "disponibilidade": {
            ("Segunda", "9-11"),
            ("Segunda", "11-13"),
            ("Terça", "9-11"),
            ("Terça", "11-13"),
            ("Quarta", "9-11"),
            ("Quarta", "11-13"),
            ("Quinta", "9-11"),
            ("Quinta", "11-13"),
            ("Sexta", "9-11"),
            ("Sexta", "11-13"),
        },
    },
}

prof_prefs: Dict[str, Dict[str, List[str]]] = {
    "Alan": {
        "dias_preferidos": ["Quinta", "Sexta"],
        "periodos_preferidos": ["7-9", "9-11"],
        "dias_indisponiveis": ["Segunda", "Terça"],
        "periodos_indisponiveis": ["11-13", "14-16", "16-18"],
    },
    "Álvaro": {
        "dias_preferidos": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
        "periodos_preferidos": ["9-11", "11-13"],
        "dias_indisponiveis": ["Terça"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Breno": {
        "dias_preferidos": ["Terça", "Quarta", "Quinta"],
        "periodos_preferidos": ["9-11", "11-13"],
        "dias_indisponiveis": ["Segunda", "Sexta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Cristiano": {
        "dias_preferidos": ["Quinta", "Sexta"],
        "periodos_preferidos": ["7-9", "9-11"],
        "dias_indisponiveis": ["Segunda", "Terça", "Quarta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Daniela": {
        "dias_preferidos": ["Terça", "Quarta", "Quinta"],
        "periodos_preferidos": ["7-9", "9-11", "11-13"],
        "dias_indisponiveis": ["Segunda", "Sexta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "José Eduardo": {
        "dias_preferidos": ["Segunda", "Terça"],
        "periodos_preferidos": ["7-9", "9-11"],
        "dias_indisponiveis": ["Quarta", "Quinta", "Sexta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Felipe": {
        "dias_preferidos": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
        "periodos_preferidos": ["7-9", "9-11"],
        "periodos_indisponiveis": ["11-13", "14-16", "16-18"],
    },
    "Luiz Gustavo": {
        "dias_preferidos": ["Quinta", "Sexta"],
        "periodos_preferidos": ["7-9", "9-11", "11-13", "14-16", "16-18"],
        "dias_indisponiveis": ["Segunda", "Terça", "Quarta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Maracajaro": {
        "dias_preferidos": ["Segunda", "Quarta", "Sexta"],
        "periodos_preferidos": ["9-11", "11-13", "14-16", "16-18"],
        "dias_indisponiveis": ["Terça", "Quinta"],
        "periodos_indisponiveis": ["7-9", "9-11", "14-16", "16-18"],
    },
    "Marcos T.": {
        "dias_preferidos": ["Segunda", "Terça", "Quarta", "Quinta"],
        "periodos_preferidos": ["7-9", "9-11"],
        "dias_indisponiveis": ["Sexta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Marcus": {
        "dias_preferidos": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
        "periodos_preferidos": ["7-9", "9-11", "11-13"],
        "dias_indisponiveis": ["Terça"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Patrícia": {
        "dias_preferidos": ["Terça", "Quarta", "Quinta"],
        "periodos_preferidos": ["7-9", "9-11", "11-13"],
        "dias_indisponiveis": ["Terça"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Patrick": {
        "dias_preferidos": ["Segunda", "Terça"],
        "periodos_preferidos": ["7-9", "9-11", "11-13"],
        "dias_indisponiveis": ["Quinta", "Sexta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Rita": {
        "dias_preferidos": ["Segunda", "Terça", "Quarta"],
        "periodos_preferidos": ["7-9", "9-11"],
        "dias_indisponiveis": ["Quinta", "Sexta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Rosendo": {
        "dias_preferidos": ["Terça", "Quarta"],
        "periodos_preferidos": ["7-9", "9-11", "11-13"],
        "dias_indisponiveis": ["Segunda", "Quinta", "Sexta"],
        "periodos_indisponiveis": ["7-9", "9-11", "11-13", "14-16", "16-18"],
    },
    "Rodrigo Delpupo": {
        "dias_preferidos": ["Terça", "Quarta", "Quinta", "Sexta"],
        "periodos_preferidos": ["7-9", "9-11", "11-13"],
        "dias_indisponiveis": ["Segunda", "Sexta"],
        "periodos_indisponiveis": ["7-9", "9-11", "11-13", "14-16", "16-18"],
    },
    "Roni": {
        "dias_preferidos": ["Segunda", "Terça", "Quinta"],
        "periodos_preferidos": ["7-9", "9-11"],
        "dias_indisponiveis": ["Quarta", "Sexta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Samuel": {
        "dias_preferidos": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
        "periodos_preferidos": ["7-9", "9-11", "11-13"],
        "dias_indisponiveis": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Simone": {
        "dias_preferidos": ["Terça", "Quarta", "Sexta"],
        "periodos_preferidos": ["7-9", "9-11", "11-13"],
        "dias_indisponiveis": ["Terça"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Vanessa": {
        "dias_preferidos": ["Terça", "Quarta"],
        "periodos_preferidos": ["7-9", "9-11", "11-13", "14-16", "16-18"],
        "dias_indisponiveis": ["Segunda", "Quinta", "Sexta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Vanuza": {
        "dias_preferidos": ["Terça", "Quarta", "Quinta"],
        "periodos_preferidos": ["9-11", "11-13"],
        "dias_indisponiveis": ["Terça"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Vladimir": {
        "dias_preferidos": ["Quarta", "Quinta", "Sexta"],
        "periodos_preferidos": ["7-9", "9-11", "11-13"],
        "dias_indisponiveis": ["Segunda", "Terça"],
        "periodos_indisponiveis": ["7-9", "9-11", "11-13", "14-16", "16-18"],
    },
    "Subst 1": {
        "dias_preferidos": ["Quinta"],
        "periodos_preferidos": ["14-16", "16-18"],
        "dias_indisponiveis": ["Terça"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Subst 2": {
        "dias_preferidos": ["Sexta"],
        "periodos_preferidos": ["9-11", "11-13"],
        "dias_indisponiveis": ["Terça"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Walter": {
        "dias_preferidos": ["Sexta"],
        "periodos_preferidos": ["14-16", "16-18"],
        "dias_indisponiveis": ["Terça"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
    "Roney": {
        "dias_preferidos": ["Quarta"],
        "periodos_preferidos": ["11-13"],
        "dias_indisponiveis": ["Segunda", "Terça", "Quinta", "Sexta"],
        "periodos_indisponiveis": ["14-16", "16-18"],
    },
}

no_same_day = {
    "Rita": True,
    "Breno": True,
    "Felipe": True,
    "Patrick": True,
    "Daniela": True,
    "Cristiano": True,
    "Alan": True,
    "Vanessa": True,
    "Álvaro": True,
    "José Eduardo": True,
    "Vladimir": True,
}


def build_schedule(
    courses: Dict[str, Dict[str, object]],
    prof_prefs: Dict[str, Dict[str, List[str]]],
    no_same_day: Dict[str, bool] | None = None,
    prereq_pairs: Sequence[Tuple[str, str]] | None = None,
) -> Dict[str, List[Slot]]:
    print("Iniciando construção do horário...")

    if no_same_day is None:
        no_same_day = {}
    if prereq_pairs is None:
        prereq_pairs = []
    if prof_prefs is None:
        prof_prefs = {}

    prob = LpProblem("Horario_Disciplinas", LpMinimize)

    print("Criando variáveis de alocação...")
    x = {
        disc: {slot: LpVariable(f"x_{disc}_{slot[0]}_{slot[1]}", cat="Binary") for slot in SLOTS}
        for disc in courses
    }

    professores = {info["professor"] for info in courses.values()}
    y = {
        prof: {dia: LpVariable(f"y_{prof}_{dia}", cat="Binary") for dia in DIAS}
        for prof in professores
    }

    course_day = {
        disc: {dia: LpVariable(f"course_day_{disc}_{dia}", cat="Binary") for dia in DIAS}
        for disc in courses
    }

    period_day = {}
    for periodo in {int(info["periodo"]) for info in courses.values()}:
        period_day[periodo] = {
            dia: LpVariable(f"period_day_{periodo}_{dia}", cat="Binary") for dia in DIAS
        }

    prereq_slack = {}

    print("Adicionando restrições...")

    print("1. Restrições de número de horários por disciplina...")
    for disc, info in courses.items():
        prob += (
            lpSum(x[disc][slot] for slot in SLOTS) == info["horarios"],
            f"ReqHorarios_{disc}",
        )

    print("2. Restrições de disponibilidade...")
    for disc, info in courses.items():
        disponibilidade = info.get("disponibilidade", set())
        for slot in SLOTS:
            if slot not in disponibilidade:
                prob += (x[disc][slot] == 0, f"Disp_{disc}_{slot[0]}_{slot[1]}")

    print("3. Restrições de conflito de professor...")
    prof_courses: Dict[str, List[str]] = {}
    for disc, info in courses.items():
        prof_courses.setdefault(info["professor"], []).append(disc)

    for prof, discs in prof_courses.items():
        for slot in SLOTS:
            prob += (
                lpSum(x[disc][slot] for disc in discs) <= 1,
                f"Conflict_{prof}_{slot[0]}_{slot[1]}",
            )

    print("4. Restrições de dias por professor...")
    max_dias_por_professor = 3
    for prof, discs in prof_courses.items():
        for dia in DIAS:
            for disc in discs:
                for periodo in PERIODOS:
                    slot = (dia, periodo)
                    prob += (
                        x[disc][slot] <= y[prof][dia],
                        f"UsaDia_{prof}_{disc}_{dia}_{periodo}",
                    )
        prob += (
            lpSum(y[prof][dia] for dia in DIAS) <= max_dias_por_professor,
            f"LimiteDias_{prof}",
        )

    for prof, discs in prof_courses.items():
        if no_same_day.get(prof, False):
            for disc in discs:
                for dia in DIAS:
                    prob += (
                        lpSum(x[disc][(dia, periodo)] for periodo in PERIODOS) <= 1,
                        f"NoSameDay_{prof}_{disc}_{dia}",
                    )

    print("5. Restrições de ativação de dias por disciplina e período...")
    period_courses: Dict[int, List[str]] = {}
    for disc, info in courses.items():
        period_courses.setdefault(int(info["periodo"]), []).append(disc)

    for disc in courses:
        for dia in DIAS:
            prob += (
                course_day[disc][dia]
                <= lpSum(x[disc][(dia, periodo)] for periodo in PERIODOS),
                f"CourseDayUpper_{disc}_{dia}",
            )
            for periodo in PERIODOS:
                prob += (
                    x[disc][(dia, periodo)] <= course_day[disc][dia],
                    f"CourseDayLink_{disc}_{dia}_{periodo}",
                )

    for periodo, discs in period_courses.items():
        for dia in DIAS:
            prob += (
                period_day[periodo][dia]
                <= lpSum(
                    x[disc][(dia, periodo_slot)]
                    for disc in discs
                    for periodo_slot in PERIODOS
                ),
                f"PeriodDayUpper_{periodo}_{dia}",
            )
            for disc in discs:
                for periodo_slot in PERIODOS:
                    prob += (
                        x[disc][(dia, periodo_slot)] <= period_day[periodo][dia],
                        f"PeriodDayLink_{disc}_{periodo}_{dia}_{periodo_slot}",
                    )

    print("6. Restrições de sobreposição de período...")
    for periodo, discs in period_courses.items():
        for slot in SLOTS:
            prob += (
                lpSum(x[disc][slot] for disc in discs) <= 1,
                f"NoOverlap_Periodo{periodo}_{slot[0]}_{slot[1]}",
            )

    if prereq_pairs:
        print("7. Restrições de pares de pré-requisitos...")
        dependentes = defaultdict(set)
        for pre_req, dependente in prereq_pairs:
            if pre_req in courses and dependente in courses:
                dependentes[dependente].add(pre_req)

        for dependente, prereqs in dependentes.items():
            prereqs = set(prereqs)
            for pre_req in prereqs:
                periodo = int(courses[pre_req]["periodo"])
                for dia in DIAS:
                    slack_var = prereq_slack.setdefault(
                        (dependente, pre_req, dia),
                        LpVariable(f"slack_prereq_{pre_req}_{dependente}_{dia}", cat="Binary"),
                    )
                    prob += (
                        course_day[dependente][dia]
                        <= course_day[pre_req][dia]
                        + 1
                        - period_day[periodo][dia]
                        + slack_var,
                        f"PrereqDay_{pre_req}_{dependente}_{dia}",
                    )

    prob += (
        lpSum(y[prof][dia] for prof in y for dia in y[prof])
        + 100 * lpSum(prereq_slack.values())
    )

    print("\nResolvendo o problema...")
    prob.solve(PULP_CBC_CMD(msg=True))

    status = LpStatus[prob.status]
    print(f"\nStatus da solução: {status}")
    if status != "Optimal":
        raise RuntimeError("Não foi possível encontrar um horário viável.")

    print("\nConstruindo o horário...")
    schedule: Dict[str, List[Slot]] = {}
    for disc in courses:
        schedule[disc] = []
        for slot in SLOTS:
            valor = x[disc][slot].value()
            if valor is not None and valor > 0.5:
                schedule[disc].append(slot)

    violations = [
        (dependente, pre_req, dia)
        for (dependente, pre_req, dia), var in prereq_slack.items()
        if var.value() is not None and var.value() > 0.5
    ]

    return schedule, violations


def visualize_schedule_matrix(
    horario: Dict[str, List[Slot]] | None = None,
    demandas: Dict[str, Dict[str, object]] | None = None,
) -> None:
    dias = DIAS
    periodos = PERIODOS

    if horario is None:
        print("\n     ", end="")
        for dia in dias:
            print(f"{dia:^12}", end="")
        print()
        for periodo in periodos:
            print(f"{periodo:4}", end=" ")
            for _ in dias:
                print("[---------]", end=" ")
            print()
        return

    horarios_por_periodo: Dict[int, Dict[str, List[Slot]]] = {}
    if demandas is None:
        demandas = course_demands

    for disciplina, slots in horario.items():
        periodo = int(demandas[disciplina].get("periodo", 1))
        horarios_por_periodo.setdefault(periodo, {})[disciplina] = slots

    for periodo_acad in sorted(horarios_por_periodo.keys()):
        print(f"\n=== {periodo_acad}º Período ===")
        print("     ", end="")
        for dia in dias:
            print(f"{dia:^12}", end="")
        print()

        for periodo in periodos:
            print(f"{periodo:4}", end=" ")
            for dia in dias:
                ocupacao = [
                    disc
                    for disc, slots in horarios_por_periodo[periodo_acad].items()
                    if (dia, periodo) in slots
                ]
                if ocupacao:
                    print(f"[{ocupacao[0][:9]:^9}]", end=" ")
                else:
                    print("[---------]", end=" ")
            print()


def get_courses_by_period() -> Dict[int, List[str]]:
    resultado: Dict[int, List[str]] = {}
    for disciplina, info in course_demands.items():
        resultado.setdefault(int(info["periodo"]), []).append(disciplina)
    return resultado


def analyze_scheduling_conflicts() -> None:
    print("\n=== Análise de Conflitos de Slots ===")
    visualize_schedule_matrix()

    print("\n=== Análise de Slots Críticos ===")
    for periodo, disciplinas in sorted(get_courses_by_period().items()):
        slots_necessarios = sum(course_demands[disc]["horarios"] for disc in disciplinas)
        slots_disponiveis = count_available_slots(disciplinas)

        print(f"\nPeríodo {periodo}:")
        print(f"Slots necessários: {slots_necessarios}")
        print(f"Slots disponíveis: {slots_disponiveis}")
        if slots_disponiveis < slots_necessarios:
            print("⚠️ ALERTA: Possível gargalo!")


def count_available_slots(disciplinas: Iterable[str]) -> int:
    slots_disponiveis = set()
    for disciplina in disciplinas:
        slots_disponiveis.update(course_demands[disciplina]["disponibilidade"])
    return len(slots_disponiveis)


def main() -> None:
    print("=== Análise Detalhada de Viabilidade de Horários ===")
    analyze_scheduling_conflicts()

    print("\n=== Tentando gerar horário ===")
    try:
        horario, violacoes = build_schedule(
            course_demands, prof_prefs, no_same_day, prereq_pairs
        )
    except RuntimeError as err:
        print(f"\nERRO: {err}")
        return

    print("\n=== Horário Gerado com Sucesso ===")

    if violacoes:
        print("\n⚠️  Aviso: Alguns pares de pré-requisito ficaram em dias sem sobreposição direta.")
        for dependente, pre_req, dia in sorted(violacoes):
            print(
                f"  - {dependente} ocorreu em {dia} sem coincidir com {pre_req} e com outro dia ativo do período."
            )
    else:
        print("\nTodos os pares de pré-requisito foram atendidos nos dias solicitados.")

    print("\n=== Visualização em Matriz ===")
    visualize_schedule_matrix(horario, course_demands)

    alocacoes = []
    for disciplina, slots in horario.items():
        professor = course_demands[disciplina]["professor"]
        for dia, periodo in slots:
            alocacoes.append((professor, disciplina, dia, periodo))

    if alocacoes:
        print_listagem_detalhada_por_professor(alocacoes, DIAS, PERIODOS)


if __name__ == "__main__":
    main()
