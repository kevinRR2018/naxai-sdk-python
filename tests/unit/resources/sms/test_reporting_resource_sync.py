"""
Unit tests for the synchronous ReportingResource class for SMS.
"""
import json
import pytest
from unittest.mock import patch, MagicMock
from naxai.resources.sms_resources.reporting import ReportingResource
from naxai.models.sms.responses.reporting_responses import (
    ListOutgoingSMSMetricsResponse,
    ListOutgoingSMSByCountryMetricsResponse,
    ListIncomingSMSMetricsResponse,
    ListDeliveryErrorMetricsResponse,
    OutgoingStats,
    OutgoingCountryStats,
    IncomingStats,
    DeliveryErrorStats
)
from naxai.base.exceptions import NaxaiValueError


class TestReportingResourceSync:
    """Test suite for the synchronous ReportingResource class for SMS."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = MagicMock()
        client._request = MagicMock()
        return client

    @pytest.fixture
    def reporting_resource(self, mock_client):
        """Create a ReportingResource instance with a mock client."""
        return ReportingResource(mock_client, "/sms")

    def test_initialization(self, reporting_resource):
        """Test that the ReportingResource initializes correctly."""
        assert reporting_resource.root_path == "/sms/reporting/metrics"
        assert reporting_resource.headers == {"Content-Type": "application/json"}

    def test_list_outgoing_metrics_day(self, reporting_resource, mock_client):
        """Test listing outgoing SMS metrics with day grouping."""
        # Setup mock response
        mock_response = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31",
            "direction": "outgoing",
            "group": "day",
            "stats": [
                {
                    "date": "2023-01-01",
                    "sms": 500,
                    "delivered": 480,
                    "failed": 10,
                    "expired": 5,
                    "unknown": 0,
                    "canceled": 3,
                    "rejected": 2,
                    "avgTimeToDeliver": 2300,
                    "avgTimeToSubmit": 120
                },
                {
                    "date": "2023-01-02",
                    "sms": 550,
                    "delivered": 530,
                    "failed": 12,
                    "expired": 3,
                    "unknown": 1,
                    "canceled": 2,
                    "rejected": 2,
                    "avgTimeToDeliver": 2200,
                    "avgTimeToSubmit": 115
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = reporting_resource.list_outgoing_metrics(
            group="day",
            start_date="2023-01-01",
            stop_date="2023-01-31"
        )

        # Verify the result
        assert isinstance(result, ListOutgoingSMSMetricsResponse)
        assert result.start_date == "2023-01-01"
        assert result.stop_date == "2023-01-31"
        assert result.direction == "outgoing"
        assert result.group == "day"
        
        assert len(result.stats) == 2
        assert isinstance(result.stats[0], OutgoingStats)
        assert result.stats[0].date == "2023-01-01"
        assert result.stats[0].sms == 500
        assert result.stats[0].delivered == 480
        assert result.stats[0].failed == 10
        assert result.stats[0].expired == 5
        assert result.stats[0].unknown == 0
        assert result.stats[0].canceled == 3
        assert result.stats[0].rejected == 2
        assert result.stats[0].avg_time_to_deliver == 2300
        assert result.stats[0].avg_time_to_submit == 120
        
        assert result.stats[1].date == "2023-01-02"
        assert result.stats[1].sms == 550

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/sms/reporting/metrics/outgoing"
        assert kwargs["headers"] == {"Content-Type": "application/json"}
        
        # Check query parameters
        expected_params = {
            "group": "day",
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31"
        }
        assert kwargs["params"] == expected_params

    def test_list_outgoing_metrics_hour(self, reporting_resource, mock_client):
        """Test listing outgoing SMS metrics with hour grouping."""
        # Setup mock response
        mock_response = {
            "startDate": "2023-01-01 00:00:00",
            "stopDate": "2023-01-01 23:59:59",
            "direction": "outgoing",
            "group": "hour",
            "stats": [
                {
                    "date": "2023-01-01T00:00:00Z",
                    "sms": 50,
                    "delivered": 48,
                    "failed": 1,
                    "expired": 1,
                    "unknown": 0,
                    "canceled": 0,
                    "rejected": 0,
                    "avgTimeToDeliver": 2100,
                    "avgTimeToSubmit": 110
                },
                {
                    "date": "2023-01-01T01:00:00Z",
                    "sms": 45,
                    "delivered": 43,
                    "failed": 1,
                    "expired": 0,
                    "unknown": 0,
                    "canceled": 1,
                    "rejected": 0,
                    "avgTimeToDeliver": 2050,
                    "avgTimeToSubmit": 105
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = reporting_resource.list_outgoing_metrics(
            group="hour",
            start_date="2023-01-01 00:00:00",
            stop_date="2023-01-01 23:59:59"
        )

        # Verify the result
        assert isinstance(result, ListOutgoingSMSMetricsResponse)
        assert result.start_date == "2023-01-01 00:00:00"
        assert result.stop_date == "2023-01-01 23:59:59"
        assert result.direction == "outgoing"
        assert result.group == "hour"
        
        assert len(result.stats) == 2
        assert result.stats[0].date == "2023-01-01T00:00:00Z"
        assert result.stats[0].sms == 50
        assert result.stats[1].date == "2023-01-01T01:00:00Z"
        assert result.stats[1].sms == 45

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/sms/reporting/metrics/outgoing"
        
        # Check query parameters
        expected_params = {
            "group": "hour",
            "startDate": "2023-01-01 00:00:00",
            "stopDate": "2023-01-01 23:59:59"
        }
        assert kwargs["params"] == expected_params

    def test_list_outgoing_metrics_invalid_date_format(self, reporting_resource):
        """Test listing outgoing SMS metrics with invalid date format."""
        # Test day grouping with invalid date format
        with pytest.raises(NaxaiValueError) as excinfo:
            reporting_resource.list_outgoing_metrics(
                group="day",
                start_date="2023-01-01 00:00:00",  # Invalid format for day grouping
                stop_date="2023-01-31"
            )
        assert "startDate must be in the format" in str(excinfo.value)
        
        # Test hour grouping with invalid date format
        with pytest.raises(NaxaiValueError) as excinfo:
            reporting_resource.list_outgoing_metrics(
                group="hour",
                start_date="2023-01-01",  # Invalid format for hour grouping
                stop_date="2023-01-01 23:59:59"
            )
        assert "startDate must be in the format" in str(excinfo.value)

    def test_list_outgoing_metrics_missing_stop_date(self, reporting_resource):
        """Test listing outgoing SMS metrics with missing stop_date for day/month grouping."""
        with pytest.raises(NaxaiValueError) as excinfo:
            reporting_resource.list_outgoing_metrics(
                group="day",
                start_date="2023-01-01"
                # Missing stop_date
            )
        assert "stopDate must be provided when group is 'day' or 'month'" in str(excinfo.value)

    def test_list_outgoing_metrics_by_country(self, reporting_resource, mock_client):
        """Test listing outgoing SMS metrics by country."""
        # Setup mock response
        mock_response = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31",
            "direction": "outgoing",
            "stats": [
                {
                    "country": "US",
                    "mcc": "310",
                    "mnc": "410",
                    "sms": 1200,
                    "delivered": 1150,
                    "failed": 30,
                    "expired": 10,
                    "unknown": 5,
                    "canceled": 3,
                    "rejected": 2,
                    "avgTimeToDeliver": 1800,
                    "avgTimeToSubmit": 110
                },
                {
                    "country": "GB",
                    "mcc": "234",
                    "mnc": "15",
                    "sms": 800,
                    "delivered": 780,
                    "failed": 12,
                    "expired": 5,
                    "unknown": 0,
                    "canceled": 2,
                    "rejected": 1,
                    "avgTimeToDeliver": 1600,
                    "avgTimeToSubmit": 105
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = reporting_resource.list_outgoing_metrics_by_country(
            start_date="2023-01-01",
            stop_date="2023-01-31"
        )

        # Verify the result
        assert isinstance(result, ListOutgoingSMSByCountryMetricsResponse)
        assert result.start_date == "2023-01-01"
        assert result.stop_date == "2023-01-31"
        assert result.direction == "outgoing"
        
        assert len(result.stats) == 2
        assert isinstance(result.stats[0], OutgoingCountryStats)
        assert result.stats[0].country == "US"
        assert result.stats[0].mcc == "310"
        assert result.stats[0].mnc == "410"
        assert result.stats[0].sms == 1200
        assert result.stats[0].delivered == 1150
        
        assert result.stats[1].country == "GB"
        assert result.stats[1].mcc == "234"
        assert result.stats[1].mnc == "15"
        assert result.stats[1].sms == 800

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/sms/reporting/metrics/outgoing-by-country"
        
        # Check query parameters
        expected_params = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31"
        }
        assert kwargs["params"] == expected_params

    def test_list_outgoing_metrics_by_country_invalid_date_format(self, reporting_resource, mock_client):
        """Test listing outgoing SMS metrics by country with invalid date format."""
        # Reset the mock to ensure it hasn't been called yet
        mock_client._request.reset_mock()

        try:
            reporting_resource.list_outgoing_metrics_by_country(
                start_date="2023-01",  # Invalid format
                stop_date="2023-01-31"
            )
            pytest.fail("Expected NaxaiValueError was not raised")
        except Exception as e:
            # Check if the mock was called (it shouldn't be if validation happens first)
            assert not mock_client._request.called, "Mock was called before validation"
            assert isinstance(e, NaxaiValueError), f"Expected NaxaiValueError but got {type(e)}"
            assert "startDate must be in the format 'YYYY-MM-DD'" in str(e)
        
        try:
            reporting_resource.list_outgoing_metrics_by_country(
                start_date="2023-01-01",
                stop_date="2023-01"  # Invalid format
            )
            pytest.fail("Expected NaxaiValueError was not raised")
        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            assert isinstance(e, NaxaiValueError), f"Expected NaxaiValueError but got {type(e)}"
            assert "stopDate must be in the format 'YYYY-MM-DD'" in str(e)

    def test_list_incoming_metrics(self, reporting_resource, mock_client):
        """Test listing incoming SMS metrics."""
        # Setup mock response
        mock_response = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31",
            "direction": "incoming",
            "group": "day",
            "stats": [
                {
                    "date": "2023-01-01",
                    "sms": 120
                },
                {
                    "date": "2023-01-02",
                    "sms": 145
                },
                {
                    "date": "2023-01-03",
                    "sms": 135
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = reporting_resource.list_incoming_metrics(
            group="day",
            start_date="2023-01-01",
            stop_date="2023-01-31"
        )

        # Verify the result
        assert isinstance(result, ListIncomingSMSMetricsResponse)
        assert result.start_date == "2023-01-01"
        assert result.stop_date == "2023-01-31"
        assert result.direction == "incoming"
        assert result.group == "day"
        
        assert len(result.stats) == 3
        assert isinstance(result.stats[0], IncomingStats)
        assert result.stats[0].date == "2023-01-01"
        assert result.stats[0].sms == 120
        
        assert result.stats[1].date == "2023-01-02"
        assert result.stats[1].sms == 145
        
        assert result.stats[2].date == "2023-01-03"
        assert result.stats[2].sms == 135

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/sms/reporting/metrics/incoming"
        
        # Check query parameters
        expected_params = {
            "group": "day",
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31"
        }
        assert kwargs["params"] == expected_params

    def test_list_delivery_errors_metrics(self, reporting_resource, mock_client):
        """Test listing delivery error metrics."""
        # Setup mock response
        mock_response = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31",
            "stats": [
                {
                    "statusCategory": "carrier",
                    "statusCode": "REJECTED_DESTINATION_BLOCKED",
                    "sms": 45
                },
                {
                    "statusCategory": "handset",
                    "statusCode": "HANDSET_BUSY",
                    "sms": 28
                },
                {
                    "statusCategory": "network",
                    "statusCode": "NETWORK_ERROR",
                    "sms": 17
                }
            ]
        }
        mock_client._request.return_value = mock_response

        # Call the method
        result = reporting_resource.list_delivery_errors_metrics(
            start_date="2023-01-01",
            stop_date="2023-01-31"
        )

        # Verify the result
        assert isinstance(result, ListDeliveryErrorMetricsResponse)
        assert result.start_date == "2023-01-01"
        assert result.stop_date == "2023-01-31"
        
        assert len(result.stats) == 3
        assert isinstance(result.stats[0], DeliveryErrorStats)
        assert result.stats[0].status_category == "carrier"
        assert result.stats[0].status_code == "REJECTED_DESTINATION_BLOCKED"
        assert result.stats[0].sms == 45
        
        assert result.stats[1].status_category == "handset"
        assert result.stats[1].status_code == "HANDSET_BUSY"
        assert result.stats[1].sms == 28
        
        assert result.stats[2].status_category == "network"
        assert result.stats[2].status_code == "NETWORK_ERROR"
        assert result.stats[2].sms == 17

        # Verify the client was called correctly
        mock_client._request.assert_called_once()
        args, kwargs = mock_client._request.call_args
        assert args[0] == "GET"
        assert args[1] == "/sms/reporting/metrics/delivery-errors"
        
        # Check query parameters
        expected_params = {
            "startDate": "2023-01-01",
            "stopDate": "2023-01-31"
        }
        assert kwargs["params"] == expected_params