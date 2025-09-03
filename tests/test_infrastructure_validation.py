"""Test suite to validate that the testing infrastructure is properly configured."""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch


class TestTestingInfrastructure:
    """Validate that the testing infrastructure is working correctly."""
    
    @pytest.mark.unit
    def test_pytest_is_working(self):
        """Test that pytest is properly configured and running."""
        assert True, "pytest is working"
    
    @pytest.mark.unit
    def test_fixtures_are_available(self, temp_dir, sample_csv_data):
        """Test that shared fixtures are properly loaded."""
        assert temp_dir.exists(), "temp_dir fixture should create a directory"
        assert isinstance(sample_csv_data, list), "sample_csv_data should be a list"
        assert len(sample_csv_data) == 3, "sample_csv_data should have 3 entries"
    
    @pytest.mark.unit
    def test_mocking_works(self, mocker):
        """Test that pytest-mock is working."""
        mock_function = mocker.Mock(return_value="mocked")
        result = mock_function("test")
        assert result == "mocked"
        mock_function.assert_called_once_with("test")
    
    @pytest.mark.unit
    def test_pandas_integration(self, sample_csv_data):
        """Test that pandas is available and working."""
        df = pd.DataFrame(sample_csv_data, columns=["Brand", "Series", "URL"])
        assert len(df) == 3
        assert list(df.columns) == ["Brand", "Series", "URL"]
        assert df.iloc[0, 0] == "Brand1"
    
    @pytest.mark.unit
    def test_temp_directory_fixture(self, temp_dir):
        """Test that temporary directory fixture works."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        assert test_file.exists()
        assert test_file.read_text() == "test content"
    
    @pytest.mark.unit
    def test_csv_fixture_creation(self, sample_brands_csv):
        """Test that CSV fixture creates proper file."""
        assert sample_brands_csv.exists()
        df = pd.read_csv(sample_brands_csv)
        assert len(df) == 3
        assert "Brand" in df.columns
    
    @pytest.mark.unit
    def test_mock_playwright_fixture(self, mock_playwright_page):
        """Test that playwright mocking fixture works."""
        mock_playwright_page.goto("https://example.com")
        mock_playwright_page.goto.assert_called_once_with("https://example.com")
        
        # Test locator chain
        locator = mock_playwright_page.locator("#test")
        assert locator is not None
    
    @pytest.mark.unit
    def test_logger_mock(self, mock_logger):
        """Test that logger mock fixture works."""
        mock_logger.info("test message")
        mock_logger.info.assert_called_once_with("test message")
    
    @pytest.mark.unit
    def test_sample_car_data_fixture(self, sample_car_data):
        """Test that sample car data fixture is properly structured."""
        assert "brand" in sample_car_data
        assert "series" in sample_car_data
        assert "parameters" in sample_car_data
        assert isinstance(sample_car_data["parameters"], dict)
    
    @pytest.mark.unit
    def test_markers_are_configured(self):
        """Test that custom markers are available."""
        # This test itself uses the @pytest.mark.unit marker
        # If it runs without error, markers are working
        assert hasattr(pytest.mark, 'unit')
        assert hasattr(pytest.mark, 'integration')
        assert hasattr(pytest.mark, 'slow')
    
    @pytest.mark.integration
    def test_integration_marker(self):
        """Test that integration marker works."""
        # This is marked as integration test
        assert True
    
    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that slow marker works."""
        # This is marked as slow test
        assert True
    
    def test_pathlib_integration(self):
        """Test that pathlib works for file operations."""
        from pathlib import Path
        current_dir = Path.cwd()
        assert current_dir.exists()
        assert current_dir.is_dir()


class TestProjectStructure:
    """Validate the project structure is correct."""
    
    @pytest.mark.unit
    def test_project_root_structure(self):
        """Test that project has expected structure."""
        project_root = Path.cwd()
        
        # Check for key files
        assert (project_root / "pyproject.toml").exists(), "pyproject.toml should exist"
        assert (project_root / "README.md").exists(), "README.md should exist"
        assert (project_root / "get_all_brands.py").exists(), "get_all_brands.py should exist"
        
        # Check for test directories
        tests_dir = project_root / "tests"
        assert tests_dir.exists(), "tests directory should exist"
        assert (tests_dir / "__init__.py").exists(), "tests/__init__.py should exist"
        assert (tests_dir / "conftest.py").exists(), "tests/conftest.py should exist"
        assert (tests_dir / "unit").exists(), "tests/unit should exist"
        assert (tests_dir / "integration").exists(), "tests/integration should exist"
    
    @pytest.mark.unit
    def test_pyproject_toml_structure(self):
        """Test that pyproject.toml has required sections."""
        import toml
        
        project_root = Path.cwd()
        pyproject_file = project_root / "pyproject.toml"
        
        config = toml.load(pyproject_file)
        
        # Check required sections
        assert "tool" in config
        assert "poetry" in config["tool"]
        assert "pytest" in config["tool"]
        assert "coverage" in config["tool"]
        
        # Check poetry configuration
        poetry_config = config["tool"]["poetry"]
        assert "name" in poetry_config
        assert "version" in poetry_config
        assert "dependencies" in poetry_config
        
        # Check testing dependencies
        assert "group" in poetry_config
        assert "dev" in poetry_config["group"]
        assert "dependencies" in poetry_config["group"]["dev"]
        
        dev_deps = poetry_config["group"]["dev"]["dependencies"]
        assert "pytest" in dev_deps
        assert "pytest-cov" in dev_deps
        assert "pytest-mock" in dev_deps