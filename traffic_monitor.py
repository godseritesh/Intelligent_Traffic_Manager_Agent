import cv2
import unittest
from unittest.mock import patch, Mock

class TrafficMonitor:
    def __init__(self):
        self.cap = cv2.VideoCapture('traffic_video.mp4')

    def monitor_traffic(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            vehicle_count = 0
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:
                    vehicle_count += 1

            print(f'Vehicle count: {vehicle_count}')
        self.cap.release()

class TestTrafficMonitor(unittest.TestCase):
    @patch('cv2.VideoCapture')
    def test_monitor_traffic(self, mock.VideoCapture):
        mock_frame = Mock()
        mock_frame.read.return_value = (True, cv2.imread('test_frame.png'))
        mock.VideoCapture.return_value = mock_frame

        monitor = TrafficMonitor()
        with patch('cv2.cvtColor') as mock.cvtColor, \
             patch('cv2.threshold') as mock.threshold, \
             patch('cv2.findContours') as mock.findContours, \
             patch('cv2.contourArea') as mock.contourArea:
            mock.cvtColor.return_value = cv2.cvtColor(mock_frame, cv2.COLOR_BGR2GRAY)
            mock.threshold.return_value = (Mock(), Mock())
            mock.findContours.return_value = ([Mock(area=150), Mock(area=50)], None)
            mock.contourArea.side_effect = [150, 50]

            monitor.monitor_traffic()
            mock.VideoCapture.assert_called_once_with('traffic_video.mp4')
            mock.cvtColor.assert_called_once_with(mock_frame, cv2.COLOR_BGR2GRAY)
            mock.threshold.assert_called_once_with(mock.cvtColor.return_value, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            mock.findContours.assert_called_once_with(mock.threshold.return_value, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            mock.contourArea.assert_has_calls([mock.call(mock.findContours.return_value[0][0]), mock.call(mock.findContours.return_value[0][1])])

    def test_monitor_traffic_no_vehicles(self):
        mock_frame = Mock()
        mock_frame.read.return_value = (True, cv2.imread('test_frame_no_vehicles.png'))
        mock.VideoCapture.return_value = mock_frame

        monitor = TrafficMonitor()
        with patch('cv2.cvtColor') as mock.cvtColor, \
             patch('cv2.threshold') as mock.threshold, \
             patch('cv2.findContours') as mock.findContours, \
             patch('cv2.contourArea') as mock.contourArea:
            mock.cvtColor.return_value = cv2.cvtColor(mock_frame, cv2.COLOR_BGR2GRAY)
            mock.threshold.return_value = (Mock(), Mock())
            mock.findContours.return_value = ([], None)
            mock.contourArea.return_value = 0

            monitor.monitor_traffic()
            mock.VideoCapture.assert_called_once_with('traffic_video.mp4')
            mock.cvtColor.assert_called_once_with(mock_frame, cv2.COLOR_BGR2GRAY)
            mock.threshold.assert_called_once_with(mock.cvtColor.return_value, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            mock.findContours.assert_called_once_with(mock.threshold.return_value, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            mock.contourArea.assert_called_once_with(mock.findContours.return_value[0][0])

if __name__ == '__main__':
    unittest.main()