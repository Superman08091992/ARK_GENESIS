from dataclasses import dataclass, field
from opt.ark.runtime.action_model.models import ToolKind
from .exceptions import ToolDenied

@dataclass(frozen=True)
class BrokerPolicy:
    allowed_tools: frozenset = field(default_factory=lambda: frozenset({ToolKind.NOOP, ToolKind.BROWSER_STUB, ToolKind.FILE_STUB, ToolKind.SHELL_STUB, ToolKind.ACCOUNT_STUB}))
    dry_run_only: bool = True
    def validate_tool(self, tool: ToolKind, *, dry_run: bool) -> None:
        if tool not in self.allowed_tools:
            raise ToolDenied('tool is not allowlisted: '+tool.value)
        if self.dry_run_only and not dry_run:
            raise ToolDenied('v0.1 broker allows dry_run only')
