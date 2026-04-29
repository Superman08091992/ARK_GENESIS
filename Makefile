.PHONY: test compile packages repo validate-packaging validate-deployment smoke-contract render-runtime-tree

PYTHON ?= python

compile:
	$(PYTHON) -m py_compile \
		opt/ark/scripts/validate_graveyard.py \
		opt/ark/runtime/kernel/*.py \
		opt/ark/runtime/policy/*.py \
		opt/ark/runtime/action_model/*.py \
		opt/ark/runtime/execution_broker/*.py \
		opt/ark/runtime/bus/*.py \
		opt/ark/runtime/evidence/*.py \
		opt/ark/runtime/api/*.py \
		scripts/*.py \
		tests/*.py

test:
	$(PYTHON) -m unittest \
		tests/test_graveyard_contracts.py \
		tests/test_kernel_contracts.py \
		tests/test_action_authorization_flow.py \
		tests/test_action_model.py \
		tests/test_execution_broker.py \
		tests/test_end_to_end_dry_run_pipeline.py \
		tests/test_event_bus.py \
		tests/test_evidence_writer.py \
		tests/test_end_to_end_recorded_pipeline.py \
		tests/test_runtime_status_api.py \
		tests/test_packaging_scaffold.py \
		tests/test_deployment_manifest.py \
		tests/test_runtime_tree_contract.py \
		tests/test_service_registry.py

validate-packaging:
	$(PYTHON) -m unittest tests/test_packaging_scaffold.py

validate-deployment:
	$(PYTHON) -m scripts validate-deployment

smoke-contract:
	$(PYTHON) -m scripts smoke-contract

render-runtime-tree:
	$(PYTHON) -m scripts render-runtime-tree

packages:
	./scripts/build-packages.sh

repo:
	./scripts/build-repo.sh
