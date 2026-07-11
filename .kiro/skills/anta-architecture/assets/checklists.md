# Project Checklists

## New API Project

### Repository Setup
- [ ] Create repo `api-{name}`
- [ ] Create `src/{ProjectName}.Api/` structure
- [ ] Add `nuget.config` with CodeArtifact
- [ ] Add `.gitignore`

### Project Structure
- [ ] `Program.cs` with ANTA extensions
- [ ] `Modules/{Module}/` folder
- [ ] `{Module}Module.cs` with DI + endpoints
- [ ] `{Module}StoredProcedures.cs` constants
- [ ] `appsettings.json` with connection strings

### Database
- [ ] `database/{Schema}/` folder
- [ ] `00_Schema.sql`
- [ ] `01_Tables.sql`
- [ ] `StoredProcedures/` folder
- [ ] `README.md` documenting tables and SPs

### First Feature
- [ ] Feature folder with all files
- [ ] Request DTO
- [ ] Response DTO (with wrapper)
- [ ] Handler
- [ ] Endpoint
- [ ] Validator (if POST/PUT)
- [ ] MappingProfile (if List/Get)
- [ ] SP in database folder

---

## New Frontend Project (Child)

### Repository Setup
- [ ] Create repo `Front{Module}`
- [ ] Create `src/{ProjectName}.Front/` structure
- [ ] Add `.npmrc` with internal registry
- [ ] Add `.gitignore`

### Project Structure
- [ ] `package.json` with name `mf-{module}-remote`
- [ ] `rsbuild.config.ts` with correct `name` (lowercase)
- [ ] `tsconfig.json` with `host/*` path mapping
- [ ] `@mf-types/host/` for Host types

### Host Integration
- [ ] `shared/adapters/` with useHostApi, useHostAuth
- [ ] Add to Host's `mf-remotes.json`
- [ ] Menu configured in backend (routes match module path)
- [ ] `eager: false` for all shared deps

### First Feature
- [ ] Feature folder with components, hooks, types
- [ ] Query hook using `createServiceQuery`
- [ ] Mutation hook using `createServiceMutation`
- [ ] Types matching API response
- [ ] Export from `index.ts`
