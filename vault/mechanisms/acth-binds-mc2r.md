---
id: acth-binds-mc2r
source: acth
target: mc2r
relationship: activates
direction: excitatory
mechanism_type: direct
scale: molecular
evidence_type: experimental
evidence_strength: strong
temporal_lag: seconds
reversible: true
context: "ACTH binds MC2R (melanocortin 2 receptor) on adrenocortical cells, activating the Gs-coupled receptor and triggering cAMP/PKA signaling cascade that initiates steroidogenesis"
species: human
sources:
  - doi: "doi:10.1016/j.mce.2013.06.005"
    study_type: experimental
    sample_size: null
    year: 2013
  - doi: "doi:10.1210/er.2003-0010"
    study_type: review
    sample_size: null
    year: 2004
confidence: 0.95
holon_context: [hpa-axis, adrenal-cortex-steroidogenesis]
contradicted_by: []
---

# ACTH Binds and Activates MC2R

## Causal Claim

[[acth]] **activates** [[mc2r]] (melanocortin 2 receptor) on adrenocortical zona fasciculata cells through direct ligand-receptor binding, initiating the Gs-coupled cAMP/PKA signaling cascade that drives steroidogenesis within seconds of receptor engagement.

## Molecular Mechanism

The melanocortin 2 receptor ([[mc2r]]) is a 297-amino-acid seven-transmembrane G protein-coupled receptor (GPCR) belonging to the melanocortin receptor family (MC1R-MC5R), and it is unique among this family in being selectively activated by [[acth]] rather than by the other melanocortin peptides (alpha-MSH, beta-MSH, gamma-MSH). [[mc2r]] is expressed predominantly in the adrenal cortex, with highest density on zona fasciculata cells (cortisol-producing) and zona reticularis cells (adrenal androgen-producing), and lower expression on zona glomerulosa cells. A distinguishing feature of [[mc2r]] is its absolute requirement for the melanocortin 2 receptor accessory protein (MRAP1) for proper folding, endoplasmic reticulum export, and cell-surface expression. Without MRAP1, [[mc2r]] is retained in the ER and never reaches the plasma membrane, rendering the cell completely unresponsive to [[acth]] -- the molecular basis of familial glucocorticoid deficiency type 2 (FGD2), caused by MRAP1 mutations.

[[acth]] binding to [[mc2r]] involves the N-terminal "message" sequence of [[acth]] (residues 1-13, the biologically active core shared with alpha-MSH) engaging the transmembrane domain binding pocket, while the "address" sequence (residues 15-18, the KKRRP motif unique to [[acth]]) interacts with extracellular loop and N-terminal domain residues that confer [[mc2r]] selectivity. This dual interaction ensures that only [[acth]] (and not shorter melanocortins) can fully activate [[mc2r]]. Upon [[acth]] binding, [[mc2r]] undergoes a conformational change that activates the coupled Gs-alpha subunit, which exchanges GDP for GTP and dissociates from the beta-gamma complex. Activated Gs-alpha directly stimulates adenylyl cyclase (primarily isoforms AC5 and AC6 in adrenocortical cells), catalyzing the conversion of ATP to cyclic AMP (cAMP). The resulting rise in intracellular cAMP activates protein kinase A (PKA) by binding to the regulatory subunits of the PKA holoenzyme, releasing the catalytic subunits to phosphorylate downstream targets.

The temporal dynamics of this receptor activation are remarkably rapid. [[acth]] binding to [[mc2r]] occurs within seconds, Gs activation and cAMP generation follow within 10-30 seconds, and PKA activation is measurable within 1-2 minutes. This places the [[acth]]-[[mc2r]] interaction among the fastest hormone-receptor coupling events in endocrinology. The receptor system also exhibits rapid desensitization: G protein-coupled receptor kinase 2 (GRK2) phosphorylates activated [[mc2r]], promoting beta-arrestin recruitment, receptor internalization via clathrin-coated pits, and transient signal termination. However, MRAP1 modulates this desensitization process, and [[mc2r]] shows relatively sustained signaling compared to many other GPCRs, consistent with the need for prolonged cAMP elevation to drive steroidogenic gene transcription during sustained [[acth]] stimulation.

