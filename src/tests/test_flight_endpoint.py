import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch
from schemas.flight import FlightConnection, FlightCircuit


class TestFlightEndpoint:

    @pytest.fixture
    def mock_flight_service(self):
        with patch('dependencies.services.flight_service') as mock_dep:
            mock_service = AsyncMock()
            mock_dep.return_value = mock_service
            yield mock_service

    def test_get_flight_success(self, client, mock_flight_service):
        flight_date = "2024-07-01"
        from_code = "EZE"
        to_code = "JFK"
        
        mock_flight_connection = FlightConnection(
            connections=0,
            path=[
                FlightCircuit(
                    flight_number="AR1234",
                    from_=from_code,
                    to=to_code,
                    departure_time=datetime(2024, 7, 1, 10, 0),
                    arrival_time=datetime(2024, 7, 1, 18, 0)
                )
            ]
        )
        
        with patch('services.flight.FlightService.search_flight', new_callable=AsyncMock, return_value=mock_flight_connection):
            response = client.get(f"/v1/api/flight/?date={flight_date}&from={from_code}&to={to_code}")

            assert response.status_code == 200

        data = response.json()
        assert data["connections"] == 0
        assert len(data["path"]) == 1
        assert data["path"][0]["flight_number"] == "AR1234"
        assert data["path"][0]["from"] == from_code
        assert data["path"][0]["to"] == to_code

    def test_get_flight_not_found(self, client):
        flight_date = "2024-07-01"
        from_code = "EZE"
        to_code = "XXX"
        
        with patch('services.flight.FlightService.search_flight', new_callable=AsyncMock, side_effect=ValueError("No flight connections found")):
            response = client.get(f"/v1/api/flight/?date={flight_date}&from={from_code}&to={to_code}")
            
            assert response.status_code == 400
            data = response.json()
            assert "No flight connections found" in data["detail"]

    def test_get_flight_same_origin_destination(self, client):
        flight_date = "2024-07-01"
        from_code = "EZE"
        to_code = "EZE"
        
        with patch('services.flight.FlightService.search_flight', new_callable=AsyncMock, side_effect=ValueError("Origin and destiny cannot be the same")):
            response = client.get(f"/v1/api/flight/?date={flight_date}&from={from_code}&to={to_code}")
            
            assert response.status_code == 400
            data = response.json()
            assert "Origin and destiny cannot be the same" in data["detail"]

    def test_get_flight_past_date(self, client):
        flight_date = "2020-01-01"
        from_code = "EZE"
        to_code = "JFK"
        
        with patch('services.flight.FlightService.search_flight', new_callable=AsyncMock, side_effect=ValueError("Flight date cannot be in the past")):
            response = client.get(f"/v1/api/flight/?date={flight_date}&from={from_code}&to={to_code}")
            
            assert response.status_code == 400
            data = response.json()
            assert "Flight date cannot be in the past" in data["detail"]

    def test_get_flight_future_date_too_far(self, client):
        flight_date = "2030-01-01"
        from_code = "EZE"
        to_code = "JFK"
        
        with patch('services.flight.FlightService.search_flight', new_callable=AsyncMock, side_effect=ValueError("Flight date cannot be more than 6 months in the future")):
            response = client.get(f"/v1/api/flight/?date={flight_date}&from={from_code}&to={to_code}")
            
            assert response.status_code == 400
            data = response.json()
            assert "Flight date cannot be more than 6 months in the future" in data["detail"]

    def test_get_flight_missing_parameters(self, client):
        response = client.get("/v1/api/flight/")
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_get_flight_origin_city_not_found(self, client):
        flight_date = "2024-07-01"
        from_code = "INVALID"
        to_code = "JFK"
        
        with patch('services.flight.FlightService.search_flight', new_callable=AsyncMock, side_effect=ValueError("City with code INVALID not found")):
            response = client.get(f"/v1/api/flight/?date={flight_date}&from={from_code}&to={to_code}")
            
            assert response.status_code == 400
            data = response.json()
            assert "City with code INVALID not found" in data["detail"]

    def test_get_flight_destination_city_not_found(self, client):
        flight_date = "2024-07-01"
        from_code = "EZE"
        to_code = "INVALID"
        
        with patch('services.flight.FlightService.search_flight', new_callable=AsyncMock, side_effect=ValueError("City with code INVALID not found")):
            response = client.get(f"/v1/api/flight/?date={flight_date}&from={from_code}&to={to_code}")
            
            assert response.status_code == 400
            data = response.json()
            assert "City with code INVALID not found" in data["detail"]

    def test_get_flight_with_connection(self, client):
        flight_date = "2024-07-01"
        from_code = "EZE"
        to_code = "MAD"
        
        mock_flight_connection = FlightConnection(
            connections=1,
            path=[
                FlightCircuit(
                    flight_number="AR1234",
                    from_="EZE",
                    to="MIA",
                    departure_time=datetime(2024, 7, 1, 10, 0),
                    arrival_time=datetime(2024, 7, 1, 16, 0)
                ),
                FlightCircuit(
                    flight_number="IB5678",
                    from_="MIA",
                    to="MAD",
                    departure_time=datetime(2024, 7, 1, 18, 0),
                    arrival_time=datetime(2024, 7, 2, 8, 0)
                )
            ]
        )
        
        with patch('services.flight.FlightService.search_flight', new_callable=AsyncMock, return_value=mock_flight_connection):
            response = client.get(f"/v1/api/flight/?date={flight_date}&from={from_code}&to={to_code}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["connections"] == 1
            assert len(data["path"]) == 2
            assert data["path"][0]["flight_number"] == "AR1234"
            assert data["path"][0]["from"] == "EZE"
            assert data["path"][0]["to"] == "MIA"
            assert data["path"][1]["flight_number"] == "IB5678"
            assert data["path"][1]["from"] == "MIA"
            assert data["path"][1]["to"] == "MAD"

