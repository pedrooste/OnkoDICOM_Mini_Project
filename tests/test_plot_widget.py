"""
Tests for plot_widget.py
"""
import pytest
from plot_widget import PlotWidget


class TestPlotWidget:
    """
    Encapsulates the test suite for plot_widget.py
    """
    @pytest.fixture
    def test_app(self):
        """
        Sets up widget for testing
        """
        test_app = PlotWidget()

        return test_app

    def test_plot_dcm(self, test_app):
        """
        Tests plot_widget test_plot_dcm function
        """
        assert test_app.plot_dcm("test files/DICOM-RT-01/CT_3_Hashed.dcm")

    def test_clear_view(self, test_app):
        """
        Tests plot_widget test_clear_view function
        """
        assert test_app.clear_view()
