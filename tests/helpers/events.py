from __future__ import annotations

from types import SimpleNamespace


def build_event_mocks(
    mocker,
    *,
    emit_event_target: str = "app.core.events.emitter.emit_event",
    log_audit_event_target: str = "app.core.audit.service.log_audit_event",
    process_pending_events_target: str = "app.core.events.processor.process_pending_events",
):
    """
    Reusable event/audit/background-task mocks.
    """
    return SimpleNamespace(
        emit_event=mocker.patch(emit_event_target),
        log_audit_event=mocker.patch(log_audit_event_target),
        process_pending_events=mocker.patch(process_pending_events_target),
    )


def mock_emit_event(mocker, target: str = "app.core.events.emitter.emit_event"):
    return mocker.patch(target)


def mock_log_audit_event(mocker, target: str = "app.core.audit.service.log_audit_event"):
    return mocker.patch(target)


def mock_process_pending_events(mocker, target: str = "app.core.events.processor.process_pending_events"):
    return mocker.patch(target)