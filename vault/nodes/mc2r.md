---
id: mc2r
type: receptor
scale: molecular
aliases: [ACTH receptor, melanocortin type 2 receptor]
holon_membership: [adrenal-cortex-steroidogenesis]
confidence: 0.93
sources:
  - "doi:10.1210/er.2005-0011"
  - "doi:10.1016/j.mce.2011.06.032"
tags: [gpcr, melanocortin-receptor]
---

# MC2R (Melanocortin 2 Receptor)

The melanocortin 2 receptor (MC2R), commonly referred to as the ACTH receptor, is a 297-amino-acid class A G protein-coupled receptor (GPCR) encoded by the MC2R gene on chromosome 18p11.21. MC2R is unique among the five melanocortin receptors (MC1R-MC5R) in that it is exclusively activated by [[acth]] and does not respond to other melanocortin peptides such as alpha-MSH, beta-MSH, or gamma-MSH. This exquisite ligand specificity is determined by amino acid residues in the transmembrane domains and extracellular loops that create a binding pocket requiring the full ACTH(1-24) sequence for efficient activation. MC2R is predominantly expressed on the plasma membrane of adrenocortical cells in the zona fasciculata (where [[cortisol]] is produced) and zona reticularis (where adrenal androgens are produced), with lower expression in the zona glomerulosa.

A distinctive feature of MC2R biology is its absolute requirement for the melanocortin-2 receptor accessory protein (MRAP). MRAP is a single-pass transmembrane protein that forms an antiparallel homodimer and physically associates with MC2R during biosynthesis in the endoplasmic reticulum. Without MRAP, MC2R is retained in the ER and fails to traffic to the cell surface, rendering adrenocortical cells completely unresponsive to [[acth]]. This MRAP dependency distinguishes MC2R from all other melanocortin receptors and has important implications for understanding adrenal physiology and the pathogenesis of familial glucocorticoid deficiency.

## Upstream Causes

MC2R expression on adrenocortical cells is constitutive but is upregulated by sustained [[acth]] exposure, a mechanism that contributes to adrenal sensitization during chronic stress. The transcriptional regulation of the MC2R gene involves steroidogenic factor 1 (SF-1/NR5A1), a nuclear receptor critical for adrenal development and steroidogenic gene expression. [[acth]] itself, through cAMP/PKA signaling, stimulates MC2R gene transcription, creating a positive feedforward loop that enhances adrenal responsiveness. Conversely, prolonged exposure to very high [[acth]] concentrations can induce MC2R desensitization through receptor phosphorylation by GPCR kinases (GRKs) and beta-arrestin-mediated internalization. The ligand for MC2R is [[acth]], released from anterior pituitary corticotrophs under the stimulatory control of [[crh]] and [[avp]]. Thus, the entire upstream [[hpa-axis]] cascade from hypothalamic stress perception through pituitary [[acth]] release converges on MC2R activation as the final receptor-mediated step before steroidogenic enzyme engagement.

## Downstream Effects

Upon [[acth]] binding, MC2R activates the stimulatory G protein alpha subunit (Gs-alpha), which stimulates adenylyl cyclase to generate cAMP from ATP. The resulting rise in intracellular cAMP activates protein kinase A (PKA), which phosphorylates multiple downstream targets critical for [[cortisol]] biosynthesis. The most immediate PKA target is steroidogenic acute regulatory protein (StAR), whose phosphorylation activates its cholesterol-transporting activity, facilitating the rate-limiting step of cholesterol transfer from the outer to inner mitochondrial membrane. This acute effect accounts for the rapid (minutes) increase in [[cortisol]] production following [[acth]] stimulation. PKA also phosphorylates and activates hormone-sensitive lipase, which mobilizes cholesterol from intracellular lipid droplets. Over longer time frames, MC2R-PKA signaling upregulates transcription of the key steroidogenic enzymes -- CYP11A1 (cholesterol side-chain cleavage), CYP17A1 (17-alpha-hydroxylase/17,20-lyase), CYP21A2 (21-hydroxylase), and CYP11B1 (11-beta-hydroxylase) -- that catalyze the sequential conversion of cholesterol to [[cortisol]]. Additionally, chronic [[acth]]-MC2R signaling promotes adrenocortical cell hypertrophy and hyperplasia, maintaining adrenal mass and functional capacity.

## Holon Context

Within the [[adrenal-cortex-steroidogenesis]] holon, MC2R occupies the critical gateway position: it is the receptor that translates the systemic endocrine signal ([[acth]]) into intracellular biochemical responses (cAMP/PKA activation) that drive steroid hormone production. MC2R represents the specificity determinant that ensures the adrenal cortex responds selectively to pituitary-derived [[acth]] rather than to other circulating melanocortins. The MRAP co-dependency adds an additional layer of tissue-specific regulation, ensuring that functional MC2R signaling occurs only in cells that co-express both the receptor and its accessory protein. In the broader context of the [[hpa-axis]], MC2R is the molecular node where neuroendocrine command (hypothalamic [[crh]] and pituitary [[acth]]) is converted into hormonal effector output ([[cortisol]]), a transduction step that determines the gain of the entire axis.

## Clinical Relevance

Loss-of-function mutations in MC2R are the most common cause of familial glucocorticoid deficiency type 1 (FGD1, OMIM #202200), an autosomal recessive disorder characterized by isolated cortisol deficiency with preserved mineralocorticoid (aldosterone) production. Affected children present in infancy with hypoglycemia, failure to thrive, hyperpigmentation (due to compensatory ACTH elevation), and susceptibility to infections. Mutations in MRAP cause familial glucocorticoid deficiency type 2 (FGD2), which is clinically indistinguishable from FGD1, confirming the essential role of the MC2R-MRAP complex. The ACTH stimulation test (using synthetic ACTH 1-24, cosyntropin) exploits MC2R pharmacology to assess adrenal reserve: failure of [[cortisol]] to rise above a threshold (typically 500 nmol/L or 18 microg/dL) after MC2R stimulation indicates adrenal insufficiency. Pharmacologically, MC2R remains a challenging drug target due to its restricted ligand specificity and tissue distribution, though understanding its signaling has informed the development of depot ACTH preparations (repository corticotropin injection) used in certain inflammatory conditions.
