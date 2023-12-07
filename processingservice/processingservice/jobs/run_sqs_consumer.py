import click

from processingservice.processingservice.awsadapters.sqs_consumer import consume_messages
from processingservice.processingservice.inference.queues_handlers import get_handlers


@click.command()
@click.option("--queue-name", "-q", type=str, required=True)
def run(queue_name: str) -> None:
    queue_handlers = get_handlers()
    return consume_messages(queue_name, queue_handlers)


if __name__ == "__main__":
    run()
