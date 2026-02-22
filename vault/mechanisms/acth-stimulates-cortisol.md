---
id: acth-stimulates-cortisol
source: acth
target: cortisol
relationship: stimulates
direction: excitatory
mechanism_type: direct
scale: molecular
evidence_type: experimental
evidence_strength: strong
temporal_lag: minutes
reversible: true
context: "ACTH binding to MC2R on zona fasciculata cells activates cAMP/PKA cascade, phosphorylates StAR protein, and drives cholesterol transport and cortisol biosynthesis"
species: human
sources:
  - doi: "doi:10.1210/er.2003-0010"
    study_type: review
    sample_size: null
    year: 2004
  - doi: "doi:10.1016/j.mce.2013.06.005"
    study_type: experimental
    sample_size: null
    year: 2013
confidence: 0.95
holon_context: [hpa-axis, adrenal-cortex-steroidogenesis]
contradicted_by: []
---

# ACTH Stimulates Cortisol Synthesis

## Causal Claim

[[acth]] **stimulates** [[cortisol]] biosynthesis through direct receptor-mediated activation of the adrenocortical steroidogenic cascade in [[zona-fasciculata]] cells of the adrenal cortex.

## Molecular Mechanism

The stimulation of [[cortisol]] production by [[acth]] represents one of the most thoroughly characterized endocrine signaling cascades in human physiology. [[acth]], a 39-amino-acid peptide cleaved from the precursor polypeptide [[pomc]] in anterior pituitary corticotrophs, circulates to the adrenal glands where it binds with high affinity to the [[mc2r]] (melanocortin 2 receptor) on the plasma membrane of zona fasciculata cells. The [[mc2r]] is a Gs-protein-coupled receptor that requires the accessory protein MRAP (melanocortin 2 receptor accessory protein) for proper folding and cell-surface expression. Upon [[acth]] binding, the Gs-alpha subunit activates adenylyl cyclase, catalyzing the conversion of ATP to cyclic AMP (cAMP), which in turn activates protein kinase A (PKA).

PKA phosphorylation events constitute the critical regulatory switch in adrenal steroidogenesis. The most important substrate is the [[star]] protein (steroidogenic acute regulatory protein), whose phosphorylation at Ser194/195 activates its cholesterol-shuttling function. Phosphorylated [[star]] facilitates the transfer of cholesterol from the outer to the inner mitochondrial membrane, a step universally recognized as the rate-limiting event in steroid hormone biosynthesis. Without [[acth]]-driven PKA activation, cholesterol remains sequestered in the outer membrane and steroidogenesis stalls, regardless of enzyme abundance. PKA also upregulates the transcription of steroidogenic enzymes including CYP11A1, CYP17A1, CYP21A2, and CYP11B1, ensuring sustained biosynthetic capacity during prolonged [[acth]] stimulation.

Once cholesterol reaches the inner mitochondrial membrane, the enzymatic cascade proceeds through a well-characterized series of hydroxylation reactions. CYP11A1 (cholesterol side-chain cleavage enzyme, also known as P450scc) converts cholesterol to pregnenolone, which exits the mitochondria and enters the endoplasmic reticulum where CYP17A1 catalyzes 17-alpha-hydroxylation to produce 17-hydroxypregnenolone. Subsequent oxidation by 3-beta-HSD2 yields 17-hydroxyprogesterone, which CYP21A2 hydroxylates to 11-deoxycortisol. The final step returns to the mitochondria, where CYP11B1 performs 11-beta-hydroxylation to generate [[cortisol]]. The entire process from [[acth]] receptor binding to detectable cortisol secretion occurs within minutes, reflecting the pre-positioned enzymatic machinery and the dependence primarily on the [[star]]-mediated cholesterol transport step.

## Downstream Cascade

The [[cortisol]] released into the adrenal venous blood enters systemic circulation where it binds to corticosteroid-binding globulin ([[cbg]]) and albumin, with approximately 5-10% remaining free and biologically active. This free [[cortisol]] then mediates the broad spectrum of glucocorticoid effects: binding to [[gr]] in hypothalamic and pituitary cells to complete the [[hpa-axis]] negative feedback loop (suppressing both [[crh]] and [[acth]]), transrepressing [[nf-kb]] in immune cells to dampen inflammatory cytokine production including [[il-6]], [[il-1beta]], and [[tnf-alpha]], and activating metabolic programs in liver, muscle, and adipose tissue. The rapid temporal dynamics of this mechanism -- minutes from [[acth]] stimulus to cortisol output -- enable the [[hpa-axis]] to mount proportionate stress responses while maintaining the capacity for rapid feedback inhibition.

## Context and Conditions

This mechanism operates under tonic and pulsatile [[acth]] stimulation, with cortisol output reflecting both the amplitude and frequency of [[acth]] pulses rather than simply the mean [[acth]] concentration. The circadian rhythm of cortisol secretion is fundamentally driven by the circadian patterning of [[crh]] and [[acth]] pulses originating from the suprachiasmatic nucleus. The mechanism saturates at supraphysiological [[acth]] concentrations, as the adrenal cortex has a finite complement of [[mc2r]] receptors and steroidogenic enzyme capacity. Chronic [[acth]] stimulation (as in Cushing disease or ectopic [[acth]] syndromes) produces adrenal hyperplasia and increased cortisol output, while chronic [[acth]] deficiency leads to adrenal atrophy of the zona fasciculata. Local tissue factors including intra-adrenal [[crh]], cytokines, and adrenomedullary catecholamines can modulate the sensitivity of this mechanism. The enzyme [[11beta-hsd2]] in mineralocorticoid target tissues and [[11beta-hsd1]] in liver and adipose tissue further regulate the local bioavailability of [[cortisol]] downstream of this synthetic step.

## Cross-Holon Implications

This mechanism is the central effector link within the [[hpa-axis]] holon, connecting the neuroendocrine signal ([[acth]]) to the systemic hormonal output ([[cortisol]]). It bridges directly into the [[adrenal-cortex-steroidogenesis]] holon, as the enzymatic cascade it activates is shared with aldosterone and adrenal androgen synthesis pathways. The [[cortisol]] produced by this mechanism feeds forward into the [[glucocorticoid-feedback]] holon by activating [[gr]]-mediated negative feedback, and into the [[innate-immune-response]] holon by suppressing [[nf-kb]]-driven cytokine cascades. Disruption of this single edge -- whether by adrenal destruction (Addison disease), enzymatic defects (congenital adrenal hyperplasia), or receptor mutations (familial glucocorticoid deficiency) -- collapses the entire downstream cortisol signaling network, underscoring its critical position in the causal metagraph.
