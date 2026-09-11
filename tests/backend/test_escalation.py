"""Mirrors explicit escalation policy; run TS tests in backend for integration."""


def policy(confidence, similarity, evidence, grounded):
    if confidence < 0.7:
        return True
    if not evidence or similarity < 0.72:
        return True
    return not grounded


def test_low_confidence_escalates():
    assert policy(0.4, 0.9, 1, True)


def test_grounded_evidence_auto_handles():
    assert not policy(0.9, 0.9, 1, True)
