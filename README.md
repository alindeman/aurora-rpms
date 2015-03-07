# aurora-rpms

[Apache Aurora](http://aurora.incubator.apache.org) is a bit tricky to build
right now. This repository builds three separate RPMs for the scheduler,
client, and thermos.

Currently uses EL7 (CentOS 7), but should be adaptable for any RPM-based
system.

## Quickstart

```
vagrant up # or vagrant provision if the VM is already up

ls RPMS/x86_64
ls SRPMS
```
