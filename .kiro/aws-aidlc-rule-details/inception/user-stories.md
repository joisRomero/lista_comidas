# User Stories - Detailed Steps

## Purpose
**Convert requirements into user-centered stories with acceptance criteria**

User Stories focus on:
- Translating business requirements into user-centered narratives
- Defining clear acceptance criteria for each story
- Creating user personas that represent different stakeholder types
- Establishing shared understanding across teams
- Providing testable specifications for implementation

## Prerequisites
- Workspace Detection must be complete
- Requirements Analysis recommended (can reference requirements if available)
- Workflow Planning must indicate User Stories stage should execute

## Intelligent Assessment Guidelines

**WHEN TO EXECUTE USER STORIES**: Use this enhanced assessment before proceeding:

### High Priority Execution (ALWAYS Execute)
- **New User Features**: Any new functionality users will directly interact with
- **User Experience Changes**: Modifications to existing user workflows or interfaces
- **Multi-Persona Systems**: Applications serving different types of users
- **Customer-Facing APIs**: Services that external users or systems will consume
- **Complex Business Logic**: Requirements with multiple scenarios or business rules
- **Cross-Team Projects**: Work requiring shared understanding across multiple teams

### Medium Priority Execution (Assess Complexity)
- **Backend User Impact**: Internal changes that indirectly affect user experience
- **Performance Improvements**: Enhancements with user-visible benefits
- **Integration Work**: Connecting systems that affect user workflows
- **Data Changes**: Modifications affecting user data, reports, or analytics
- **Security Enhancements**: Changes affecting user authentication or permissions

### Complexity Assessment Factors
For medium priority cases, execute user stories if ANY of these apply:
- **Scope**: Changes span multiple components or user touchpoints
- **Ambiguity**: Requirements have unclear aspects that stories could clarify
- **Risk**: High business impact or potential for misunderstanding
- **Stakeholders**: Multiple business stakeholders involved in requirements
- **Testing**: User acceptance testing will be required
- **Options**: Multiple valid implementation approaches exist

### Skip Only For Simple Cases
- **Pure Refactoring**: Internal code improvements with zero user impact
- **Isolated Bug Fixes**: Simple, well-defined fixes with clear scope
- **Infrastructure Only**: Changes with no user-facing effects
- **Developer Tooling**: Build processes, CI/CD, or development environment changes
- **Documentation**: Updates that don't affect functionality

### Default Decision Rule
**When in doubt, include user stories AND ask clarifying questions.** The overhead of creating comprehensive stories with proper clarification is typically outweighed by the benefits of:
- Clearer requirements understanding
- Better team alignment
- Improved testing criteria
- Enhanced stakeholder communication
- Reduced implementation risks
- Fewer costly changes during development
- Better user experience outcomes

---

# PART 1: PLANNING

## Step 1: Validate User Stories Need (MANDATORY)

**CRITICAL**: Before proceeding with user stories, perform this assessment:

### Assessment Process
1. **Analyze Request Context**:
   - Review the original user request and requirements
   - Identify user-facing vs internal-only changes
   - Assess complexity and scope of the work
   - Evaluate business stakeholder involvement

2. **Apply Assessment Criteria**:
   - Check against High Priority indicators (always execute)
   - Evaluate Medium Priority factors (complexity-based decision)
   - Confirm this isn't a simple case that should be skipped

3. **Document Assessment Decision**:
   - Create `aidlc-docs/inception/plans/user-stories-assessment.md`
   - Include reasoning for why user stories are valuable for this request
   - Reference specific assessment criteria that apply
   - Explain expected benefits (clarity, testing, stakeholder alignment)

4. **Proceed Only If Justified**:
   - User stories must add clear value to the project
   - Assessment must show concrete benefits outweigh overhead
   - Decision should be defensible to project stakeholders

### Assessment Documentation Template
```markdown
# User Stories Assessment

## Request Analysis
- **Original Request**: [Brief summary]
- **User Impact**: [Direct/Indirect/None]
- **Complexity Level**: [Simple/Medium/Complex]
- **Stakeholders**: [List involved parties]

## Assessment Criteria Met
- [ ] High Priority: [List applicable criteria]
- [ ] Medium Priority: [List applicable criteria with complexity justification]
- [ ] Benefits: [Expected value from user stories]

## Decision
**Execute User Stories**: [Yes/No]
**Reasoning**: [Detailed justification]

## Expected Outcomes
- [List specific benefits user stories will provide]
- [How stories will improve project success]
```

## Step 2: Create Story Plan
- Assume the role of a product owner
- Generate a comprehensive plan with step-by-step execution checklist for story development
- Each step and sub-step should have a checkbox []
- Focus on methodology and approach for converting requirements into user stories

