# Frozen research/revision demonstration

Question: can a reader trace a revised noncoding explanation to a small inspected source packet and distinguish factual errors, mismatched citations, and unsupported evidence?

The authoring assistant inspected two NASA Science pages on 2026-10-19 using web retrieval and the agent-reach Jina route. sources.json contains short authored paraphrases, original URLs, and section locators; no images or full pages are redistributed. These notes are a deliberately narrow evidence packet, not a literature review or independent annotation. Reader access to every necessary task fact is local; upstream links permit attribution checks.

The five-claim draft is an authored failure fixture. It is not a recorded hallucination. Before inference, expect C1/C2 contradicted by S1; C3 contradicted by S2; C4 supported but incorrectly attributed, with S2 as its support; C5 unsupported by the supplied packet, with no supporting source. The invented S3 is absent. Do not claim that the survey's nonexistence has been proven by an exhaustive search.

One actual revision call, requested gpt-6.1-sol with low reasoning effort, fresh ephemeral CLI session, read-only setting, 180-second timeout, no retries, no application tools. This records source-conditioned revision, not autonomous web research. No dollar or native output-token cap is enforced. Retain exact assembled request, final output, code/protocol/source/draft hashes, requested CLI configuration, process status and duration; omit CLI stdout/stderr, hidden reasoning and account metadata. Refuse an existing output directory.

Check JSON structure, five distinct claim IDs, the frozen verdict/source mappings, paragraph length, and source-ID allowlisting. These mechanical checks do not verify entailment, factual correctness of every revised sentence, or whether the paragraph is good teaching. Separately retain an explicit author review of the actual paragraph, including any limitations or failure. Do not repair the recorded response or retry to obtain a favorable example. No baseline model call, comparative improvement, human-review result, or general hallucination-rate claim is planned.
