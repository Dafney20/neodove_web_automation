import os
import pytest

# Create the reports directory if it doesn't exist
if not os.path.exists('reports'):
    os.makedirs('reports')

# Run pytest with the configuration from pytest.ini
pytest.main()
