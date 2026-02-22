---
id: avp
type: molecule
scale: molecular
aliases: [ADH, antidiuretic hormone, argipressin]
holon_membership: [hpa-axis, hypothalamus-crh-circuit]
confidence: 0.92
sources:
  - "doi:10.1210/er.2003-0010"
  - "doi:10.1016/j.pharmthera.2010.01.001"
  - "doi:10.1111/jne.12000"
tags: [neuropeptide, hypothalamic-hormone]
---

# AVP (Arginine Vasopressin)

Arginine vasopressin (AVP), also known as antidiuretic hormone (ADH), is a 9-amino-acid cyclic peptide (Cys-Tyr-Phe-Gln-Asn-Cys-Pro-Arg-Gly-NH2) synthesized primarily by magnocellular and parvocellular neurons of the hypothalamic paraventricular nucleus (PVN) and supraoptic nucleus (SON). The peptide is derived from a larger preprohormone (prepro-vasopressin-neurophysin II-copeptin) encoded by the AVP gene on chromosome 20p13. AVP has a short plasma half-life of 10-35 minutes and is cleared primarily by hepatic and renal peptidases. Structurally, AVP differs from oxytocin by only two amino acids (positions 3 and 8), yet the two peptides have dramatically divergent receptor specificities and physiological functions, reflecting the exquisite selectivity of peptide-receptor interactions.

AVP is best known for its role in water homeostasis, acting through V2 receptors in the renal collecting duct to promote aquaporin-2 insertion and water reabsorption. However, its role as a co-regulator of the [[hpa-axis]] is equally important and often underappreciated. Parvocellular AVP neurons in the PVN co-express and co-release AVP with [[crh]] into the hypophyseal portal circulation, where it acts on anterior pituitary corticotrophs to potentiate [[acth]] secretion. The relative contribution of AVP to HPA axis drive increases during chronic stress, as the CRH:AVP co-expression ratio in parvocellular neurons shifts toward greater AVP production, a mechanism thought to maintain HPA axis responsiveness when CRH-R1 receptors undergo desensitization.

## Upstream Causes

AVP synthesis and release from parvocellular PVN neurons are regulated by many of the same afferent inputs that govern [[crh]] secretion, including stress-related noradrenergic projections from the brainstem, limbic inputs from the amygdala and hippocampus, and circulating pro-inflammatory cytokines such as [[il-6]], [[il-1beta]], and [[tnf-alpha]]. Osmotic stimuli are the primary regulators of magnocellular AVP secretion (for water balance), but parvocellular AVP relevant to HPA axis function is more responsive to stress and inflammatory signals. Chronic stress is a particularly important driver: repeated or sustained stressors upregulate AVP mRNA expression in parvocellular neurons while [[crh]] expression may plateau or decline, shifting the secretory profile of PVN neurons. [[cortisol]] negative feedback via the [[gr]] suppresses both [[crh]] and AVP transcription in parvocellular neurons, though AVP may be less sensitive to glucocorticoid suppression than [[crh]], contributing to its relative prominence during chronic stress states.

## Downstream Effects

The principal HPA-axis-relevant action of AVP is the potentiation of [[crh]]-stimulated [[acth]] release from anterior pituitary corticotrophs. AVP binds to V1b (also designated V3) receptors on corticotrophs, which are Gq-coupled GPCRs that activate phospholipase C (PLC), generating inositol trisphosphate (IP3) and diacylglycerol (DAG). IP3 mobilizes calcium from intracellular stores, while DAG activates protein kinase C (PKC). This calcium/PKC pathway synergizes with the cAMP/PKA pathway activated by [[crh]] via CRH-R1, resulting in markedly enhanced [[acth]] secretory granule exocytosis. Importantly, AVP alone is a relatively weak [[acth]] secretagogue, but when combined with [[crh]], it amplifies the [[acth]] response by 2-3 fold, providing a multiplicative rather than merely additive interaction. Beyond the HPA axis, AVP acts on V1a receptors in vascular smooth muscle to cause vasoconstriction (contributing to blood pressure regulation), on V2 receptors in the renal collecting duct to promote water reabsorption (antidiuretic effect), and on V1b receptors in pancreatic islets to modulate insulin secretion.

## Holon Context

Within the [[hpa-axis]] holon, AVP functions as a modulatory co-signal that fine-tunes the sensitivity and dynamic range of the hypothalamic-pituitary relay. While [[crh]] is the primary driver of [[acth]] release, AVP provides a parallel signaling channel that employs a distinct second messenger system (Gq/calcium/PKC versus Gs/cAMP/PKA), enabling the corticotroph to perform biochemical signal integration. This dual-input architecture confers several advantages: it allows the HPA axis to maintain responsiveness during chronic stress (when CRH-R1 may desensitize, V1b-mediated AVP signaling can sustain [[acth]] release), and it provides independent regulatory axes for basal versus stress-induced [[cortisol]] output. Within the [[hypothalamus-crh-circuit]] holon, AVP co-expression in parvocellular [[crh]] neurons represents a form of neuropeptide multiplexing, where a single neuronal population encodes multiple signal dimensions through the ratio and temporal pattern of co-released peptides.

## Clinical Relevance

The dual roles of AVP in water balance and HPA axis regulation intersect in several clinical contexts. In the syndrome of inappropriate antidiuretic hormone secretion (SIADH), excessive AVP release causes dilutional hyponatremia; V2 receptor antagonists (vaptans) such as tolvaptan are used therapeutically. In adrenal insufficiency, the loss of [[cortisol]] negative feedback leads to elevated [[crh]] and AVP, contributing to the impaired free water clearance seen in adrenal crisis. Desmopressin (DDAVP), a V2-selective synthetic AVP analogue, is used in the desmopressin stimulation test to help differentiate pituitary Cushing disease from ectopic ACTH syndrome, exploiting the fact that V1b receptors are overexpressed on corticotroph adenomas. Central diabetes insipidus, caused by destruction of magnocellular AVP neurons, highlights the essential role of AVP in water homeostasis but does not typically impair HPA axis function because parvocellular AVP secretion may be preserved. Research into V1b receptor antagonists as potential anxiolytic and antidepressant agents reflects growing recognition of AVP's contribution to stress-related psychiatric pathology.
