from opt.ark.runtime.kernel import Checkpoint, CubeFace, CubeState, ODAFrame, OperationEnvelope


def make_envelope(*, dry_run=True, aletheia_ref='aletheia:verified:1', joey_plan_ref='joey:plan:1', hrm_approval_ref='hrm:approval:1'):
    cube = CubeState('cube:1', CubeFace.CONCIPERE, 'state:initial')
    oda = ODAFrame('obs:1', 'decision:1', 'action:1')
    checkpoint = Checkpoint('cp:1', 'env:1', 'hash:abc', 'operator:local')
    return OperationEnvelope('env:1', 'operator:local', cube, oda, aletheia_ref, joey_plan_ref, hrm_approval_ref, checkpoint, 'intent:1', dry_run)
