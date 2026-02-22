---
id: gr-mediates-feedback
source: gr
target: crh
relationship: inhibits
direction: inhibitory
mechanism_type: direct
scale: molecular
evidence_type: experimental
evidence_strength: strong
temporal_lag: hours
reversible: true
context: "GR activation by cortisol mediates negative feedback at hypothalamic and pituitary levels, suppressing CRH and ACTH to constrain HPA axis output"
species: human
sources:
  - doi: "doi:10.1210/er.2003-0010"
    study_type: review
    sample_size: null
    year: 2004
  - doi: "doi:10.1016/j.neubiorev.2009.09.005"
    study_type: review
    sample_size: null
    year: 2010
confidence: 0.95
holon_context: [glucocorticoid-feedback, hpa-axis]
contradicted_by: []
---

# GR Mediates Glucocorticoid Negative Feedback

## Causal Claim

[[gr]] (glucocorticoid receptor, NR3C1) **inhibits** [[crh]] gene expression and release when activated by [[cortisol]], mediating the negative feedback mechanism at hypothalamic and pituitary levels that constrains [[hpa-axis]] output and maintains neuroendocrine homeostasis.

## Molecular Mechanism

The [[gr]] is a 777-amino-acid ligand-activated nuclear receptor belonging to the NR3C subfamily, expressed ubiquitously but with particularly high density in parvocellular neurons of the PVN, hippocampal pyramidal neurons, and anterior pituitary corticotrophs -- the three primary sites of [[hpa-axis]] negative feedback. The [[gr]] has a relatively low affinity for [[cortisol]] (Kd approximately 20-30 nM), meaning it is only substantially occupied at the stress-range cortisol concentrations (above 100 nM) that exceed the capacity of the higher-affinity [[mr]] (Kd approximately 0.5-1 nM). This affinity differential creates a two-tier receptor system: [[mr]] mediates tonic, basal feedback at low cortisol concentrations, while [[gr]] mediates the reactive, stress-level feedback that is the subject of this mechanism edge.

In the unliganded state, [[gr]] resides in the cytoplasm complexed with molecular chaperones HSP90, HSP70, and the immunophilins FKBP51 and FKBP52. [[cortisol]] binding induces a conformational change that releases the chaperone complex, exposes a nuclear localization signal, and triggers importin-alpha/beta-mediated nuclear translocation. Within the nucleus, ligand-bound [[gr]] can function as a homodimer binding to GREs, as a monomer interacting with other transcription factors, or through non-canonical mechanisms. At the [[crh]] promoter in PVN neurons, [[gr]] mediates transcriptional repression through binding to negative GREs (nGREs) and through tethering transrepression of CREB and other positive regulators of [[crh]] transcription, as detailed in the [[cortisol-inhibits-crh]] mechanism. At the [[pomc]] promoter in corticotrophs, [[gr]] similarly represses transcription through nGRE binding and interference with the corticotroph-specific transcription factors Nur77 and Tpit, as detailed in the [[cortisol-inhibits-acth]] mechanism.

A critical feature of [[gr]]-mediated feedback is its autoregulatory modulation through the FKBP5 gene. [[gr]] activation drives transcription of FKBP51 (encoded by FKBP5), a co-chaperone that competes with FKBP52 for binding to the [[gr]]-HSP90 complex. FKBP51 reduces [[gr]] nuclear translocation efficiency and thus dampens [[gr]] signaling, creating an ultrashort negative feedback loop that limits [[gr]] responsiveness during sustained cortisol elevation. FKBP5 polymorphisms and epigenetic modifications at the FKBP5 locus are strongly associated with individual differences in [[hpa-axis]] reactivity and risk for stress-related psychiatric disorders, demonstrating the clinical importance of this molecular feedback mechanism. Additionally, [[gr]] abundance is itself subject to autoregulation: prolonged cortisol elevation downregulates [[gr]] mRNA and protein through both transcriptional (repression of the NR3C1 promoter) and post-translational (ubiquitin-proteasome degradation of activated [[gr]]) mechanisms.

## Downstream Cascade

The functional consequence of [[gr]]-mediated feedback is restraint of [[hpa-axis]] output at two levels. At the hypothalamus, [[gr]] suppression of [[crh]] transcription reduces the excitatory drive on corticotrophs, decreasing [[acth]] secretion. At the pituitary, [[gr]] suppression of [[pomc]] transcription and [[crh-r1]] expression reduces both [[acth]] biosynthesis and corticotroph sensitivity to [[crh]]. The combined effect is a proportional reduction in adrenal [[cortisol]] output, completing the negative feedback loop. In the hippocampus, [[gr]] activation in CA1 pyramidal neurons enhances inhibitory projections to the PVN through multi-synaptic circuits, providing an additional layer of central feedback. The integrity of [[gr]] function at all three sites determines the overall gain and set point of the [[hpa-axis]], with [[gr]] impairment at any site producing proportional increases in basal and stress-evoked cortisol output.

## Context and Conditions

[[gr]]-mediated feedback is concentration-dependent, engaging progressively as cortisol levels rise above the threshold for significant [[gr]] occupancy. At basal morning cortisol levels (approximately 300-500 nM total, 15-25 nM free), [[gr]] occupancy is estimated at 30-50%, providing moderate tonic feedback. At peak stress cortisol levels (500-1000 nM total), [[gr]] occupancy approaches 70-90%, producing maximal feedback inhibition. This dose-response relationship ensures that feedback intensity scales with the magnitude of [[hpa-axis]] activation. Several pathological conditions impair [[gr]]-mediated feedback: chronic stress-induced [[gr]] downregulation reduces receptor density, pro-inflammatory cytokines ([[il-1beta]], [[il-6]], [[tnf-alpha]]) can activate [[nf-kb]] and AP-1 in hypothalamic cells, which interfere with [[gr]] transcriptional activity through mutual transrepression, producing a state of central glucocorticoid resistance. Epigenetic silencing of the NR3C1 gene (encoding [[gr]]) through promoter methylation, as observed following early-life adversity, produces a long-lasting reduction in [[gr]] expression and impaired feedback that can persist into adulthood. Conversely, enriched early-life environments are associated with enhanced NR3C1 expression and more efficient [[gr]]-mediated feedback.

## Cross-Holon Implications

[[gr]]-mediated feedback is the molecular machinery that implements the [[glucocorticoid-feedback]] holon. Without functional [[gr]], the entire negative feedback architecture of the [[hpa-axis]] collapses, producing unrestrained [[crh]] and [[acth]] secretion and cortisol hypersecretion -- a state approximated by the rare condition of generalized glucocorticoid resistance (Chrousos syndrome) due to NR3C1 loss-of-function mutations. The intersection of [[gr]] function with [[nf-kb]] signaling creates a bidirectional bridge between the [[glucocorticoid-feedback]] holon and the [[innate-immune-response]] holon: [[gr]] suppresses [[nf-kb]] (the [[cortisol-suppresses-nfkb]] mechanism), while [[nf-kb]] impairs [[gr]] function (mutual transrepression), establishing a competitive equilibrium between inflammatory and anti-inflammatory signaling. This molecular tug-of-war at the [[gr]] level is the fundamental mechanism determining whether the organism resolves inflammation and returns to homeostasis or enters a pathological state of chronic inflammation with glucocorticoid resistance, making [[gr]] the single most important molecular node in the cross-holon architecture of stress and immune regulation.
