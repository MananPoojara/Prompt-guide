# Anthropic autonomous-coding prompts: source and licensing note

The official claude-quickstarts repository publishes an initializer prompt and a continuation coding prompt, and its prompts.py loads those exact files into the example harness. At inspected revision `9ec32b91df50b0d4906cae64b13c6298055ff40d`:

- [Initializer prompt](https://github.com/anthropics/claude-quickstarts/blob/9ec32b91df50b0d4906cae64b13c6298055ff40d/autonomous-coding/prompts/initializer_prompt.md)
- [Coding prompt](https://github.com/anthropics/claude-quickstarts/blob/9ec32b91df50b0d4906cae64b13c6298055ff40d/autonomous-coding/prompts/coding_prompt.md)
- [Prompt loader](https://github.com/anthropics/claude-quickstarts/blob/9ec32b91df50b0d4906cae64b13c6298055ff40d/autonomous-coding/prompts.py)
- [Example README](https://github.com/anthropics/claude-quickstarts/blob/9ec32b91df50b0d4906cae64b13c6298055ff40d/autonomous-coding/README.md)

The root repository license is MIT, but this example's README ends with a license statement of “Internal Anthropic use.” We have not resolved that conflict, so the full files are linked rather than republished here. This is an attribution and redistribution limitation, not a claim that the source is unavailable.

The initializer asks for a large feature list and setup artifacts. The coding prompt assumes those artifacts, Git, a running application, and browser-automation tools. It is not a general chat prompt. It also contains an unlimited-time instruction; that does not create an actual unlimited runtime budget. These prompts were inspected, not executed in this repository.
