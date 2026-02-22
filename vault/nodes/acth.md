---
id: acth
type: molecule
scale: molecular
aliases: [adrenocorticotropin, corticotropin]
holon_membership: [hpa-axis, pituitary-acth-release]
confidence: 0.95
sources:
  - "doi:10.1210/er.2003-0010"
  - "doi:10.1210/endrev/bnaa020"
tags: [peptide-hormone, pituitary-hormone]
---

# ACTH (Adrenocorticotropic Hormone)

Adrenocorticotropic hormone (ACTH) is a 39-amino-acid polypeptide hormone produced by corticotroph cells in the anterior pituitary gland. It is derived from post-translational cleavage of pro-opiomelanocortin (POMC), a 241-amino-acid precursor protein that also gives rise to beta-endorphin, alpha-melanocyte-stimulating hormone (alpha-MSH), and beta-lipotropin through tissue-specific processing by prohormone convertases PC1 and PC2. ACTH has a plasma half-life of approximately 10 minutes and is rapidly degraded by endopeptidases. Its biological activity resides primarily within the first 24 amino acids of the N-terminal region (ACTH 1-24), which is sufficient for full activation of its cognate receptor, the [[mc2r]]. ACTH secretion is pulsatile, with approximately 7-15 secretory bursts per 24 hours superimposed on a circadian rhythm that parallels and drives the diurnal pattern of [[cortisol]] release.

ACTH is the central relay molecule of the [[hpa-axis]], transducing hypothalamic stress signals into adrenal glucocorticoid output. Corticotroph cells in the anterior pituitary integrate multiple afferent signals -- most prominently [[crh]] acting via CRH-R1 receptors and [[avp]] acting via V1b (V3) receptors -- to calibrate the magnitude and duration of ACTH secretory episodes. The synthesis and release of ACTH are tightly regulated at every level: transcriptionally (POMC gene expression is stimulated by [[crh]] and inhibited by [[cortisol]] via the [[gr]]), post-translationally (processing of POMC to ACTH), and at the level of secretory vesicle exocytosis.

## Upstream Causes

The principal stimulatory input to ACTH release is [[crh]], which is secreted from parvocellular neurons of the paraventricular nucleus (PVN) of the hypothalamus into the hypophyseal portal vasculature. [[crh]] binds to CRH-R1 (CRH receptor type 1) on corticotroph cells, activating Gs-coupled adenylyl cyclase, raising intracellular cAMP, and stimulating PKA-dependent exocytosis of ACTH-containing secretory granules. [[avp]], co-released with [[crh]] from parvocellular neurons, acts synergistically via V1b receptors coupled to Gq and phospholipase C, raising intracellular calcium and activating protein kinase C (PKC). While [[avp]] alone is a weak ACTH secretagogue, it potentiates [[crh]]-stimulated ACTH release by 2-3 fold. Pro-inflammatory cytokines, particularly [[il-6]], [[il-1beta]], and [[tnf-alpha]], can also directly stimulate ACTH secretion from corticotrophs, providing a direct immune-to-endocrine signaling pathway that bypasses hypothalamic [[crh]]. Additionally, catecholamines and other stress mediators modulate ACTH release through their effects on hypothalamic [[crh]] neurons.

## Downstream Effects

The primary downstream effect of ACTH is the stimulation of [[cortisol]] biosynthesis and secretion from the zona fasciculata of the adrenal cortex. ACTH binds to [[mc2r]] on adrenocortical cells, activating adenylyl cyclase and the cAMP/PKA signaling cascade. This rapidly (within minutes) increases cholesterol delivery to the inner mitochondrial membrane via StAR protein phosphorylation and, over longer time frames (hours to days), upregulates the expression of steroidogenic enzymes (CYP11A1, CYP17A1, CYP21A2, CYP11B1) required for [[cortisol]] synthesis. ACTH also exerts trophic effects on the adrenal cortex, maintaining adrenocortical cell mass, vascularity, and enzymatic capacity; chronic ACTH deficiency leads to adrenal atrophy, while chronic excess causes adrenal hyperplasia. Beyond steroidogenesis, ACTH stimulates adrenal androgen production (DHEA, androstenedione) and, at supraphysiological concentrations, can activate other melanocortin receptors (MC1R, MC3R, MC4R, MC5R), contributing to hyperpigmentation in conditions of ACTH excess such as Addison disease and Nelson syndrome.

## Holon Context

Within the [[hpa-axis]] holon, ACTH serves as the intermediate relay between hypothalamic neuropeptide signals ([[crh]], [[avp]]) and adrenal effector output ([[cortisol]]). It functions as a gain-control element: the amplitude and frequency of ACTH pulses determine the magnitude of adrenocortical activation, and thus the systemic glucocorticoid tone. ACTH is itself subject to negative feedback by [[cortisol]] acting via [[gr]] on corticotroph cells, creating a closed-loop control system. Within the [[pituitary-acth-release]] holon, ACTH release is the emergent output of intracellular signaling integration in corticotrophs, where cAMP (from [[crh]]) and calcium/PKC (from [[avp]]) pathways converge on secretory vesicle fusion machinery. The pulsatile and circadian patterns of ACTH secretion encode temporal information critical for maintaining [[cortisol]] rhythmicity and adrenal responsiveness.

## Clinical Relevance

ACTH measurement is fundamental to the differential diagnosis of adrenal disorders. Elevated ACTH with elevated [[cortisol]] suggests Cushing disease (pituitary corticotroph adenoma) or ectopic ACTH syndrome (e.g., small cell lung carcinoma), whereas suppressed ACTH with elevated [[cortisol]] indicates an autonomous adrenal source (adrenal adenoma, carcinoma, or exogenous glucocorticoid administration). In primary adrenal insufficiency (Addison disease), ACTH is markedly elevated due to loss of [[cortisol]] negative feedback, and the resulting melanocortin receptor activation produces characteristic skin hyperpigmentation. The ACTH stimulation test (Synacthen/cosyntropin test) using synthetic ACTH(1-24) is the gold standard for assessing adrenal reserve. Congenital defects in the [[mc2r]] receptor or its accessory protein MRAP (melanocortin-2 receptor accessory protein) cause familial glucocorticoid deficiency, a rare but instructive condition demonstrating the absolute requirement for ACTH-[[mc2r]] signaling in adrenal steroidogenesis.
