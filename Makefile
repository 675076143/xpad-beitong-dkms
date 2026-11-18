obj-m := xpad.o

IS_CLANG := $(shell grep -q '^CONFIG_CC_IS_CLANG=y' $(KERNEL_DIR)/include/config/auto.conf 2>/dev/null && echo 1 || echo 0)

ifeq ($(IS_CLANG),1)
    LLVM_FLAG := LLVM=1
else
    LLVM_FLAG :=
endif

all:
	$(MAKE) -C $(KERNEL_DIR) M=$(PWD) $(LLVM_FLAG) modules

clean:
	$(MAKE) -C $(KERNEL_DIR) M=$(PWD) $(LLVM_FLAG) clean
