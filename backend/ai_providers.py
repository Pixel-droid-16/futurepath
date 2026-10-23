<<<<<<< HEAD
"""Compatibility import surface for existing tests and code.

To edit Claude -> backend/providers/claude.py
To edit RunPod -> backend/providers/runpod.py
To edit skill evidence validation -> backend/providers/validation.py
"""
from .providers.validation import (IntegrationError,SYSTEM,allowed_catalogue,prompt_for,parse_json,validate_candidates)
from .providers.claude import claude_extract,claude_extract_pdf,configured as claude_configured
from .providers.runpod import runpod_extract,runpod_url
=======
"""Compatibility import surface for existing tests and code.

To edit Claude -> backend/providers/claude.py
To edit RunPod -> backend/providers/runpod.py
To edit skill evidence validation -> backend/providers/validation.py
"""
from .providers.validation import (IntegrationError,SYSTEM,allowed_catalogue,prompt_for,parse_json,validate_candidates)
from .providers.claude import claude_extract,claude_extract_pdf,configured as claude_configured
from .providers.runpod import runpod_extract,runpod_url
>>>>>>> da0787dab49148d066631b796b12e2b882c85231
