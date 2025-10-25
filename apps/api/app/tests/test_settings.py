from app.core.config import get_settings


def test_settings_defaults():
    settings = get_settings()
    assert settings.mongo_uri.endswith("/tetris")
    assert settings.rake_percent == 10
    assert settings.min_stake == 50
