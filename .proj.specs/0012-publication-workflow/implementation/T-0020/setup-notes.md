# Direct-check setup observations

Website checks initially reused existing dependencies through a local node_modules symlink. The native verifier correctly refused that linked output root; the link was removed and replaced with a physical copy-on-write copy of the same installed dependencies. No installation or validator change was made. The successful native readback is retained separately.

The first focused attempt also lacked permission for the parent loopback listener; later actual probe runs permit the parent listener while keeping deny-default sandbox-exec children. This is not a weakened candidate sandbox.
