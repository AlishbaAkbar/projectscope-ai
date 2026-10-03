# 🚀 ProjectScope AI — Deployment Guide

## Prerequisites

- Docker 24+ & Docker Compose v2
- Domain name (e.g., `yourdomain.com`)
- Server: 2 vCPU, 4GB RAM, 40GB SSD (minimum)
- Ports 80 and 443 open

## Quick Start

### 1. Clone & Configure

```bash
git clone https://github.com/AlishbaAkbar/projectscope-ai.git
cd projectscope-ai

cp .env.prod.example .env.prod
nano .env.prod  # Fill in real values