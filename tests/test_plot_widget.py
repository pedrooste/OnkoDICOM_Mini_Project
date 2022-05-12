import pytest
from plot_widget import PlotWidget


class TestPlotWidget:
    @pytest.fixture
    def test_app(self, qtbot):
        """sets up widget for testing"""
        test_app = PlotWidget()

        return test_app

    def test_plot_dcm(self, test_app):
        assert test_app.plot_dcm("test files/DICOM-RT-01/CT_3_Hashed.dcm")

    def test_clear_view(self, test_app):
        assert test_app.clear_view()
