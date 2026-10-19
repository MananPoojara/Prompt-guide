# Plain-language glossary

[Start](../START-HERE.md)

| Term | Meaning in this resource | Concrete example |
|---|---|---|
| Agent | A system that can choose actions and continue using their results | Inspect code, edit it, run tests, then report |
| API | A defined interface through which programs request operations | Send a model request or query a service |
| Artifact | A saved item you can inspect | Prompt file, raw response, test log |
| Benchmark | A defined collection of tasks and scoring rules | A fixed set of extraction cases with expected answers |
| Compaction | Condensing conversation state for continuation | Preserve decisions and unfinished work in a shorter summary |
| Context | Material available for a particular model request | Instructions, notes, messages, tool results |
| Context window | The request's supported token capacity under the model's accounting | Limits how much material can be processed together |
| Embedding | Numerical representation useful for comparing items | Retrieve passages similar to a question |
| Evaluation / eval | A procedure for judging performance against criteria | Compare extracted owners against expected values |
| Fixture | A deliberately prepared input used for testing | The stack implementation with a known duplicate-minimum bug |
| Frontmatter | Metadata at the start of a document | A skill's name and description between `---` lines |
| Graph | States or components connected by explicit transitions | Failed test routes back to repair |
| Grounding | Connecting an answer to supplied or retrieved evidence | Cite the note that says a date is only proposed |
| Harness | Runtime software around model calls | Assemble context, execute tools, track state, stop the loop |
| Hook | Code triggered by a specified runtime event | Check evidence before allowing a completion-related write |
| Inference | Using an existing model to produce a result | Generate an answer from the current request |
| JSON | A structured text format for data | `{"owner": null}` |
| Latency | Time until a response or operation completes | Time spent retrieving a note and answering |
| MCP | A protocol for connecting hosts to capability-providing servers | Discover and call `read_note` |
| Memory | Stored information made available across interactions | A saved project decision retrieved into a later request |
| Model parameters | Learned numerical values used during inference | Training changes them; a normal chat message does not |
| Plugin | A host-specific package of capabilities | A Claude Code package containing a skill |
| Prompt | Input that asks or instructs a model to perform work | Extract confirmed owners and deadlines |
| Prompt injection | Untrusted content trying to redirect the system's behavior | A retrieved document telling the agent to ignore its task |
| Provenance | Where an artifact or claim came from | Publisher, source path, commit, license, and retrieval date |
| RAG | Retrieval-augmented generation | Fetch relevant notes, then generate an answer using them |
| Regression | Previously working behavior broken by a change | Search normalization accidentally changes product order |
| Role | Message category used by a model interface | User request or tool result |
| Rubric | Explicit criteria for judging an answer | Correctness, completeness, and source support |
| Schema | A machine-readable description of data shape | Required string field `note_id` |
| Skill | Packaged task instructions loaded by a supporting host | Review a claim against local evidence |
| stdio | A process's standard input and output streams | Local MCP client/server communication |
| Token | A unit used to represent model input/output | A word fragment or punctuation unit |
| Tool | An operation the runtime can execute | Read a note, run tests, or search files |
| Trace | Recorded steps in an execution | Requests, calls, results, and decisions |
| Training | Optimization that changes model parameters | Learn patterns from examples and objectives |
| Verdict | An evaluator's stated judgment | PASS, FAIL, or insufficient evidence |

A term can have narrower meanings in a specific provider's API. When running code, use the versioned interface documented for that example.
