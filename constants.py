SYMMETRY_BREAKING = 0
NO_SYMMETRY_BREAKING = 1
SYM_DICT = {SYMMETRY_BREAKING: "_symbreak", NO_SYMMETRY_BREAKING: ""}
# SYM_DICT = {NO_SYMMETRY_BREAKING: ""}

# CP

# SAT
LINEAR_SEARCH = 0
BINARY_SEARCH = 1
CBC = 0
GLPK = 1
HIGH = 2
STRATEGIES_DICT = {LINEAR_SEARCH: "linear", BINARY_SEARCH: "binary"}
# STRATEGIES_DICT = {LINEAR_SEARCH: "linear"}
#STRATEGIES_DICT = {BINARY_SEARCH: "binary"}
STRATEGIES_MIP_DICT = {HIGH: "HIGH",CBC:"CBC",GLPK: "GLPK"}
# SMT

# MIP