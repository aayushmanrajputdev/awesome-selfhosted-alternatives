# Contributing to awesome-selfhosted-alternatives

We welcome contributions! This directory helps you find the right place to contribute, whether you're a first-time contributor or a seasoned maintainer.

## 🎯 Where to Start

### For First-Time Contributors
1. **Good First Issues** - Look for issues labeled `good first issue` or `beginner-friendly`
2. **Add Missing Tools** - Check if your favorite SaaS tool is missing an alternative
3. **Add Screenshots** - Visual documentation helps everyone
4. **Fix Typos** - Small improvements make a big difference

### For Experienced Contributors
1. **Review & Improve Entries** - Verify Docker images, add benchmarks
2. **Add New Categories** - Expand the catalog's coverage
3. **Write Documentation** - Create guides for deployment patterns
4. **Build Automation** - Improve the CLI tool or add new commands

## 📋 How to Submit Contributions

### Adding a New Alternative

1. **Check if it already exists**:
   ```bash
   grep -i "toolname" data/*.json
   ```

2. **Create a new entry** in the appropriate category file:
   ```bash
   data/productivity.json  # For productivity tools
   data/communication.json  # For communication tools
   # ... etc
   ```

3. **Follow this format**:
   ```json
   {
     "saas_tool": {
       "name": "Notion",
       "url": "https://www.notion.so/",
       "description": "All-in-one workspace"
     },
     "alternative": {
       "name": "Logseq",
       "url": "https://logseq.com/",
       "license": "MIT",
       "docker": {
         "official": true,
         "image": "logseq/logseq",
         "tags": ["latest", "stable"]
       },
       "self_hosted": true,
       "cloud_variants": false,
       "category_tags": ["note-taking", "knowledge-base"]
     },
     "added_date": "2024-01-15",
     "contributor": "your-github-username"
   }
   ```

4. **Submit a Pull Request** with a clear description

### Improving Documentation

- Edit files in `/docs/` directory
- Use clear, concise language
- Include code examples where helpful
- Update README if needed

### Reporting Issues

Use the issue templates:
- **Bug Report**: Something doesn't work
- **Feature Request**: Missing tool or alternative
- **Documentation**: Typo, outdated info, or missing guide

## 🏷️ Labels We Use

| Label | What It Means | Good For |
|-------|--------------|----------|
| `good first issue` | Beginner-friendly | New contributors |
| `documentation` | Docs only | Writers, editors |
| `docker` | Docker-related | DevOps, sysadmins |
| `security` | Security concerns | Security folks |
| `help wanted` | Need assistance | All contributors |

## 📚 Style Guide

### Naming Conventions
- **SaaS tools**: Use common brand names (Notion, Slack, Dropbox)
- **Alternatives**: Use official project names (Logseq, Mattermost, Nextcloud)

### Categories
Choose from our predefined structure:
- Productivity
- Communication
- Analytics
- Monitoring
- Storage
- Media
- Development
- Security
- Finance
- Health

### Verification Checklist
Before submitting, verify:
- [ ] Alternative actually works
- [ ] Docker image exists and is maintained
- [ ] License is open-source
- [ ] Project has public documentation
- [ ] No obvious security issues

## 🤝 Communication

- **GitHub Discussions**: General questions, feedback, ideas
- **Issues**: Bug reports, feature requests
- **Pull Requests**: Code/documentation contributions

## 🙏 Attribution

Contributors who submit useful pull requests appear in our [CONTRIBUTORS.md](./CONTRIBUTORS.md) file!

---

**Ready to contribute? Let's make self-hosted alternatives the default choice for developers everywhere! 🚀**