# Direct-check setup observations

Website checks initially reused existing dependencies through a local node_modules symlink. The native verifier correctly refused that linked output root; the link was removed and replaced with a physical copy-on-write copy of the same installed dependencies. No installation or validator change was made. The successful native readback is retained separately.

This second-generation clone initially lacked local main/staging refs. Direct historical ticket validation refused missing landing evidence until the required local refs were supplied from a fresh remote readback: main8b31956f47075a831cfd0339339f616af96b3dae/staging05fc16c30f978bbafab4b8cc89f24f8657ab3045. No receipt or target ref was changed remotely. The first full source run had been interrupted after a review finding; only the revised complete run is reported as passing.
