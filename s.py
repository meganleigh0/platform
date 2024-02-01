from unittest.mock import MagicMock, create_autospec

# Mock the SimPy Environment and Process
self.env_mock = MagicMock()
self.env_mock.process = MagicMock(return_value=create_autospec(spec=(), spec_set=True))


self.env_mock.timeout = MagicMock()

# Ensure the department mock behaves as expected
department_mock = self.department_dict_mock['Dept1']
department_mock.heads.capacity = 2
department_mock.heads.users = []
department_mock.request_head = MagicMock(return_value=MagicMock())
