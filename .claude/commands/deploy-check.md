Pre-deployment checklist for monorepo:

$ARGUMENTS (specify: frontend|backend|all)

1. **Code Quality Gates**:
   - Run all tests and report failures
   - Execute linting and fix issues
   - Verify TypeScript compilation
   - Check for security vulnerabilities

2. **Build Verification**:
   - Build specified apps/packages
   - Verify no build warnings
   - Check bundle sizes for frontend

3. **Documentation Updates**:
   - Ensure CLAUDE.md files are current
   - Check if README files need updates
   - Verify API documentation matches code

4. **Final Commit**:
   - Create meaningful commit message
   - Tag release if deploying to production
   - Update version numbers if needed

Only proceed with deployment if all checks pass.