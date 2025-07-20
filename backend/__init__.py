"""
Blastify Backend Package

A comprehensive bulk email sender with AI-powered content generation.
"""

__version__ = "1.0.0"
__author__ = "Blastify Team"
__description__ = "Bulk email sender with Gemini AI and Resend integration"

# Import main modules for easy access
from . import parser
from . import email_sender
from . import gemini_api
from . import utils

__all__ = ['parser', 'email_sender', 'gemini_api', 'utils']
