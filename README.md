# dnans.org Ansible Test Playground

# present state - completely broken, I'm mid-stream of a refactor of many things so this is presently a development branch

dnans is [gradyp's](https://www.gradyp.com) dev environment. this is purely a place to learn and play.

currently this is my Ansible playground where I'm exploring potential replacements for [snand.org's](https://snand.org) script based setup.

**disclaimer**:  
this repo is experimental and contains work-in-progress code.  it's not intended for public use, but if you find anything here useful, feel free...

---

## current focus

- ~~setting up a basic Ansible project structure.~~
- automating server configurations, including:
  - ~~installing essential packages (`sudo`, `docker`, `samba`, `nfs`).~~
  - managing system services.
  - setting up persistent mounts using UUIDs.
  - configuring SMB shares
- installing docker projects
- ~~traefik~~
 - cloudflare
 - Wordpress
 - immich


## future enhancements

- versioning for .env and compose files
  - .env skipped if it exists, need logic for checking version or something in case of future change

---

## Versioning

| Version   | Status        | Description                      |
|-----------|---------------|----------------------------------|
| `v0.0.2`  | wip | Docker, traefik and wordpress working. |
| `v0.0.1`  | wip | Initial setup, basic configurations. |
| `v0.0.x`  | begin progress | Iterative improvements and testing. |

