from aws_lambda_context import LambdaContext


def mock_context():
    context = LambdaContext()
    context.function_name = 'test'
    context.function_version = 'test'
    context.invoked_function_arn = 'test'
    context.memory_limit_in_mb = 'test'
    context.aws_request_id = 'test'
    context.log_group_name = 'test'
    context.log_stream_name = 'test'
    return context