## Step 3: Generate Context-Appropriate Questions

**MANDATORY — Mandatory Skill Deduplication**: Before generating questions, check `aidlc-state.md` → Organizational Skills for ANY mandatory skills loaded for this stage (e.g., `hu-template`). For each mandatory skill:
1. Read the skill's FULL content (not just frontmatter)
2. For EACH potential question, check: "Does the skill already define this, provide a default value, or prescribe a specific approach?"
3. **If YES → DO NOT ASK. Use the skill's value directly.**
4. **If NO → the skill leaves this unspecified → OK to ask.**

**When `hu-template` is mandatory, these topics are ALREADY DECIDED (DO NOT ASK):**
- Story format → "Como/Quiero/Para" (skill line 36-39)
- Field structure → Epic, Layer, Repo, Historia, CA, Reglas, Mockup, Datos, Deps, Notas, Prioridad, Estimacion, Sprint (skill template)
- Numbering → `{REPO_CODE}-{SEQ}` continuous (skill line 101-106)
- Acceptance criteria format → SMART + checkboxes, minimum 3 (skill line 165-178)
- Grouping → by Epic + Layer/Repo (skill line 84-122)
- Estimation type → `S/M/L/XL` (skill line 78)
- Priority values → `Alta/Media/Baja` (skill line 77)
- Sprint field → number, default `TBD` if unknown (skill line 79)
- Mockup field → link or "Pendiente" if no mockups exist (skill line 57). If Prototyping stage executed, reference generated prototypes.
- Granularity → 1 HU per action/endpoint (backend) + 1 HU per screen (frontend). Skill examples (lines 131-153) show this pattern: "SP ListEquipment + endpoint GET" = 1 HU, "Pantalla listado de equipos" = 1 HU. DO NOT ask the user to choose granularity.

**When `hu-template` is mandatory, ONLY these topics remain unspecified (OK to ask):**
- How many user personas to document
- Whether catalog/lookup entities get their own HUs or are dependencies only
- Business context not covered in Requirements Analysis

**DIRECTIVE**: Only ask questions about topics the mandatory skill leaves genuinely unspecified. A field having a template placeholder (like `{número}`) does NOT mean you need to ask — it means use a sensible default (TBD) or infer from context.

**See `common/question-format-guide.md` for question formatting rules**

- EMBED questions using [Answer]: tag format
- Focus ONLY on genuinely ambiguous topics not covered by loaded mandatory skills
- **When in doubt, check the skill first** — if the skill has ANY guidance on the topic, use it instead of asking
- Aim for 3-5 questions maximum when a mandatory skill is loaded (the skill handles the rest)

**Question categories to evaluate** (SKIP categories already covered by mandatory skills):
- **User Personas** - Ask about user types, roles, characteristics, and motivations
  - **Smart default**: If personas are self-explanatory from requirements (e.g., `SSO_Admin`, `SSO_Viewer`, role-based names), default to **Thin personas** (role + permissions summary only) without asking. Only ask about Rich/Hybrid personas if Prototyping or UX research is in scope, or if personas have complex motivations not obvious from their role name.
- ~~**Story Granularity**~~ - SKIP if mandatory skill defines granularity (e.g., `hu-template` → 1 HU per endpoint/screen)
- ~~**Story Format**~~ - SKIP if mandatory skill defines format (e.g., `hu-template` → "Como/Quiero/Para")
- ~~**Breakdown Approach**~~ - SKIP if mandatory skill defines grouping (e.g., `hu-template` → Epic + Layer/Repo)
- ~~**Acceptance Criteria**~~ - SKIP if mandatory skill defines format (e.g., `hu-template` → SMART + min 3)
- ~~**Mockups/Prototypes**~~ - SKIP — skill defaults to "Pendiente" + Prototyping stage handles visual references
- **User Journeys** - Ask about user workflows, interaction patterns, and experience flows
- **Business Context** - Ask about business goals, success metrics, and stakeholder needs
- **Technical Constraints** - Ask about technical limitations, integration requirements, and system boundaries

## Step 4: Include Mandatory Story Artifacts in Plan
- **ALWAYS** include these mandatory artifacts in the story plan:
  - [ ] Generate stories.md with user stories following INVEST criteria
  - [ ] Generate personas.md with user archetypes and characteristics
  - [ ] Ensure stories are Independent, Negotiable, Valuable, Estimable, Small, Testable
  - [ ] Include acceptance criteria for each story
  - [ ] Map personas to relevant user stories

