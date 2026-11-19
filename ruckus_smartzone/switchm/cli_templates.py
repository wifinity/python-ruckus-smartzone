"""CLI template wrapper (``/clitemplate``).

Two kinds:

* ``provision`` — runs once, on a factory switch's first approval into the
  group, for the matching model. The switch's startup config is replaced by the
  template and the switch reloads, whatever ``overwrite`` says. The body is
  applied a few minutes after the switch is back on the network.
* ``update`` — applies to the running config of the listed switches, with no
  reload.

A template whose line fails leaves the earlier lines applied on the switch;
there is no rollback, so template CLI should be safe to re-run.
"""

from typing import Any, Dict, Iterable, List, Mapping, Optional, Union

from ruckus_smartzone.switchm.base import SwitchmResource, build_body, join_macs

TEMPLATE_KINDS = ("provision", "update")

_DEFINITIONS = {
    "provision": "cliTemplates_createProvisionCliTemplate",
    "update": "cliTemplates_createUpdateCliTemplate",
}


def _kind(kind: str) -> str:
    if kind not in TEMPLATE_KINDS:
        raise ValueError(f"kind must be one of {TEMPLATE_KINDS}, got {kind!r}")
    return kind


class CLITemplatesResource(SwitchmResource):
    """Operations on provision and update CLI templates."""

    def list(self, kind: str, group_id: str) -> List[Dict[str, Any]]:
        """Return a group's templates of one kind.

        Each entry's ``id`` is what :meth:`delete` takes; its
        ``cliTemplateConfigId`` is what :meth:`get` and :meth:`replace` take.
        """
        return self.switchm.get_pages(
            f"clitemplate/{_kind(kind)}", params={"switchGroupId": group_id}
        )

    def get(self, kind: str, cli_template_config_id: str) -> Optional[Dict[str, Any]]:
        """Return one template's config by ``cliTemplateConfigId``."""
        return self.switchm.get(f"clitemplate/{_kind(kind)}/{cli_template_config_id}")

    def create_provision(
        self,
        group_id: str,
        name: str,
        cli: str,
        models: Union[str, Iterable[str]],
        *,
        overwrite: Optional[bool] = None,
        variables: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Create a provision template for one or more switch models.

        Returns:
            ``{id}`` of the new template config.
        """
        model_list = models if isinstance(models, str) else ",".join(models)
        body = build_body(
            _DEFINITIONS["provision"],
            {
                "groupId": group_id,
                "name": name,
                "cli": cli,
                "models": model_list,
                "overwrite": overwrite,
                "variables": variables,
            },
        )
        return self.switchm.post("clitemplate/provision", json=body)

    def create_update(
        self,
        group_id: str,
        name: str,
        cli: str,
        switch_ids: Union[str, Iterable[str]],
        *,
        reload: Optional[bool] = None,
        push_time_type: Optional[str] = None,
        push_time: Optional[int] = None,
        variables: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Create an update template and push it to the given switches.

        Args:
            switch_ids: Switch MACs; one or many switches of the group.
            push_time_type: ``NOW`` (controller default) or ``SCHEDULE``.

        Returns:
            ``{id}`` of the new template config.
        """
        body = build_body(
            _DEFINITIONS["update"],
            {
                "groupId": group_id,
                "name": name,
                "cli": cli,
                "switches": join_macs(switch_ids),
                "reload": reload,
                "pushTimeType": push_time_type,
                "pushTime": push_time,
                "variables": variables,
            },
        )
        return self.switchm.post("clitemplate/update", json=body)

    def replace(
        self, kind: str, cli_template_config_id: str, fields: Mapping[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Change some fields of a template config, keeping the rest.

        Reads the object and PUTs it back in full with ``fields`` applied
        (see :meth:`SwitchmResource.merge_put`), so pass only what changes.
        """
        return self.merge_put(
            f"clitemplate/{_kind(kind)}/{cli_template_config_id}",
            _DEFINITIONS[kind],
            fields,
        )

    def delete(self, kind: str, template_id: str) -> Optional[Dict[str, Any]]:
        """Delete a template by its list entry ``id`` (not ``cliTemplateConfigId``)."""
        return self.switchm.delete(f"clitemplate/{_kind(kind)}/{template_id}")
