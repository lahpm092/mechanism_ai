---
id: hypothalamus-crh-circuit
type: holon
scale: organ
parent_holon: hpa-axis
children_holons: []
inputs:
  - node: stress-signal
    description: "Afferent stress inputs from amygdala, brainstem, cortex"
  - node: circadian-signal
    description: "SCN circadian drive"
  - node: il-6
    description: "Cytokine signaling via circumventricular organs"
  - node: il-1beta
    description: "Cytokine signaling"
  - node: cortisol
    description: "Negative feedback signal via GR"
outputs:
  - node: crh
    description: "CRH released into hypophyseal portal system"
  - node: avp
    description: "AVP co-released with CRH"
internal_nodes:
  - parvocellular-neuron
  - crh
  - avp
  - gr
internal_edges:
  - stress-activates-crh
  - cortisol-inhibits-crh
  - gr-mediates-feedback
sources:
  - "doi:10.1016/j.yfrne.2019.100784"
confidence: 0.90
---

# Hypothalamus CRH Circuit

The [[hypothalamus-crh-circuit]] is the apical node of the [[hpa-axis]] cascade, responsible for converting diverse neural and humoral inputs into a neuroendocrine output that initiates the systemic stress response. This holon is anatomically centered on the [[parvocellular-neuron]] population of the paraventricular nucleus (PVN) of the hypothalamus -- a compact cluster of approximately 2,000 neuroendocrine neurons in humans that synthesize and secrete [[crh]] (corticotropin-releasing hormone, a 41-amino-acid peptide) and its co-secretagogue [[avp]] (arginine vasopressin). These neurons represent the final common pathway through which the central nervous system communicates with the endocrine arm of the stress response, funneling information from cortical, limbic, brainstem, and immune sources into a single output channel: the hypophyseal portal vasculature that connects the median eminence to the anterior pituitary gland.

## Integration of Afferent Inputs

The [[parvocellular-neuron]] population in the PVN functions as a biological signal integrator, receiving and weighting inputs from multiple distinct sources. The [[stress-signal]] input encompasses several anatomically separable afferent pathways. The central nucleus of the amygdala provides glutamatergic and GABAergic projections that relay threat-related information processed by the basolateral amygdala; these projections are critical for mounting HPA responses to psychological stressors such as predator exposure or social defeat. The brainstem catecholaminergic nuclei -- particularly the A1/A2 noradrenergic cell groups of the nucleus tractus solitarius and the C1/C3 adrenergic groups of the ventrolateral medulla -- convey information about physiological stressors including hemorrhage, hypoxia, and infection via ascending noradrenergic fibers that directly innervate PVN [[parvocellular-neuron]] cells. The prefrontal cortex, especially the infralimbic and prelimbic subdivisions, exerts top-down modulatory control over PVN output, generally providing inhibitory regulation that constrains HPA axis activation during cognitive appraisal of ambiguous stimuli. The hippocampus, rich in [[gr]] and [[mr]] receptors, provides an additional layer of inhibitory feedback that is critical for terminating HPA axis responses after acute stress.

## Circadian and Immune Modulation

Beyond the [[stress-signal]] inputs, the [[hypothalamus-crh-circuit]] receives a tonic [[circadian-signal]] from the suprachiasmatic nucleus (SCN), the master circadian pacemaker. The SCN communicates with PVN [[parvocellular-neuron]] cells through both direct projections and indirect relays via the subparaventricular zone and the dorsomedial hypothalamus, imposing a circadian rhythm on [[crh]] secretion that produces the characteristic diurnal pattern of [[cortisol]] release -- peaking in the early morning hours and reaching a nadir around midnight. This circadian patterning is essential for synchronizing metabolic, immune, and cognitive functions with the light-dark cycle, and its disruption (as in shift work, jet lag, or chronic stress) has far-reaching consequences for metabolic health and immune function. Simultaneously, pro-inflammatory cytokines from the [[innate-immune-response]] -- principally [[il-6]], [[il-1beta]], and [[tnf-alpha]] -- reach the PVN through several routes: via circumventricular organs such as the organum vasculosum of the lamina terminalis (OVLT) and the median eminence, which lack a functional blood-brain barrier; via active transport mechanisms across the blood-brain barrier; via vagal afferent relay through the nucleus tractus solitarius; and via local production by brain-resident microglia and perivascular macrophages. These immune signals drive [[crh]] transcription and release, forming the afferent limb of the neuroendocrine-immune regulatory loop.

## CRH and AVP Co-Release

The primary output of this holon is the pulsatile release of [[crh]] and [[avp]] from [[parvocellular-neuron]] axon terminals in the external zone of the median eminence into the hypophyseal portal capillaries. [[crh]] and [[avp]] are synthesized in the same neurons but are packaged into partially overlapping populations of secretory vesicles, allowing for differential regulation of their release ratios. Under basal conditions, [[crh]] is the dominant secretagogue driving [[corticotroph]] activation in the [[pituitary-acth-release]] holon. However, under conditions of chronic or repeated stress, the ratio shifts toward increased [[avp]] co-expression and release -- a phenomenon that has important functional consequences because [[avp]] acts synergistically with [[crh]] at the pituitary level, potentiating [[acth]] release through V1b receptor-mediated signaling while being less susceptible to glucocorticoid-mediated suppression. This CRH-to-AVP shift represents a form of stress-history-dependent plasticity within the [[hypothalamus-crh-circuit]] that can alter the gain and feedback sensitivity of the entire [[hpa-axis]].

## Negative Feedback via Glucocorticoid Receptors

The [[hypothalamus-crh-circuit]] is a primary target of the [[glucocorticoid-feedback]] mechanism that constrains [[hpa-axis]] output. Circulating [[cortisol]] enters PVN neurons and binds to intracellular [[gr]] (glucocorticoid receptors, NR3C1), which translocate to the nucleus and suppress [[crh]] gene transcription by binding to negative glucocorticoid response elements (nGREs) in the CRH promoter and by recruiting co-repressor complexes. This genomic feedback operates on a timescale of hours and is responsible for the slow phase of HPA axis feedback inhibition. Additionally, [[cortisol]] exerts rapid non-genomic feedback effects at the PVN, including stimulation of endocannabinoid synthesis that suppresses glutamatergic excitatory inputs to [[parvocellular-neuron]] cells -- a mechanism that operates within minutes and contributes to the fast phase of feedback. The [[mr]] (mineralocorticoid receptor, NR3C2) also participates in feedback regulation, particularly at low circulating [[cortisol]] concentrations that are insufficient to saturate the higher-affinity [[mr]], and is thought to be critical for maintaining the basal tone of the axis and regulating the circadian nadir of [[cortisol]]. When [[gr]]-mediated feedback is impaired -- as occurs in chronic stress, major depressive disorder, or genetic polymorphisms of the GR gene -- the [[hypothalamus-crh-circuit]] becomes tonically hyperactive, driving sustained [[crh]] release and contributing to the hypercortisolism and feedback resistance characteristic of stress-related pathology. This positions the [[gr]] within this holon as a critical node for both physiological homeostasis and pathological dysregulation of the [[hpa-axis]].
