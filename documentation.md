[dnans.yaml] 
  ├── Vault Initialization
  │    ├── Load existing vault.yaml
  │    ├── Generate missing sensitive variables
  │    └── Save updated vault.yaml
  ├── Infrastructure Setup
  │    ├── dnans_host
  │    │    ├── Install packages
  │    │    ├── Configure Docker
  │    │    └── Setup SMB shares
  │    └── dnans_smb
  │         └── Configure SMB shares
  ├── Docker Environment Setup
  │    ├── dnans_docker
  │    │    ├── Create Docker network
  │    │    └── Deploy Traefik
  │    └── Application-Specific Roles
  │         ├── dnans_wordpress
  │         │    ├── Generate .env
  │         │    └── Deploy WordPress
  │         └── dnans_immich
  │              ├── Generate .env
  │              └── Deploy Immich
  └── Service Deployment
       └── Start all Docker Compose projects
       

---
