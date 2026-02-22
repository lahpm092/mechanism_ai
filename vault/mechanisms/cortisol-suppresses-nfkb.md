---
id: cortisol-suppresses-nfkb
source: cortisol
target: nf-kb
relationship: inhibits
direction: inhibitory
mechanism_type: direct
scale: molecular
evidence_type: experimental
evidence_strength: strong
temporal_lag: minutes
reversible: true
context: "Cortisol-GR complex translocates to nucleus and physically blocks NF-kB p65 DNA binding via transrepression, while also inducing IkBa transcription to sequester NF-kB in cytoplasm"
species: human
sources:
  - doi: "doi:10.1038/nri3552"
    study_type: review
    sample_size: null
    year: 2013
  - doi: "doi:10.1016/j.pharmthera.2007.01.005"
    study_type: review
    sample_size: null
    year: 2007
confidence: 0.95
holon_context: [innate-immune-response, glucocorticoid-feedback]
contradicted_by: []
---

# Cortisol Suppresses NF-kB Signaling

## Causal Claim

[[cortisol]] **inhibits** [[nf-kb]] transcriptional activity through direct protein-protein interaction between the [[gr]] and the NF-kB p65 (RelA) subunit (transrepression) and through transcriptional induction of IkB-alpha, constituting the primary molecular mechanism of glucocorticoid anti-inflammatory action.

## Molecular Mechanism

The suppression of [[nf-kb]] by [[cortisol]] is widely regarded as the single most important molecular mechanism underlying the anti-inflammatory and immunosuppressive effects of glucocorticoids. [[nf-kb]] is a family of dimeric transcription factors, with the p65/p50 heterodimer being the most abundant and transcriptionally active form in immune cells. Under resting conditions, [[nf-kb]] is sequestered in the cytoplasm by inhibitory IkB proteins (IkB-alpha, IkB-beta, IkB-epsilon). Upon inflammatory stimulation -- triggered by pathogen-associated molecular patterns (PAMPs), damage-associated molecular patterns (DAMPs), or pro-inflammatory cytokines such as [[il-1beta]] and [[tnf-alpha]] -- the IKK complex phosphorylates IkB, targeting it for ubiquitination and proteasomal degradation. Freed [[nf-kb]] dimers then translocate to the nucleus and bind kB enhancer elements in the promoters of hundreds of inflammatory genes.

[[cortisol]] antagonizes this inflammatory cascade through two principal mechanisms. The first and most rapid is direct transrepression: the ligand-activated [[gr]], upon nuclear translocation, physically interacts with the p65 subunit of [[nf-kb]] through protein-protein binding between the [[gr]] DNA-binding domain and the Rel homology domain of p65. This interaction prevents [[nf-kb]] from engaging with kB DNA elements, effectively silencing [[nf-kb]]-dependent gene transcription without requiring [[gr]] to bind its own GRE elements. The transrepression complex also recruits histone deacetylase 2 (HDAC2) to [[nf-kb]]-occupied promoters, deacetylating histone H4 and condensing local chromatin structure to further suppress transcription. This mechanism accounts for the suppression of a broad swath of inflammatory mediators including [[il-6]], [[il-1beta]], [[tnf-alpha]], [[cox-2]], iNOS, ICAM-1, and numerous chemokines -- all of which contain [[nf-kb]]-dependent promoter elements.

The second mechanism is transactivation of anti-inflammatory genes, most notably IkB-alpha (NFKBIA). The [[cortisol]]-[[gr]] complex binds to a GRE in the IkB-alpha promoter and drives transcription of new IkB-alpha protein, which enters the nucleus, strips [[nf-kb]] from DNA, and escorts it back to the cytoplasm in an inactive state. This mechanism creates a self-reinforcing inhibitory cycle: cortisol both directly blocks [[nf-kb]] DNA binding and replenishes the cytoplasmic inhibitor that keeps [[nf-kb]] sequestered. Additional transactivation targets include MAPK phosphatase 1 (MKP-1/DUSP1), which dephosphorylates and inactivates p38 MAPK and JNK -- kinases that contribute to [[nf-kb]] activation and inflammatory mRNA stability -- and [[annexin-a1]], which has broader anti-inflammatory effects on lipid mediator pathways.

## Downstream Cascade

Suppression of [[nf-kb]] by [[cortisol]] leads to a global dampening of inflammatory gene expression. The immediate downstream effects include reduced transcription and secretion of [[il-6]], [[il-1beta]], [[tnf-alpha]], IL-8, and other chemokines from macrophages, dendritic cells, and epithelial cells. Reduced [[cox-2]] expression decreases prostaglandin synthesis, attenuating pain, fever, and vasodilation. Suppression of iNOS reduces nitric oxide production, limiting inflammatory tissue damage. Reduced ICAM-1 and VCAM-1 expression on endothelial cells decreases leukocyte adhesion and tissue infiltration. Collectively, these effects constitute the anti-inflammatory program that resolves acute inflammatory responses and, when dysregulated, underlies both the therapeutic utility and the immunosuppressive risks of glucocorticoid pharmacology.

## Context and Conditions

This mechanism is operational in virtually all nucleated cells expressing [[gr]], but is most physiologically relevant in cells of the innate immune system -- macrophages, monocytes, dendritic cells, and neutrophils -- where [[nf-kb]] activity is high and cortisol-mediated suppression has the greatest functional impact. The efficacy of transrepression depends on the level of [[gr]] expression and the intensity of [[nf-kb]] activation: in severe inflammation with massive [[nf-kb]] nuclear translocation, physiological cortisol concentrations may be insufficient to fully suppress [[nf-kb]], producing a state of relative glucocorticoid resistance. This phenomenon is observed in sepsis, treatment-resistant asthma, and chronic inflammatory diseases. Chronic [[cortisol]] exposure can downregulate [[gr]] expression and impair HDAC2 function (through oxidative and nitrosative modifications), progressively reducing the efficacy of this suppressive mechanism. The glucocorticoid resistance seen in a subset of patients with inflammatory diseases is often attributable to impaired [[gr]]-[[nf-kb]] transrepression rather than to pharmacokinetic factors.

## Cross-Holon Implications

This edge represents the most critical bridge between the [[hpa-axis]]/[[glucocorticoid-feedback]] holons and the [[innate-immune-response]] holon. By suppressing [[nf-kb]], [[cortisol]] directly restrains the inflammatory output that would otherwise be amplified through [[nf-kb]]-driven positive feedback loops (NF-kB driving [[tnf-alpha]] and [[il-1beta]], which further activate [[nf-kb]]). This creates a counter-regulatory circuit: inflammatory cytokines stimulate [[crh]] and [[acth]] release, driving [[cortisol]] production, which then suppresses the [[nf-kb]] activity generating those cytokines. The integrity of this cross-holon brake is essential for preventing cytokine storm and uncontrolled systemic inflammation. When this mechanism fails -- due to adrenal insufficiency, glucocorticoid resistance, or overwhelming inflammatory stimulus -- the resulting unchecked [[nf-kb]] activation can produce septic shock, multi-organ failure, and death, illustrating the life-and-death importance of this single molecular edge in the causal metagraph.
