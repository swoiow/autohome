"""Shared pytest fixtures for the autohome scraper test suite."""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import pandas as pd
import logging


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_csv_data():
    """Sample CSV data for testing."""
    return [
        ["Brand1", "series1", "https://example.com/series1"],
        ["Brand2", "series2", "https://example.com/series2"],
        ["Brand3", "series3", "https://example.com/series3"]
    ]


@pytest.fixture
def sample_brands_csv(temp_dir, sample_csv_data):
    """Create a sample brands.csv file in temp directory."""
    csv_file = temp_dir / "brands.csv"
    df = pd.DataFrame(sample_csv_data, columns=["Brand", "Series", "URL"])
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    return csv_file


@pytest.fixture
def mock_playwright_page():
    """Mock playwright page object."""
    page = Mock()
    page.goto = Mock()
    page.wait_for_load_state = Mock()
    page.locator = Mock()
    
    # Mock locator chain
    locator = Mock()
    locator.all = Mock(return_value=[])
    locator.click = Mock()
    locator.inner_text = Mock(return_value="Test Brand")
    locator.get_attribute = Mock(return_value="test-id")
    
    page.locator.return_value = locator
    locator.locator.return_value = locator
    
    return page


@pytest.fixture
def mock_playwright_browser(mock_playwright_page):
    """Mock playwright browser object."""
    browser = Mock()
    browser.new_page = Mock(return_value=mock_playwright_page)
    browser.close = Mock()
    return browser


@pytest.fixture
def mock_playwright_context(mock_playwright_browser):
    """Mock playwright context manager."""
    context_manager = Mock()
    context_manager.webkit = Mock()
    context_manager.webkit.launch = Mock(return_value=mock_playwright_browser)
    return context_manager


@pytest.fixture
def mock_sync_playwright(mock_playwright_context):
    """Mock sync_playwright context manager."""
    with patch('get_all_brands.sync_playwright') as mock_sync:
        mock_sync.return_value.__enter__ = Mock(return_value=mock_playwright_context)
        mock_sync.return_value.__exit__ = Mock(return_value=None)
        yield mock_sync


@pytest.fixture
def mock_pandas_to_csv():
    """Mock pandas DataFrame.to_csv method."""
    with patch.object(pd.DataFrame, 'to_csv') as mock_csv:
        yield mock_csv


@pytest.fixture
def mock_logger():
    """Mock logger for testing."""
    logger = Mock(spec=logging.Logger)
    logger.info = Mock()
    logger.error = Mock()
    logger.warning = Mock()
    logger.debug = Mock()
    return logger


@pytest.fixture
def mock_file_handler():
    """Mock file handler for logging."""
    with patch('logging.FileHandler') as mock_handler:
        yield mock_handler


@pytest.fixture
def sample_car_data():
    """Sample car data structure."""
    return {
        "brand": "Toyota",
        "series": "Camry",
        "id": "camry_2024",
        "url": "https://car.autohome.com.cn/camry/",
        "parameters": {
            "engine": "2.0L",
            "power": "178hp",
            "fuel_type": "Gasoline"
        }
    }


@pytest.fixture
def mock_network_error():
    """Fixture to simulate network errors."""
    def _raise_network_error(*args, **kwargs):
        raise ConnectionError("Network error")
    return _raise_network_error


@pytest.fixture
def mock_timeout_error():
    """Fixture to simulate timeout errors."""
    def _raise_timeout_error(*args, **kwargs):
        raise TimeoutError("Request timeout")
    return _raise_timeout_error


@pytest.fixture(autouse=True)
def clean_up_test_files():
    """Automatically clean up test files after each test."""
    yield
    # Clean up any test files that might have been created
    test_files = ["brands.csv", "brands.txt", "test_brands.csv"]
    for file_name in test_files:
        file_path = Path(file_name)
        if file_path.exists():
            file_path.unlink(missing_ok=True)


@pytest.fixture
def mock_env_vars():
    """Mock environment variables."""
    env_vars = {
        "DOMAIN": "https://car.autohome.com.cn/",
        "USER_AGENT": "TestAgent/1.0"
    }
    with patch.dict('os.environ', env_vars):
        yield env_vars


# Markers for test categorization
pytest_plugins = []

def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (slower, with dependencies)"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running tests"
    )