#!/usr/bin/env bash
set -euo pipefail

# GitHub Copilot Environment Setup Script
# Purpose: Preinstall CLI tools for agent-augmented development
# Reference: Directive 001 (CLI & Shell Tooling)
# Platform: Linux (apt) and macOS (brew)
# Performance target: <2 minutes

SCRIPT_VERSION="1.0.0"
SETUP_START_TIME=$(date +%s)

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
        log_info "Installing yq..."
        local yq_version="v4.40.5"
        if [ "$os" = "linux" ]; then
            if curl -sL "https://github.com/mikefarah/yq/releases/download/${yq_version}/yq_linux_amd64" -o /tmp/yq && \
               sudo install /tmp/yq /usr/local/bin/yq && \
               rm /tmp/yq; then
                log_success "yq installed successfully"
            else
                log_error "Failed to install yq"
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
    
    # Install ast-grep - structural code search (via npm)
    if ! command_exists "ast-grep"; then
        log_info "Installing ast-grep via npm..."
        if [ "$os" = "linux" ]; then
            # Install ast-grep globally via npm (GitHub Actions runners have Node.js pre-installed)
            if command_exists "npm"; then
                if sudo npm install -g @ast-grep/cli; then
                    log_success "ast-grep installed successfully via npm"
                else
                    log_error "Failed to install ast-grep via npm"
                    failed_tools+=("ast-grep")
                fi
            else
                log_error "npm not found - cannot install ast-grep"
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
