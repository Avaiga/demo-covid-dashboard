from pages.world.world import initialize_world, data


def test_initialize_world_returns_expected_structure():
    outputs = initialize_world(data)
    assert len(outputs) == 5
    assert all([hasattr(df, "columns") for df in outputs])
