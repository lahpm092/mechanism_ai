---
id: cortisol
type: molecule
scale: molecular
aliases: [hydrocortisone, compound F]
holon_membership: [hpa-axis, adrenal-cortex-steroidogenesis, glucocorticoid-feedback]
confidence: 0.95
sources:
  - "doi:10.1210/er.2003-0010"
  - "doi:10.1016/j.bbi.2006.02.004"
  - "doi:10.1038/nri3552"
tags: [glucocorticoid, steroid-hormone, anti-inflammatory]
---

# Cortisol

Cortisol (hydrocortisone) is the primary endogenous glucocorticoid in humans, synthesized from cholesterol in the zona fasciculata of the adrenal cortex. It is a 21-carbon steroid hormone with the chemical formula C21H30O5 and a molecular weight of 362.46 Da. Cortisol circulates in the blood predominantly bound to corticosteroid-binding globulin (CBG, transcortin) and albumin, with only approximately 5-10% existing in the free, biologically active form. Its plasma half-life is roughly 60-90 minutes, and it is metabolized primarily in the liver through A-ring reduction and conjugation with glucuronic acid or sulfate before renal excretion. Cortisol secretion follows a robust circadian rhythm, with peak concentrations occurring in the early morning hours (06:00-08:00) and a nadir around midnight, a pattern driven by the suprachiasmatic nucleus and its regulation of [[crh]] pulsatility.

Cortisol serves as the principal effector molecule of the [[hpa-axis]], functioning as the key bridge node between the neuroendocrine and immune systems. Its biological actions are mediated primarily through binding to two intracellular nuclear receptors: the [[gr]] (glucocorticoid receptor, NR3C1) and the [[mr]] (mineralocorticoid receptor, NR3C2). Upon binding to [[gr]], cortisol induces receptor dimerization, nuclear translocation, and interaction with glucocorticoid response elements (GREs) in DNA, driving transactivation of anti-inflammatory genes such as annexin A1, MAPK phosphatase 1 (MKP-1), and IkB-alpha. Equally important is the transrepression mechanism, whereby the cortisol-[[gr]] complex physically interacts with and inhibits pro-inflammatory transcription factors, most notably [[nf-kb]] and AP-1, thereby suppressing the transcription of hundreds of inflammatory mediators.

## Upstream Causes

Cortisol biosynthesis is driven by [[acth]] acting on the [[mc2r]] receptor on adrenocortical cells of the zona fasciculata. [[acth]] binding to [[mc2r]] activates adenylyl cyclase via the Gs-alpha subunit, increasing intracellular cAMP and activating protein kinase A (PKA). PKA phosphorylates and activates steroidogenic acute regulatory protein (StAR), which facilitates cholesterol transfer from the outer to inner mitochondrial membrane -- the rate-limiting step in steroidogenesis. Cholesterol is then converted to pregnenolone by CYP11A1 (cholesterol side-chain cleavage enzyme), and subsequently to cortisol through a series of hydroxylation reactions catalyzed by CYP17A1, CYP21A2, and CYP11B1. The local tissue concentration of active cortisol is further regulated by the interconversion between cortisol and inactive cortisone, mediated by [[11beta-hsd1]] (which regenerates cortisol from cortisone) and [[11beta-hsd2]] (which inactivates cortisol to cortisone).

## Downstream Effects

Cortisol exerts a vast array of downstream effects spanning metabolic, immune, cardiovascular, and neuroendocrine systems. In the context of the [[hpa-axis]], cortisol completes the negative feedback loop by inhibiting [[crh]] release from hypothalamic parvocellular neurons and [[acth]] secretion from anterior pituitary corticotrophs, acting through [[gr]] at both sites and through [[mr]] in hippocampal neurons that project to the hypothalamus. Immunologically, cortisol suppresses the innate immune response by inhibiting [[nf-kb]], thereby reducing the transcription and secretion of pro-inflammatory cytokines including [[il-6]], [[il-1beta]], and [[tnf-alpha]]. Cortisol also induces [[il-10]] production and promotes a shift from Th1 to Th2 immune polarization, suppressing [[il-2]] and interferon-gamma while enhancing Th2 cytokines. It inhibits [[cox-2]] expression both directly (via GRE-mediated transrepression) and indirectly through induction of annexin A1, which inhibits phospholipase A2 and thereby reduces arachidonic acid availability for prostaglandin synthesis. Additional metabolic effects include stimulation of hepatic gluconeogenesis, promotion of protein catabolism in muscle, and facilitation of lipolysis in adipose tissue.

## Holon Context

Within the [[hpa-axis]] holon, cortisol occupies the terminal effector position, translating neuroendocrine signals originating from hypothalamic [[crh]] and pituitary [[acth]] into systemic physiological responses. It simultaneously functions as the primary feedback signal that constrains the axis, creating a classic negative feedback loop that maintains homeostatic set points. Within the [[adrenal-cortex-steroidogenesis]] holon, cortisol represents the principal product of the zona fasciculata enzymatic cascade, the output of a tightly regulated biosynthetic pathway. Within the [[glucocorticoid-feedback]] holon, cortisol operates at multiple scales: at the molecular scale through receptor binding kinetics (high-affinity [[mr]] saturation at basal levels, lower-affinity [[gr]] recruitment at stress levels), at the cellular scale through transcription factor modulation, and at the systems scale through circuit-level feedback on the [[hpa-axis]]. The molecule also bridges into the [[innate-immune-response]] holon, where its suppression of [[nf-kb]] and pro-inflammatory cytokines positions it as the major endogenous anti-inflammatory signal that prevents immune overshoot during stress responses.

## Clinical Relevance

Dysregulation of cortisol is implicated in a wide spectrum of pathology. Chronic cortisol excess, whether endogenous (Cushing syndrome due to pituitary adenoma, ectopic ACTH secretion, or adrenal adenoma) or exogenous (iatrogenic from prolonged glucocorticoid therapy), produces a characteristic constellation of central obesity, proximal myopathy, skin thinning, osteoporosis, hyperglycemia, immunosuppression, and psychiatric disturbances. Conversely, cortisol deficiency in primary adrenal insufficiency (Addison disease) or secondary adrenal insufficiency (from pituitary or hypothalamic disease) causes fatigue, hypotension, hypoglycemia, and potentially life-threatening adrenal crisis. Chronic stress-mediated elevations in cortisol have been associated with insulin resistance, visceral adiposity, hippocampal atrophy, depression, and accelerated immunosenescence. The therapeutic exploitation of cortisol's anti-inflammatory properties through synthetic glucocorticoids (prednisone, dexamethasone, budesonide) remains one of the most widely used pharmacological strategies in medicine, applied across autoimmune diseases, transplant rejection, asthma, and inflammatory bowel disease, though invariably constrained by the metabolic and immunosuppressive side effects that mirror Cushing syndrome.
