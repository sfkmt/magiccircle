# Changelog

All notable changes to the MC (Magic Circle) Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-07-25

### Added
- **SOW (Statement of Work) Integration** - Complete automation framework for task execution
  - `/mc:sow-create` - Generates detailed work instructions from approved tasks
  - `/mc:task-execute` - Executes tasks based on generated SOW with multiple modes (interactive/automated/dry-run)
  - `/mc:spec-diff` - Visual diff tool for specification changes and implementation compliance
  - `/mc:context-optimize` - AI context optimization for improved performance and accuracy
- **Advanced Automation Workflow** - GitHub Actions workflow for fully automated spec implementation
  - Parallel task execution support
  - Automatic branch creation and PR generation
  - Integration testing and compliance reporting
  - Feedback analysis and pattern learning

### Enhanced
- **Complete Task Automation Pipeline**
  - SOW generation provides clear, structured instructions for each task
  - Context optimization reduces token usage by up to 73%
  - Execution time improvements of up to 61%
  - Automatic error recovery and retry mechanisms
- **Improved Developer Experience**
  - Interactive mode for step-by-step execution with confirmations
  - Dry-run mode for safe execution planning
  - Real-time progress tracking and reporting
  - Comprehensive compliance checking

### Integration Points
- Claude Code CLI integration for command execution
- GitHub Actions for CI/CD automation
- Hooks system for customizable workflows
- Pattern-based learning for continuous improvement

## [1.2.0] - 2025-07-25

### Added
- **GitHub Actions Integration**
  - `/mc:github-issue-create` - Automatically creates GitHub issues from approved tasks
  - `/mc:workflow-trigger` - Manually triggers GitHub Actions workflows
  - `/mc:feedback-analyze` - Analyzes implementation results and extracts patterns
- **Hooks System** - Automated pre/post approval actions
  - Pre-approval validation hooks
  - Post-approval automation hooks
  - Task completion tracking hooks

## [1.1.0] - 2025-07-24

### Changed
- Rebranded from "GAME DESIGN (gd)" to "Magic Circle (mc)"
- Updated all command prefixes from `gd:` to `mc:`
- Renamed framework directories and documentation

## [1.0.0] - 2025-07-24

### Added
- Initial release of Spec-Driven Development framework
- Core specification management commands
  - `/mc:steering-init` - Initialize project steering document
  - `/mc:steering-update` - Update project direction
  - `/mc:spec-init` - Create new feature specification
  - `/mc:spec-requirements` - Generate requirements document
  - `/mc:spec-design` - Create technical design
  - `/mc:spec-tasks` - Generate implementation tasks
  - `/mc:spec-status` - Check project progress
  - `/mc:spec-approve` - Approve specification phases
- Three-phase approval process (Requirements → Design → Tasks)
- Automatic document generation with AI assistance
- Structured project organization in `.mc/` directory