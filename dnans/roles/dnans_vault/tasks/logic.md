- check if vault.yaml exists
	- if so check if become password is set in vault.yaml
		- if so skip this vault logic and proceed with step 2
		- if not check if this playbook was run with --ask-become-password.
			- if not, error out with a message stating that become password must be in vault.yaml or this playbook must be executed with --ask-become-password
			- if so proceed with playbook.
	2.  if not, create ./vault.yaml from vault.default.yaml (currently /files/vault.default.yaml but could also be turned into a .j2 template in /templates)
		- encrypt vault
		- open vault for editing (instructions provided in vault.yaml comments)


1. check if vault.yaml exists
	1. if so, proceed with the rest of the playbook.
	2. if not, create vault.yaml from "template" (either a file in /files or a .j2 template in /templates.  this is a file with comments describing which values are necessary and which are optional.)
2. check if become password is set in vault.yaml
	1. if so, proceed with the rest of the playbook.
	2. if not, check if playbook was run with --ask-become-password
		1. if so proceed with the rest of the playbook.
		2. if not stop and present the user a message a message stating that become password must be in vault.yaml or this playbook must be executed with --ask-become-password
			1. if not error out with a message reiterating that a become password must be in vault.yaml or this playbook must be executed with --ask-become-password.
3. encrypt vault.yaml
	1. check if ansible vault pass is declared and available, use it if possible, else use the built-in ansible logic to prompt for password.