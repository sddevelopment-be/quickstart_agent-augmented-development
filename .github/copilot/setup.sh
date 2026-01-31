#!/usr/bin/env bash
set -euo pipefail

# GitHub Copilot Environment Setup Script
# Purpose: Preinstall CLI tools for agent-augmented development
# Reference: Directive 001 (CLI & Shell Tooling)
# Platform: Linux (apt) and macOS (brew)
# Performance target: <2 minutes
# Security: SHA256 checksum verification for binary downloads

SCRIPT_VERSION="1.1.0"
SETUP_START_TIME=$(date +%s)

# SHA256 checksums for binary downloads (security hardening)
# To update checksums when upgrading tool versions:
# 1. Download the new binary: curl -sL <URL> -o /tmp/binary
# 2. Calculate checksum: sha256sum /tmp/binary
# 3. Update the constant below with the new checksum
# 4. Update the version variable in the installation section
# 5. Test the installation: bash .github/copilot/setup.sh
readonly YQ_VERSION="v4.40.5"
readonly YQ_LINUX_AMD64_SHA256="0d6aaf1cf44a8d18fbc7ed0ef14f735a8df8d2e314c4cc0f0242d35c0a440c95"

readonly AST_GREP_VERSION="0.15.1"
readonly AST_GREP_LINUX_X86_64_SHA256="c30cd436e7e33ebe8a25e2dd1be0e8ae9650610991a51f723211a5e70bb23377"

