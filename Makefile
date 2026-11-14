# Kbuild is separate so DKMS's KERNELRELEASE does not bypass this wrapper.
.DEFAULT_GOAL := all
KVER ?= $(shell uname -r)
KDIR ?= /usr/lib/modules/$(KVER)/build

# XPAD_LLVM also overrides LLVM appended by some DKMS versions.
ifneq ($(origin XPAD_LLVM),undefined)
override LLVM := $(XPAD_LLVM)
endif

# Kbuild does not infer LLVM from the target kernel configuration.
# An explicit LLVM= (GCC), LLVM=1, LLVM=-NN or LLVM=/path/ wins.
ifeq ($(origin LLVM),undefined)
ifeq ($(shell grep -cx 'CONFIG_CC_IS_CLANG=y' "$(KDIR)/.config" 2>/dev/null),1)
LLVM := 1
else ifeq ($(shell grep -cx 'CONFIG_CC_IS_GCC=y' "$(KDIR)/.config" 2>/dev/null),1)
LLVM :=
else
$(error Cannot identify target compiler in $(KDIR)/.config; provide valid headers or explicit LLVM)
endif
endif

.PHONY: all modules clean
all modules:
	$(MAKE) -C "$(KDIR)" M="$(CURDIR)" LLVM="$(LLVM)" modules

clean:
	$(MAKE) -C "$(KDIR)" M="$(CURDIR)" LLVM="$(LLVM)" clean
