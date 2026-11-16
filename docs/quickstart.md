# 🚀 Quick Start Guide

Welcome to the self-hosted alternatives ecosystem! This guide will get you started in minutes.

## 📋 Prerequisites

Before you begin, ensure you have:
- Docker and Docker Compose installed
- A domain name (optional but recommended)
- Portainer or similar for management (recommended)

## 🏃‍♂️ Quick Deployment

### Option 1: Docker Compose (Easy)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  logseq:
    image: logseq/logseq:latest
    container_name: logseq
    ports:
      - "3000:3000"
    volumes:
      - ./data:/data
    restart: unless-stopped
    environment:
      - TZ=UTC

  wekan:
    image: wekan/wekan:latest
    container_name: wekan
    ports:
      - "8080:80"
    depends_on:
      - mongo
    restart: unless-stopped
    environment:
      - MONGO_URL=mongodb://mongo:27017/wekan
      - ROOT_URL=http://localhost:8080

  mongo:
    image: mongo:6
    container_name: wekan-mongo
    restart: unless-stopped
    volumes:
      - ./mongo-data:/data/db
```

Then run:
```bash
docker-compose up -d
```

### Option 2: Single Container

For quick testing, use single-container deployments:

```bash
# Logseq (note-taking)
docker run -d -p 3000:3000 -v $PWD/logseq-data:/data logseq/logseq

# Joplin (another note-taking option)
docker run -d -p 22300:22300 -v $PWD/joplin-data:/home/user/.config/joplin-desktop joplin/joplin:latest

# Wekan (Trello alternative)
docker run -d -p 8080:80 --name wekan wekan/wekan
```

## 🔐 Production Setup

### Reverse Proxy (Caddy)

```yaml
version: '3.8'

services:
  caddy:
    image: caddy:latest
    container_name: caddy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    restart: unless-stopped

  logseq:
    image: logseq/logseq:latest
    restart: unless-stopped
    volumes:
      - logseq_data:/data

volumes:
  caddy_data:
  caddy_config:
  logseq_data:
```

### Caddyfile Configuration

```
notion.yourdomain.com {
    reverse_proxy logseq:3000
    encode gzip
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
    }
}

todo.yourdomain.com {
    reverse_proxy wekan:80
    encode gzip
}
```

## 🛡️ Security Best Practices

### 1. Environment Variables

Never hardcode secrets in compose files:

```yaml
environment:
  - SECRET_KEY_BASE=${SECRET_KEY_BASE}
  - DATABASE_URL=${DATABASE_URL}
```

Use `.env` files:
```bash
# .env (never commit this!)
SECRET_KEY_BASE=your-secret-key-here
DATABASE_URL=postgres://user:pass@db:5432/app
```

### 2. User Isolation

Run containers as non-root users:

```yaml
user: "1000:1000"
```

### 3. Read-Only Root Filesystem

```yaml
read_only: true
tmpfs:
  - /tmp
volumes:
  - ./config:/config:rw
  - ./data:/data:rw
```

### 4. Resource Limits

```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
```

## 📊 Monitoring

### Health Checks

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Logs Aggregation

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## 🔄 Backup Strategies

### Automated Backups

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup Logseq
docker exec logseq tar -czf - /data > "$BACKUP_DIR/logseq_$DATE.tar.gz"

# Backup Wekan database
docker exec wekan-mongo mongodump --archive=/dump.tar.gz --gzip
docker cp wekan-mongo:/dump.tar.gz "$BACKUP_DIR/wekan_$DATE.tar.gz"

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### Scheduled Backups (Cron)

```cron
# Daily at 2 AM
0 2 * * * /scripts/backup.sh
# Weekly on Sunday at 3 AM
0 3 * * 0 /scripts/backup.sh --full
```

## 📱 Mobile Access

Most self-hosted alternatives have mobile apps:

| Tool | iOS | Android | Notes |
|------|-----|---------|-------|
| Logseq | ✅ | ✅ | Native apps available |
| Wekan | ✅ | ✅ | Web app works on mobile |
| Joplin | ✅ | ✅ | Native apps |
| Outline | ❌ | ❌ | Web only |
| LanguageTool | ✅ | ✅ | Via web or apps |

## 🆘 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find what's using the port
netstat -tulpn | grep 3000
# Or
lsof -i :3000

# Kill the process
kill -9 $(lsof -t -i :3000)
```

**Container Won't Start**
```bash
# Check container logs
docker logs container-name

# Check for port conflicts
docker-compose ps

# Recreate container
docker-compose down
docker-compose up -d
```

**Database Connection Issues**
```bash
# Check if database is healthy
docker exec mongo-name mongosh --eval "db.adminCommand('ping')"

# Check network
docker network ls
docker inspect network-name
```

## 📚 Next Steps

- Read the [full documentation](./documentation.md)
- Check [alternative documentation](./productivity.md)
- Join our [GitHub Discussions](https://github.com/aayushmanrajputdev/awesome-selfhosted-alternatives/discussions)
- [Submit a missing tool](https://github.com/aayushmanrajputdev/awesome-selfhosted-alternatives/issues/new?template=add_tool.md)

---

**Ready to self-host your productivity stack?**  
[← Back to Catalog](../index.md)