## Downstream Cascade

The cAMP/PKA signaling initiated by [[acth]]-[[mc2r]] binding drives a cascade of steroidogenic events. The immediate PKA target of greatest importance is [[star]] protein, whose phosphorylation at Ser194/195 activates cholesterol transfer from the outer to inner mitochondrial membrane, the rate-limiting step in steroidogenesis (detailed in [[acth-stimulates-cortisol]]). PKA also phosphorylates CREB, driving transcription of steroidogenic genes including CYP11A1, CYP17A1, CYP21A2, CYP11B1, and StAR itself, ensuring sustained biosynthetic capacity. Longer-term, [[acth]]-[[mc2r]] signaling maintains adrenocortical cell viability and prevents apoptosis through PKA-dependent activation of pro-survival pathways (Akt, ERK). Chronic [[acth]] stimulation drives adrenocortical cell proliferation and hypertrophy (trophic effect), while chronic [[acth]] deprivation leads to zona fasciculata atrophy. The end result of this signaling cascade is [[cortisol]] secretion, which then engages the full downstream network of metabolic, immune, and feedback mechanisms described throughout this vault.

## Context and Conditions

The sensitivity of adrenocortical cells to [[acth]] is determined by [[mc2r]] surface expression, MRAP1 availability, and the activity of downstream signaling components. Under normal conditions, the adrenal cortex responds to picomolar concentrations of [[acth]] with measurable cortisol output, reflecting the high receptor density and efficient Gs coupling. The [[acth]]-[[mc2r]] dose-response curve is sigmoidal, with half-maximal cortisol output occurring at approximately 10-20 pg/mL of [[acth]] and maximal output at approximately 100-200 pg/mL. Supraphysiological [[acth]] does not produce further cortisol increase, indicating receptor and enzymatic saturation. Chronic [[acth]] stimulation upregulates [[mc2r]] and MRAP1 expression, increasing adrenal sensitivity (a feedforward mechanism), while chronic [[acth]] deprivation (as during exogenous glucocorticoid therapy) downregulates [[mc2r]] and produces adrenal atrophy, explaining why abrupt glucocorticoid withdrawal can precipitate adrenal crisis. Mutations in [[mc2r]] (producing familial glucocorticoid deficiency type 1, FGD1) or MRAP1 (FGD2) cause selective cortisol deficiency with preserved aldosterone production (since aldosterone is primarily regulated by the renin-angiotensin system rather than [[acth]]), demonstrating the non-redundant role of this receptor in cortisol biosynthesis.

## Cross-Holon Implications

The [[acth]]-[[mc2r]] interaction is the molecular gate between the neuroendocrine signal ([[acth]] from the [[hpa-axis]] holon) and the steroidogenic output ([[cortisol]] from the [[adrenal-cortex-steroidogenesis]] holon). It is the single point through which the entire [[hpa-axis]] signal is transduced into adrenal steroid output, making [[mc2r]] a critical node in the causal metagraph. The dependence of [[mc2r]] on MRAP1 for function adds a regulatory layer unique among melanocortin receptors and makes MRAP1 a potential pharmacological target for modulating [[hpa-axis]] output. The cAMP/PKA signal generated by [[mc2r]] activation is shared with many other GPCR systems, but its specific coupling to [[star]] phosphorylation and steroidogenic enzyme gene expression in adrenocortical cells creates a tissue-specific output (cortisol) from a generic second messenger (cAMP). This receptor edge also connects to the [[innate-immune-response]] holon indirectly: the [[cortisol]] produced downstream of [[mc2r]] activation is the primary endogenous suppressor of [[nf-kb]]-driven inflammatory cytokine production, meaning that loss of [[mc2r]] function (as in FGD) eliminates the body's primary anti-inflammatory hormone and can produce life-threatening inflammatory dysregulation during infection or stress.
