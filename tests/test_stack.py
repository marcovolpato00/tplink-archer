from tplink_archer import Stack


def test_stack_equals():
    stack1_raw = '[1.0]0\nfoo=bar\nfoob=barf\n[1.0]0\nfoo=bar\nfoob=barf'
    stack2_raw = stack1_raw
    stack1 = Stack(stack1_raw)
    stack2 = Stack(stack2_raw)

    assert stack1 == stack2

    stack2_raw = '[1.0]0\nfoo=rab\nfoob=fabr\n[2.0]0\nfoo=rab\nfoob=fabr'
    stack2.parse(stack2_raw)

    assert stack1 != stack2
