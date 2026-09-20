# Agent Matrix

| Factory | Agent | Model | Effort | Sandbox | Primary responsibility |
|---|---|---|---|---|---|
| General | general_explorer | Luna | medium | read-only | Cheap evidence/file/context scan |
| General | general_researcher | Terra | high | read-only | Multi-source investigation |
| General | general_planner | Sol | medium | read-only | Decomposition and planning |
| General | verification_reviewer | Sol | high | read-only | Independent verification |
| General | astra_problem_specialist | Astra | medium | read-only | Hard reasoning bottleneck only |
| Software | software_repo_mapper | Luna | high | read-only | Codebase/call-path mapping |
| Software | software_dependency_researcher | Terra | high | read-only | API/version/dependency verification |
| Software | software_builder | Terra | high | workspace-write | Routine bounded implementation |
| Software | software_senior_builder | Sol | high | workspace-write | Complex multi-file implementation |
| Software | software_architect | Sol | high | read-only | Architecture and migration design |
| Software | software_debugger | Sol | high | workspace-write | Root-cause debug and fix |
| Software | software_test_engineer | Terra | high | workspace-write | Regression/edge-case tests |
| Software | software_reviewer | Sol | high | read-only | Owner-level review |
| Software | software_integration_owner | Sol | high | workspace-write | Final single-writer integration |
| Software | software_astra_debug_specialist | Astra | medium | read-only | Persistent/novel software failures |
| CAD/3DP | cad_geometry_inspector | Terra | high | read-only | STEP/STL/BRep measurements/topology |
| CAD/3DP | cad_reference_researcher | Terra | high | read-only | Proven mechanisms/standards/material refs |
| CAD/3DP | cad_recipe_engineer | Sol | medium | workspace-write | Typed deterministic CAD recipe |
| CAD/3DP | cad_model_builder | Terra | high | workspace-write | Bounded CAD execution |
| CAD/3DP | cad_mechanism_engineer | Sol | high | read-only | Kinematics/load-path/mechanism design |
| CAD/3DP | cad_3dp_dfm_engineer | Sol | medium | read-only | FDM/DFMA/process review |
| CAD/3DP | cad_simulation_analyst | Sol | high | read-only | FEM/CAE setup and interpretation |
| CAD/3DP | cad_optimization_engineer | Sol | high | read-only | Mass/stiffness/load-path optimization |
| CAD/3DP | cad_integration_owner | Sol | high | workspace-write | Final mechanical integration |
| CAD/3DP | cad_astra_mechanism_specialist | Astra | medium | read-only | Novel/conflicting mechanism reasoning |
| Research | research_scout | Luna | medium | read-only | Cheap source scouting |
| Research | research_deep_researcher | Terra | high | read-only | Evidence collection/comparison |
| Research | research_synthesizer | Sol | high | read-only | High-quality synthesis |
| Research | research_fact_checker | Sol | high | read-only | Citation/scope/version audit |
| Data | data_analyst | Terra | high | workspace-write | Reproducible bounded analysis |
| Document | document_editor | Terra | high | workspace-write | Structured document transformation |

Astra is deliberately absent from bulk writing. If Astra supplies the decisive diagnosis or mechanism concept, implementation returns to a Sol/Terra owner unless the later router explicitly chooses a rescue path.
