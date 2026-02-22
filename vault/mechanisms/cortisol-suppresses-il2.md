---
id: cortisol-suppresses-il2
source: cortisol
target: il-2
relationship: inhibits
direction: inhibitory
mechanism_type: direct
scale: molecular
evidence_type: experimental
evidence_strength: strong
temporal_lag: hours
reversible: true
context: "Cortisol-GR suppresses IL-2 transcription in T-cells via transrepression of NF-AT and AP-1, reducing T-cell proliferation and clonal expansion"
species: human
sources:
  - doi: "doi:10.1038/nri3552"
    study_type: review
    sample_size: null
    year: 2013
  - doi: "doi:10.1016/j.it.2004.09.007"
    study_type: review
    sample_size: null
    year: 2004
confidence: 0.90
holon_context: [adaptive-immune-response, glucocorticoid-feedback]
contradicted_by: []
---

# Cortisol Suppresses IL-2 Transcription

## Causal Claim

[[cortisol]] **inhibits** [[il-2]] gene transcription in T-lymphocytes through [[gr]]-mediated transrepression of the transcription factors NFAT and AP-1, reducing T-cell autocrine proliferative signaling and suppressing clonal expansion of activated T-cells.

## Molecular Mechanism

[[il-2]] is the principal autocrine growth factor for T-lymphocytes, essential for clonal expansion following antigen-driven T-cell receptor (TCR) activation. The IL-2 gene promoter is one of the most intensively studied cytokine promoters and contains binding sites for multiple transcription factors that must cooperatively engage for maximal transcription: NFAT (nuclear factor of activated T-cells), AP-1 (Fos/Jun heterodimer), [[nf-kb]], and Oct-1. Upon TCR engagement and costimulatory signaling, calcineurin dephosphorylates NFAT, enabling its nuclear translocation, while Ras/MAPK signaling activates AP-1 through phosphorylation of c-Jun and induction of c-Fos. The cooperative binding of NFAT and AP-1 at composite NFAT:AP-1 elements in the IL-2 promoter is the critical event that drives transcriptional activation.

[[cortisol]] suppresses [[il-2]] transcription through [[gr]]-mediated interference with these TCR-driven transcription factors. The ligand-bound [[gr]], upon nuclear translocation, engages in direct protein-protein interactions with both AP-1 and NFAT through its DNA-binding domain and hinge region. The [[gr]]-AP-1 interaction involves physical binding between the [[gr]] zinc finger domain and the leucine zipper domain of c-Jun, preventing AP-1 from engaging its cognate DNA elements in the IL-2 promoter. The [[gr]]-NFAT interaction, though less completely characterized structurally, similarly disrupts NFAT DNA binding and transactivation function. Because the composite NFAT:AP-1 site requires simultaneous occupancy by both factors, [[gr]]-mediated interference with either factor is sufficient to collapse the cooperative enhanceosome and silence [[il-2]] transcription. Additionally, [[gr]] can interact with [[nf-kb]] p65 at the IL-2 promoter through the same transrepression mechanism operative at inflammatory cytokine promoters (detailed in [[cortisol-suppresses-nfkb]]), providing a third point of transcriptional interference.

Beyond transrepression, [[cortisol]] modulates T-cell IL-2 signaling through additional mechanisms. [[gr]] activation induces GILZ (glucocorticoid-induced leucine zipper), a protein that inhibits [[nf-kb]] and AP-1 activity, providing sustained suppression of [[il-2]] transcription even after [[gr]] itself has been recycled. [[cortisol]] also reduces IL-2 receptor alpha-chain (CD25) expression on T-cells through [[gr]]-dependent mechanisms, diminishing T-cell sensitivity to whatever [[il-2]] is produced and amplifying the functional impact of reduced [[il-2]] secretion. The combined effect of reduced [[il-2]] production and reduced IL-2 receptor expression profoundly suppresses the autocrine proliferative loop that drives T-cell clonal expansion.

## Downstream Cascade

Suppression of [[il-2]] has far-reaching consequences for adaptive immune function. Reduced [[il-2]] availability impairs T-cell proliferation (clonal expansion), the process by which a small number of antigen-specific T-cells multiply to generate an effector population sufficient to clear infection or reject foreign tissue. Impaired [[il-2]] signaling also reduces the survival and function of cytotoxic CD8+ T-cells, decreases NK cell cytotoxicity (NK cells are IL-2-responsive), and -- critically -- impairs the development and maintenance of regulatory T-cells (Tregs), which paradoxically depend on [[il-2]] for survival via high-affinity CD25 expression. This creates a complex immunological outcome: acute cortisol-mediated [[il-2]] suppression broadly immunosuppresses T-cell function, while chronic cortisol-mediated [[il-2]] depletion can paradoxically reduce Treg-mediated immune tolerance, contributing to the complex immune dysregulation observed in chronic stress states.

## Context and Conditions

This mechanism operates in all T-cell subsets but is most functionally significant in recently activated CD4+ T-helper cells, where [[il-2]] production is highest and the autocrine proliferative loop is most active. The temporal lag of hours reflects the requirement for sustained [[gr]] nuclear occupancy to effectively suppress the rapidly induced [[il-2]] transcriptional response. The dose-response relationship shows that physiological stress-level cortisol concentrations (300-600 nM total) are sufficient to produce measurable [[il-2]] suppression, while pharmacological glucocorticoid doses produce near-complete silencing of [[il-2]] production -- the basis for the immunosuppressive use of glucocorticoids in transplant rejection and autoimmune disease. The suppressive effect is reversible: upon cortisol withdrawal, [[il-2]] transcription recovers as [[gr]] returns to the cytoplasm and the TCR-driven enhanceosome reassembles, consistent with the reversible nature specified in the frontmatter. Calcineurin inhibitors (cyclosporine, tacrolimus) block [[il-2]] transcription through the parallel mechanism of NFAT inhibition, and the combination of glucocorticoids with calcineurin inhibitors produces synergistic [[il-2]] suppression -- the basis of modern transplant immunosuppression protocols.

## Cross-Holon Implications

This mechanism extends the immunomodulatory reach of [[cortisol]] from the [[innate-immune-response]] holon (where [[nf-kb]] suppression dampens innate cytokine production) into the [[adaptive-immune-response]] holon, where [[il-2]] suppression constrains T-cell clonal expansion and effector function. The cortisol-[[il-2]] axis is a key component of the broader cortisol-mediated Th1/Th2 shift (detailed in [[cortisol-shifts-th1-to-th2]]), as [[il-2]] is a prototypical Th1 cytokine whose suppression tilts the T-helper balance toward Th2 dominance. Within the [[glucocorticoid-feedback]] holon, [[il-2]] suppression represents one of the most clinically exploited consequences of [[gr]] activation, underlying the use of glucocorticoids in virtually all transplant rejection protocols, graft-versus-host disease, autoimmune conditions, and allergic diseases. The connection between chronic [[hpa-axis]] hyperactivity (elevated cortisol) and impaired adaptive immunity -- manifested as increased susceptibility to viral infections, reduced vaccine responses, and impaired tumor immunosurveillance -- is substantially mediated through this cortisol-[[il-2]] suppressive mechanism.
