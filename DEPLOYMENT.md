# Deployment Guide

## GitHub Actions

### Setup

1. **Create GitHub secrets:**
   ```
   DOCKER_USERNAME: your-docker-hub-username
   DOCKER_PASSWORD: your-docker-hub-token (or password)
   ```

2. **Workflow file:** `.github/workflows/docker-build.yml`
   - Builds on every push to `main`/`master`
   - Builds on every tag `v*`
   - Runs tests
   - Generates docs
   - Pushes to Docker Hub + GitHub Container Registry

3. **Features:**
   - ✅ Tests run before build
   - ✅ Linting checks
   - ✅ Multi-stage caching
   - ✅ Multiple registries
   - ✅ Artifacts upload (docs)
   - ✅ PR builds (no push)

4. **Push Docker image:**
   ```bash
   # Just push code
   git push origin main
   
   # Or tag release
   git tag v1.0.0
   git push origin v1.0.0
   ```

5. **Access image:**
   ```bash
   docker pull yourusername/transactional-outbox:latest
   docker pull ghcr.io/yourusername/transactional-outbox:latest
   ```

---

## Docker Image Variants

### Production
```bash
docker run \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -p 8000:8000 \
  transactional-outbox:latest
```

### With Seeding
```bash
docker run \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SEED_DATA=true \
  -e SEED_COUNT=50 \
  -p 8000:8000 \
  transactional-outbox:latest
```

### With Chaos Engineering
```bash
docker run \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e WORKER_CHAOS=0.1 \
  -p 8000:8000 \
  transactional-outbox:latest
```

---

## Local Development

### Build locally
```bash
docker build -f app/Dockerfile -t transactional-outbox:dev .
```

### Test build with docker-compose
```bash
docker-compose up --build
```

### Push to local registry
```bash
docker save transactional-outbox:dev | gzip > outbox.tar.gz
```

---

## Monitoring

### GitHub Actions
- View logs: Actions tab in GitHub
- Artifacts: Generated docs available for download

---

## Security

### GitHub Actions
- Secrets encrypted at rest
- Never shown in logs
- Scoped to workflow

### Docker Registry
- Enable image scanning
- Use image digests (SHA256)
- Regular vulnerability scans