## Step 5: Present Story Options
- Include different approaches for story breakdown in the plan document:
  - **User Journey-Based**: Stories follow user workflows and interactions
  - **Feature-Based**: Stories organized around system features and capabilities
  - **Persona-Based**: Stories grouped by different user types and their needs
  - **Domain-Based**: Stories organized around business domains or contexts
  - **Epic-Based**: Stories structured as hierarchical epics with sub-stories
- Explain trade-offs and benefits of each approach
- Allow for hybrid approaches with clear decision criteria

## Step 6: Store Story Plan
- Save the complete story plan with embedded questions in `aidlc-docs/inception/plans/` directory
- Filename: `story-generation-plan.md`
- Include all [Answer]: tags for user input
- Ensure plan is comprehensive and covers all story development aspects

## Step 7: Request User Input
- Ask user to fill in all [Answer]: tags directly in the story plan document
- Emphasize importance of audit trail and decision documentation
- Provide clear instructions on how to fill in the [Answer]: tags
- Explain that all questions must be answered before proceeding

## Step 8: Collect Answers
- Wait for user to provide answers to all questions using [Answer]: tags in the document
- Do not proceed until ALL [Answer]: tags are completed
- Review the document to ensure no [Answer]: tags are left blank

## Step 9: ANALYZE ANSWERS (MANDATORY)
Before proceeding, you MUST carefully review all user answers for:
- **Vague or ambiguous responses**: "mix of", "somewhere between", "not sure", "depends", "maybe", "probably"
- **Undefined criteria or terms**: References to concepts without clear definitions
- **Contradictory answers**: Responses that conflict with each other
- **Missing generation details**: Answers that lack specific guidance for implementation
- **Answers that combine options**: Responses that merge different approaches without clear decision rules
- **Incomplete explanations**: Answers that reference external factors without defining them
- **Assumption-based responses**: Answers that assume knowledge not explicitly stated

## Step 10: MANDATORY Follow-up Questions
If the analysis in step 9 reveals ANY ambiguous answers, you MUST:
- Create a separate clarification questions file using [Answer]: tags
- DO NOT proceed to approval until ALL ambiguities are completely resolved
- **CRITICAL**: Be thorough - ask follow-up questions for every unclear response
- Examples of required follow-ups:
  - "You mentioned 'mix of A and B' - what specific criteria should determine when to use A vs B?"
  - "You said 'somewhere between A and B' - can you define the exact middle ground approach?"
  - "You indicated 'not sure' - what additional information would help you decide?"
  - "You mentioned 'depends on complexity' - how do you define complexity levels and thresholds?"
  - "You chose 'hybrid approach' - what are the specific rules for when to use each method?"
  - "You said 'probably X' - what factors would make it definitely X vs definitely not X?"
  - "You referenced 'standard practice' - can you define what that standard practice is?"

## Step 11: Avoid Implementation Details
- Focus on story creation methodology, not prioritization or development tasks
- Do not discuss technical generation at this stage
- Avoid creating development timelines or sprint planning
- Keep focus on story structure and format decisions

## Step 12: Log Approval Prompt
- Before asking for approval, log the prompt with timestamp in `aidlc-docs/audit.md`
- Include the complete approval prompt text
- Use ISO 8601 timestamp format

## Step 13: Wait for Explicit Approval of Plan
- Do not proceed until the user explicitly approves the story approach
- Approval must be clear and unambiguous
- If user requests changes, update the plan and repeat the approval process

## Step 14: Record Approval Response
- Log the user's approval response with timestamp in `aidlc-docs/audit.md`
- Include the exact user response text
- Mark the approval status clearly

---

# PART 2: GENERATION

## Step 15: Load Story Generation Plan
- [ ] Read the complete story plan from `aidlc-docs/inception/plans/story-generation-plan.md`
- [ ] Identify the next uncompleted step (first [ ] checkbox)
- [ ] Load the context and requirements for that step

## Step 16: Execute Current Step

### SKILL CHECK: hu-format / hu-template
**IF** `aidlc-state.md` → Organizational Skills section lists a skill with ID `hu-format` or `hu-template`:
1. Load the skill file content
2. Read the `enforcement` field from the skill's YAML frontmatter
3. **IF enforcement = "mandatory"**:
   → Auto-apply the skill's format as the default template for all stories. Do NOT ask for confirmation.
   → Inform the user: *"Applying mandatory organizational standard: `[skill ID]` — [brief summary of template]. These rules are fixed. You can override specific parts if needed."*
   → The skill defines the structure (fields, numbering, sections) — the AI-DLC workflow provides the content (personas, acceptance criteria, business rules derived from requirements).
