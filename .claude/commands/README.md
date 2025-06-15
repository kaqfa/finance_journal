# Custom Claude Commands for WealthWise Development

This directory contains custom Claude Code commands optimized for WealthWise monorepo development workflow.

## 📋 Available Commands

### `/project-status` 
**Purpose**: Get comprehensive project status dan current development progress
**Usage**: Quick overview of all modules, current sprint goals, dan next priorities
**Output**: 
- Current sprint progress
- Module completion status  
- Immediate action items
- Blockers dan risks

### `/update-progress`
**Purpose**: Update development progress dan mark completed tasks
**Usage**: After completing major features atau milestones
**Behavior**:
- Updates CLAUDE.md dengan latest progress
- Marks completed tasks di roadmap
- Updates sprint metrics
- Identifies next priorities

### `/deploy-check`
**Purpose**: Pre-deployment checklist dan validation
**Usage**: Before deploying to staging atau production
**Validation**:
- All tests passing
- Code quality metrics
- Security requirements
- Documentation completeness

### `/monorepo-status`
**Purpose**: Monorepo health check dan structure validation
**Usage**: Verify monorepo setup dan dependencies
**Checks**:
- Package dependencies
- Build system status
- Cross-package compatibility
- Development environment

### `/daily-standup`
**Purpose**: Daily development summary dan planning
**Usage**: Start of development session
**Output**:
- Yesterday's completed work
- Today's priorities
- Current blockers
- Sprint goal progress

## 🔧 Command Implementation

### Command Structure
Each command is implemented as a markdown file with:
- Clear purpose dan usage instructions
- Expected inputs dan outputs
- Error handling procedures
- Integration dengan project workflow

### Integration dengan Development Workflow
Commands are designed to:
- Work seamlessly dengan existing development process
- Update project documentation automatically
- Provide actionable insights untuk decision making
- Support both individual dan team development

### Best Practices
- Run `/project-status` at start of each development session
- Use `/update-progress` after completing major milestones
- Execute `/deploy-check` before any deployment
- Daily `/daily-standup` untuk consistent progress tracking

## 📚 Documentation Integration

### Auto-Documentation Updates
Commands automatically update:
- CLAUDE.md progress tracking
- Sprint goal completion status
- Development metrics
- Next action priorities

### Consistency Maintenance
- Ensure documentation stays current dengan code
- Maintain consistent terminology across project
- Track dependencies dan integration points
- Monitor technical debt dan improvement opportunities

---

*Commands optimized for AI-assisted development workflow*  
*Version: 1.0*  
*Last Updated: June 14, 2025*