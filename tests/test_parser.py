from parser import parse_queue_spots


def test_parse_queue_spot_handles_label_variations():
    html = """
    <article class="queue-card">
        <div class="queue-title">Stockholm Bostadskö</div>

        <div class="item">
            <div class="label">Reg. date</div>
            <div class="value">2023-01-01</div>
        </div>

        <div class="item">
            <div class="label">Updated</div>
            <div class="value">2024-01-15</div>
        </div>

        <div class="item">
            <div class="label">Please refresh before</div>
            <div class="value">2024-06-01</div>
        </div>

        <div class="item">
            <div class="label">Status</div>
            <div class="value">Active</div>
        </div>
    </article>
    """

    result = parse_queue_spots(html)

    assert len(result) == 1
    spot = result[0]

    assert spot.registration_date == "2023-01-01"
    assert spot.last_updated == "2024-01-15"
    assert spot.update_before == "2024-06-01"
    assert spot.status == "active"
    assert spot.inactive_reason is None


def test_parse_queue_spot_includes_inactive_reason_when_inactive():
    html = """
    <article class="queue-card">
        <div class="queue-title">Uppsala Housing Queue</div>

        <div class="item">
            <div class="label">Registration date</div>
            <div class="value">2022-05-10</div>
        </div>

        <div class="item">
            <div class="label">Last updated</div>
            <div class="value">2024-02-01</div>
        </div>

        <div class="item">
            <div class="label">Update before</div>
            <div class="value">2024-07-01</div>
        </div>

        <div class="item">
            <div class="label">Status</div>
            <div class="value">Inactive</div>
        </div>

        <div class="divider">
            <div class="label">Inactive reason</div>
            <div class="value">Missing update</div>
        </div>
    </article>
    """

    result = parse_queue_spots(html)

    assert len(result) == 1
    spot = result[0]

    assert spot.status == "inactive"
    assert spot.inactive_reason == "Missing update"


def test_parse_queue_spot_excludes_inactive_reason_when_active():
    html = """
    <article class="queue-card">
        <div class="queue-title">Malmö Queue</div>

        <div class="item">
            <div class="label">Registration date</div>
            <div class="value">2021-03-20</div>
        </div>

        <div class="item">
            <div class="label">Last updated</div>
            <div class="value">2024-03-01</div>
        </div>

        <div class="item">
            <div class="label">Update before</div>
            <div class="value">2024-08-01</div>
        </div>

        <div class="item">
            <div class="label">Status</div>
            <div class="value">Active</div>
        </div>
    </article>
    """

    result = parse_queue_spots(html)

    assert len(result) == 1
    spot = result[0]

    assert spot.status == "active"
    assert spot.inactive_reason is None