4. **IF enforcement = "optional" OR field is absent**:
   → Present to the user: *"I found an organizational skill for User Story format: `[skill ID]`. It defines [brief summary]. Should I use this as the base template for generating stories?"*
   → **IF user confirms** → Use the skill's format as the default template
   → **IF user declines** → Proceed with standard AI-DLC story generation (INVEST criteria, generic format)
**ELSE** (no skill available):
- Continue with standard story generation behavior

**See `common/organizational-skills.md` for the full skills system documentation (including enforcement levels).**

- [ ] Perform exactly what the current step describes
- [ ] Generate story artifacts as specified in the plan
- [ ] Follow the approved methodology and format from Planning (or from the loaded skill template if confirmed)
- [ ] Use the story breakdown approach specified in the plan

## Step 17: Update Progress
- [ ] Mark the completed step as [x] in the story generation plan
- [ ] Update `aidlc-docs/aidlc-state.md` current status
- [ ] Save all generated artifacts

## Step 18: Continue or Complete Generation
- [ ] If more steps remain, return to Step 14
- [ ] If all steps complete, verify stories are ready for next stage
- [ ] Ensure all mandatory artifacts are generated

## Step 19: Log Approval Prompt
- Before asking for approval, log the prompt with timestamp in `aidlc-docs/audit.md`
- Include the complete approval prompt text
- Use ISO 8601 timestamp format

## Step 20: Present Completion Message
- Present completion message in this structure:
     1. **Completion Announcement** (mandatory): Always start with this:

```markdown
# 📚 User Stories Complete
```

     2. **AI Summary** (optional): Provide structured bullet-point summary of generated stories
        - Format: "User stories generation has created [description]:"
        - List key personas generated (bullet points)
        - List user stories created with counts and organization
        - Mention story structure and compliance (INVEST criteria, acceptance criteria)
        - DO NOT include workflow instructions ("please review", "let me know", "proceed to next phase", "before we proceed")
        - Keep factual and content-focused
     3. **Formatted Workflow Message** (mandatory): Always end with this exact format:

```markdown
> **📋 REVIEW REQUIRED:**  
> Please examine the user stories and personas at: `aidlc-docs/inception/user-stories/stories.md` and `aidlc-docs/inception/user-stories/personas.md`



> **🚀 WHAT'S NEXT?**
>
> **You may:**
>
> - 🔧 **Request Changes** -  Ask for modifications to the stories or personas based on your review  
> - ✅ **Approve & Continue** - Approve user stories and proceed to **Workflow Planning**

---
```

## Step 21: Wait for Explicit Approval of Generated Stories
- Do not proceed until the user explicitly approves the generated stories
- Approval must be clear and unambiguous
- If user requests changes, update stories and repeat the approval process

## Step 22: Record Approval Response
- Log the user's approval response with timestamp in `aidlc-docs/audit.md`
- Include the exact user response text
- Mark the approval status clearly

## Step 23: Update Progress
- Mark User Stories stage complete in `aidlc-state.md`
- Update the "Current Status" section
- Prepare for transition to next stage

---

# CRITICAL RULES

## Planning Phase Rules
- **CONTEXT-APPROPRIATE QUESTIONS**: Only ask questions relevant to this specific context
- **MANDATORY ANSWER ANALYSIS**: Always analyze answers for ambiguities before proceeding
- **NO PROCEEDING WITH AMBIGUITY**: Must resolve all vague answers before generation
- **EXPLICIT APPROVAL REQUIRED**: User must approve plan before generation starts

## Generation Phase Rules
- **NO HARDCODED LOGIC**: Only execute what's written in the story generation plan
- **FOLLOW PLAN EXACTLY**: Do not deviate from the step sequence
- **UPDATE CHECKBOXES**: Mark [x] immediately after completing each step
- **USE APPROVED METHODOLOGY**: Follow the story approach from Planning
- **VERIFY COMPLETION**: Ensure all story artifacts are complete before proceeding

## Back-Propagation Rule (Cross-Stage Consistency)
When User Stories introduces a NEW business rule, error code, or constraint that was NOT in `requirements.md`:
1. Mark it in `stories.md` with: `> NEW RULE: [description] — not in requirements.md`
2. At the end of the stage, list ALL new rules/codes introduced
3. Ask the user: "User Stories introduced N new rules not in requirements. Update requirements.md retroactively?"
4. If user approves, update `requirements.md` with the new rules before proceeding
5. This ensures traceability chain (Requirements → Stories → API → Code) stays consistent

## Completion Criteria
- All planning questions answered and ambiguities resolved
- Story plan explicitly approved by user
- All steps in story generation plan marked [x]
- All story artifacts generated according to plan (stories.md, personas.md)
- Generated stories explicitly approved by user
- Stories verified and ready for next stage
