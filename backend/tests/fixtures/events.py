import pytest


@pytest.fixture
def mock_event_publisher(
    mocker,
):

    return mocker.patch(
        "app.core.events.publisher.publish_event"
    )