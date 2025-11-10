REPO_ROOT ?= $(shell git rev-parse --show-toplevel)

DEFINES += -DHEXPATH=\"$(REPO_ROOT)/part2/sigmoid/\"
PCF_PATH = $(REPO_ROOT)/part2/sigmoid/icebreaker.pcf
-include $(REPO_ROOT)/frag/simulate.mk
-include $(REPO_ROOT)/frag/synth.mk
-include $(REPO_ROOT)/frag/fpga.mk

