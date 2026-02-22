---
id: cortisol-induces-annexin-a1
source: cortisol
target: annexin-a1
relationship: upregulates
direction: excitatory
mechanism_type: direct
scale: molecular
evidence_type: experimental
evidence_strength: strong
temporal_lag: hours
reversible: true
context: "Cortisol-GR complex activates annexin-a1 (lipocortin-1) gene transcription via GRE binding; annexin-a1 then inhibits PLA2 and COX-2, contributing to anti-inflammatory glucocorticoid actions"
species: human
sources:
  - doi: "doi:10.1016/j.pharmthera.2007.01.005"
    study_type: review
    sample_size: null
    year: 2007
  - doi: "doi:10.1038/nrd3524"
    study_type: review
    sample_size: null
    year: 2012
confidence: 0.90
holon_context: [innate-immune-response, glucocorticoid-feedback]
contradicted_by: []
---

# Cortisol Induces Annexin A1 Expression

## Causal Claim

[[cortisol]] **upregulates** [[annexin-a1]] (lipocortin-1) gene expression through [[gr]]-mediated transactivation, producing a key anti-inflammatory mediator that inhibits phospholipase A2 ([[pla2]]) and suppresses prostaglandin synthesis downstream of [[cox-2]].

## Molecular Mechanism

[[annexin-a1]] (formerly known as lipocortin-1) is a 37-kDa calcium-dependent phospholipid-binding protein that was identified in the 1980s as one of the principal mediators of the anti-inflammatory effects of glucocorticoids. The induction of [[annexin-a1]] by [[cortisol]] proceeds through classical [[gr]]-mediated transactivation. When [[cortisol]] binds cytoplasmic [[gr]], the receptor sheds its HSP90 chaperone complex, dimerizes, and translocates to the nucleus, where it binds to glucocorticoid response elements (GREs) in the ANXA1 gene promoter region. This binding recruits coactivator complexes including SRC-1 (steroid receptor coactivator-1) and CBP/p300, which acetylate local histones and open chromatin, facilitating RNA polymerase II recruitment and ANXA1 mRNA transcription. The temporal lag of this induction is on the order of hours, as it requires de novo transcription and translation to produce functional [[annexin-a1]] protein.

Once synthesized, [[annexin-a1]] exerts its anti-inflammatory effects through both intracellular and extracellular mechanisms. Intracellularly, [[annexin-a1]] binds to and inhibits cytosolic phospholipase A2 ([[pla2]]), the enzyme responsible for cleaving arachidonic acid from membrane phospholipids. Arachidonic acid is the obligate substrate for both cyclooxygenase ([[cox-2]]) and lipoxygenase (5-LOX) pathways, so [[annexin-a1]]-mediated [[pla2]] inhibition simultaneously reduces production of prostaglandins (PGE2, PGD2, PGI2), thromboxanes (TXA2), and leukotrienes (LTB4, LTC4). This substrate-level inhibition is mechanistically distinct from and complementary to the direct suppression of [[cox-2]] gene expression by [[cortisol]] via [[nf-kb]] transrepression, providing a two-tier anti-inflammatory blockade of the prostanoid pathway.

Extracellularly, [[annexin-a1]] is secreted from cells (particularly neutrophils, macrophages, and epithelial cells) and binds to formyl peptide receptors (FPR2/ALX) on neighboring immune cells. FPR2 activation by [[annexin-a1]] triggers signaling cascades that inhibit neutrophil transmigration across endothelial barriers, promote macrophage efferocytosis (phagocytic clearance of apoptotic cells), and reduce pro-inflammatory cytokine release. These paracrine and autocrine effects position [[annexin-a1]] as a critical mediator of the resolution phase of inflammation, actively promoting the return to tissue homeostasis rather than merely suppressing inflammatory signals. Recent evidence also suggests that [[annexin-a1]] can modulate adaptive immune responses by influencing dendritic cell maturation and T-cell activation thresholds.

## Downstream Cascade

The induction of [[annexin-a1]] creates a downstream anti-inflammatory cascade that extends beyond simple enzyme inhibition. Reduced arachidonic acid release diminishes substrate availability for both [[cox-2]] and 5-lipoxygenase, decreasing prostaglandin, thromboxane, and leukotriene production. Reduced PGE2 levels attenuate pain sensitization, fever, and inflammatory vasodilation. Reduced LTB4 production decreases neutrophil chemotaxis and degranulation. The extracellular [[annexin-a1]] acting through FPR2 promotes the switch from pro-inflammatory to pro-resolving lipid mediator profiles, facilitating the generation of lipoxins, resolvins, and protectins that actively drive inflammation resolution. This positions [[annexin-a1]] induction as a bridge between the suppressive and pro-resolving arms of the glucocorticoid anti-inflammatory response.

## Context and Conditions

[[annexin-a1]] induction is most prominent in cells of the innate immune system, particularly neutrophils, monocytes, and macrophages, where both [[gr]] expression and [[pla2]] activity are high. The magnitude of [[annexin-a1]] induction is dose-dependent on [[cortisol]] concentration and requires sustained glucocorticoid exposure (hours), making this mechanism more relevant to the sustained anti-inflammatory effects of cortisol than to rapid immunomodulation. In some cell types, [[annexin-a1]] is constitutively expressed and rapidly externalized upon glucocorticoid exposure, suggesting a reservoir mechanism for rapid deployment. Chronic glucocorticoid treatment can eventually downregulate [[annexin-a1]] expression through [[gr]] desensitization, which may contribute to the phenomenon of glucocorticoid tolerance in long-term therapy. Post-translational modifications, including phosphorylation at Ser27 and proteolytic cleavage of the N-terminal domain, regulate [[annexin-a1]] bioactivity and receptor binding affinity, adding complexity beyond simple transcriptional regulation.

## Cross-Holon Implications

This mechanism provides a critical link between the [[glucocorticoid-feedback]] holon and the [[innate-immune-response]] holon through the lipid mediator pathway. While [[cortisol]] suppression of [[nf-kb]] acts on the transcription factor level, [[annexin-a1]] induction operates at the enzymatic and substrate level, providing an independent and complementary anti-inflammatory mechanism. The extracellular signaling functions of [[annexin-a1]] through FPR2 connect to the broader resolution-of-inflammation network, linking glucocorticoid signaling to the specialized pro-resolving mediator (SPM) pathway. In [[annexin-a1]]-deficient animal models, glucocorticoid anti-inflammatory efficacy is significantly impaired, demonstrating that this edge carries substantial mechanistic weight rather than being a redundant pathway. The ability of [[annexin-a1]] to promote efferocytosis also connects to tissue repair and remodeling holons, illustrating how a single cortisol-induced protein can bridge neuroendocrine, immune, and tissue homeostasis domains.