# Color output for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Version comparison helper
version_ge() {
    [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$2" ]
}

# Verify SHA256 checksum of downloaded file
# Usage: verify_checksum <file_path> <expected_sha256> <tool_name>
# Returns: 0 if checksum matches, 1 if mismatch
verify_checksum() {
    local file_path="$1"
    local expected_checksum="$2"
    local tool_name="$3"
    
    if [ ! -f "$file_path" ]; then
        log_error "File not found for checksum verification: $file_path"
        return 1
    fi
    
    log_info "Verifying SHA256 checksum for $tool_name..."
    local actual_checksum
    actual_checksum=$(sha256sum "$file_path" | awk '{print $1}')
    
    if [ "$actual_checksum" = "$expected_checksum" ]; then
        log_success "Checksum verification passed for $tool_name"
        return 0
    else
        log_error "Checksum verification FAILED for $tool_name"
        log_error "Expected: $expected_checksum"
        log_error "Actual:   $actual_checksum"
        log_error "This may indicate a compromised download or version mismatch."
        log_error "DO NOT install this binary. Please investigate."
        return 1
    fi
}

# Install tool with idempotency check
install_tool() {
    local tool_name="$1"
    local install_cmd="$2"
    local version_check="${3:-}"
    
    if command_exists "$tool_name"; then
        if [ -n "$version_check" ]; then
            local current_version
            current_version=$($version_check 2>/dev/null || echo "unknown")
            log_success "$tool_name already installed: $current_version"
        else
            log_success "$tool_name already installed"
        fi
        return 0
    fi
    
    log_info "Installing $tool_name..."
    if eval "$install_cmd"; then
        log_success "$tool_name installed successfully"
        return 0
    else
        log_error "Failed to install $tool_name"
        return 1
    fi
}

# Main setup function
main() {
    log_info "Starting GitHub Copilot tooling setup v${SCRIPT_VERSION}"
    log_info "Target: <2 minutes for common tools"
    
    local os
    os=$(detect_os)
    log_info "Detected OS: $os"
    
    if [ "$os" = "unknown" ]; then
        log_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    
    local failed_tools=()
    
    # Update package manager (once)
    if [ "$os" = "linux" ]; then
        log_info "Updating apt package list..."
        if ! sudo apt-get update -qq; then
            log_warning "apt-get update failed, continuing anyway..."
        fi
    fi
    
    # Install ripgrep (rg) - fast code search
    if [ "$os" = "linux" ]; then
        if ! install_tool "rg" "sudo apt-get install -y ripgrep" "rg --version | head -n1"; then
            failed_tools+=("ripgrep")
        fi
    else
        if ! install_tool "rg" "brew install ripgrep" "rg --version | head -n1"; then
            failed_tools+=("ripgrep")
        fi
    fi
    
    # Install fd - fast file finder
    if [ "$os" = "linux" ]; then
        if ! install_tool "fd" "sudo apt-get install -y fd-find && sudo ln -sf \$(which fdfind) /usr/local/bin/fd 2>/dev/null || true" "fd --version"; then
            failed_tools+=("fd")
        fi
    else
        if ! install_tool "fd" "brew install fd" "fd --version"; then
            failed_tools+=("fd")
        fi
    fi
    
    # Install jq - JSON processor
    if [ "$os" = "linux" ]; then
        if ! install_tool "jq" "sudo apt-get install -y jq" "jq --version"; then
            failed_tools+=("jq")
        fi
    else
        if ! install_tool "jq" "brew install jq" "jq --version"; then
            failed_tools+=("jq")
        fi
    fi
    
    # Install yq - YAML processor (using mikefarah/yq via binary download for consistency)
    if ! command_exists "yq"; then
        log_info "Installing yq ${YQ_VERSION}..."
        if [ "$os" = "linux" ]; then
            local yq_url="https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64"
            local yq_tmp="/tmp/yq_download"
            
            # Download binary
            if ! curl -sL "$yq_url" -o "$yq_tmp"; then
                log_error "Failed to download yq from $yq_url"
                failed_tools+=("yq")
            # Verify checksum
            elif ! verify_checksum "$yq_tmp" "$YQ_LINUX_AMD64_SHA256" "yq"; then
                log_error "Checksum verification failed for yq - aborting installation"
                rm -f "$yq_tmp"
                failed_tools+=("yq")
            # Install if verification passes
            elif sudo install "$yq_tmp" /usr/local/bin/yq && rm -f "$yq_tmp"; then
                log_success "yq installed successfully with verified checksum"
            else
                log_error "Failed to install yq"
                rm -f "$yq_tmp"
                failed_tools+=("yq")
            fi
        else
            if ! install_tool "yq" "brew install yq" "yq --version"; then
                failed_tools+=("yq")
            fi
        fi
    else
        log_success "yq already installed: $(yq --version 2>/dev/null || echo 'unknown')"
    fi
    
    # Install fzf - fuzzy finder
    if [ "$os" = "linux" ]; then
        if ! install_tool "fzf" "sudo apt-get install -y fzf" "fzf --version"; then
            failed_tools+=("fzf")
        fi
    else
        if ! install_tool "fzf" "brew install fzf" "fzf --version"; then
            failed_tools+=("fzf")
        fi
    fi
    
    # Install ast-grep - structural code search (via direct binary download with checksum verification)
    if ! command_exists "ast-grep"; then
        log_info "Installing ast-grep ${AST_GREP_VERSION}..."
        if [ "$os" = "linux" ]; then
            local sg_url="https://github.com/ast-grep/ast-grep/releases/download/${AST_GREP_VERSION}/sg-x86_64-unknown-linux-gnu.zip"
            local sg_zip="/tmp/ast-grep.zip"
            local sg_tmp_dir="/tmp/ast-grep-extract"
            
            # Download binary archive
            if ! curl -sL "$sg_url" -o "$sg_zip"; then
                log_error "Failed to download ast-grep from $sg_url"
                failed_tools+=("ast-grep")
            # Verify checksum
            elif ! verify_checksum "$sg_zip" "$AST_GREP_LINUX_X86_64_SHA256" "ast-grep"; then
                log_error "Checksum verification failed for ast-grep - aborting installation"
                rm -f "$sg_zip"
                failed_tools+=("ast-grep")
            # Extract and install if verification passes (binary is named 'sg', create ast-grep symlink)
            elif mkdir -p "$sg_tmp_dir" && \
                 unzip -q "$sg_zip" -d "$sg_tmp_dir" && \
                 sudo install "$sg_tmp_dir/sg" /usr/local/bin/sg && \
                 sudo ln -sf /usr/local/bin/sg /usr/local/bin/ast-grep; then
                log_success "ast-grep installed successfully with verified checksum"
                rm -rf "$sg_zip" "$sg_tmp_dir"
            else
                log_error "Failed to install ast-grep"
                rm -rf "$sg_zip" "$sg_tmp_dir"
                failed_tools+=("ast-grep")
            fi
        else
            # macOS: use homebrew
            if ! install_tool "ast-grep" "brew install ast-grep" "ast-grep --version"; then
                failed_tools+=("ast-grep")
            fi
        fi
    else
        log_success "ast-grep already installed: $(ast-grep --version 2>/dev/null || echo 'unknown')"
    fi
    
    # Summary
    local setup_end_time
    setup_end_time=$(date +%s)
    local duration=$((setup_end_time - SETUP_START_TIME))
    
    echo ""
    log_info "=========================================="
    log_info "Setup completed in ${duration} seconds"
    log_info "=========================================="
    
    # Verify installations
    echo ""
    log_info "Verifying tool availability..."
    local verification_failed=false
    
    for tool in rg fd jq yq fzf ast-grep; do
        if command_exists "$tool"; then
            local version
            case "$tool" in
                rg) version=$(rg --version | head -n1) ;;
                fd) version=$(fd --version) ;;
                jq) version=$(jq --version) ;;
                yq) version=$(yq --version) ;;
                fzf) version=$(fzf --version) ;;
                ast-grep) version=$(ast-grep --version) ;;
            esac
            echo -e "  ${GREEN}✓${NC} $tool: $version"
        else
            echo -e "  ${RED}✗${NC} $tool: NOT FOUND"
            verification_failed=true
        fi
    done
    
    echo ""
    if [ "$verification_failed" = true ] || [ ${#failed_tools[@]} -gt 0 ]; then
        log_warning "Some tools failed to install or are not available"
        if [ ${#failed_tools[@]} -gt 0 ]; then
            log_warning "Failed tools: ${failed_tools[*]}"
        fi
        exit 1
    else
        log_success "All tools installed and verified successfully!"
        log_info "GitHub Copilot environment is ready for agent-augmented development"
        exit 0
    fi
}

# Run main function
main "$@"
