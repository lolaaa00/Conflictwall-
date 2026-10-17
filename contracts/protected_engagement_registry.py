# v0.2.18
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

import typing
from dataclasses import dataclass


@gl.contract_interface
class IConflictWall:
    class View:
        def is_permitted(
            self,
            engagement_id: u256,
            expected_policy_id: u256,
            expected_actor: Address,
            expected_engagement_ref: str,
            expected_consumer: Address,
        ) -> bool: ...

    class Write:
        def consume(self, engagement_id: u256) -> None: ...


@allow_storage
@dataclass
class RegistryReceipt:
    caller: Address
    actor: Address
    engagement_id: u256
    policy_id: u256
    engagement_ref: str
    accepted_at: str


def current_datetime() -> str:
    message = getattr(gl, "message", None)
    raw = getattr(message, "raw", None)
    value = getattr(raw, "datetime", None)
    if isinstance(value, str) and value:
        return value
    mapping = getattr(gl, "message_raw", None)
    if isinstance(mapping, dict):
        fallback = mapping.get("datetime")
        if isinstance(fallback, str) and fallback:
            return fallback
    return ""


def require_address(value: typing.Any, label: str) -> Address:
    if isinstance(value, Address):
        return value
    try:
        return Address(value)
    except Exception as exc:
        raise gl.vm.UserError(f"EXPECTED: invalid {label}") from exc


class ProtectedEngagementRegistry(gl.Contract):
    """Tiny consumer proving ConflictWall permits can gate another IC."""

    conflictwall_address: Address
    owner: Address
    receipts: TreeMap[u256, RegistryReceipt]
    receipt_count: u256

    def __init__(self, conflictwall_address: Address):
        self.conflictwall_address = require_address(conflictwall_address, "ConflictWall address")
        self.owner = gl.message.sender_address
        self.receipt_count = u256(0)

    @gl.public.write
    def accept(
        self,
        engagement_id: u256,
        policy_id: u256,
        actor: Address,
        engagement_ref: str,
    ) -> None:
        if gl.message.sender_address != self.owner:
            raise gl.vm.UserError("EXPECTED: only registry owner may accept")
        if engagement_id in self.receipts:
            raise gl.vm.UserError("EXPECTED: engagement already accepted")
        actor = require_address(actor, "actor")

        wall = IConflictWall(self.conflictwall_address)
        if not wall.view().is_permitted(
            engagement_id,
            policy_id,
            actor,
            str(engagement_ref),
            gl.message.contract_address,
        ):
            raise gl.vm.UserError("EXPECTED: ConflictWall permit is not valid")

        receipt = self.receipts.get_or_insert_default(engagement_id)
        receipt.caller = gl.message.sender_address
        receipt.actor = actor
        receipt.engagement_id = engagement_id
        receipt.policy_id = policy_id
        receipt.engagement_ref = str(engagement_ref)
        receipt.accepted_at = current_datetime()
        self.receipt_count = u256(int(self.receipt_count) + 1)

        wall.emit(on="finalized").consume(engagement_id)

    @gl.public.view
    def was_accepted(self, engagement_id: u256) -> bool:
        return engagement_id in self.receipts

    @gl.public.view
    def get_receipt(self, engagement_id: u256) -> dict[str, typing.Any]:
        item = self.receipts.get(engagement_id)
        if item is None:
            raise gl.vm.UserError("EXPECTED: unknown registry receipt")
        return {
            "caller": str(item.caller),
            "actor": str(item.actor),
            "engagement_id": int(item.engagement_id),
            "policy_id": int(item.policy_id),
            "engagement_ref": str(item.engagement_ref),
            "accepted_at": str(item.accepted_at),
        }
